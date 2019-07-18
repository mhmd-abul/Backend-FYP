from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from tableapp import *
engine = create_engine('sqlite:///swiftpay.db', echo=True)

app = Flask(__name__)

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
        return render_template('dashboard.html')
    else:
        flash('Invalid Username and Password, Please Try Again')
    return home()


    """if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['login'] = True
    else:
        flash('Invalid Username and Password')
    return home()""" 



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
        abort(400) # existing user
    user = Student(tpnumber = tpnumber, password = password, balance = 0)
    session_database.add(user)
    session_database.commit()
    return jsonify({ 'tpnumber': user.tpnumber }), 201

    

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)