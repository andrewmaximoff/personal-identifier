"""empty message

Revision ID: 00a058808dbe
Revises: 
Create Date: 2019-03-18 22:45:30.066824

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '00a058808dbe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('family',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('picture_path', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('name_lower', sa.String(length=64), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('family_id', postgresql.UUID(), nullable=True),
    sa.Column('picture_path', sa.String(length=1024), nullable=True),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('visit',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('visit_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', postgresql.UUID(), nullable=True),
    sa.Column('family_id', postgresql.UUID(), nullable=False),
    sa.Column('picture_path', sa.String(length=1024), nullable=True),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('visit')
    op.drop_table('user')
    op.drop_table('family')
    # ### end Alembic commands ###
