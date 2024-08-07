"""some changes

Revision ID: fbe13515165f
Revises: 05ffc3e41f7d
Create Date: 2024-08-07 17:59:27.060270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbe13515165f'
down_revision = '05ffc3e41f7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('houseuser', schema=None) as batch_op:
        batch_op.drop_index('house_id')
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('houseuser', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('house_id', ['house_id'], unique=True)

    # ### end Alembic commands ###