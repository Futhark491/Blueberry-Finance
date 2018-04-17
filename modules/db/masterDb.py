from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///master.db', echo = True)
Base = declarative_base()

class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key = True)
    userId = Column(Integer, nullable = False)
    catName = Column(String, nullable = False)
    catVal = Column(Integer, nullable = False)

    def __init__(self, user, name, val):
        self.userId = user
        self.catName = name
        self.catVal = val

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    income = Column(Integer, nullable = True)

    def __init__(self, username, password, income):
        self.username = username
        self.password = password
        self.income = income

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key = True)
    userId = Column(Integer, nullable = False)
    tranCat = Column(String, nullable = False)
    tranVal = Column(Integer, nullable = False)
    tranDesc = Column(String, nullable = True)
    tranDate = Column(String, nullable = False)

    def __init__(self, user, cat, val, desc, date):
        self.userId = user
        self.tranCat = cat
        self.tranVal = val
        self.tranDesc = desc
        self.tranDate = date

Base.metadata.create_all(engine)
