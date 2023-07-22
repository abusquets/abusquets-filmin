from fastapi.routing import APIRouter

from .country import router as country_router


router = APIRouter(prefix='/core', tags=['core'])
router.include_router(country_router)
