from fastapi import Depends, FastAPI

from app.routes.api import router as api_router
from app.endpoints.base import get_api_key


app = FastAPI(dependencies = [Depends(get_api_key)])

app.include_router(api_router)
