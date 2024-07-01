from datetime import datetime
from app.extensions import db


class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    restock_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    location = db.Column(db.String(255), nullable=True)
    
    parent_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=True)
    children = db.relationship('Inventory', backref=db.backref('parent', remote_side=[id]))

    # Define the relationship with the products table
    product = db.relationship('Product', back_populates='inventory_items', overlaps="inventory_items,product")
