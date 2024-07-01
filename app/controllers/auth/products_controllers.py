from datetime import datetime
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.products import Product

products = Blueprint('products',__name__, url_prefix='/api/v1/products')

@products.route('/create', methods=['POST'])
def create_product():
    data = request.get_json()
    try:
        new_product = Product(
            category_id=data['category_id'],
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            quantity=data['quantity'],
            image=data.get('image')
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@products.route('/update/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'category_id': product.category_id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'quantity': product.quantity,
        'image': product.image,
        'created_at': product.created_at,
        'updated_at': product.updated_at
    })

@products.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    try:
        product.category_id = data.get('category_id', product.category_id)
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.quantity = data.get('quantity', product.quantity)
        product.image = data.get('image', product.image)
        product.updated_at = datetime.now()
        
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@products.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
