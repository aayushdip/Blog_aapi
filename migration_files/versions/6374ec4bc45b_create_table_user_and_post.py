"""Create User and Todo tables

Revision ID: 001
Revises: None
Create Date: 2023-07-20 08:40:50.093249

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('fullname', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String()),
        sa.Column('is_active', sa.Boolean(), default=True),
    )

    op.create_table(
        'todo',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('title', sa.String(), index=True),
        sa.Column('description', sa.String(), index=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey("users.id")),
    )


def downgrade():
    op.drop_table('todo')
    op.drop_table('users')
