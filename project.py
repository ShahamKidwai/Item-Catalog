from time import strftime
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
from flask import Flask, render_template, request, redirect
from flask import url_for, flash, jsonify
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response
import os
import random
import string
import jinja2
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog App"

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")
            return redirect('/login')
    return decorated_function


# this function creates a JSON endpoint to view Categories and the items


@app.route('/JSON/')
def catalogJSON():
    categories_all = session.query(Category).all()
    items_all = session.query(Item).all()
    return jsonify(Category=[c.serialize for c in categories_all],
                   Item=[i.serialize for i in items_all])

# this function creates a JSON endpoint to view particular item information


@app.route('/category/<string:category>/<string:item>/JSON')
def showitemsJSON(category, item):
    category = session.query(Category).filter_by(name=category).one()
    item = session.query(Item).filter_by(title=item).one()
    return jsonify(category=category.serialize, item=item.serialize)

# below is a login function that renders login page


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# below function calls the gdisconnect function and redirects to home page


@app.route('/logout')
def logout():
    gdisconnect()
    return redirect('/')

# below function contains steps for obtaining authorization code to use google
# below function obtains authorization code in exchange of one time code


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps
                                 ('Failed to upgrade the authorization code.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the acces token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# the below function is called to logout user from google account


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps(
                'Failed to revoke token for given user.',
                400))
        response.headers['Content-Type'] = 'application/json'
        return response

# below function displays all the categories


@app.route('/')
@app.route('/categories')
def showcategories():
    if 'user_id' not in login_session:
        Categories = session.query(Category).all()
        islogin = False
        return render_template(
            'publicCategories.html',
            cate=Categories,
            isLogin=islogin)
    else:
        Categories = session.query(Category).all()
        islogin = True
        return render_template(
            'ItemCategories.html',
            cate=Categories,
            isLogin=islogin)

# below function allows the User to create a new category


@app.route('/category/new/', methods=['GET', 'POST'])
@login_required
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],
                               user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showcategories'))
    else:
        return render_template('newCategory.html')

# below function displays items from specific category


@app.route('/category/<int:category_id>/Items')
@app.route('/category/<int:category_id>')
def showitems(category_id):
    if 'user_id' not in login_session:
        category = session.query(Category).filter_by(id=category_id).one()
        creator = getUserInfo(category.user_id)
        Categories = session.query(Category).all()
        Items = session.query(Item).filter_by(category_id=category.id).all()
        islogin = False
        return render_template(
            'publicItems.html',
            category=category,
            cate=Categories,
            items=Items,
            isLogin=islogin)
    else:
        category = session.query(Category).filter_by(id=category_id).one()
        creator = getUserInfo(category.user_id)
        Categories = session.query(Category).all()
        Items = session.query(Item).filter_by(category_id=category.id).all()
        if creator.id != login_session['user_id']:
            islogin = True
            return render_template(
                'publicItems.html',
                category=category,
                cate=Categories,
                items=Items,
                isLogin=islogin)
        else:
            islogin = True
            return render_template(
                'Items.html',
                category=category,
                cate=Categories,
                items=Items,
                isLogin=islogin)

# below function displays specific item information from one particular
# category


@app.route('/category/<int:category_id>/Items/<int:item_id>/')
def ItemDescription(category_id, item_id):
    if 'user_id' not in login_session:
        islogin = False
        category = session.query(Category).filter_by(id=category_id).one()
        Categories = session.query(Category).all()
        itemone = session.query(Item).filter_by(id=item_id).one()
        Items = session.query(Item).filter_by(category_id=category.id).all()
        return render_template(
            'publicItemDescription.html',
            category=category,
            cate=Categories,
            item=itemone,
            items=Items,
            isLogin=islogin)
    else:
        category = session.query(Category).filter_by(id=category_id).one()
        Categories = session.query(Category).all()
        itemone = session.query(Item).filter_by(id=item_id).one()
        creator = getUserInfo(category.user_id)
        Items = session.query(Item).filter_by(category_id=category.id).all()
        islogin = True
        if creator.id != login_session['user_id']:
            return render_template(
                'publicItemDescription.html',
                category=category,
                cate=Categories,
                item=itemone,
                items=Items,
                isLogin=islogin)
        else:
            return render_template(
                'ItemDescription.html',
                category=category,
                cate=Categories,
                item=itemone,
                items=Items,
                isLogin=islogin)


# below function allows user to update item description from a particular
# category


@app.route(
    '/category/<int:category_id>/Items/<int:item_id>/editdescription',
    methods=[
        'GET',
        'POST'])
@login_required
def editdescription(category_id, item_id):
    uitem = session.query(Item).filter_by(
        id=item_id, category_id=category_id).one()
    cates = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    if request.method == 'POST':
        if creator.id != login_session['user_id']:
            response = make_response(json.dumps('Only the owner can update an \
                                     item description.', 401))
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            description = request.form['description']
            uitem.description = description
            session.add(uitem)
            session.commit()
            return redirect(
                url_for(
                    'ItemDescription',
                    category_id=category_id,
                    item_id=item_id))
    else:
        if 'user_id' in login_session:
            islogin = True
        else:
            islogin = False
        return render_template(
            'EditDescription.html',
            item=uitem,
            category_id=category.id,
            cate=cates,
            cat=category,
            isLogin=islogin)

# below function allows the user to delete item description


@app.route(
    '/category/<int:category_id>/Items/<int:item_id>/deletedescription',
    methods=[
        'GET',
        'POST'])
@login_required
def deletedescription(category_id, item_id):
    uitem = session.query(Item).filter_by(
        id=item_id, category_id=category_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    Categories = session.query(Category).all()
    creator = getUserInfo(category.user_id)
    if request.method == 'POST':
        if creator.id != login_session['user_id']:
            response = make_response(json.dumps('Only the owner can delete an \
                                                item Description.', 401))
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            uitem.description = " "
            session.add(uitem)
            session.commit()
            return redirect(
                url_for(
                    'ItemDescription',
                    category_id=category_id,
                    item_id=item_id))
    else:
        if 'user_id' in login_session:
            islogin = True
        else:
            islogin = False
        return render_template(
            'DeleteDescription.html',
            item=uitem,
            cate=Categories,
            cat=category,
            category_id=category.id,
            isLogin=islogin)

# below function allows user to create new item in a particular category


@app.route('/category/<int:category_id>/Items/new', methods=['GET', 'POST'])
@login_required
def newitem(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    if request.method == 'POST':
        if creator.id != login_session['user_id']:
            response = make_response(
                json.dumps(
                    'Only the owner can create, update and delete item.',
                    401))
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            newItem = Item(
                title=request.form['name'],
                description=request.form['description'],
                category_id=request.form['category'],
                user_id=login_session['user_id'])
            session.add(newItem)
            session.commit()
            return redirect(url_for('showitems', category_id=category_id))
    else:
        if 'user_id' in login_session:
            islogin = True
        else:
            islogin = False
        return render_template(
            'NewItem.html',
            category_id=category_id,
            cate=categories,
            categories=categories,
            cat=category,
            isLogin=islogin)

# below function allows the user to update item name in a particular category


@app.route(
    '/category/<int:category_id>/Items/<int:item_id>/edit',
    methods=[
        'GET',
        'POST'])
@login_required
def edititem(category_id, item_id):
    uitem = session.query(Item).filter_by(
        id=item_id, category_id=category_id).one()
    cates = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    Categories = session.query(Category).all()
    creator = getUserInfo(category.user_id)
    if request.method == 'POST':
        if creator.id != login_session['user_id']:
            response = make_response(
                json.dumps(
                    'Only the owner can create, update and delete item.',
                    401))
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            title = request.form['title']
            description = request.form['description']
            category_id = request.form['category']
            uitem.title = title
            uitem.description = description
            uitem.category_id = category_id
            session.add(uitem)
            session.commit()
            return redirect(url_for('showitems', category_id=category_id))
    else:
        if 'user_id' in login_session:
            islogin = True
        else:
            islogin = False
        return render_template(
            'item-edit.html',
            item=uitem,
            cate=Categories,
            category_id=category_id,
            cat=category,
            cats=cates,
            isLogin=islogin)

# below function allows user to delete item in a particular category


@app.route(
    '/category/<int:category_id>/Items/<int:item_id>/delete',
    methods=[
        'GET',
        'POST'])
@login_required
def delete_item(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    Categories = session.query(Category).all()
    creator = getUserInfo(category.user_id)
    if request.method == 'POST':
        if creator.id != login_session['user_id']:
            response = make_response(
                json.dumps(
                    'Only the owner can create, update and delete item.',
                    401))
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            session.delete(itemToDelete)
            session.commit()
            return redirect(url_for('showitems', category_id=category_id))
    else:
        if 'user_id' in login_session:
            islogin = True
        else:
            islogin = False
        return render_template(
            'DeleteItem.html',
            i=itemToDelete,
            cate=Categories,
            isLogin=islogin)

# below function takes user_id as input and returns the user object


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# below function takes user email as input and returns the user id


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None

# below function extracts user info from login session and stores it in a
# user table


def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
