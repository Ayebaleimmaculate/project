from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.orders import Order  # Assuming Order model is defined in app/models/orders.py

order = Blueprint('orders', __name__, url_prefix='/api/orders')

# Endpoint to create a new order
@order.route('/create', methods=['POST'])
def create_order():
    data = request.get_json()
    
    # Data validation can be added here
    customer_id = data.get('customer_id')
    product_id = data.get('product_id')
    status = data.get('status')
    quantity = data.get('quantity')
    total_price = data.get('total_price')
    gender = data.get('gender')  # Assuming gender can be included
    
    new_order = Order(
        customer_id=customer_id,
        product_id=product_id,
        status=status,
        quantity=quantity,
        total_price=total_price,
        gender=gender
    )
    
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify({
        'message': 'Order created successfully',
        'order': {
            'id': new_order.id,
            'customer_id': new_order.customer_id,
            'product_id': new_order.product_id,
            'status': new_order.status,
            'quantity': new_order.quantity,
            'total_price': new_order.total_price,
            'created_at': new_order.created_at,
            'updated_at': new_order.updated_at,
            'gender': new_order.gender
        }
    }), 201

# Endpoint to update an order
@order.route('/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()
    
    # Update order attributes based on data received
    order.customer_id = data.get('customer_id', order.customer_id)
    order.product_id = data.get('product_id', order.product_id)
    order.status = data.get('status', order.status)
    order.quantity = data.get('quantity', order.quantity)
    order.total_price = data.get('total_price', order.total_price)
    order.gender = data.get('gender', order.gender)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Order updated successfully',
        'order': {
            'id': order.id,
            'customer_id': order.customer_id,
            'product_id': order.product_id,
            'status': order.status,
            'quantity': order.quantity,
            'total_price': order.total_price,
            'created_at': order.created_at,
            'updated_at': order.updated_at,
            'gender': order.gender
        }
    })

# Endpoint to delete an order
@order.route('/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    
    return jsonify({'message': 'Order deleted successfully'}), 200

# Endpoint to get all orders
@order.route('/', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    serialized_orders = [{
        'id': order.id,
        'customer_id': order.customer_id,
        'product_id': order.product_id,
        'status': order.status,
        'quantity': order.quantity,
        'total_price': order.total_price,
        'created_at': order.created_at,
        'updated_at': order.updated_at,
        'gender': order.gender
    } for order in orders]
    
    return jsonify({'orders': serialized_orders}), 200
