from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///trantable.db', echo = True)
Base = declarative_base()

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key = True)
    userId = Column(Integer, nullable = False)
    tranName = Column(String, nullable = False)
    tranVal = Column(Integer, nullable = False)
    tranDesc = Column(String, nullable=True)

    def __init__(self, user, name, val, desc):
        self.userId = user
        self.tranName = name
        self.tranVal = val
        self.tranDesc = desc

Base.metadata.create_all(engine)