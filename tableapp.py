from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///swiftpay.db', echo=True)
Base = declarative_base()

########################################################################
class Student(Base):
    
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    tpnumber = Column(String)
    password = Column(String)
    balance = Column(Integer)
    

#----------------------------------------------------------------------
    def __init__(self, tpnumber, password, balance):
        
        self.tpnumber = tpnumber
        self.password = password
        self.balance = balance

# create tables
Base.metadata.create_all(engine)