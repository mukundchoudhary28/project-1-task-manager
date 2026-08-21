"""add task priority

Revision ID: b352846c00bb
Revises: 343bf1e0f5be
Create Date: 2026-08-21 18:20:23.814404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b352846c00bb'
down_revision: Union[str, Sequence[str], None] = '343bf1e0f5be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     
    priority_enum = postgresql.ENUM(
        "low",
        "medium",
        "high",
        name="priority_enum",
    )

    priority_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "tasks",
        sa.Column(
            "priority",
            sa.Enum("low", "medium", "high", name="priority_enum"),
            nullable=True,
        ),
    )

    op.execute("UPDATE tasks SET priority = 'medium'")

    op.alter_column(
        "tasks",
        "priority",
        nullable=False,
    )

    op.alter_column(
        "tasks",
        "priority",
        server_default=sa.text("'medium'::priority_enum"),
    )


def downgrade() -> None:
    op.drop_column("tasks", "priority")