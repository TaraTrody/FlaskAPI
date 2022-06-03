from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event # need to make foreign key constraint configuration function
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify
# App  
app = Flask(__name__) # points to a flask object

# Database configuration
# Allows use of local file as database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()  
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


now = datetime.now()
# models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    name = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost")

class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)   
    # the blog post has a user Id associated and it's linked to the user Table so the id 
    # can't be null. That's why we use the enforce foreign key configuration above
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) 
