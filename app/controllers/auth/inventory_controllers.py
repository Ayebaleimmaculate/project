from flask import Blueprint, request, jsonify
from datetime import datetime
from app.extensions import db
from app.models.inventory import Inventory
from app.models.products import Product
from http import HTTPStatus

inventory = Blueprint('inventory', __name__, url_prefix='/api/v1/inventory')

@inventory.route('/create', methods=['POST'])
def create_inventory_item():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    location = data.get('location')
    parent_id = data.get('parent_id')

    if not product_id or not quantity:
        return jsonify({'error': 'Product ID and quantity are required'}), HTTPStatus.BAD_REQUEST

    try:
        new_inventory = Inventory(
            product_id=product_id,
            quantity=quantity,
            restock_date=datetime.now(),
            location=location,
            parent_id=parent_id
        )
        db.session.add(new_inventory)
        db.session.commit()
        return jsonify({'message': 'Inventory item created successfully!', 'inventory_item': new_inventory.id}), HTTPStatus.CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@inventory.route('/<int:id>', methods=['GET'])
def get_inventory_item(id):
    inventory_item = Inventory.query.get(id)
    if not inventory_item:
        return jsonify({'error': 'Inventory item not found'}), HTTPStatus.NOT_FOUND

    return jsonify({
        'id': inventory_item.id,
        'product_id': inventory_item.product_id,
        'quantity': inventory_item.quantity,
        'restock_date': inventory_item.restock_date,
        'location': inventory_item.location,
        'parent_id': inventory_item.parent_id
    }), HTTPStatus.OK


@inventory.route('/<int:id>', methods=['PUT'])
def update_inventory_item(id):
    inventory_item = Inventory.query.get_or_404(id)
    data = request.get_json()
    try:
        if 'quantity' in data:
            inventory_item.quantity = data['quantity']
        if 'product_id' in data:
            inventory_item.product_id = data['product_id']
        if 'location' in data:
            inventory_item.location = data['location']
        
        db.session.commit()
        return jsonify({'message': 'Inventory item updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@inventory.route('/<int:id>', methods=['DELETE'])
def delete_inventory_item(id):
    try:
        inventory_item = Inventory.query.get(id)
        if not inventory_item:
            return jsonify({'error': 'Inventory item not found'}), HTTPStatus.NOT_FOUND

        db.session.delete(inventory_item)
        db.session.commit()
        return jsonify({'message': 'Inventory item deleted successfully!'}), HTTPStatus.OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
