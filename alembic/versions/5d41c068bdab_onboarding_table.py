"""onboarding table and enrollment modifications

Revision ID: 5d41c068bdab
Revises: 338a30968ceb
Create Date: 2024-12-09 16:42:15.977318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5d41c068bdab'
down_revision: Union[str, None] = '338a30968ceb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create new onboarding table
    op.create_table('onboarding',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('created_at', sa.Date(), nullable=False),
        sa.Column('expires_at', sa.Date(), nullable=False),
        sa.Column('is_used', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('associated_user_id', sa.Integer(), nullable=True),
        sa.Column('emails', sa.JSON(), nullable=False),
        sa.Column('phone_numbers', sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(['associated_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_onboarding_id'), 'onboarding', ['id'], unique=False)
    op.create_index(op.f('ix_onboarding_token'), 'onboarding', ['token'], unique=True)

    # Modify enrollments table
    op.alter_column('enrollments', 'user_id',
        existing_type=sa.Integer(),
        nullable=True)
    
    op.add_column('enrollments', sa.Column('onboarding_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'enrollments', 'onboarding', ['onboarding_id'], ['id'], ondelete='CASCADE')
    
    # Add check constraint to ensure either user_id or onboarding_id is set, but not both
    op.create_check_constraint(
        'enrollment_owner_check',
        'enrollments',
        '(user_id IS NULL AND onboarding_id IS NOT NULL) OR (user_id IS NOT NULL AND onboarding_id IS NULL)'
    )


def downgrade() -> None:
    # Remove check constraint
    op.drop_constraint('enrollment_owner_check', 'enrollments', type_='check')
    
    # Revert enrollments table changes
    op.drop_constraint(None, 'enrollments', type_='foreignkey')
    op.drop_column('enrollments', 'onboarding_id')
    op.alter_column('enrollments', 'user_id',
        existing_type=sa.Integer(),
        nullable=False)
    
    # Drop onboarding table and its indexes
    op.drop_index(op.f('ix_onboarding_token'), table_name='onboarding')
    op.drop_index(op.f('ix_onboarding_id'), table_name='onboarding')
    op.drop_table('onboarding')