from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.extensions import db, migrate, bcrypt, jwt

# Import blueprints
from app.controllers.auth.auths_controllers import auth
from app.controllers.auth.category_controllers import categories
from app.controllers.auth.customers_controllers import customer
from app.controllers.auth.inventory_controllers import inventory
from app.controllers.auth.orders_controllers import order
from app.controllers.auth.products_controllers import products

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('config.Config')

    # Configure your JWT secret key
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure key

    # Enable debug mode
    app.config['DEBUG'] = True

    # Initialize extensions
    db.init_app(app)  # Ensure SQLAlchemy is properly initialized with the app
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/api/v1/auth')
    app.register_blueprint(categories, url_prefix='/api/v1/categories')
    app.register_blueprint(customer, url_prefix='/api/v1/customers')
    app.register_blueprint(inventory, url_prefix='/api/v1/inventory')
    app.register_blueprint(order, url_prefix='/api/v1/orders')
    app.register_blueprint(products, url_prefix='/api/v1/products')

    # Import models to ensure they are registered with SQLAlchemy
    from app.models.category import Category
    from app.models.customers import Customer
    from app.models.inventory import Inventory
    from app.models.orders import Order
    from app.models.products import Product
    from app.models.users import User

    @app.route('/')
    def home():
        print("Home route accessed") 
        return "Welcome to our bakery shop"

    @app.errorhandler(500)
    def internal_error(error):
        print(f"Internal Server Error: {error}")  
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
