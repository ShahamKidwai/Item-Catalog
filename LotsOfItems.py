from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


User1 = User(name="RoboBarista", email="tinnyTim@udacity.com")
session.add(User1)
session.commit()

Soccer = Category(user_id=1, name = "Soccer")
session.add(Soccer)
session.commit()

Shinguards = Item(title = "Shinguards", user_id = 1, description = "The best shinguards to protect players from injuries", category = Soccer)
session.add(Shinguards)
session.commit()

Jersey = Item(title ="Jersey", user_id = 1, description="Soccer Player Clothing", category = Soccer)
session.add(Jersey)
session.commit()

SoccerCleats = Item(title = "Soccer Cleats", user_id = 1, description="The best Soccer Cleats to help in movement", category = Soccer)
session.add(SoccerCleats)
session.commit()

TwoShinguards = Item(title = "Two Shinguards", user_id = 1, description="Two Shinguards", category = Soccer)
session.add(TwoShinguards)
session.commit()


BasketBall = Category(user_id=1, name = "BasketBall")
session.add(BasketBall)
session.commit()

Shoes = Item(title = "Shoes", user_id = 1, description = "The best BasketBall shoes in the market", category = BasketBall)
session.add(Shoes)
session.commit()

socks = Item(title = "Basketball Socks", user_id = 1, description = "Nice fit, finish, very comfortable, and stylish", category = BasketBall)
session.add(socks)
session.commit()

Basketb = Item(title = "BasketBall", user_id = 1, description = "BasketBall", category = BasketBall)
session.add(Basketb)
session.commit()

Headbands = Item(title = "Headbands", user_id = 1, description = "Head Bands to relieve stress on the head", category = BasketBall)
session.add(Headbands)
session.commit()

BaseBall = Category(user_id=1, name = "BaseBall")
session.add(BaseBall)
session.commit()

Bat = Item(title = "Bat", user_id = 1, description = "The best BaseBall Bat in the market", category = BaseBall)
session.add(Bat)
session.commit()

BattingGloves = Item(title = "Batting Gloves", user_id = 1, description = "Hand Gloves to help achieve a solid grip", category = BaseBall)
session.add(BattingGloves)
session.commit()

BaseBallCleats = Item(title = "Baseball Cleats", user_id = 1, description = "Baseball Cleats to help in movement", category = BaseBall)
session.add(BaseBallCleats)
session.commit()

Frisbee = Category(user_id=1, name = "Frisbee")
session.add(Frisbee)
session.commit()

Snowboarding = Category(user_id=1, name = "Snowboarding")
session.add(Snowboarding)
session.commit()

Snowboard = Item(title = "Snowboard", user_id = 1, description = "The best snowboard that makes you feel confident", category = Snowboarding)
session.add(Snowboard)
session.commit()

Goggles = Item(title = "Googles", user_id = 1, description = "Goggles", category = Snowboarding)
session.add(Goggles)
session.commit()


RockClimbing = Category(user_id=1, name = "RockClimbing")
session.add(RockClimbing)
session.commit()

Football = Category(user_id=1, name = "Football")
session.add(Football)
session.commit()

Skating = Category(user_id=1, name = "Skating")
session.add(Skating)
session.commit()

Hockey = Category(user_id=1, name = "Hockey")
session.add(Hockey)
session.commit()

Stick = Item(title = "Stick", user_id = 1, description = "hockey stick", category = Hockey)
session.add(Stick)
session.commit()




