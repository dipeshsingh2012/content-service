"""create content_lanes table

Revision ID: 001_content_lanes
Revises: 
Create Date: 2026-09-12 17:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001_content_lanes"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = inspector.get_table_names()

    if "content_lanes" in tables:
        return

    jsonb_type = sa.JSON().with_variant(postgresql.JSONB, "postgresql")

    op.create_table(
        "content_lanes",
        sa.Column("id", sa.String(), primary_key=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("subtitle", sa.String(), nullable=True),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("lane_type", sa.String(), nullable=False, server_default="category_lane"),
        sa.Column("placement", sa.String(), nullable=False, server_default="homepage"),
        sa.Column("card_style", sa.String(), nullable=False, server_default="circular"),
        sa.Column("has_navigation_arrows", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("status", sa.String(), nullable=False, server_default="active"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("items", jsonb_type, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_index("ix_content_lanes_id", "content_lanes", ["id"])
    op.create_index("ix_content_lanes_title", "content_lanes", ["title"])
    op.create_index("ix_content_lanes_slug", "content_lanes", ["slug"], unique=True)
    op.create_index("ix_content_lanes_placement", "content_lanes", ["placement"])
    op.create_index("ix_content_lanes_status", "content_lanes", ["status"])


def downgrade() -> None:
    op.drop_index("ix_content_lanes_status", table_name="content_lanes")
    op.drop_index("ix_content_lanes_placement", table_name="content_lanes")
    op.drop_index("ix_content_lanes_slug", table_name="content_lanes")
    op.drop_index("ix_content_lanes_title", table_name="content_lanes")
    op.drop_index("ix_content_lanes_id", table_name="content_lanes")
    op.drop_table("content_lanes")
