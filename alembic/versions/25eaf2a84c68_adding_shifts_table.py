"""Adding shifts table

Revision ID: 25eaf2a84c68
Revises: c49ded84b443
Create Date: 2023-08-20 20:11:03.394967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25eaf2a84c68'
down_revision: Union[str, None] = 'c49ded84b443'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shifts',
                    sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('start_time', sa.DateTime(), nullable=True),
                    sa.Column('end_time', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shifts')
    # ### end Alembic commands ###