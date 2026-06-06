from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from database import engine, Base
from exceptions import AppException, app_exception_handler, unhandled_exception_handler
from routes import (
    project_routes, upload_routes, graph_routes,
    script_routes, review_routes, storyboard_routes,
    export_routes, task_routes,
)
from logger import logger

settings = get_settings()

Base.metadata.create_all(bind=engine)
logger.info("Database tables created")

app = FastAPI(
    title="Novel2Screen API",
    description="基于大语言模型的小说影视化创作平台后端 API",
    version="1.0.0",
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project_routes.router, prefix="/api", tags=["projects"])
app.include_router(upload_routes.router, prefix="/api", tags=["upload"])
app.include_router(graph_routes.router, prefix="/api", tags=["graph"])
app.include_router(script_routes.router, prefix="/api", tags=["script"])
app.include_router(review_routes.router, prefix="/api", tags=["review"])
app.include_router(storyboard_routes.router, prefix="/api", tags=["storyboard"])
app.include_router(export_routes.router, prefix="/api", tags=["export"])
app.include_router(task_routes.router, prefix="/api", tags=["tasks"])


@app.get("/")
async def root():
    return {"message": "Novel2Screen API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
