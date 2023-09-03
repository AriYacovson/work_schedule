"""Remove date from unavailable shifts table

Revision ID: f1a160c1ac8f
Revises: 0c9d48b42fbe
Create Date: 2023-08-28 14:48:24.918215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1a160c1ac8f'
down_revision: Union[str, None] = '0c9d48b42fbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('employee_unavailable_shifts', 'date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee_unavailable_shifts', sa.Column('date', sa.DATE(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###