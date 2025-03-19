from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, field_validator


# Pydantic Model for Request Body
class ReferralCodeRequest(BaseModel):
    expire_date: datetime

    @field_validator('expire_date')
    @classmethod
    def validate_expire_date(cls, value):
        """Ensure the expire_date is not earlier than tomorrow."""
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        if value < datetime.now(timezone.utc) + timedelta(days=1):
            raise ValueError('Expire date must be at least tomorrow.')
        return value


class ReferralCodeResponse(BaseModel):
    referral_code_id: int
    referral_code: str
