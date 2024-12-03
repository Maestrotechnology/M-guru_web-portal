"""Message describing the migration

Revision ID: 3527638e1554
Revises: 871c556a5d84
Create Date: 2024-12-02 15:15:02.849023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '3527638e1554'
down_revision: Union[str, None] = '871c556a5d84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attendance', sa.Column('work_status', mysql.TINYINT(), nullable=True, comment='1-> chek_in 2 -> check_out'))
    op.add_column('task_detail', sa.Column('complete_status', mysql.TINYINT(), nullable=True, comment='1-> complete 2 -> not complete'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task_detail', 'complete_status')
    op.drop_column('attendance', 'work_status')
    # ### end Alembic commands ###