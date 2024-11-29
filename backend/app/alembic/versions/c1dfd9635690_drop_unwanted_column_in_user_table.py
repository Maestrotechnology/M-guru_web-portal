"""drop unwanted column in user table

Revision ID: c1dfd9635690
Revises: 66a44ce50cbf
Create Date: 2024-11-27 16:32:39.834868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'c1dfd9635690'
down_revision: Union[str, None] = '66a44ce50cbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'updated_at')
    op.drop_column('user', 'status')
    op.drop_column('user', 'created_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('created_at', mysql.DATETIME(), nullable=True))
    op.add_column('user', sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('updated_at', mysql.DATETIME(), nullable=True))
    # ### end Alembic commands ###