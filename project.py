from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#Fake Categories
catesy = {'name': 'Soccer', 'id': '1'}
catess = [{'name': 'Soccer', 'id': '1'}, {'name': 'BasketBall', 'id': '2'},{'name' : 'Baseball', 'id': '3'}, {'name': 'Frisbee', 'id': '4'}, {'name': 'Snowboarding', 'id': '5'},
               {'name': 'Rock Climbing' , 'id': '6'}, {'name': 'Foosball', 'id': '7'}]


Ite = [{'name': 'Snowboard', 'id': '1'}, {'name': 'Goggles', 'id': '2'},{'name' : 'Shinguards', 'id': '3'}, {'name': 'Jersey', 'id': '4'}, {'name': 'Soccer Cleats', 'id': '5'},
              {'name': 'Two Shinguards' , 'id': '6'}, {'name': 'Shoes', 'id': '7'}]


@app.route('/')
@app.route('/categories')
def showcategories():
    Categories = session.query(Category).all()
    return render_template('ItemCategories.html', cate = Categories)

@app.route('/category/<int:category_id>/Items')
@app.route('/category/<int:category_id>')
def showitems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    Items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('Items.html', category = category, item = Items )

@app.route('/category/new')
def newcategory():
    return "category items"

@app.route('/category/<int:category_id>/Items/<int:item_id>/')
def ItemDescription(category_id, item_id):
    category = session.query(Category).filter_by(id = category_id).one()
    itemone = session.query(Item).filter_by(id = item_id).one()
    return render_template('ItemDescription.html', category = category, item = itemone)

@app.route('/category/<int:category_id>/Items/<int:item_id>/edit', methods = ['GET', 'POST'])
def edititem(category_id, item_id):
    uitem = session.query(Item).filter_by(id = item_id, category_id = category_id).one()
    if request.method == 'POST':
       title = request.form['title']
       description = request.form['description']
       category = request.form['category']
       uitem.title = title
       uitem.description = description
       uitem.categoryID = category
       session.add(uitem)
       session.commit()
       return redirect(url_for('showitems', category_id = category_id))
    else:
         cates = session.query(Category).all()
         return render_template('item-edit.html', i = uitem, category_id = category_id, cat = cates)

@app.route('/category/<int:category_id>/Items/new',  methods = ['GET', 'POST'])
def newitem(category_id):
     if request.method == 'POST':
        newItem = Item(title=request.form['name'], description=request.form['description'],  category_id=category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showitems', category_id = category_id))
     else:
          return render_template('NewItem.html', category_id = category_id)
        

@app.route('/category/<int:category_id>/Items/<int:item_id>/delete', methods = ['GET', 'POST'])
def delete_item(category_id, item_id):
    itemToDelete = session.query(Item).filter_by(id = item_id).one()
    if request.method == 'POST':
       session.delete(itemToDelete)
       session.commit()
       return redirect(url_for('showitems', category_id = category_id))
    else:
         return render_template('DeleteItem.html', i = itemToDelete)

if __name__ == '__main__':
     app.debug = True
     app.run(host = '0.0.0.0', port = 5000)



     




