from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event # need to make foreign key constraint configuration function
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import linked_list

# App  
app = Flask(__name__) # points to a flask object

# Database configuration
# Allows use of local file as database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

# configure sqlite3 to enforce foreign key constraints

# connect database to app
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
    email = db.Column(db.String(50))
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


@app.route("/user", methods=["POST"])
def create_user(): 
    data = request.get_json()   
    new_user = User(
        name  = data["name"],
        email  = data["email"],
        address  = data["address"],
        phone  = data["phone"],
    )
    db.session.add(new_user) 
    db.session.commit()   
    return jsonify({"message": "User Created"}), 200


@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    users = User.query.all() # returns users in ascending order by id
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "address": user.address,
                "phone": user.phone,

            }
        )
    return jsonify(all_users_ll.to_list()), 200

@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    pass

@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    pass

@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    pass

@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    pass

@app.route("/user/<user_id>", methods=["GET"])
def get_all_blog_posts(user_id):
    pass

@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    pass

@app.route("/blog_post/<blog_post_id>", methods=["DELETE"])
def delete_blog_post(blog_post_id): 
    pass

if __name__ == "__main__":
    app.run(debug=True)