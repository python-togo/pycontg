import typing

from app.schemas.models import ContactFormPayload
if not hasattr(typing, "_ClassVar") and hasattr(typing, "ClassVar"):
    typing._ClassVar = typing.ClassVar

from fastapi import FastAPI, HTTPException, Request
from app.routers.router_2025 import router_2025
from app.routers.router_2026 import router as router_2026
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from datetime import datetime,  timezone
from pathlib import Path
from app.core.settings import settings
import httpx


ENV = settings.env

app = FastAPI(
    title=settings.name,
    description="The official website for PyCon Togo, the premier Python conference in Togo. Join us for an unforgettable experience filled with inspiring talks, hands-on workshops, and vibrant community engagement. Whether you're a seasoned developer or just starting your Python journey, PyCon Togo offers something for everyone. Stay tuned for updates on speakers, schedules, and registration details as we prepare to bring the Python community together in Togo!",
    version=settings.version,
    openapi_url="/openapi.json" if ENV in ["dev",
                                           "local", "development"] else None,
    docs_url="/docs" if ENV in ["dev", "local", "development"] else None,
    redoc_url="/redoc" if ENV in ["dev", "local", "development"] else None,
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


@app.get("/talents")
def talents(request: Request):
    return template.TemplateResponse(
        request=request,
        name="talents.html",
        context={
            "year": year,
        },
    )


@app.post("/contact/send")
async def send_contact_message(payload: ContactFormPayload):
    normalized_payload = {
        "name": payload.name.strip(),
        "email": str(payload.email).strip(),
        "subject": payload.subject.strip() or "General inquiry",
        "message": payload.message.strip(),
    }

    target_url = (
        f"{settings.python_togo_api_base_url.rstrip('/')}/contacts/send"
    )
    print(
        f"Prepared contact form payload: {normalized_payload} to be sent to {target_url}")
    headers = {
        "Authorization": f"Bearer {settings.python_togo_api_key}",
        "Content-Type": "application/json",
    }
    print(
        f"Sending contact form data to {target_url} with payload: {normalized_payload}")

    try:
        async with httpx.AsyncClient(
            timeout=settings.python_togo_api_timeout_seconds
        ) as client:
            response = await client.post(
                target_url,
                headers=headers,
                json=normalized_payload,
            )
    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The contact service took too long to respond.",
        ) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to reach the contact service.",
        ) from exc

    if response.status_code >= 400:
        error_detail = "Contact submission failed. Please try again later."
        try:
            api_error = response.json()
            if isinstance(api_error, dict):
                detail_value = api_error.get(
                    "detail") or api_error.get("message")
                if detail_value:
                    error_detail = str(detail_value)

        except ValueError:
            pass

        raise HTTPException(
            status_code=response.status_code, detail=error_detail)

    success_message = "Message sent successfully."
    try:
        data = response.json()
        if isinstance(data, dict) and data.get("message"):
            success_message = str(data["message"])
    except ValueError:
        pass

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"ok": True, "message": success_message},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8800)
