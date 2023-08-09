from fastapi.routing import APIRouter

from .token import router as token_router


router = APIRouter(prefix='/auth', tags=['auth'])
router.include_router(token_router)
