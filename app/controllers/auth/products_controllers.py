from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.products import Product

product = Blueprint('products', __name__, url_prefix='/api/products')

# Endpoint to create a new product
@product.route('/create', methods=['POST'])
def create_product():
    data = request.get_json()
    
    # Data validation can be added here
    name = data.get('name')
    category_id = data.get('category_id')
    description = data.get('description')
    price = data.get('price')
    stock_quantity = data.get('stock_quantity')
    image = data.get('image')
    
    new_product = Product(
        name=name,
        category_id=category_id,
        description=description,
        price=price,
        stock_quantity=stock_quantity,
        image=image
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({
        'message': 'Product created successfully',
        'product': {
            'id': new_product.id,
            'name': new_product.name,
            'category_id': new_product.category_id,
            'description': new_product.description,
            'price': str(new_product.price),
            'stock_quantity': new_product.stock_quantity,
            'image': new_product.image,
            'created_at': new_product.created_at,
            'updated_at': new_product.updated_at
        }
    }), 201

# Endpoint to update a product
@product.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    # Update product attributes based on data received
    product.name = data.get('name', product.name)
    product.category_id = data.get('category_id', product.category_id)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
    product.image = data.get('image', product.image)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Product updated successfully',
        'product': {
            'id': product.id,
            'name': product.name,
            'category_id': product.category_id,
            'description': product.description,
            'price': str(product.price),
            'stock_quantity': product.stock_quantity,
            'image': product.image,
            'created_at': product.created_at,
            'updated_at': product.updated_at
        }
    })

# Endpoint to delete a product
@product.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Product deleted successfully'}), 200
