from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///cattable.db', echo = True)
Base = declarative_base()

class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key = True)
    userId = Column(Integer, nullable = False)
    catName = Column(String, nullable = False)
    catVal = Column(Integer, nullable = False)
    tranList = Column(String, nullable = True)

    def __init__(self, user, name, val, tranlist):
        self.userId = user
        self.catName = name
        self.catVal = val
        self.tranList = tranlist


Base.metadata.create_all(engine)