import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_database
from app.config import settings

from app.router import router as assessment_router

v1 = APIRouter(prefix="/api")

v1.include_router(assessment_router)

app = FastAPI(title="Assessment API", version="0.1.0", docs_url="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(v1)

if settings.LOCAL:
    create_database()

@app.get("/")
async def root():
    return {"msg": "Hello World"}
if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)