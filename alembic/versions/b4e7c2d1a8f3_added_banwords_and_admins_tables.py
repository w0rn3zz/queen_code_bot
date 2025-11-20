"""added banwords and admins tables

Revision ID: b4e7c2d1a8f3
Revises: f03cc0a69911
Create Date: 2025-11-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4e7c2d1a8f3'
down_revision: Union[str, Sequence[str], None] = 'f03cc0a69911'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('banwords',
    sa.Column('word', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_banwords'))
    )
    op.create_index(op.f('ix_banwords_word'), 'banwords', ['word'], unique=True)
    
    op.create_table('admins',
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('added_by_tg_id', sa.BigInteger(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_admins'))
    )
    op.create_index(op.f('ix_admins_tg_id'), 'admins', ['tg_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_admins_tg_id'), table_name='admins')
    op.drop_table('admins')
    op.drop_index(op.f('ix_banwords_word'), table_name='banwords')
    op.drop_table('banwords')
