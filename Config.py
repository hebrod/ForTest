from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

host = environ.get("DBHOST")
port = environ.get("DBPORT")
user = environ.get("DBUSERNAME")
clave = environ.get("DBUSERPASS")
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + user  + ':' + clave + '@' + host + ':' + port + '/ForTest'
app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy(app)