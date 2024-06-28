from datetime import datetime
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    # Relationships
    orders = db.relationship('Order', back_populates='user')
    customers = db.relationship('Customer', back_populates='user', cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, password, user_type, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.user_type = user_type
        self.is_admin = is_admin

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"

