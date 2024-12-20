"""mark column added in studentexamdetail model

Revision ID: c3e3bd25582d
Revises: aa79b4eddf2f
Create Date: 2024-12-17 17:07:50.063115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3e3bd25582d'
down_revision: Union[str, None] = 'aa79b4eddf2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student_exam_detail', sa.Column('mark', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student_exam_detail', 'mark')
    # ### end Alembic commands ###
