"""Make Migrations

Revision ID: 7c061dd91f1f
Revises: bfa5cb83c491
Create Date: 2025-02-27 20:29:10.982987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c061dd91f1f'
down_revision: Union[str, None] = 'bfa5cb83c491'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
