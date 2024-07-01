from flask import Blueprint, request, jsonify
from app.models.category import Category
from app.extensions import db
from flask_jwt_extended import jwt_required

categories = Blueprint('categories', __name__, url_prefix='/api/v1/categories')

@categories.route('/register', methods=['POST'])
@jwt_required()
def create_category():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400

        name = data.get('name')
        description = data.get('description')

        if not name:
            return jsonify({'error': 'Name field is required'}), 400

        new_category = Category(
            name=name,
            description=description,
        )

        db.session.add(new_category)
        db.session.commit()

        return jsonify({
            "message": f"Category '{new_category.name}', ID '{new_category.id}' has been created",
            "category": {
                'id': new_category.id,
                'name': new_category.name,
                'description': new_category.description,
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@categories.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    try:
        category = Category.query.get(category_id)
        if category is None:
            return jsonify({"error": f"Category with ID {category_id} not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400

        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']

        db.session.commit()

        return jsonify({
            "message": f"Category with ID {category_id} successfully updated",
            "category": {
                'id': category.id,
                'name': category.name,
                'description': category.description,
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@categories.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    try:
        category = Category.query.get(id)
        if not category:
            return jsonify({'error': 'Category does not exist'}), 404

        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
