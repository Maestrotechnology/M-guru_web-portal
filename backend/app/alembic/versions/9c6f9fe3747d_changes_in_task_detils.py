"""changes in task detils

Revision ID: 9c6f9fe3747d
Revises: c3e3bd25582d
Create Date: 2024-12-26 17:40:55.249744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '9c6f9fe3747d'
down_revision: Union[str, None] = 'c3e3bd25582d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_detail', sa.Column('task_description', sa.Text(), nullable=True))
    op.add_column('task_detail', sa.Column('mentor_description', sa.Text(), nullable=True))
    op.drop_column('task_detail', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_detail', sa.Column('description', mysql.TEXT(), nullable=True))
    op.drop_column('task_detail', 'mentor_description')
    op.drop_column('task_detail', 'task_description')
    # ### end Alembic commands ###
