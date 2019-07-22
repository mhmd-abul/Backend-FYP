from sqlalchemy import *
import datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from tableapp import *

engine = create_engine('sqlite:///swiftpay.db', echo=True)
Base = declarative_base()

########################################################################
class Transaction(Base):
    
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)
    tpnumber = Column(String, nullable=False) # (Student.tpnumber) --> Class.entity
    date = Column(DateTime)
    transaction_type = Column(String)
    nominal = Column(Integer)
    

#----------------------------------------------------------------------
    def __init__(self, tpnumber, transaction_type, nominal):
        
        self.tpnumber = tpnumber
        self.date = datetime.datetime.utcnow()
        self.transaction_type = transaction_type
        self.nominal = nominal

# create tables
Base.metadata.create_all(engine)