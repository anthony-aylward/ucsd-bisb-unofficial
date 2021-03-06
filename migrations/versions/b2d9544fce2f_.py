"""empty message

Revision ID: b2d9544fce2f
Revises: f1eb35e2d0dc
Create Date: 2019-07-22 15:44:28.046126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2d9544fce2f'
down_revision = 'f1eb35e2d0dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('confidentiality_agreed', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('confidentiality_agreed_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'confidentiality_agreed_on')
    op.drop_column('user', 'confidentiality_agreed')
    # ### end Alembic commands ###
