"""add batch id in application table

Revision ID: 871c556a5d84
Revises: df2d3fc61b69
Create Date: 2024-12-02 11:48:14.774139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '871c556a5d84'
down_revision: Union[str, None] = 'df2d3fc61b69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('application_details', sa.Column('batch_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'application_details', 'batch', ['batch_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'application_details', type_='foreignkey')
    op.drop_column('application_details', 'batch_id')
    # ### end Alembic commands ###
