from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///trantable.db', echo = False)
Base = declarative_base()

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key = True)
    userId = Column(Integer, nullable = False)
    tranName = Column(String, nullable = False)
    tranVal = Column(Integer, nullable = False)
    tranDesc = Column(String, nullable = True)
    tranDate = Column(String, nullable = False)

    def __init__(self, user, name, val, desc, date):
        self.userId = user
        self.tranName = name
        self.tranVal = val
        self.tranDesc = desc
        self.tranDate = date

Base.metadata.create_all(engine)