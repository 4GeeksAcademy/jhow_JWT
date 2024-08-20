"""empty message

Revision ID: 0219f6b4abc3
Revises: 54b0d7941a74
Create Date: 2024-08-16 17:15:45.009222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0219f6b4abc3'
down_revision = '54b0d7941a74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.Date(), nullable=False))
        batch_op.alter_column('bedtime',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
        batch_op.alter_column('water',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
        batch_op.alter_column('extra',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.alter_column('extra',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=120),
               existing_nullable=True)
        batch_op.alter_column('water',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('bedtime',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.drop_column('date')

    # ### end Alembic commands ###
