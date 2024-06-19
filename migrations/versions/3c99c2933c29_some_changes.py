"""Some changes

Revision ID: 3c99c2933c29
Revises: 
Create Date: 2024-06-19 13:27:47.261568

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3c99c2933c29'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('wastecollectionschedule', schema=None) as batch_op:
        batch_op.drop_index('id')

    op.drop_table('wastecollectionschedule')
    with op.batch_alter_table('wastecollection', schema=None) as batch_op:
        batch_op.add_column(sa.Column('waste_type', sa.Integer(), nullable=False))
        batch_op.drop_constraint('wastecollection_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'wastetype', ['waste_type'], ['id'])
        batch_op.drop_column('waste_type_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('wastecollection', schema=None) as batch_op:
        batch_op.add_column(sa.Column('waste_type_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('wastecollection_ibfk_2', 'wastetype', ['waste_type_id'], ['id'])
        batch_op.drop_column('waste_type')

    op.create_table('wastecollectionschedule',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('collection_date', mysql.DATETIME(), nullable=False),
    sa.Column('waste_type', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('status', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('notified', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='wastecollectionschedule_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('wastecollectionschedule', schema=None) as batch_op:
        batch_op.create_index('id', ['id'], unique=True)

    # ### end Alembic commands ###