from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.customers import Customer
from http import HTTPStatus
import validators


customer = Blueprint('customers', __name__, url_prefix='/api/v1/customers')

@customer.route('/register', methods=['POST'])
def register_customer():
    data = request.get_json()
    user_id = data.get('user_id')  # Assuming user_id is passed in the request
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    address = data.get('address')

    if not all([user_id, first_name, last_name, email, phone_number, address]):
        return jsonify({'error': 'All fields are required'}), HTTPStatus.BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': 'Email is not valid'}), HTTPStatus.BAD_REQUEST

    if Customer.query.filter_by(email=email).first():
        return jsonify({'error': 'Email address already in use'}), HTTPStatus.BAD_REQUEST

    try:
        new_customer = Customer(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address,
        )
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({
            'message': f'Customer {new_customer.get_full_name()} has been successfully registered!',
            'customer': {
                'id': new_customer.id,
                'email': new_customer.email,
                'created_at': new_customer.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format date as string
            }
        }), HTTPStatus.CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@customer.route('/update/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    phone_number = data.get('phone_number')
    address = data.get('address')

    if not phone_number and not address:
        return jsonify({'error': 'At least one field (phone_number or address) is required'}), HTTPStatus.BAD_REQUEST

    try:
        customer = Customer.query.get(id)
        if not customer:
            return jsonify({'error': 'Customer not found!'}), HTTPStatus.NOT_FOUND

        if phone_number:
            customer.update_contact(phone_number)
        if address:
            customer.update_address(address)

        db.session.commit()
        return jsonify({'message': 'Customer updated successfully!'}), HTTPStatus.OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@customer.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()

    return jsonify({'message': 'Customer deleted successfully'}), HTTPStatus.OK
