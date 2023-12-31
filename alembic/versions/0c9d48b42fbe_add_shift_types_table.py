"""Add shift_types table

Revision ID: 0c9d48b42fbe
Revises: 523b27493e46
Create Date: 2023-08-28 12:55:05.307384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0c9d48b42fbe'
down_revision: Union[str, None] = '523b27493e46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shift_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shift_types_id'), 'shift_types', ['id'], unique=True)
    op.create_index(op.f('ix_shift_types_name'), 'shift_types', ['name'], unique=False)
    op.add_column('shifts', sa.Column('shift_type_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_shifts_id'), 'shifts', ['id'], unique=False)
    op.create_foreign_key(None, 'shifts', 'shift_types', ['shift_type_id'], ['id'])
    op.drop_column('shifts', 'start_time')
    op.drop_column('shifts', 'end_time')
    op.drop_column('shifts', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shifts', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('shifts', sa.Column('end_time', postgresql.TIME(), autoincrement=False, nullable=False))
    op.add_column('shifts', sa.Column('start_time', postgresql.TIME(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'shifts', type_='foreignkey')
    op.drop_index(op.f('ix_shifts_id'), table_name='shifts')
    op.drop_column('shifts', 'shift_type_id')
    op.drop_index(op.f('ix_shift_types_name'), table_name='shift_types')
    op.drop_index(op.f('ix_shift_types_id'), table_name='shift_types')
    op.drop_table('shift_types')
    # ### end Alembic commands ###
