"""remove the enrollment owner constraint to make it less restrictive

Revision ID: 0aa06cf04e62
Revises: 08917ddec33f
Create Date: 2025-01-04 17:50:59.923751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0aa06cf04e62'
down_revision: Union[str, None] = '08917ddec33f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('enrollments') as batch_op:
        batch_op.drop_constraint('enrollment_owner_check', type_='check')
        
        batch_op.create_check_constraint(
            constraint_name='enrollment_owner_check',
            condition='(user_id IS NOT NULL OR onboarding_id IS NOT NULL)'
        )


def downgrade():
    with op.batch_alter_table('enrollments') as batch_op:
        batch_op.drop_constraint('enrollment_owner_check', type_='check')
        
        batch_op.create_check_constraint(
            constraint_name='enrollment_owner_check',
            condition='(your_previous_condition_here)'
        )
