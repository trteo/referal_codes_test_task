import httpx
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import User
from app.models.users import UserCreate, UserRead, UserUpdate
from src.users import auth_backend, current_active_user, fastapi_users
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request

router = APIRouter()


templates = Jinja2Templates(directory="temolates")


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'http://localhost:8002/users_router/login2',
            # json={"grant_type": "password", "login": "user@example.com", "password": "string"},
        )
        print(response.status_code)
    return templates.TemplateResponse(name="auth/login.html", context={"id": 3}, request=request)
templates = Jinja2Templates(directory="temolates")


@router.post("/login2")
async def login():
    return {'ok': '6543534'}


@router.get("/success", response_class=HTMLResponse)
async def success_page(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    # tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@router.post("/auth/jwt", response_class=HTMLResponse)
def login(request: Request):
    auth_backend.login()
    return templates.TemplateResponse(name="auth/login.html", context={"id": 3}, request=request)
