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


    def __init__(self, user, name, val):
        self.userId = user
        self.catName = name
        self.catVal = val


Base.metadata.create_all(engine)