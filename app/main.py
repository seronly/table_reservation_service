from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.api.routers import api_router


app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    pass
