"""empty message

Revision ID: b3e18cba552b
Revises: e92246b53b8a
Create Date: 2023-04-18 18:50:37.088858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3e18cba552b'
down_revision = 'e92246b53b8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=250), nullable=False))
        batch_op.create_unique_constraint(None, ['cif'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('password')

    # ### end Alembic commands ###
