from fastapi import APIRouter

from app.endpoints import examples
from app.endpoints.base import response_codes


router = APIRouter()
router.include_router(examples.router, responses = {401: response_codes[401]})
