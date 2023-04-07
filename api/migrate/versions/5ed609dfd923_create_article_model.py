"""create article model

Revision ID: 5ed609dfd923
Revises: 8b70fd3f48fa
Create Date: 2023-03-30 17:44:18.720196

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5ed609dfd923"
down_revision = "8b70fd3f48fa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "article",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("update_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("body", sa.String(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("article")
    # ### end Alembic commands ###