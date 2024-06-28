from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flasgger import  Swagger


db = SQLAlchemy()   
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
swagger = Swagger()

