"""Created Society Table

Revision ID: 99d102951468
Revises: 
Create Date: 2023-10-12 22:51:51.810894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99d102951468'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('societies',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True, unique=True),
                    sa.Column('name', sa.String(), nullable=False, unique=True),
                    sa.Column('college_level', sa.Boolean(), nullable=False, server_default='True'),
                    sa.Column('convenor', sa.String(), nullable=False),
                    sa.Column('gen_sec', sa.String(), nullable=False),
                    sa.Column('creator_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
                    # Events should have a foreign key from the societies
                    # sa.ForeignKeyConstraint('events', ev)

                    )




def downgrade() -> None:
    op.drop_table('societies')
