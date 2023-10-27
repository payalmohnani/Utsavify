"""Create events table

Revision ID: bba3a55617d9
Revises: 99d102951468
Create Date: 2023-10-15 10:38:07.161819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bba3a55617d9'
down_revision: Union[str, None] = '99d102951468'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('events',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, unique=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('organizing_society', sa.String(), nullable=False),
        sa.Column('event_time', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
        # sa.Column('creator'), # User
        # sa.Column('organizer') # Society
    )
    op.create_foreign_key('event_society_fk',source_table='events', referent_table='societies', local_cols=['organizing_society'], remote_cols=['name'], ondelete='CASCADE')
    # op.create_foreign_key('event_user_fk',source_table='events', referent_table='users', local_cols=['creator_id'], remote_cols=['id'])


def downgrade() -> None:
    op.drop_table('events')
