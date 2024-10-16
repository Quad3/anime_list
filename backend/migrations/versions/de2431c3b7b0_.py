"""empty message

Revision ID: de2431c3b7b0
Revises: 7e92c96e17ad
Create Date: 2024-09-04 16:12:42.127068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'de2431c3b7b0'
down_revision: Union[str, None] = '7e92c96e17ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('anime_from_to',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from', sa.Date(), nullable=True),
    sa.Column('to', sa.Date(), nullable=True),
    sa.Column('anime_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['anime_id'], ['anime.uuid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('anime', 'from_to')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('anime', sa.Column('from_to', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False))
    op.drop_table('anime_from_to')
    # ### end Alembic commands ###