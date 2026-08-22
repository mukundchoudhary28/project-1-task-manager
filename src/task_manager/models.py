import uuid
from datetime import datetime,UTC

from enum import Enum as PyEnum
from sqlalchemy import Boolean, DateTime, Enum, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Priority(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Role(str, PyEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"

    
class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    priority: Mapped[Priority] = mapped_column(
    Enum(
        Priority,
        name="priority_enum",
        values_callable=lambda enum: [member.value for member in enum],
    ),
    default=Priority.MEDIUM,
    nullable=False,
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
        )

    email: Mapped[str] = mapped_column(
        String(255),
        unique = True,
        nullable = False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    role: Mapped[Role] = mapped_column(
        Enum(
                Role,
                name="roles_enum",
                values_callable=lambda enum: [member.value for member in enum],
            ),
            default=Role.EMPLOYEE,
            nullable=False
    )
