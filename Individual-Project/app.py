from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


Confing = {
  "apiKey": "AIzaSyDJ6vkFeCawvL7eCwTUMuK-SI6hcO7DZJA",
  "authDomain": "personal-2e819.firebaseapp.com",
  "projectId": "personal-2e819",
  "storageBucket": "personal-2e819.appspot.com",
  "messagingSenderId": "142795146406",
  "appId": "1:142795146406:web:ca301bd0b45f2f822f2067",
  "measurementId": "G-D3LZB688TW",
  "databaseURL":"https://personal-2e819-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase= pyrebase.initialize_app(Confing)
auth = firebase.auth()
db = firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signup():
  error = ""
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    age = request.form['age']
    try:
      login_session['user'] = auth.create_user_with_email_and_password(email, password)
      return redirect(url_for('signin'))
    except:
      error = "Authentication failed"
  return render_template("signup.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  error = ""
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    try:
      login_session['user'] = auth.sign_in_with_email_and_password(email, password)
      return redirect(url_for('homepage'))
    except:
      error = "Authentication failed"
  return render_template("signin.html")

@app.route('/home', methods=['GET', 'POST'])
def homepage():
  post = db.child("posts").get().val()
  user = db.child("users").get().val()
  return render_template("home.html", t = post )

@app.route('/add_post', methods=['GET', 'POST'])
def addpost():
        
  if request.method == 'POST':
    title = request.form["title"]
    text = request.form["text"]
    username = request.form["username"]
    try:
      post = {"title" : title, "text" : text , "uid":login_session['user']['localId'], "username": username}
      db.child("posts").push(post)
      return redirect(url_for('homepage'))
    except:
      error = "Authentication failed"
  return render_template("add_post.html")

@app.route('/about_us')
def aboutus():
  return render_template("about_us.html")

if __name__ == '__main__':
  app.run(debug=True)