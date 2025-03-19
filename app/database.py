from typing import List, Optional
from datetime import datetime, UTC

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey, DateTime, String, Boolean, Integer, UUID, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    referral_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    referral_codes: Mapped[Optional[List['ReferralCode']]] = relationship(
        'ReferralCode',
        back_populates='creator',
        cascade='all, delete-orphan'
    )


class ReferralCode(Base):
    __tablename__ = 'referral_codes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    value: Mapped[UUID] = mapped_column(UUID)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    expire_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    creator: Mapped['User'] = relationship('User', back_populates='referral_codes')


