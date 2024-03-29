from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, url_for
import os
import json
from sqlalchemy.orm import sessionmaker
from tabledef import *
from tableapp import *
from historytable import *
from flask_marshmallow import Marshmallow
from sqlalchemy import desc
engine = create_engine('sqlite:///swiftpay.db', echo=True)

app = Flask(__name__)

ma = Marshmallow(app)

class TransactionSchema(ma.Schema):
    class Meta:
        fields = ('tpnumber', 'date', 'transaction_type', 'nominal')

transaction_schema = TransactionSchema(many=True)

@app.route('/')
def home():
    if not session.get('login'):
        return render_template('login.html')
    else:
        return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def admin_login():
    
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    session_database = Session() #important note
    query = session_database.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['login'] = True
        return redirect(url_for('overview_transaction'))
    else:
        flash('Invalid Username and Password, Please Try Again')
        return render_template('login.html', message='Invalid Username and Password, Please Try Again')
    return render_template('login.html')

@app.route("/logout")
def logout():
    session['login'] = False
    return render_template('homepage.html')

@app.route("/login_page")
def login_page():
    return render_template ('login.html')

@app.route('/username', methods=['POST'])
def username():
    POST_USERNAME = str(request.form['username'])
    Session = sessionmaker(bind=engine)
    session_database = Session() #important note
    query = session_database.query(User).filter(User.username.in_([POST_USERNAME]))
    return render_template('dashboard.html', appuser=POST_USERNAME)
    result = query.first()

@app.route('/student_registration', methods = ['POST'])
def student_registration():
    tpnumber = request.json.get('tpnumber')
    password = request.json.get('password')
    print(tpnumber)
    print(password)
    Session = sessionmaker(bind=engine)
    session_database = Session() #important note
    if tpnumber is None or password is None:
        abort(400) # missing arguments
    if session_database.query(Student).filter_by(tpnumber = tpnumber).first() is not None:
        return jsonify({ 'error': 'TP number is already existing' }), 201
    user = Student(tpnumber = tpnumber, password = password, balance = 0)
    session_database.add(user)
    session_database.commit()
    return jsonify({ 'tpnumber': user.tpnumber, 'balance': user.balance }), 201

@app.route('/student_login', methods = ['POST'])
def student_login():
    tpnumber = request.json.get('tpnumber')
    password = request.json.get('password')
    Session = sessionmaker(bind=engine)
    session_database = Session() #important note
    if tpnumber is None or password is None:
        abort(400) # missing arguments

    query = session_database.query(Student).filter(Student.tpnumber.in_([tpnumber]), Student.password.in_([password]))
    result = query.first()
    if result:
        print('success')
        return jsonify({ 'tpnumber': result.tpnumber , 'balance': result.balance }), 201
    else:
        print('Invalid User')
        return jsonify({ 'error': 'Invalid user' }), 201


@app.route('/student_topup', methods = ['POST'])
def student_topup():
    tpnumber = request.json.get('tpnumber')
    transaction_type = request.json.get('transaction_type')
    nominal = request.json.get('nominal')
    print(tpnumber)
    print(transaction_type)
    print(nominal)
    Session = sessionmaker(bind=engine)
    session_database = Session() #important note
    if tpnumber is None or transaction_type is None or nominal is None:
        abort(400) # missing arguments
    history = Transaction(tpnumber = tpnumber, transaction_type = transaction_type, nominal = nominal)
    session_database.add(history)
    session_database.commit()

    student = session_database.query(Student).filter_by(tpnumber=tpnumber).first()
    student.balance += nominal
    session_database.commit()

    return jsonify({
        'tpnumber': student.tpnumber,
        'balance': student.balance
        }), 201


@app.route('/student_payment', methods = ['POST'])
def student_payment():
    tpnumber = request.json.get('tpnumber')
    transaction_type = request.json.get('transaction_type')
    nominal = request.json.get('nominal')
    print(tpnumber) #for debugging and checking the value only, removing this line is wont affecting the program
    print(transaction_type) #for debugging and checking the value only, removing this line is wont affecting the program
    print(nominal) #for debugging and checking the value only, removing this line is wont affecting the program
    Session = sessionmaker(bind=engine)
    session_database = Session() #important note
    if tpnumber is None or transaction_type is None or nominal is None:
        abort(400) # missing arguments
    history = Transaction(tpnumber = tpnumber, transaction_type = transaction_type, nominal = nominal)
    session_database.add(history)
    session_database.commit()

    student = session_database.query(Student).filter_by(tpnumber=tpnumber).first()
    student.balance -= nominal
    session_database.commit()

    return jsonify({
        'tpnumber': student.tpnumber,
        'balance': student.balance
        }), 201

@app.route('/student_transaction/<tpnumber>', methods = ['GET'])
def student_transaction(tpnumber):
    Session = sessionmaker(bind=engine)
    session_database = Session() #important note
    transaction = session_database.query(Transaction).filter_by(tpnumber=tpnumber).order_by(desc(Transaction.date)).all()
    transaction_serialized = transaction_schema.dump(transaction)
    return jsonify(transaction_serialized.data)


@app.route('/overview_transaction', methods = ['GET'])
def overview_transaction():
    Session = sessionmaker(bind=engine)
    session_database = Session() #important note
    transaction = session_database.query(Transaction).order_by(desc(Transaction.date)).all()
    return render_template('dashboard.html', transaction_display = transaction)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)