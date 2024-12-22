"""B-tree index on transaction category and type

Revision ID: 6d5f10e80e38
Revises: 5d41c068bdab
Create Date: 2024-12-22 17:53:31.265847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d5f10e80e38'
down_revision: Union[str, None] = '5d41c068bdab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('onboarding', 'is_used',
               existing_type=sa.BOOLEAN(),
               server_default=None,
               nullable=True)
    op.create_index('ix_transaction_details_category', 'transaction_details', ['category'], unique=False, postgresql_using='btree')
    op.create_index('ix_transactions_status', 'transactions', ['status'], unique=False, postgresql_using='btree')
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_index('ix_transactions_status', table_name='transactions', postgresql_using='btree')
    op.drop_index('ix_transaction_details_category', table_name='transaction_details', postgresql_using='btree')
    op.alter_column('onboarding', 'is_used',
               existing_type=sa.BOOLEAN(),
               server_default=sa.text('false'),
               nullable=False)
    # ### end Alembic commands ###
