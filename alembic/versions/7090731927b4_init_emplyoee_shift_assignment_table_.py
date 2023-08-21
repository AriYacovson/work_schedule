"""Init emplyoee_shift_assignment table and adding relationship for shifts and employees tables

Revision ID: 7090731927b4
Revises: acd1d44eff7a
Create Date: 2023-08-21 14:56:32.376612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7090731927b4'
down_revision: Union[str, None] = 'acd1d44eff7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # create employee_shift_assignments table
    op.create_table(
        'employee_shift_assignments',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('employee_id', sa.Integer, sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('shift_id', sa.Integer, sa.ForeignKey('shifts.id'), nullable=False),
        sa.Column('date', sa.Date, nullable=False)
    )

def downgrade():
    op.drop_table('employee_shift_assignments')
