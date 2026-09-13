"""create cms_pages and cms_site_shell tables

Revision ID: 002_cms_tables
Revises: 001_content_lanes
Create Date: 2026-09-13 11:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "002_cms_tables"
down_revision: Union[str, None] = "001_content_lanes"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = inspector.get_table_names()

    jsonb_type = sa.JSON().with_variant(postgresql.JSONB, "postgresql")

    if "cms_pages" not in tables:
        op.create_table(
            "cms_pages",
            sa.Column("id", sa.String(), primary_key=True, nullable=False),
            sa.Column("page_type", sa.String(), nullable=False, server_default="static"),
            sa.Column("title", sa.String(), nullable=False),
            sa.Column("slug", sa.String(), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.text("true")),
            sa.Column("sections", jsonb_type, nullable=False, server_default=sa.text("'[]'::jsonb")),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

        op.create_index("ix_cms_pages_id", "cms_pages", ["id"])
        op.create_index("ix_cms_pages_page_type", "cms_pages", ["page_type"])
        op.create_index("ix_cms_pages_title", "cms_pages", ["title"])
        op.create_index("ix_cms_pages_slug", "cms_pages", ["slug"], unique=True)
        op.create_index("ix_cms_pages_is_published", "cms_pages", ["is_published"])

    if "cms_site_shell" not in tables:
        op.create_table(
            "cms_site_shell",
            sa.Column("id", sa.String(), primary_key=True, nullable=False, server_default="default"),
            sa.Column("promo_bar", jsonb_type, nullable=False, server_default=sa.text("'{}'::jsonb")),
            sa.Column("header", jsonb_type, nullable=False, server_default=sa.text("'{}'::jsonb")),
            sa.Column("footer", jsonb_type, nullable=False, server_default=sa.text("'{}'::jsonb")),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        )


def downgrade() -> None:
    op.drop_index("ix_cms_pages_is_published", table_name="cms_pages")
    op.drop_index("ix_cms_pages_slug", table_name="cms_pages")
    op.drop_index("ix_cms_pages_title", table_name="cms_pages")
    op.drop_index("ix_cms_pages_page_type", table_name="cms_pages")
    op.drop_index("ix_cms_pages_id", table_name="cms_pages")
    op.drop_table("cms_pages")
    op.drop_table("cms_site_shell")

