import enum
from sqlalchemy import Boolean, Enum, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class AutomationMode(str, enum.Enum):
    manual = 'manual'
    semi_auto = 'semi_auto'
    full_auto = 'full_auto'


class Business(TimestampMixin, Base):
    __tablename__ = 'businesses'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    google_account_id: Mapped[str] = mapped_column(String(255), unique=True)


class Website(TimestampMixin, Base):
    __tablename__ = 'websites'

    id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(ForeignKey('businesses.id'), index=True)
    site_url: Mapped[str] = mapped_column(String(500), unique=True)

    business = relationship('Business')


class ApprovalAction(TimestampMixin, Base):
    __tablename__ = 'approval_actions'

    id: Mapped[int] = mapped_column(primary_key=True)
    module: Mapped[str] = mapped_column(String(100), index=True)
    action_type: Mapped[str] = mapped_column(String(100), index=True)
    title: Mapped[str] = mapped_column(String(255))
    payload: Mapped[dict] = mapped_column(JSON)
    before_state: Mapped[dict | None] = mapped_column(JSON)
    expected_impact: Mapped[float | None] = mapped_column(Float)
    mode: Mapped[AutomationMode] = mapped_column(Enum(AutomationMode), default=AutomationMode.manual)
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
    executed: Mapped[bool] = mapped_column(Boolean, default=False)


class AuditLog(TimestampMixin, Base):
    __tablename__ = 'audit_logs'

    id: Mapped[int] = mapped_column(primary_key=True)
    action_id: Mapped[int | None] = mapped_column(ForeignKey('approval_actions.id'))
    actor: Mapped[str] = mapped_column(String(255), default='agent')
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    message: Mapped[str] = mapped_column(Text)
    details: Mapped[dict | None] = mapped_column('metadata', JSON)


class OAuthCredential(TimestampMixin, Base):
    __tablename__ = 'oauth_credentials'

    id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(ForeignKey('businesses.id'), index=True)
    provider: Mapped[str] = mapped_column(String(50), default='google')
    encrypted_access_token: Mapped[str] = mapped_column(Text)
    encrypted_refresh_token: Mapped[str | None] = mapped_column(Text)
    scopes: Mapped[str] = mapped_column(Text)
