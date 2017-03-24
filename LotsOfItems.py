from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

Soccer = Category(name = "Soccer")
session.add(Soccer)
session.commit()

Shinguards = Item(title = "Shinguards", description = "The best shinguards to protect players from injuries", category = Soccer)
session.add(Shinguards)
session.commit()

Jersey = Item(title ="Jersey", description="Soccer Player Clothing", category = Soccer)
session.add(Jersey)
session.commit()

SoccerCleats = Item(title = "Soccer Cleats", description="The best Soccer Cleats to help in movement", category = Soccer)
session.add(SoccerCleats)
session.commit()

TwoShinguards = Item(title = "Two Shinguards", description="Two Shinguards", category = Soccer)
session.add(TwoShinguards)
session.commit()


BasketBall = Category(name = "BasketBall")
session.add(BasketBall)
session.commit()

Shoes = Item(title = "Shoes", description = "The best BasketBall shoes in the market", category = BasketBall)
session.add(Shoes)
session.commit()

socks = Item(title = "Basketball Socks", description = "Nice fit, finish, very comfortable, and stylish", category = BasketBall)
session.add(socks)
session.commit()

Basketb = Item(title = "BasketBall", description = "BasketBall", category = BasketBall)
session.add(Basketb)
session.commit()

Headbands = Item(title = "Headbands", description = "Head Bands to relieve stress on the head", category = BasketBall)
session.add(Headbands)
session.commit()

BaseBall = Category(name = "BaseBall")
session.add(BaseBall)
session.commit()

Bat = Item(title = "Bat", description = "The best BaseBall Bat in the market", category = BaseBall)
session.add(Bat)
session.commit()

BattingGloves = Item(title = "Batting Gloves", description = "Hand Gloves to help achieve a solid grip", category = BaseBall)
session.add(BattingGloves)
session.commit()

BaseBallCleats = Item(title = "Baseball Cleats", description = "Baseball Cleats to help in movement", category = BaseBall)
session.add(BaseBallCleats)
session.commit()

Frisbee = Category(name = "Frisbee")
session.add(Frisbee)
session.commit()

Snowboarding = Category(name = "Snowboarding")
session.add(Snowboarding)
session.commit()

Snowboard = Item(title = "Snowboard", description = "The best snowboard that makes you feel confident", category = Snowboarding)
session.add(Snowboard)
session.commit()

Goggles = Item(title = "Googles", description = "Goggles", category = Snowboarding)
session.add(Goggles)
session.commit()


RockClimbing = Category(name = "RockClimbing")
session.add(RockClimbing)
session.commit()

Football = Category(name = "Football")
session.add(Football)
session.commit()

Skating = Category(name = "Skating")
session.add(Skating)
session.commit()

Hockey = Category(name = "Hockey")
session.add(Hockey)
session.commit()

Stick = Item(title = "Stick", description = "hockey stick", category = Hockey)
session.add(Stick)
session.commit()




