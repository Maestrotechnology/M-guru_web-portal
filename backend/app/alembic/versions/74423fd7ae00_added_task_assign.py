"""added task_assign

Revision ID: 74423fd7ae00
Revises: c04c239d9581
Create Date: 2025-01-02 16:53:44.798455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '74423fd7ae00'
down_revision: Union[str, None] = 'c04c239d9581'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task_assign',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('batch_id', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['batch_id'], ['batch.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_assign_id'), 'task_assign', ['id'], unique=False)
    op.create_foreign_key(None, 'assign_exam', 'question_set', ['set_id'], ['id'])
    op.alter_column('exam', 'course_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.create_foreign_key(None, 'exam', 'course', ['course_id'], ['id'])
    op.drop_constraint('student_project_detail_ibfk_2', 'student_project_detail', type_='foreignkey')
    op.drop_column('student_project_detail', 'user_id')
    op.drop_constraint('task_ibfk_1', 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'user', ['created_by'], ['id'])
    op.drop_column('task', 'created_by_user_id')
    op.drop_index('user_id', table_name='task_detail')
    op.drop_constraint('task_detail_ibfk_5', 'task_detail', type_='foreignkey')
    op.create_foreign_key(None, 'task_detail', 'user', ['created_by'], ['id'])
    op.drop_constraint('type_of_question_ibfk_1', 'type_of_question', type_='foreignkey')
    op.create_foreign_key(None, 'type_of_question', 'user', ['created_by'], ['id'])
    op.drop_constraint('work_report_ibfk_3', 'work_report', type_='foreignkey')
    op.create_foreign_key(None, 'work_report', 'user', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'work_report', type_='foreignkey')
    op.create_foreign_key('work_report_ibfk_3', 'work_report', 'user', ['created_by'], ['id'], onupdate='RESTRICT', ondelete='RESTRICT')
    op.drop_constraint(None, 'type_of_question', type_='foreignkey')
    op.create_foreign_key('type_of_question_ibfk_1', 'type_of_question', 'user', ['created_by'], ['id'], onupdate='RESTRICT', ondelete='RESTRICT')
    op.drop_constraint(None, 'task_detail', type_='foreignkey')
    op.create_foreign_key('task_detail_ibfk_5', 'task_detail', 'user', ['created_by'], ['id'], onupdate='RESTRICT', ondelete='RESTRICT')
    op.create_index('user_id', 'task_detail', ['student_id'], unique=False)
    op.add_column('task', sa.Column('created_by_user_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key('task_ibfk_1', 'task', 'user', ['created_by_user_id'], ['id'])
    op.add_column('student_project_detail', sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('student_project_detail_ibfk_2', 'student_project_detail', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'exam', type_='foreignkey')
    op.alter_column('exam', 'course_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.drop_constraint(None, 'assign_exam', type_='foreignkey')
    op.drop_index(op.f('ix_task_assign_id'), table_name='task_assign')
    op.drop_table('task_assign')
    # ### end Alembic commands ###