"""Add constraints to credit profile preferences

Revision ID: 338a30968ceb
Revises: 69c422f5ad08
Create Date: 2024-11-22 19:53:50.378110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '338a30968ceb'
down_revision: Union[str, None] = '69c422f5ad08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_check_constraint(
        "check_credit_score_range",
        "credit_profile_preferences",
        "credit_score >= 300 AND credit_score <= 850"
    )
    op.create_check_constraint(
        "check_positive_salary",
        "credit_profile_preferences",
        "salary >= 0"
    )

def downgrade():
    op.drop_constraint("check_credit_score_range", "credit_profile_preferences")
    op.drop_constraint("check_positive_salary", "credit_profile_preferences")
