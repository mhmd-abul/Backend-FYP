import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tableapp import *

engine = create_engine('sqlite:///swiftpay.db', echo=True)

# create a Session
# Session = sessionmaker(bind=engine)
# session = Session()

# user = User("mobile","password")
# session.add(user)
Student.__table__.drop(engine)

# commit the record the database
# session.commit()