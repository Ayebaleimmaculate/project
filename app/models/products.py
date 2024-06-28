from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.extensions import db


# db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=True)  # URL or file path
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    # Relationships
    inventory_items = db.relationship('Inventory', back_populates='product', overlaps="product_inventory")
    orders = db.relationship('Order', back_populates='product', overlaps="product_inventory")
    category = db.relationship('Category', back_populates='products', overlaps="products")
