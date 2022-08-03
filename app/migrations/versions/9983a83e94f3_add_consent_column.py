"""add consent column

Revision ID: 9983a83e94f3
Revises: f9c634db477d
Create Date: 2022-08-03 11:46:50.748926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9983a83e94f3'
down_revision = 'f9c634db477d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('dialog', sa.Column('consent', sa.Boolean()))


def downgrade() -> None:
    op.drop_column('dialog', 'consent')
