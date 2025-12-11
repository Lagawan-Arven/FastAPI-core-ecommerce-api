from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String,Integer,Column,ForeignKey

Base = declarative_base()

class Customer(Base):
    __tablename__ = "Customers"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    age = Column(Integer)
    sex = Column(String)
    occupation = Column(String)

    username = Column(String)
    password = Column(String)