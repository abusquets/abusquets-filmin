from fastapi.routing import APIRouter

from .genre import router as genre_router
from .movie import router as movie_router
from .production_company import router as production_company_router


router = APIRouter(prefix='/filmin', tags=['filmin'])
router.include_router(production_company_router)
router.include_router(genre_router)
router.include_router(movie_router)
