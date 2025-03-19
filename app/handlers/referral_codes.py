from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import ReferralCode, User
from app.dependencies import get_session
from app.models.referral_codes import ReferralCodeResponse, ReferralCodeRequest
from src.referral_codes import generate_referral_code, deactivate_referral_code
from src.users import current_active_user

router = APIRouter()


@router.post("/generate-referral-code", response_model=ReferralCodeResponse)
async def register_new_referral_code(
        request: ReferralCodeRequest,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(current_active_user)
):
    """
    Generate a referral code that expires on the provided date.

    - **expire_date**: The date when the referral code will expire. Must be at least tomorrow.
    - **Returns**: A referral code and its expiration date.
    """
    # Generate a UUID
    await deactivate_referral_code(user_id=user.id, db_session=session)
    new_referral_code = await generate_referral_code(expire_date=request.expire_date, user_id=user.id, db_session=session)

