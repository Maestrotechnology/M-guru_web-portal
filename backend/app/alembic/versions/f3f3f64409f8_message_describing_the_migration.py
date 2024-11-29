"""Message describing the migration

Revision ID: f3f3f64409f8
Revises: 4827d4e59392
Create Date: 2024-11-28 18:16:09.024073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f3f3f64409f8'
down_revision: Union[str, None] = '4827d4e59392'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('work_report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('check_in', sa.DateTime(), nullable=True),
    sa.Column('check_out', sa.DateTime(), nullable=True),
    sa.Column('task', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('work_time', sa.Integer(), nullable=True),
    sa.Column('break_time', sa.Integer(), nullable=True),
    sa.Column('in_ip', sa.String(length=255), nullable=True),
    sa.Column('out_ip', sa.String(length=255), nullable=True),
    sa.Column('in_latitude', sa.DECIMAL(precision=15, scale=7), nullable=True),
    sa.Column('in_longitude', sa.DECIMAL(precision=15, scale=7), nullable=True),
    sa.Column('out_latitude', sa.DECIMAL(precision=15, scale=7), nullable=True),
    sa.Column('out_longitude', sa.DECIMAL(precision=15, scale=7), nullable=True),
    sa.Column('status', mysql.TINYINT(), nullable=True, comment='1-> active 2 -> inactive'),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_work_report_id'), 'work_report', ['id'], unique=False)
    op.create_table('work_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('work_report_id', sa.Integer(), nullable=True),
    sa.Column('break_time', sa.DateTime(), nullable=True),
    sa.Column('work_time', sa.DateTime(), nullable=True),
    sa.Column('status', mysql.TINYINT(), nullable=True, comment='1-> active 2 -> inactive'),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['work_report_id'], ['work_report.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_work_history_id'), 'work_history', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_work_history_id'), table_name='work_history')
    op.drop_table('work_history')
    op.drop_index(op.f('ix_work_report_id'), table_name='work_report')
    op.drop_table('work_report')
    # ### end Alembic commands ###
