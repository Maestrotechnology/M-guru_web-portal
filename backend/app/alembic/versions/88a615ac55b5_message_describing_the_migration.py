"""Message describing the migration

Revision ID: 88a615ac55b5
Revises: 3527638e1554
Create Date: 2024-12-03 10:05:01.031552

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '88a615ac55b5'
down_revision: Union[str, None] = '3527638e1554'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_detail', sa.Column('expected_time', sa.DateTime(), nullable=True))
    op.add_column('task_detail', sa.Column('priority', mysql.TINYINT(), nullable=True, comment='1-> High 2 -> medium 3 -> ow'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task_detail', 'priority')
    op.drop_column('task_detail', 'expected_time')
    # ### end Alembic commands ###
