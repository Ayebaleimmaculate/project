"""Add columns and relationships to models

Revision ID: 72437be837af
Revises: ba703a5ad933
Create Date: 2024-06-24 15:48:58.836550

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '72437be837af'
down_revision = 'ba703a5ad933'
branch_labels = None
depends_on = None


def table_exists(table_name):
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    return table_name in inspector.get_table_names()


def upgrade():
    # Create Users table if it doesn't exist
    if not table_exists('users'):
        op.create_table(
            'users',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('username', sa.String(100), nullable=False, unique=True),
            # Add other columns as needed
        )

    # Create Categories table if it doesn't exist
    if not table_exists('categories'):
        op.create_table(
            'categories',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(100), unique=True, nullable=False),
            sa.Column('description', sa.String(255), nullable=True),
            sa.Column('created_at', sa.DateTime, default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now()),
        )

    # Create Products table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('stock_quantity', sa.Integer, nullable=False),
        sa.Column('image', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('categories.id'), nullable=False),
    )

    # Create Orders table
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('customer_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id'), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('total_price', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Create Inventory table
    op.create_table(
        'inventory',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id'), nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('restock_date', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('location', sa.String(255), nullable=True),
    )

    # Create Customers table
    op.create_table(
        'customers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('customer_name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(120), nullable=False, unique=True),
        sa.Column('contact', sa.String(20), nullable=False),
        sa.Column('address', sa.String(200), nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('gender', sa.String(10), nullable=True),
    )


def downgrade():
    # Drop tables in reverse order
    op.drop_table('customers')
    op.drop_table('inventory')
    op.drop_table('orders')
    op.drop_table('products')
    op.drop_table('categories')
    op.drop_table('users')
