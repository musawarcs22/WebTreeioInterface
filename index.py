from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for, jsonify
import sqlite3 as sql
import pyrebase
import json

##################################
app = Flask(__name__)

config = {
    "apiKey": "AIzaSyC_jZz1ZGq-jXptVH3iFxKRYaZk6C-ODO8",
    "authDomain": "treeiopro.firebaseapp.com",
    "databaseURL": "https://treeiopro-default-rtdb.firebaseio.com",
    "projectId": "treeiopro",
    "storageBucket": "treeiopro.appspot.com",
    "messagingSenderId": "896546914363",
    "appId": "1:896546914363:web:86f2ce4cbde5489b789c1e"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
#################################
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
   if (request.method == 'POST'):
      email = request.form['name']
      password = request.form['password']
      
      print(email+password)
      try:
            auth.sign_in_with_email_and_password(email, password)
            #user_id = auth.get_account_info(user['idToken'])
            #session['usr'] = user_id
            return render_template('home.html')
      except:
            unsuccessful = 'Please check your credentials'
            return render_template('login.html', umessage=unsuccessful)
   return render_template('login.html')


@app.route('/logout')
def logout():
   return render_template('login.html')

@app.route('/newrecord',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         with sql.connect("database.db") as con:
            cur = con.cursor()
            #cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            cur.execute("INSERT INTO mystudents (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/delrecord',methods = ['POST', 'GET'])

#For Deleting Records
def delrecord():
   s_id = None
   if request.method == 'POST' or request.method == 'GET':
      try:
         s_id = request.form['student_id']         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            #cur.execute("DELETE TABLE mystudents")

            cur.execute("DELETE FROM mystudents WHERE student_id = (?)",s_id)
            con.commit()
            msg = "Record successfully deleted"
            return redirect(url_for('list'))
      except:
         con.rollback()
         msg = "error in delete operation"
         return redirect(url_for('list'))
      finally:
         return redirect(url_for('list'))
         con.close()

@app.route('/list', methods=['POST'])
def list():
   db = firebase.database()
   records = db.child("+923099721779").get()
   print(records)
   print(records.val()) # {"Morty": {"name": "Mortimer 'Morty' Smith"}, "Rick": {"name": "Rick Sanchez"}}
   
   print("+++++++++++++++++++++++++++++++++++++++++++\n\n\n")
   all_users = db.child("+923099721779").get()
   for user in all_users.each():
      print(user.key()) # -MgtBeNdzTQMn0wIaPDZ
    
      records = user.val().get("mImageTitle")
      print(records)
      records = user.val()["mlatitude"]
      print(records)
      records = user.val()["mlongitude"]    
      print(records)
      print("\n\n****************************\n\n")
      #print(user.val()) # {....}
      
   print(json.dumps(all_users.val()))
   data = json.dumps(all_users.val())
   #data = jsonify(data)
   print(data)
   return data



@app.route('/process_qtc', methods=['POST', 'GET'])
def process_qt_calculation():

    if request.method == "POST":
        qtc_data = request.get_json()
        print(qtc_data)
 
    results = {'processed': 'true'}
    return jsonify(results)


"""
@app.route('/')
def home():
   return render_template('home.html')
"""

if __name__ == '__main__':
   app.run(debug = True)


#### create table 
"""
import sqlite3
conn = sqlite3.connect('database.db')
print("Opened database successfully")
conn.execute('CREATE TABLE mystudents (student_id INTEGER PRIMARY KEY,name TEXT, addr TEXT, city TEXT, pin TEXT)')
print("Table created successfully")
conn.close()
print("asdasda")
"""
