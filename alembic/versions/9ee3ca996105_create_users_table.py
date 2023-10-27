"""Create Users Table

Revision ID: 9ee3ca996105
Revises: bba3a55617d9
Create Date: 2023-10-15 15:11:49.559798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ee3ca996105'
down_revision: Union[str, None] = 'bba3a55617d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False, unique=True, primary_key=True),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('display_name', sa.String(), nullable=False, unique=True),
        sa.Column('email_id', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('college_roll_no', sa.Integer(), nullable=False, unique=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    op.create_foreign_key('event_user_fk',source_table='events', referent_table='users', local_cols=['creator_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('event_user_fk', table_name='events')
    op.drop_table('users')
