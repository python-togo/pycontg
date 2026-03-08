
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime, timezone
from pathlib import Path


template = Jinja2Templates(
    directory=str(Path(__file__).resolve(
    ).parent.parent / "templates" / "2026")
)


router = APIRouter()

today = datetime.now(timezone.utc)

year = today.year


@router.get("/")
def home(request: Request):
    return template.TemplateResponse(
        request=request,
        name="2026_coming_soon.html",
        context={
            "year": year,
        },
    )
