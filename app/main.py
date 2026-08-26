from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.routes.health import router as health_router
from app.api.routes.tasks import router as tasks_router


app = FastAPI(
    title="Task Tracker API",
    description="A small learning project for tracking tasks.",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(tasks_router)


@app.get("/", include_in_schema=False)
def frontend() -> FileResponse:
    return FileResponse(Path(__file__).resolve().parent.parent / "frontend" / "index.html")


@app.get("/app.js", include_in_schema=False)
def frontend_script() -> FileResponse:
    return FileResponse(
        Path(__file__).resolve().parent.parent / "frontend" / "app.js",
        media_type="application/javascript",
    )
