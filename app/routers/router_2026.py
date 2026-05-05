
from typing import Any, Literal
import hashlib
import hmac
import json
from threading import Lock

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone
from pathlib import Path

from app.core.settings import settings
from app.utils.email_validator import validate_email

template = Jinja2Templates(
    directory=str(Path(__file__).resolve(
    ).parent.parent / "templates" / "2026")
)


router = APIRouter(tags=["2026"])


today = datetime.now(timezone.utc)

year = today.year


PartnerType = Literal[
    "partnership",
    "sponsorship",
    "python_community_partner",
    "community_partner",
    "other",
]

PackageTier = Literal[
    "headline",
    "platinum",
    "or",
    "argent",
    "nature",
    "gold",
    "silver",
    "bronze",
    "heart",
    "custom",
]


class SponsorInquiryPayload(BaseModel):
    name: str
    contact_name: str
    contact_email: EmailStr
    contact_phone: str | None = None
    logo_url: str | None = None
    partner_type: PartnerType
    package_tier: PackageTier | None = None
    website_url: str | None = None
    description: str | None = None


class Proposalubmission(BaseModel):
    agreed_to_code_of_conduct: bool
    agreed_to_privacy_policy: bool
    shared_with_sponsors: bool
    form_data: dict[str, Any]


class CfpDraftSavePayload(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    form_data: dict[str, Any]


class CfpDraftResumePayload(BaseModel):
    email: EmailStr
    password: str


def _normalize_email(value: str) -> str:
    return value.strip().lower()


def _draft_key_by_email(email: str) -> str:
    return email


def _password_is_strong(password: str) -> bool:
    if len(password) < 8:
        return False
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_special = any(not ch.isalnum() for ch in password)
    return has_upper and has_lower and has_digit and has_special


def _hash_password(password: str, salt: str) -> str:
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120_000,
    )
    return derived.hex()


def _build_api_url(path: str) -> str:
    base = settings.python_togo_api_base_url.rstrip("/")
    if base.endswith("/api/v2"):
        return f"{base}{path}"
    return f"{base}/api/v2{path}"


def render_page(
    request: Request,
    name: str,
    active_page: str,
    page_css: str,
    page_title: str,
    extra_context: dict | None = None,
):
    context = {
        "year": year,
        "active_page": active_page,
        "page_css": page_css,
        "page_title": page_title,
    }
    if extra_context:
        context.update(extra_context)

    return template.TemplateResponse(
        request=request,
        name=name,
        context=context,
    )


def _extract_partner_rows(data: object) -> list[dict]:
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        # Some APIs wrap arrays in a data/items field.
        if isinstance(data.get("data"), list):
            return [row for row in data["data"] if isinstance(row, dict)]
        if isinstance(data.get("items"), list):
            return [row for row in data["items"] if isinstance(row, dict)]
    return []


def _extract_event_object(data: object) -> dict:
    if isinstance(data, dict):
        if isinstance(data.get("data"), dict):
            return data["data"]
        if isinstance(data.get("item"), dict):
            return data["item"]
        return data
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                return item
    return {}


def _parse_date(value: object) -> datetime | None:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str):
        raw = value.strip()
        if not raw:
            return None
        try:
            parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _extract_first_datetime(event: dict, keys: list[str]) -> datetime | None:
    if not event:
        return None
    for key in keys:
        if key in event:
            parsed = _parse_date(event.get(key))
            if parsed:
                return parsed
    return None


def _format_datetime(value: datetime | None, lang: str) -> str:
    if not value:
        return ""

    months_en = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    months_fr = [
        "janvier", "fevrier", "mars", "avril", "mai", "juin",
        "juillet", "aout", "septembre", "octobre", "novembre", "decembre",
    ]
    months = months_fr if lang == "fr" else months_en
    month = months[value.month - 1]

    if lang == "fr":
        return f"{value.day} {month} {value.year} {value.strftime('%H:%M')} UTC"
    return f"{month} {value.day}, {value.year} {value.strftime('%H:%M')} UTC"


def _format_date_range(start: datetime | None, end: datetime | None, lang: str) -> str:
    if not start:
        return ""

    months_en = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    months_fr = [
        "janvier", "fevrier", "mars", "avril", "mai", "juin",
        "juillet", "aout", "septembre", "octobre", "novembre", "decembre",
    ]
    months = months_fr if lang == "fr" else months_en

    if not end:
        month = months[start.month - 1]
        return f"{start.day} {month} {start.year}"

    if start.year == end.year and start.month == end.month:
        month = months[start.month - 1]
        return f"{start.day}-{end.day} {month} {start.year}"

    start_month = months[start.month - 1]
    end_month = months[end.month - 1]
    return f"{start.day} {start_month} {start.year} - {end.day} {end_month} {end.year}"


def _build_meta_line(location: str, date_range: str, duration_label: str) -> str:
    parts = [part for part in [location, date_range, duration_label] if part]
    return " · ".join(parts)


async def _fetch_event_details() -> dict:
    event_code = getattr(settings, "python_togo_event_code", None)
    if not event_code:
        return {}

    headers = {"Authorization": f"Bearer {settings.python_togo_api_key}"}
    candidate_paths = [
        f"/events/get/{event_code}",
    ]

    try:
        async with httpx.AsyncClient(timeout=settings.python_togo_api_timeout_seconds) as client:
            for path in candidate_paths:
                response = await client.get(_build_api_url(path), headers=headers)
                if response.status_code >= 400:
                    continue
                payload = response.json()
                event_obj = _extract_event_object(payload)
                if event_obj:
                    return event_obj
    except Exception:
        return {}

    return {}


async def _build_event_context() -> dict:
    event = await _fetch_event_details()

    name = (event.get("name") or event.get(
        "title") or "").strip() if event else ""
    city = (event.get("city") or "").strip() if event else ""
    country = (event.get("country") or "").strip() if event else ""
    location_value = ", ".join([part for part in [city, country] if part])

    start_raw = None
    end_raw = None
    if event:
        start_raw = event.get("start_date") or event.get(
            "startDate") or event.get("date_start")
        end_raw = event.get("end_date") or event.get(
            "endDate") or event.get("date_end")

    start_date = _parse_date(start_raw)
    end_date = _parse_date(end_raw)
    date_range_en = _format_date_range(start_date, end_date, "en")
    date_range_fr = _format_date_range(start_date, end_date, "fr")

    duration_days = ""
    if start_date and end_date:
        delta = (end_date.date() - start_date.date()).days + 1
        if delta > 0:
            duration_days = str(delta)

    duration_en = f"{duration_days}-day event" if duration_days else ""
    duration_fr = f"Evenement sur {duration_days} jours" if duration_days else ""

    event_meta_en = _build_meta_line(
        location_value, date_range_en, duration_en)
    event_meta_fr = _build_meta_line(
        location_value, date_range_fr, duration_fr)

    program_heading_en = f"Your Experience from {date_range_en}" if date_range_en else "Your Experience"
    program_heading_fr = f"Votre experience du {date_range_fr}" if date_range_fr else "Votre experience"

    about_date_en = f"Date: {date_range_en}" if date_range_en else ""
    about_date_fr = f"Date : {date_range_fr}" if date_range_fr else ""
    about_location_en = f"Location: {location_value}" if location_value else ""
    about_location_fr = f"Lieu : {location_value}" if location_value else ""

    cfp_open_at = _extract_first_datetime(event, [
        "cfp_open_at",
        "cfp_opening_at",
        "cfp_opening_date",
        "cfp_open_date",
        "cfp_start_at",
        "cfp_start_date",
        "proposal_open_at",
        "proposals_open_at",
        "call_for_proposals_open_at",
        "call_for_speakers_open_at",
        "cfpOpenAt",
    ])
    cfp_close_at = _extract_first_datetime(event, [
        "cfp_close_at",
        "cfp_closing_at",
        "cfp_closing_date",
        "cfp_close_date",
        "cfp_end_at",
        "cfp_end_date",
        "proposal_close_at",
        "proposals_close_at",
        "call_for_proposals_close_at",
        "call_for_speakers_close_at",
        "cfpCloseAt",
    ])

    now_utc = datetime.now(timezone.utc)
    cfp_status = "open"
    if cfp_open_at and now_utc < cfp_open_at:
        cfp_status = "upcoming"
    elif cfp_close_at and now_utc > cfp_close_at:
        cfp_status = "closed"

    cfp_open_at_en = _format_datetime(cfp_open_at, "en")
    cfp_open_at_fr = _format_datetime(cfp_open_at, "fr")
    cfp_close_at_en = _format_datetime(cfp_close_at, "en")
    cfp_close_at_fr = _format_datetime(cfp_close_at, "fr")

    return {
        "event_name": name,
        "event_location": location_value,
        "event_date_range_en": date_range_en,
        "event_date_range_fr": date_range_fr,
        "event_meta_en": event_meta_en,
        "event_meta_fr": event_meta_fr,
        "program_heading_en": program_heading_en,
        "program_heading_fr": program_heading_fr,
        "about_date_en": about_date_en,
        "about_date_fr": about_date_fr,
        "about_location_en": about_location_en,
        "about_location_fr": about_location_fr,
        "cfp_status": cfp_status,
        "cfp_open_at_en": cfp_open_at_en,
        "cfp_open_at_fr": cfp_open_at_fr,
        "cfp_close_at_en": cfp_close_at_en,
        "cfp_close_at_fr": cfp_close_at_fr,
    }


async def _assert_cfp_open() -> None:
    event_context = await _build_event_context()
    if event_context.get("cfp_status") != "open":
        raise HTTPException(
            status_code=403,
            detail="Call for Speakers is not open at this time.",
        )


async def _render_page_with_event(
    request: Request,
    name: str,
    active_page: str,
    page_css: str,
    page_title: str,
    extra_context: dict | None = None,
):
    event_context = await _build_event_context()
    merged_context = {**event_context, **(extra_context or {})}
    return render_page(
        request=request,
        name=name,
        active_page=active_page,
        page_css=page_css,
        page_title=page_title,
        extra_context=merged_context,
    )


def _group_confirmed_partners(rows: list[dict]) -> dict:
    grouped = {
        "sponsors": [],
        "partnership_partners": [],
        "community_partners": [],
        "python_community_partners": [],
        "media_partners": [],
        "other_partners": [],
    }

    for row in rows:
        if not row.get("is_confirmed"):
            continue

        item = {
            "name": row.get("name") or "Unnamed",
            "description": row.get("description") or "",
            "logo_url": row.get("logo_url") or "",
            "website_url": row.get("website_url") or "",
            "partner_type": row.get("partner_type") or "other",
            "package_tier": row.get("package_tier") or "",
        }

        partner_type = item["partner_type"]
        if partner_type == "sponsorship":
            grouped["sponsors"].append(item)
        elif partner_type == "partnership":
            grouped["partnership_partners"].append(item)
        elif partner_type == "community_partner":
            grouped["community_partners"].append(item)
        elif partner_type == "python_community_partner":
            grouped["python_community_partners"].append(item)
        elif partner_type in {"media_partner", "media-partner", "media"}:
            grouped["media_partners"].append(item)
        else:
            grouped["other_partners"].append(item)

    return grouped


def _sort_topics_by_created_at(rows: list[dict]) -> list[dict]:
    def sort_key(row: dict) -> tuple[bool, datetime | None]:
        return (_parse_date(row.get("created_at")) is None, _parse_date(row.get("created_at")))

    return sorted(rows, key=sort_key)


def _extract_topics(data: object) -> list[dict]:
    if isinstance(data, list):
        rows = [row for row in data if isinstance(row, dict)]
    elif isinstance(data, dict):
        if isinstance(data.get("data"), list):
            rows = [row for row in data["data"] if isinstance(row, dict)]
        elif isinstance(data.get("items"), list):
            rows = [row for row in data["items"] if isinstance(row, dict)]
        else:
            rows = []
    else:
        rows = []

    normalized: list[dict] = []
    for row in rows:
        topic_id = row.get("id")
        name_en = (row.get("name_en") or row.get("name") or "").strip()
        name_fr = (row.get("name_fr") or row.get("name") or name_en).strip()
        if not topic_id or not name_en:
            continue

        normalized.append({
            "id": str(topic_id),
            "name_en": name_en,
            "name_fr": name_fr,
            "description_en": (row.get("description_en") or row.get("description") or "").strip(),
            "description_fr": (row.get("description_fr") or row.get("description") or "").strip(),
            "created_at": row.get("created_at") or "",
            "updated_at": row.get("updated_at") or "",
        })

    return _sort_topics_by_created_at(normalized)


async def _fetch_topics() -> list[dict]:
    event_code = getattr(settings, "python_togo_event_code", None)
    if not event_code:
        return []

    headers = {"Authorization": f"Bearer {settings.python_togo_api_key}"}
    url = _build_api_url(f"/topics/list/{event_code}")

    try:
        async with httpx.AsyncClient(timeout=settings.python_togo_api_timeout_seconds) as client:
            response = await client.get(url, headers=headers)
        if response.status_code < 400:
            payload = response.json()
            return _extract_topics(payload)
    except Exception:
        return []

    return []


async def _fetch_formats() -> list[dict]:
    event_code = getattr(settings, "python_togo_event_code", None)
    if not event_code:
        return []

    headers = {"Authorization": f"Bearer {settings.python_togo_api_key}"}
    url = _build_api_url(f"/proposal-formats/list/{event_code}")

    try:
        async with httpx.AsyncClient(timeout=settings.python_togo_api_timeout_seconds) as client:
            response = await client.get(url, headers=headers)
        if response.status_code < 400:
            payload = response.json()
            return _extract_topics(payload)
    except Exception:
        return []

    return []


async def _fetch_partner_sections() -> dict:
    event_code = getattr(settings, "python_togo_event_code", None)
    grouped = {
        "sponsors": [],
        "partnership_partners": [],
        "community_partners": [],
        "python_community_partners": [],
        "media_partners": [],
        "other_partners": [],
    }

    if not event_code:
        return grouped

    url = _build_api_url(f"/partners-sponsors/confirmed/all/{event_code}")
    headers = {"Authorization": f"Bearer {settings.python_togo_api_key}"}

    try:
        async with httpx.AsyncClient(timeout=settings.python_togo_api_timeout_seconds) as client:
            response = await client.get(url, headers=headers)
        if response.status_code < 400:
            payload = response.json()
            rows = _extract_partner_rows(payload)
            return _group_confirmed_partners(rows)
    except Exception:
        return grouped

    return grouped


def _extract_featured_speakers(data: object) -> list[dict]:

    response_exemple = [
        {
            "full_name": "string",
            "headline": "string",
            "organization": "string",
            "company_logo_url": "string",
            "country": "string",
            "bio": "string",
            "photo_url": "string",
            "social_links": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
            },
            "sessions": [
                {
                    "additionalProp1": "string",
                    "additionalProp2": "string",
                    "additionalProp3": "string"
                }
            ],
            "is_featured": False,
            "created_at": "2026-04-27T15:30:17.565Z",
            "updated_at": "2026-04-27T15:30:17.565Z"
        }
    ]
    if isinstance(data, list):
        rows = [row for row in data if isinstance(row, dict)]
    elif isinstance(data, dict):
        if isinstance(data.get("data"), list):
            rows = [row for row in data["data"] if isinstance(row, dict)]
        elif isinstance(data.get("items"), list):
            rows = [row for row in data["items"] if isinstance(row, dict)]
        else:
            rows = []
    else:
        rows = []
    speakers: list[dict] = []
    for row in rows:
        full_name = (row.get("full_name") or "").strip()
        headline = (row.get("headline") or "").strip()
        organization = (row.get("organization") or "").strip()
        company_logo_url = (row.get("company_logo_url") or "").strip()
        country = (row.get("country") or "").strip()
        bio = (row.get("bio") or "").strip()
        photo_url = (row.get("photo_url") or "").strip()
        social_links = row.get("social_links") or {}
        sessions = row.get("sessions") or []
        speakers.append({
            "full_name": full_name,
            "headline": headline,
            "organization": organization,
            "company_logo_url": company_logo_url,
            "country": country,
            "bio": bio,
            "photo_url": photo_url,
            "social_links": social_links,
            "sessions": sessions,
        })
    return speakers


async def _fetch_featured_speakers() -> list[dict]:
    """Fetch featured speakers from the API. This is a placeholder implementation and should be updated to match the actual API response structure."""
    event_code = getattr(settings, "python_togo_event_code", None)
    url = _build_api_url(f"/speakers/featured/{event_code}")
    headers = {"Authorization": f"Bearer {settings.python_togo_api_key}"}
    try:
        async with httpx.AsyncClient(timeout=settings.python_togo_api_timeout_seconds) as client:
            response = await client.get(url, headers=headers)
        if response.status_code < 400:
            payload = response.json()
            return _extract_featured_speakers(payload)
    except Exception:
        return []

    return []


@router.get("/")
async def home(request: Request):
    partner_sections = await _fetch_partner_sections()
    python_community = partner_sections.get("python_community_partners", [])
    # community = partner_sections.get("community_partners", [])
    speakers = await _fetch_featured_speakers()
    # Keep PSF always first on the home page, then append dynamic community names.
    home_partner_names: list[str] = ["Python Software Foundation"]
    seen = {"python software foundation"}

    return await _render_page_with_event(
        request=request,
        name="index.html",
        active_page="home",
        page_css="home.css",
        page_title="PyCon Togo 2026 — Home",
        extra_context={"speakers": speakers},
    )


@router.get("/speakers")
async def speakers(request: Request):
    event_context = await _build_event_context()
    if event_context.get("cfp_status") != "open":
        return render_page(
            request=request,
            name="2026_call_for_speakers_coming_soon.html",
            active_page="speakers",
            page_css="coming-soon.css",
            page_title="PyCon Togo 2026 — Call for Speakers",
            extra_context=event_context,
        )

    topics = await _fetch_topics()
    formats = await _fetch_formats()
    return render_page(
        request=request,
        name="2026_call_for_speakers.html",
        active_page="speakers",
        page_css="call-for-speakers.css",
        page_title="PyCon Togo 2026 — Call for Speakers",
        extra_context={
            **event_context,
            "topics": topics,
            "proposal_formats": formats,
        },
    )


@router.get("/schedule")
async def schedule(request: Request):
    return await home(request)


@router.get("/venue")
async def venue(request: Request):
    return await home(request)


@router.get("/tickets")
async def tickets(request: Request):
    return await _render_page_with_event(
        request=request,
        name="2026_tickets_coming_soon.html",
        active_page="tickets",
        page_css="coming-soon.css",
        page_title="PyCon Togo 2026 — Tickets (Opening Soon)",
    )


@router.get("/registration")
async def registration(request: Request):
    return await tickets(request)


@router.get("/contact")
async def contact(request: Request):
    return await _render_page_with_event(
        request=request,
        name="2026_contact.html",
        active_page="contact",
        page_css="contact.css",
        page_title="PyCon Togo 2026 — Contact",
    )


@router.get("/about")
async def about(request: Request):
    return await _render_page_with_event(
        request=request,
        name="2026_about.html",
        active_page="about",
        page_css="about.css",
        page_title="PyCon Togo 2026 — About",
    )


@router.get("/team")
async def team(request: Request):
    return await _render_page_with_event(
        request=request,
        name="2026_teams.html",
        active_page="team",
        page_css="team.css",
        page_title="PyCon Togo 2026 — Team",
    )


@router.get("/teams")
async def teams(request: Request):
    return await team(request)


@router.get("/visit")
async def visit(request: Request):
    return await _render_page_with_event(
        request=request,
        name="2026_visit.html",
        active_page="visit",
        page_css="about.css",
        page_title="PyCon Togo 2026 — Visit Togo",
    )


@router.get("/coc")
async def coc(request: Request):
    return await _render_page_with_event(
        request=request,
        name="2026_coc.html",
        active_page="about",
        page_css="about.css",
        page_title="PyCon Togo 2026 — Code of Conduct",
    )


@router.get("/code-of-conduct")
async def coc_slug(request: Request):
    return await coc(request)


@router.get("/health_security")
async def health_security(request: Request):
    return await _render_page_with_event(
        request=request,
        name="2026_health_security.html",
        active_page="about",
        page_css="about.css",
        page_title="PyCon Togo 2026 — Health & Safety Policy",
    )


@router.get("/health-safety")
async def health_safety_slug(request: Request):
    return await health_security(request)


@router.get("/privacy-policy")
async def privacy_policy(request: Request):
    return await _render_page_with_event(
        request=request,
        name="2026_privacy_policy.html",
        active_page="about",
        page_css="about.css",
        page_title="PyCon Togo 2026 — Privacy Policy",
    )


@router.get("/privacy_policy")
async def privacy_policy_slug(request: Request):
    return await privacy_policy(request)


@router.get("/sponsors")
async def sponsors(request: Request):
    return await _render_page_with_event(
        request=request,
        name="2026_sponsors.html",
        active_page="sponsors",
        page_css="sponsors.css",
        page_title="PyCon Togo 2026 — Sponsors",
    )


@router.get("/partners")
async def partners(request: Request):
    grouped = await _fetch_partner_sections()

    return await _render_page_with_event(
        request=request,
        name="2026_partners.html",
        active_page="partners",
        page_css="partners.css",
        page_title="PyCon Togo 2026 — Partners Directory",
        extra_context={"partner_sections": grouped},
    )


@router.post("/sponsors/inquiry")
async def sponsors_inquiry(payload: SponsorInquiryPayload):
    event_code = getattr(settings, "python_togo_event_code", None)

    if not validate_email(payload.contact_email).is_valid:

        raise HTTPException(
            status_code=400, detail="Failed to validate email address please check your email address.")
    if not event_code:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized.",
        )

    url = _build_api_url(f"/partners-sponsors/inquiry/{event_code}")
    headers = {
        "Authorization": f"Bearer {settings.python_togo_api_key}",
        "Content-Type": "application/json",
    }

    try:
        payload = payload.model_dump(mode="json")
        async with httpx.AsyncClient(timeout=settings.python_togo_api_timeout_seconds) as client:
            response = await client.post(url, headers=headers, json=payload)
    except httpx.RequestError as exc:
        #   TODO  - LOG ERROR
        raise HTTPException(
            status_code=502, detail=f"unreachable")

    if response.status_code >= 400:
        message = "Sponsor API error"
        try:
            body = response.json()
            message = body.get("message") or body.get("detail") or message
        except ValueError:
            message = response.text or message
        return JSONResponse(
            status_code=response.status_code,
            content={"ok": False, "message": message},
        )

    return {"ok": True, "message": "Sponsorship inquiry sent"}


@router.get("/cfp")
async def cfp(request: Request):
    return await speakers(request)


@router.get("/call-for-speakers")
async def call_for_speakers(request: Request):
    return await speakers(request)


@router.post("/submit-proposal")
async def submit_proposal(payload: Proposalubmission):
    await _assert_cfp_open()
    if not payload.agreed_to_code_of_conduct:
        raise HTTPException(
            status_code=400, detail="You must agree to the Code of Conduct.")
    if not payload.agreed_to_privacy_policy:
        raise HTTPException(
            status_code=400, detail="You must agree to the Privacy Policy.")

    proposal_data = payload.form_data

    if not validate_email(proposal_data["email"]).is_valid:
        raise HTTPException(
            status_code=400, detail="Failed to validate email address please check your email address.")
    url = _build_api_url(
        f"/proposals/create/{settings.python_togo_event_code}")
    headers = {
        "Authorization": f"Bearer {settings.python_togo_api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=settings.python_togo_api_timeout_seconds) as client:
            response = await client.post(url, headers=headers, json=proposal_data)
    except httpx.RequestError as exc:

        #  TODO - log errors
        raise HTTPException(
            status_code=502, detail=f"Sponsor API unreachable")

    if response.status_code >= 400:
        message = "Sponsor API error"
        try:
            body = response.json()
            message = body.get("message") or body.get("detail") or message
        except ValueError:
            message = response.text or message

        return JSONResponse(
            status_code=response.status_code,
            content={"ok": False, "message": message},
        )

    data = None
    try:
        data = response.json()
    except ValueError:
        data = {"message": "Request accepted"}

    return {"ok": True, "message": "Sponsorship inquiry sent"}


@router.post("/call-for-speakers/drafts/save")
async def save_cfp_draft(payload: CfpDraftSavePayload):
    await _assert_cfp_open()

    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=400, detail="Password confirmation does not match.")

    if not _password_is_strong(payload.password):
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 chars with uppercase, lowercase, number, and special character.",
        )

    email = _normalize_email(str(payload.email))
    if not validate_email(email).is_valid:
        raise HTTPException(
            status_code=400, detail="Failed to validate email address please check your email address.")

    key = _draft_key_by_email(email)
    hash_password = _hash_password(payload.password, key)
    url = _build_api_url(
        f"/proposals/save-draft/{settings.python_togo_event_code}")
    headers = {
        "Authorization": f"Bearer {settings.python_togo_api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "email": email,
        "password_hash": hash_password,
        "proposal_data": payload.form_data,
    }

    try:
        message = ""
        async with httpx.AsyncClient(timeout=settings.python_togo_api_timeout_seconds) as client:
            response = await client.post(url, headers=headers, json=body)

        if response.status_code >= 400:
            message = "Failed to save draft"
            try:
                body = response.json()
                message = body.get("message") or body.get("detail") or message
            except ValueError:
                message = response.text or message

            raise HTTPException(
                status_code=response.status_code, detail=message)
    except httpx.RequestError as exc:
        # Log the exception details for debugging purposes
        raise HTTPException(
            status_code=502, detail=f"unreachable")

    return {
        "ok": True,
        "message": message or "Draft saved successfully",
        "data": {"email": email},
    }


@router.post("/call-for-speakers/drafts/resume")
async def resume_cfp_draft(payload: CfpDraftResumePayload):
    await _assert_cfp_open()

    email = _normalize_email(str(payload.email))
    if not validate_email(email).is_valid:
        raise HTTPException(
            status_code=400, detail="Failed to validate email address please check your email address.")
    key = _draft_key_by_email(email)

    hash_password = _hash_password(payload.password, key)
    url = _build_api_url(
        f"/proposals/resume-draft/{settings.python_togo_event_code}")
    headers = {
        "Authorization": f"Bearer {settings.python_togo_api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "email": email,
        "password": hash_password,
    }
    try:
        message = ""
        async with httpx.AsyncClient(timeout=settings.python_togo_api_timeout_seconds) as client:
            response = await client.post(url, headers=headers, json=body)

        if response.status_code >= 400:
            message = "Failed to resume draft"
            try:
                body = response.json()
                message = body.get("message") or body.get("detail") or message
            except ValueError:
                message = response.text or message

            raise HTTPException(
                status_code=response.status_code, detail=message)
        response_payload = response.json()
        proposal_data = response_payload.get("proposal_data")

        if not isinstance(proposal_data, dict):
            proposal_data = {}

        return {
            "ok": True,
            "message": "Draft restored. You can continue your proposal.",
            "data": {
                "email": email,
                "form_data": proposal_data,
                "proposal_data": proposal_data,
            },
            "proposal_data": proposal_data,
        }
    except httpx.RequestError as exc:
        # Log the exception details for debugging purposes
        raise HTTPException(
            status_code=502, detail=f"unreachable")


@router.get("/volunteers")
def volunteers(request: Request):
    # TODO - create a volunteers page with a form to sign up as a volunteer
    pass


@router.get("/feedback")
def feedback(request: Request):
    # TODO - create a feedback page with a form to submit feedback
    pass


@router.get("/shop")
def shop(request: Request):
    # TODO - create a shop page with conference merchandise
    pass
