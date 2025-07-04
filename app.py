from flask import Flask, render_template,request , redirect, url_for , flash
from config import Config
from extension import db, migrate

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
  
from models import * 
from routes import *  

if __name__ == '__main__':  
    with app.app_context():
        db.create_all()
        print("✅ Tables created, DB should exist at:", app.config['SQLALCHEMY_DATABASE_URI'])

    app.run(debug=True)  
