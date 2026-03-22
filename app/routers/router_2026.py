
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


@router.get("/speakers")
def speakers(request: Request):
    return template.TemplateResponse(
        request=request,
        name="2026_speakers.html",
        context={
            "year": year,
        },
    )


@router.get("/schedule")
def schedule(request: Request):
    return template.TemplateResponse(
        request=request,
        name="2026_schedule.html",
        context={
            "year": year,
        },
    )


@router.get("/venue")
def venue(request: Request):
    return template.TemplateResponse(
        request=request,
        name="2026_venue.html",
        context={
            "year": year,
        },
    )


@router.get("/registration")
def registration(request: Request):
    return template.TemplateResponse(
        request=request,
        name="2026_registration.html",
        context={
            "year": year,
        },
    )


@router.get("/contact")
def contact(request: Request):
    return template.TemplateResponse(
        request=request,
        name="2026_contact.html",
        context={
            "year": year,
        },
    )


@router.get("/about")
def about(request: Request):
    return template.TemplateResponse(
        request=request,
        name="2026_about.html",
        context={
            "year": year,
        },
    )


@router.get("/teams")
def teams(request: Request):
    return template.TemplateResponse(
        request=request,
        name="2026_teams.html",
        context={
            "year": year,
        },
    )


@router.get("/coc")
def coc(request: Request):
    return template.TemplateResponse(
        request=request,
        name="2026_coc.html",
        context={
            "year": year,
        },
    )


@router.get("/health_security")
def health_security(request: Request):
    return template.TemplateResponse(
        request=request,
        name="2026_health_security.html",
        context={
            "year": year,
        },
    )


@router.get("/sponsors")
def sponsors(request: Request):
    return template.TemplateResponse(
        request=request,
        name="2026_sponsors.html",
        context={
            "year": year,
        },
    )


@router.get("/cfp")
def cfp(request: Request):
    return template.TemplateResponse(
        request=request,
        name="2026_cfp.html",
        context={
            "year": year,
        },
    )


@router.get("/volunteers")
def volunteers(request: Request):
    return template.TemplateResponse(
        request=request,
        name="2026_volunteers.html",
        context={
            "year": year,
        },
    )
