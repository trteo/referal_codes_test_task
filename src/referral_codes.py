from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import ReferralCode
from app.models.referral_codes import ReferralCodeResponse


async def generate_referral_code(expire_date: datetime, user_id: int, db_session: AsyncSession):
    referral_code_value = uuid4()

    referral_code = ReferralCode(
        creator_id=user_id,
        value=referral_code_value,
        expire_date=expire_date.replace(tzinfo=None),
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        is_active=True,
    )
    db_session.add(referral_code)
    await db_session.commit()
    await db_session.refresh(referral_code)

    return ReferralCodeResponse(
        referral_code_id=referral_code.id,
        referral_code=str(referral_code_value),
    )


async def deactivate_referral_code(user_id: int, db_session: AsyncSession):
    stmt = (
        update(ReferralCode)
        .where(
            and_(
                ReferralCode.creator_id == user_id,
                ReferralCode.is_active.is_(True),
            )
        ).values(is_active=False)
    )

    # Execute the update query
    result = await db_session.execute(stmt)
    await db_session.commit()

    # Return the number of rows affected
    return result.rowcount