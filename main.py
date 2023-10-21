import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_database
from app.config import settings
from brief import summary,docs,description

from app.router import router as assessment_router

v1 = APIRouter(prefix="/api/v1")

v1.include_router(assessment_router)

app = FastAPI(title="Assessment API", version="0.1.0",summary=summary,description=description, docs_url=docs)


app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:3000', settings.FRONTEND_URL],
  allow_credentials=True,
  allow_methods=["GET", "POST", "OPTIONS"], 
  allow_headers=["Content-Type","Set-Cookie"],
)

app.include_router(v1)

if settings.LOCAL:
    create_database()

@app.get("/")
async def root():
    return {"msg": "Hello World"}
if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)