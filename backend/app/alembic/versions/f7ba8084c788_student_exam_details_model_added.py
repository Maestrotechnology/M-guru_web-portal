"""student_exam_details model added

Revision ID: f7ba8084c788
Revises: 297c90aea60a
Create Date: 2024-12-17 10:53:04.952642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f7ba8084c788'
down_revision: Union[str, None] = '297c90aea60a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student_exam_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('option_ids', sa.String(length=50), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.Column('status', mysql.TINYINT(), nullable=True, comment='1-> active , 2-> inactive'),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('assign_exam_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['assign_exam_id'], ['assign_exam.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_exam_detail_assign_exam_id'), 'student_exam_detail', ['assign_exam_id'], unique=False)
    op.create_index(op.f('ix_student_exam_detail_id'), 'student_exam_detail', ['id'], unique=False)
    op.create_index(op.f('ix_student_exam_detail_question_id'), 'student_exam_detail', ['question_id'], unique=False)
    op.create_index(op.f('ix_student_exam_detail_student_id'), 'student_exam_detail', ['student_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_student_exam_detail_student_id'), table_name='student_exam_detail')
    op.drop_index(op.f('ix_student_exam_detail_question_id'), table_name='student_exam_detail')
    op.drop_index(op.f('ix_student_exam_detail_id'), table_name='student_exam_detail')
    op.drop_index(op.f('ix_student_exam_detail_assign_exam_id'), table_name='student_exam_detail')
    op.drop_table('student_exam_detail')
    # ### end Alembic commands ###
