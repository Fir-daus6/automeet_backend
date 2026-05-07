from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.orm_registry import import_all_models

import_all_models()

def get_application() -> FastAPI:
    _app = FastAPI(
        title=settings.APP_NAME,
        version=settings.API_VERSION,
        openapi_url="/openapi.json",
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(api_router, prefix="/api/v1")

    return _app

app = get_application()

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Automeet API is running"}
