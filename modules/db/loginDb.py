from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///usertable.db', echo = True)
Base = declarative_base()


class User(Base):
        __tablename_ = "users"

        id = Column(Integer, primary_key = True)
        username = Column(String, nullable = False)
        password = Column(String, nullable = False)

        def __init__(self, username, password):

            self.username = username
            self.password = password


Base.metadata.create_all(engine)