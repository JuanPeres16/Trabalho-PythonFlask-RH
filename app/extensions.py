from flask_migrate import Migrate
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
mongo = PyMongo()
