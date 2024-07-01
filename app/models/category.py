from app.extensions import db
from datetime import datetime

# db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)


#relationship
    products = db.relationship('Product', back_populates='category', overlaps="category_associated")


    def __repr__(self):
        return f'<Category {self.name}>'