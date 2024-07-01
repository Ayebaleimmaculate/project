from datetime import datetime
from app.extensions import db



class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    gender = db.Column(db.String(10), nullable=True)

    # Relationships
    customer = db.relationship('Customer', back_populates='orders')
    product = db.relationship('Product', back_populates='orders')
    user = db.relationship('User', back_populates='orders', overlaps="customer")

def __init__(self, customer_id, product_id, user_id, status, quantity, total_price, gender=None):
        self.customer_id = customer_id
        self.product_id = product_id
        self.user_id = user_id
        self.status = status
        self.quantity = quantity
        self.total_price = total_price
        self.gender = gender