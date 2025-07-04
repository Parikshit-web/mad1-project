from flask import render_template,request,url_for,flash,redirect,session
from app import app
from extension import db
from datetime import datetime, time
from models import db, Admin,User,Subject,Quiz,Question,Chapter,Scores
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from config import Config
from sqlalchemy import func

ADMIN_USERNAME = Config.ADMIN_USERNAME
ADMIN_PASSWORD = Config.ADMIN_PASSWORD

@app.route('/')
def index():
     db.create_all()
     if not Admin.query.first():
         new_admin= Admin(username ="admin", password=generate_password_hash("adminpassword@123"))
         db.session.add(new_admin)
         db.session.commit()
    return render_template('index.html')
     

   
# --------------------------------------------------------------------login----------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
      username=request.form.get('username')
      password=request.form.get('password')

      if not username or not password:
        flash("Enter username and password")
        return redirect(url_for('login'))
      
      admin=Admin.query.filter_by(username=username).first()

      if admin and check_password_hash(admin.password, password):
          flash("Admin logged in successfully")
          session['user_id'] = admin.id
          return redirect(url_for('admin'))

      user=User.query.filter_by(username=username).first()  

      if not user:
        flash("Username does not exists") 
        return redirect(url_for('login'))
      if not check_password_hash(user.passhash, password):
        flash('Incorrect password')
        return redirect(url_for('login'))
    
    
      session['user_id']=user.id
      flash(" User loged in successfully")  
      return redirect('user_dashboard')

    return render_template('login.html')

# ----------------------------------------------------------------login end-------------------------------------------------------------------------

#-----------------------------------------------------------------register--------------------------------------------------------------------------     
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':

      username=request.form.get('username')
      password=request.form.get('password')
      c_password=request.form.get('password1')
      fullname=request.form.get('fullname')
      qualification=request.form.get('qualification')
      dob=request.form.get('dob')
      date_object=datetime.strptime(dob,'%Y-%m-%d')
    
      if not username or not password or not c_password:
        flash("please fill out all these fields")
        return redirect(url_for('register'))
      if password!=c_password:
        flash("Password do not match ")
        return redirect(url_for('register'))
      user = User.query.filter_by(username=username).first()
      if user:
        flash('Username already exists')
        return redirect(url_for('register'))
    
      password_hash=generate_password_hash(password)
      new_user = User(username=username, passhash=password_hash, fullName=fullname, qualification=qualification, dob=date_object)
      db.session.add(new_user)
      db.session.commit()
      flash("Registration successfull")
      return redirect(url_for('login'))
    
    return render_template('register.html')
# ------------------------------------------------------------------register end-------------------------------------------------------------------------
# ------------------------------------------------------------------auth----------------------------------------------------------------------------------
def auth_require(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            flash("please login to continue")
            return redirect(url_for('login'))
    return inner