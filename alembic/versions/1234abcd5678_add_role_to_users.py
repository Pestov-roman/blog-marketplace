import sqlalchemy as sa

from alembic import op

revision = "1234abcd5678"
down_revision = "5d0b46d86d3f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "role", sa.String(length=10), nullable=False, server_default="reader"
        ),
    )
    op.alter_column("users", "role", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "role")
