from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for
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
            user = auth.sign_in_with_email_and_password(email, password)
            user_id = auth.get_account_info(user['idToken'])
            session['usr'] = user_id
            #
            try:
                if (session['usr']):
                    return render_template('home.html')
            except:
                unsuccessful = 'Please Login'
                return render_template('login.html', umessage=unsuccessful)
      except:
            unsuccessful = 'Please check your credentials'
            return render_template('login.html', umessage=unsuccessful)
   return render_template('login.html')


@app.route('/logout')
def logout():
    try:
        session.pop('usr',None)
        return render_template('login.html')
    except:
        pass

@app.route('/getRecordsFromFirebase', methods=['POST'])
def getRecordsFromFirebase():
    
   UserId = "+923099721779" #I was suppose to get this value after phone authentication using OTP
   # but pyrebase doesn't support phone authentication. That's why I have hardcoded it. In future, 
   # I will add an option for the users using the mobile app to link their accounts to their web 
   # app so that I may get the user id using emails of the users.
   db = firebase.database()
   records = db.child(UserId).get()
   #print(records)
   #print(records.val()) 
   #print("+++++++++++++++++++++++++++++++++++++++++++\n\n\n")
   all_users = db.child(UserId).get()
   for user in all_users.each():
      print(user.key()) # some thing like: -MgtBeNdzTQMn0wIaPDZ
    
      records = user.val().get("mImageTitle")
      print(records)
      records = user.val()["mlatitude"]
      print(records)
      records = user.val()["mlongitude"]    
      print(records)
      print("\n\n****************************\n\n")
      #print(user.val()) # {....}
      
   #print(json.dumps(all_users.val()))
   data = json.dumps(all_users.val())
   #print(data)
   return data




if __name__ == '__main__':
   app.secret_key = "1^#$1212121asd/asdad/ad23435##$@#$" 
   app.run(debug = True)
