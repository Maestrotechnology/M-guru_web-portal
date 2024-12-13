"""Message describing the migration

Revision ID: 8c914cd2c403
Revises: 823e649ca8c8
Create Date: 2024-12-13 10:03:02.942223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '8c914cd2c403'
down_revision: Union[str, None] = '823e649ca8c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('work_report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trainer_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('batch_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=350), nullable=True),
    sa.Column('taken_time', sa.DateTime(), nullable=True),
    sa.Column('status', mysql.TINYINT(), nullable=True, comment='1-> active 2 -> inactive'),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['batch_id'], ['batch.id'], ),
    sa.ForeignKeyConstraint(['trainer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_work_report_id'), 'work_report', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_work_report_id'), table_name='work_report')
    op.drop_table('work_report')
    # ### end Alembic commands ###
