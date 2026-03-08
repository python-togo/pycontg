import typing
if not hasattr(typing, "_ClassVar") and hasattr(typing, "ClassVar"):
    typing._ClassVar = typing.ClassVar


import os
from fastapi import FastAPI, HTTPException, Request
from app.routers.router_2025 import router as router_2025
from app.routers.router_2026 import router as router_2026
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from datetime import datetime,  timezone
from pathlib import Path

load_dotenv()


ENV = os.getenv("ENV", "dev")

app = FastAPI(
    title="PyCon Tog0 Official Website",
    description="The official website for PyCon Tog0, the premier Python conference in Togo. Join us for an unforgettable experience filled with inspiring talks, hands-on workshops, and vibrant community engagement. Whether you're a seasoned developer or just starting your Python journey, PyCon Tog0 offers something for everyone. Stay tuned for updates on speakers, schedules, and registration details as we prepare to bring the Python community together in Togo!",
    version="1.1.0",
    openapi_url="/openapi.json" if ENV == "dev" or ENV == "local" else None,
    docs_url="/docs" if ENV == "dev" or ENV == "local" else None,
    redoc_url="/redoc" if ENV == "dev" or ENV == "local" else None,
)

BASE_DIR = Path(__file__).resolve().parent
template = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

year = datetime.now(timezone.utc).year


@app.get("/talents", response_class=HTMLResponse)
def talents(request: Request):
    return template.TemplateResponse(
        request=request,
        name="talents.html",
        context={
            "year": year,
        },
    )


app.include_router(router_2025, prefix="/2025")
app.include_router(router_2026)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with custom error templates"""
    status_code = exc.status_code

    error_map = {
        400: ("400.html", "Bad Request: The server could not understand the request due to invalid syntax."),
        403: ("403.html", "Forbidden: You don't have access to this resource."),
        404: ("404.html", "Oops! The page you're looking for seems to have disappeared or doesn't exist. Perhaps it has gone off to discover the wild python in Africa!"),
        422: ("422.html", "Unprocessable Entity: The server understands the content type of the request entity, but was unable to process the contained instructions."),
        500: ("500.html", "Oops! Something went wrong on our end."),
        502: ("502.html", "Bad Gateway: The server received an invalid response."),
        503: ("503.html", "Service Unavailable: The server is temporarily unable to handle the request."),
    }

    template_name, default_message = error_map.get(
        status_code, ("404.html", "An error occurred."))

    try:
        return template.TemplateResponse(
            request=request,
            name=template_name,
            status_code=status_code,
            context={
                "year": year,
                "message": exc.detail or default_message,
                "status_code": status_code,
            },
        )
    except Exception:
        # Fallback to plain text if template rendering fails
        return Response(
            content=f"{status_code}: {exc.detail or default_message}",
            status_code=status_code,
            media_type="text/plain",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8800)
