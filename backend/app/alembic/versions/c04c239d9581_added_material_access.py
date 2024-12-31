"""added material_access

Revision ID: c04c239d9581
Revises: 684fdb05771d
Create Date: 2024-12-30 18:30:34.576371

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'c04c239d9581'
down_revision: Union[str, None] = '684fdb05771d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # Step 1: Drop the foreign key constraint that uses the 'ix_set_exam_id' index
    # op.drop_constraint('set_ibfk_1', 'set', type_='foreignkey')  # Drop foreign key on 'exam_id'
    # op.drop_constraint('set_ibfk_1', 'set', type_='foreignkey')

    # Step 2: Drop the indexes that are problematic
    # op.drop_index('ix_set_exam_id', table_name='set')
    # op.drop_index('ix_set_id', table_name='set')
    # op.drop_constraint('assign_exam_ibfk_4', 'assign_exam', type_='foreignkey')

    # op.drop_constraint('assign_exam_ibfk_4', 'assign_exam', type_='foreignkey')  # Drop foreign key in 'assign_exam'
    # op.drop_constraint('question_ibfk_3', 'question', type_='foreignkey')
    
    # Step 3: Create foreign key with CASCADE on delete for assign_exam
    # op.create_foreign_key('assign_exam_ibfk_7', 'assign_exam', 'question_set', ['set_id'], ['id'], ondelete='CASCADE')

    # Step 4: Drop the 'set' table
    # op.drop_table('set')

    # Step 5: Drop the 'work_history' table and related index
    # op.drop_index('ix_work_history_id', table_name='work_history')
    # op.drop_table('work_history')

    # Step 6: Drop the 'passwordyear' table and related index
    # op.drop_index('ix_passwordyear_id', table_name='passwordyear')
    # op.drop_table('passwordyear')

    # Step 7: Modify 'application_details' table to add a 'created_by' column and create the foreign key
    # op.add_column('application_details', sa.Column('created_by', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'application_details', 'user', ['created_by'], ['id'])

    # Step 8: Modify 'assign_exam' table to add 'assigned_by' column and update foreign key
    # op.add_column('assign_exam', sa.Column('assigned_by', sa.Integer(), nullable=True))
    # op.drop_constraint('assign_exam_ibfk_4', 'assign_exam', type_='foreignkey')
    op.create_foreign_key(None, 'assign_exam', 'user', ['assigned_by'], ['id'])
    # op.create_foreign_key(None, 'assign_exam', 'question_set', ['set_id'], ['id'])

    # Step 9: Add 'created_by' foreign key in 'batch' table
    # op.add_column('batch', sa.Column('created_by', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'batch', 'user', ['created_by'], ['id'])

    # Step 10: Add 'created_by' foreign key in 'course' table
    # op.add_column('course', sa.Column('created_by', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'course', 'user', ['created_by'], ['id'])

    # Step 11: Modify 'course_material' table to add 'created_by' column and remove the old FK
    # op.add_column('course_material', sa.Column('created_by', sa.Integer(), nullable=True))
    # op.drop_constraint('course_material_ibfk_2', 'course_material', type_='foreignkey')
    op.create_foreign_key(None, 'course_material', 'user', ['created_by'], ['id'])
    # op.drop_column('course_material', 'created_by_user_id')

    # Step 12: Add 'created_by' foreign key in 'course_media' table
    # op.add_column('course_media', sa.Column('created_by', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'course_media', 'user', ['created_by'], ['id'])

    # Step 13: Add 'created_by' foreign key in 'enquiry_type' table
    # op.add_column('enquiry_type', sa.Column('created_by', sa.Integer(), nullable=True))
    # op.create_foreign_key(None, 'enquiry_type', 'user', ['created_by'], ['id'])

    # Step 14: Add 'created_by' foreign key in 'exam' table
    # op.add_column('exam', sa.Column('created_by', sa.Integer(), nullable=True))
    # op.create_foreign_key(None, 'exam', 'user', ['created_by'], ['id'])

    # Step 15: Add 'created_by' foreign key in 'interview' table
    # op.add_column('interview', sa.Column('created_by', sa.Integer(), nullable=True))
    # op.create_foreign_key(None, 'interview', 'user', ['created_by'], ['id'])

    # # Step 16: Add 'created_by' foreign key in 'option' table
    # op.add_column('option', sa.Column('created_by', sa.Integer(), nullable=True))
    # op.create_foreign_key(None, 'option', 'user', ['created_by'], ['id'])

    # Step 17: Add 'created_by' foreign key in 'question' table
    # op.add_column('question', sa.Column('created_by', sa.Integer(), nullable=True))
    # op.drop_constraint('question_ibfk_3', 'question', type_='foreignkey')
    # op.create_foreign_key(None, 'question', 'user', ['created_by'], ['id'])
    op.create_foreign_key(None, 'question', 'question_set', ['set_id'], ['id'])

    # Step 18: Add 'created_by' foreign key in 'score' table
    # op.add_column('score', sa.Column('created_by', sa.Integer(), nullable=True))
    # op.create_foreign_key(None, 'score', 'user', ['created_by'], ['id'])

    # Step 19: Add 'created_by' foreign key in 'student_exam_detail' table
    # op.add_column('student_exam_detail', sa.Column('created_by', sa.Integer(), nullable=True))
    # op.create_foreign_key(None, 'student_exam_detail', 'user', ['created_by'], ['id'])

    # Step 20: Add 'created_by' foreign key in 'student_project_detail' table and clean up old columns
    # op.add_column('student_project_detail', sa.Column('created_by', sa.Integer(), nullable=True))
    # op.add_column('student_project_detail', sa.Column('student_id', sa.Integer(), nullable=True))
    # # op.drop_constraint('student_project_detail_ibfk_2', 'student_project_detail', type_='foreignkey')
    # op.create_foreign_key(None, 'student_project_detail', 'user', ['student_id'], ['id'])
    # op.create_foreign_key(None, 'student_project_detail', 'user', ['created_by'], ['id'])
    # op.drop_column('student_project_detail', 'user_id')

    # Step 21: Create 'question_set' table with InnoDB engine
    # op.create_table(
    #     'question_set',
    #     sa.Column('id', sa.Integer(), nullable=False),
    #     sa.Column('name', sa.String(length=50), nullable=True),
    #     sa.Column('status', mysql.TINYINT(), nullable=True, comment='1-> active , 2-> inactive'),
    #     sa.Column('created_at', sa.DateTime(), nullable=True),
    #     sa.Column('updated_at', sa.DateTime(), nullable=True),
    #     sa.Column('created_by', sa.Integer(), nullable=True),
    #     sa.Column('exam_id', sa.Integer(), nullable=True),
    #     sa.ForeignKeyConstraint(['created_by'], ['user.id']),
    #     sa.ForeignKeyConstraint(['exam_id'], ['exam.id']),
    #     sa.PrimaryKeyConstraint('id'),
    #     mysql_engine='InnoDB'  # MySQL-specific storage engine
    # )

    # Step 22: Create indexes for 'question_set'
    # op.create_index(op.f('ix_question_set_exam_id'), 'question_set', ['exam_id'], unique=False)
    # op.create_index(op.f('ix_question_set_id'), 'question_set', ['id'], unique=False)

    # # Step 23: Create 'material_access' table
    # op.create_table(
    #     'material_access',
    #     sa.Column('id', sa.Integer(), nullable=False),
    #     sa.Column('material_id', sa.Integer(), nullable=True),
    #     sa.Column('material_type', sa.String(length=255), nullable=True),
    #     sa.Column('access_type', sa.String(length=255), nullable=True),
    #     sa.Column('created_by', sa.Integer(), nullable=True),
    #     sa.ForeignKeyConstraint(['created_by'], ['user.id']),
    #     sa.PrimaryKeyConstraint('id'),
    #     mysql_engine='InnoDB'  # MySQL-specific storage engine
    # )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'work_report', type_='foreignkey')
    op.drop_column('work_report', 'created_by')
    op.drop_constraint(None, 'type_of_question', type_='foreignkey')
    op.drop_column('type_of_question', 'created_by')
    op.add_column('task_detail', sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'task_detail', type_='foreignkey')
    op.drop_constraint(None, 'task_detail', type_='foreignkey')
    op.create_foreign_key('task_detail_ibfk_3', 'task_detail', 'user', ['user_id'], ['id'])
    op.drop_column('task_detail', 'created_by')
    op.drop_column('task_detail', 'student_id')
    op.add_column('task', sa.Column('created_by_user_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key('task_ibfk_1', 'task', 'user', ['created_by_user_id'], ['id'])
    op.drop_column('task', 'created_by')
    op.add_column('student_project_detail', sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'student_project_detail', type_='foreignkey')
    op.drop_constraint(None, 'student_project_detail', type_='foreignkey')
    # op.create_foreign_key('student_project_detail_ibfk_2', 'student_project_detail', 'user', ['user_id'], ['id'])
    op.drop_column('student_project_detail', 'student_id')
    op.drop_column('student_project_detail', 'created_by')
    op.drop_constraint(None, 'student_exam_detail', type_='foreignkey')
    op.drop_column('student_exam_detail', 'created_by')
    op.drop_constraint(None, 'score', type_='foreignkey')
    op.drop_column('score', 'created_by')
    op.drop_constraint(None, 'question', type_='foreignkey')
    op.drop_constraint(None, 'question', type_='foreignkey')
    op.create_foreign_key('question_ibfk_3', 'question', 'set', ['set_id'], ['id'])
    op.drop_column('question', 'created_by')
    op.drop_constraint(None, 'option', type_='foreignkey')
    op.drop_column('option', 'created_by')
    op.drop_constraint(None, 'interview', type_='foreignkey')
    op.drop_column('interview', 'created_by')
    op.drop_constraint(None, 'exam', type_='foreignkey')
    op.drop_column('exam', 'created_by')
    op.drop_constraint(None, 'enquiry_type', type_='foreignkey')
    op.drop_column('enquiry_type', 'created_by')
    op.drop_constraint(None, 'course_media', type_='foreignkey')
    op.drop_column('course_media', 'created_by')
    op.add_column('course_material', sa.Column('created_by_user_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'course_material', type_='foreignkey')
    op.create_foreign_key('course_material_ibfk_2', 'course_material', 'user', ['created_by_user_id'], ['id'])
    op.drop_column('course_material', 'created_by')
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.drop_column('course', 'created_by')
    op.drop_constraint(None, 'batch', type_='foreignkey')
    op.drop_column('batch', 'created_by')
    op.drop_constraint(None, 'assign_exam', type_='foreignkey')
    op.drop_constraint(None, 'assign_exam', type_='foreignkey')
    # op.create_foreign_key('assign_exam_ibfk_4', 'assign_exam', 'set', ['set_id'], ['id'])
    op.drop_column('assign_exam', 'assigned_by')
    op.drop_constraint(None, 'application_details', type_='foreignkey')
    op.drop_column('application_details', 'created_by')
    op.create_table('passwordyear',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=4), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_passwordyear_id', 'passwordyear', ['id'], unique=False)
    op.create_table('work_history',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('attendance_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('break_time', mysql.DATETIME(), nullable=True),
    sa.Column('breakEnd_time', mysql.DATETIME(), nullable=True),
    sa.Column('work_time', mysql.DATETIME(), nullable=True),
    sa.Column('workEnd_time', mysql.DATETIME(), nullable=True),
    sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-> active 2 -> inactive'),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.Column('Ispaused', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-> yes 2 -> no'),
    sa.Column('taskDetail_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['attendance_id'], ['attendance.id'], name='work_history_ibfk_1'),
    sa.ForeignKeyConstraint(['taskDetail_id'], ['task_detail.id'], name='work_history_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # op.create_index('ix_work_history_id', 'work_history', ['id'], unique=False)
    # op.create_table('set',
    # sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    # sa.Column('name', mysql.VARCHAR(length=50), nullable=True),
    # sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-> active , 2-> inactive'),
    # sa.Column('created_at', mysql.DATETIME(), nullable=True),
    # sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    # sa.Column('exam_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    # sa.PrimaryKeyConstraint('id'),
    # mysql_collate='utf8mb4_0900_ai_ci',
    # mysql_default_charset='utf8mb4',
    # mysql_engine='InnoDB'
    # sa.ForeignKeyConstraint(['exam_id'], ['exam.id'], name='set_ibfk_1'),
    # )
    # op.create_index('ix_set_id', 'set', ['id'], unique=False)
    # op.create_index('ix_set_exam_id', 'set', ['exam_id'], unique=False)
    # op.drop_index(op.f('ix_material_access_id'), table_name='material_access')
    # op.drop_table('material_access')
    # op.drop_index(op.f('ix_question_set_id'), table_name='question_set')
    # op.drop_index(op.f('ix_question_set_exam_id'), table_name='question_set')
    # op.drop_table('question_set')
    # # ### end Alembic commands ###
