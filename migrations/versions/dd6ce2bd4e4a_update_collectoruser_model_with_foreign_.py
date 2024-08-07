"""Update CollectorUser model with foreign key and primary key

Revision ID: dd6ce2bd4e4a
Revises: 
Create Date: 2024-08-07 16:52:18.219411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd6ce2bd4e4a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('collectoruser', schema=None) as batch_op:
        batch_op.drop_index('collector_id')
        batch_op.drop_index('firstname')
        batch_op.drop_index('secondname')
        batch_op.create_foreign_key(None, 'adminuser', ['companyname'], ['companyname'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('collectoruser', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_index('secondname', ['secondname'], unique=True)
        batch_op.create_index('firstname', ['firstname'], unique=True)
        batch_op.create_index('collector_id', ['collector_id'], unique=True)

    # ### end Alembic commands ###
