from fastapi import APIRouter

from app.endpoints import examples


router = APIRouter()
router.include_router(examples.router)
