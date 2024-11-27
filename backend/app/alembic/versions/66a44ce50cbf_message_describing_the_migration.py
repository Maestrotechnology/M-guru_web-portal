"""Message describing the migration

Revision ID: 66a44ce50cbf
Revises: ed6677cd8af1
Create Date: 2024-11-27 14:51:47.334154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '66a44ce50cbf'
down_revision: Union[str, None] = 'ed6677cd8af1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('token', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('renewed_at', sa.DateTime(), nullable=True),
    sa.Column('device_type', mysql.TINYINT(display_width=1), nullable=False, comment='1-Android, 2-iOS'),
    sa.Column('validity', mysql.TINYINT(display_width=1), nullable=False, comment='0-Expired, 1- Lifetime'),
    sa.Column('device_id', sa.String(length=255), nullable=True),
    sa.Column('push_device_id', sa.String(length=255), nullable=True),
    sa.Column('device_ip', sa.String(length=255), nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=False, comment='1-active, -1 inactive, 0- deleted'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('status', mysql.TINYINT(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'status')
    op.drop_table('api_tokens')
    # ### end Alembic commands ###
