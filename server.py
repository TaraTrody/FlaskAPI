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
