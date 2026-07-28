"""widen status column to Text

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-28
"""

from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    # status strings from CricAPI can exceed 50 chars (e.g. award decisions)
    op.alter_column("matches", "status",
                    type_=sa.Text(),
                    existing_type=sa.String(50),
                    existing_nullable=True)


def downgrade():
    op.alter_column("matches", "status",
                    type_=sa.String(50),
                    existing_type=sa.Text(),
                    existing_nullable=True)
