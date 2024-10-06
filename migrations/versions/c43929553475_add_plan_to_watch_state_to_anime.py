"""Add PLAN_TO_WATCH state to anime

Revision ID: c43929553475
Revises: 454461072839
Create Date: 2024-10-06 10:03:52.130125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic_postgresql_enum import TableReference

# revision identifiers, used by Alembic.
revision: str = 'c43929553475'
down_revision: Union[str, None] = '454461072839'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values('public', 'state', ['WATCHING', 'WATCHED', 'DROPPED', 'PLAN_TO_WATCH'],
                        [TableReference(table_schema='public', table_name='anime', column_name='state')],
                        enum_values_to_rename=[])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values('public', 'state', ['WATCHED', 'WATCHING', 'DROPPED'],
                        [TableReference(table_schema='public', table_name='anime', column_name='state')],
                        enum_values_to_rename=[])
    # ### end Alembic commands ###
