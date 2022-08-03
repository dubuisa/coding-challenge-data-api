"""create table dialog

Revision ID: f9c634db477d
Revises: 
Create Date: 2022-08-03 08:35:40.689142

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = 'f9c634db477d'
down_revision = '9947d2b2e466'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('dialog',
    sa.Column('id', sa.Integer(), nullable=True, autoincrement=True, primary_key=True),
    sa.Column('dialogId', sa.Integer(), nullable=False),
    sa.Column('customerId', sa.Integer(), nullable=False),
    sa.Column('text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('language', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    )

    op.create_index(op.f('ix_dialog_id'), 'dialog', ['id'], unique=False)
    op.create_index(op.f('ix_dialog_dialogId'), 'dialog', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_dialog_id'), table_name='dialog')
    op.drop_index(op.f('ix_dialog_dialogId'), table_name='dialog')
    op.drop_table('dialog')