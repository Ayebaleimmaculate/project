from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.orders import Order
from datetime import datetime
from app.models.users import User
from app.models.customers import Customer
from app.models.products import Product


order = Blueprint('orders', __name__, url_prefix='/api/v1/orders')

@order.route('/created', methods=['POST'])
def create_order():
    data = request.get_json()
    try:
        new_order = Order(
            customer_id=data['customer_id'],
            product_id=data['product_id'],
            user_id=data['user_id'],
            status=data['status'],
            quantity=data['quantity'],
            total_price=data['total_price'],
            gender=data.get('gender')
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@order.route('/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify({
        'id': order.id,
        'customer_id': order.customer_id,
        'product_id': order.product_id,
        'user_id': order.user_id,
        'status': order.status,
        'quantity': order.quantity,
        'total_price': order.total_price,
        'created_at': order.created_at,
        'updated_at': order.updated_at,
        'gender': order.gender
    })


@order.route('/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()
    try:
        # Update order attributes based on the data received
        order.customer_id = data.get('customer_id', order.customer_id)
        order.product_id = data.get('product_id', order.product_id)
        order.user_id = data.get('user_id', order.user_id)
        order.status = data.get('status', order.status)
        order.quantity = data.get('quantity', order.quantity)
        order.total_price = data.get('total_price', order.total_price)
        order.gender = data.get('gender', order.gender)
        order.updated_at = datetime.now()
        
        db.session.commit()
        return jsonify({'message': 'Order updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
@order.route('/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    try:
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
