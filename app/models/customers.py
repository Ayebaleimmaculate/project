from datetime import datetime
from app.extensions import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    # Relationships
    user = db.relationship('User', back_populates='customers')
    orders = db.relationship('Order', back_populates='customer')

    def __init__(self, user_id, first_name, last_name, email, phone_number, address, gender=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.gender = gender

    def update_contact(self, new_contact):
        self.phone_number = new_contact

    def update_address(self, new_address):
        self.address = new_address

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_customer_details(self):
        return {
            'full_name': self.get_full_name(),
            'email': self.email,
            'contact': self.phone_number,
            'address': self.address,
            'join_date': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as string
            'gender': self.gender
        }
