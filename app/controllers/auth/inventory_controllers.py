from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.inventory import Inventory
from datetime import datetime

inventorys = Blueprint('inventory', __name__, url_prefix='/api/inventory')

# Endpoint to create a new inventory item
@inventorys.route('/create', methods=['POST'])
def create_inventory():
    data = request.get_json()
    
    # Data validation can be added here
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    restock_date = data.get('restock_date')
    location = data.get('location')
    parent_id = data.get('parent_id')
    
    new_inventory = Inventory(
        product_id=product_id,
        quantity=quantity,
        restock_date=datetime.fromisoformat(restock_date) if restock_date else datetime.now(),
        location=location,
        parent_id=parent_id
    )
    
    db.session.add(new_inventory)
    db.session.commit()
    
    return jsonify({
        'message': 'Inventory item created successfully',
        'inventory': {
            'id': new_inventory.id,
            'product_id': new_inventory.product_id,
            'quantity': new_inventory.quantity,
            'restock_date': new_inventory.restock_date.isoformat(),
            'location': new_inventory.location,
            'parent_id': new_inventory.parent_id
        }
    }), 201

# Endpoint to update an inventory item
@inventorys.route('/<int:id>', methods=['PUT'])
def update_inventory(id):
    inventory = Inventory.query.get_or_404(id)
    data = request.get_json()
    
    # Update inventory attributes based on data received
    inventory.product_id = data.get('product_id', inventory.product_id)
    inventory.quantity = data.get('quantity', inventory.quantity)
    inventory.restock_date = datetime.fromisoformat(data.get('restock_date')) if data.get('restock_date') else inventory.restock_date
    inventory.location = data.get('location', inventory.location)
    inventory.parent_id = data.get('parent_id', inventory.parent_id)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Inventory item updated successfully',
        'inventory': {
            'id': inventory.id,
            'product_id': inventory.product_id,
            'quantity': inventory.quantity,
            'restock_date': inventory.restock_date.isoformat(),
            'location': inventory.location,
            'parent_id': inventory.parent_id
        }
    }), 200

# Endpoint to delete an inventory item
@inventorys.route('/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    inventory = Inventory.query.get_or_404(id)
    db.session.delete(inventory)
    db.session.commit()
    
    return jsonify({'message': 'Inventory item deleted successfully'}), 200
