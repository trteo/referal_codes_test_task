import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.handlers.referral_codes import router as referral_codes_router
from app.handlers.users import router as users_router
from settings.config import settings

app = FastAPI(title='Referrals codes service')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(referral_codes_router, prefix="/referral_codes", tags=["Managing referral codes"])
app.include_router(users_router, prefix="/users_router", tags=["Managing users"])

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        port=8002,
        host='0.0.0.0',
        reload=settings.DEV,
        log_config='settings/logger_config.json'
    )
