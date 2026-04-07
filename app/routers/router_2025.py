import requests
from uuid import uuid4, UUID
from app.utils.validator import (
    is_valid_email,
)

from app.database.datas import (
    get_swags,
    get_sponsorteirs,
    get_sponsortirtbytitle,
    get_something_email,
    insert_something,
    # get_everything,
    # get_everything_where,
)
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from pathlib import Path
from app.utils.schedule import get_schedule, get_speaker_images, get_event_info
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


router_2025 = APIRouter(tags=["2025"])


template = Jinja2Templates(
    directory=str(Path(__file__).resolve(
    ).parent.parent / "templates" / "2025")
)


load_dotenv()


close_volunteer_date = datetime(2025, 5, 31, 16, 0, 0)
close_volunteer_date = close_volunteer_date.replace(tzinfo=timezone.utc)
year = datetime.now(timezone.utc).year
event_date = datetime(2025, 8, 23, 7, 0, 0)
event_date_str = event_date.strftime("%d %B %Y at %H:%M")
registration_date = datetime(2025, 7, 23, 16, 45, 0)
registration_closing_date = datetime(2025, 8, 10, 16, 0, 0)
schedule_release_date = datetime(2025, 8, 10, 16, 30, 0)
schedule_release_date = schedule_release_date.replace(tzinfo=timezone.utc)
LIVE_DATETIME = datetime(2025, 8, 23, 8, 0, 0)
LIVE_DATETIME = LIVE_DATETIME.replace(tzinfo=timezone.utc)
YOUTUBE_URL = "https://www.youtube.com/@PythonTogo"

registration_closing_date = registration_closing_date.replace(
    tzinfo=timezone.utc)

registration_date = registration_date.replace(tzinfo=timezone.utc)
opening_in = registration_date - datetime.now(timezone.utc)

opening_in_days = opening_in.days

sponsor_tiers = get_sponsorteirs()
proposal_opining_date = datetime(
    2025, 6, 3, 16).strftime("%d %B %Y at %H:%M UTC")
proposal_closing_date = datetime(
    2025, 6, 30, 16).strftime("%d %B %Y at %H:%M UTC")


API_ROOT = os.getenv("API_ROOT", "http://127.0.0.1:8000/api")
speakers_list = requests.get(f"{API_ROOT}/speakers")
if speakers_list.status_code == 200:
    speakers_list = speakers_list.json()
else:
    speakers_list = []


paidsponsors = requests.get(f"{API_ROOT}/sponsors")
if paidsponsors.status_code == 200:
    paidsponsors = paidsponsors.json()
else:
    paidsponsors = []


gold_sponsors = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "gold"]
silver_sponsors = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "silver"
]
bronze_sponsors = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "bronze"
]
headline_sponsors = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "headline"
]
inkind_sponsors = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "inkind"
]
community_sponsors = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "community"
]
media_sponsors = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "media"
]
educational_supporters = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "educational"
]


@router_2025.get("/")
def home_25(request: Request):

    return template.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "year": year,
            "event_date": event_date_str,
            "sponsor_tiers": sponsor_tiers,
            "proposal_opining_date": proposal_opining_date,
            "proposal_closing_date": proposal_closing_date,
            "paidsponsors": paidsponsors,
        },)


@router_2025.get("/report")
def report_2025():
    return RedirectResponse(url="https://report.pytogo.org/")


@router_2025.get("/livestreaming")
def live_page(request: Request):
    now = datetime.now(timezone.utc)
    if now >= LIVE_DATETIME:
        return RedirectResponse(url=YOUTUBE_URL)
    else:
        return template.TemplateResponse(request=request, name="livestreaming.html", context={"year": year})


@router_2025.get("/shop")
def shop_swag(request: Request):

    return template.TemplateResponse(
        request=request,
        name="shop.html",
        context={
            "year": year,
            "swags": get_swags(),
        },
    )


@router_2025.get("/register")
def register_get(request: Request):

    if registration_date > datetime.now(timezone.utc):
        return template.TemplateResponse(
            request=request,
            name="registration.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "registration_open": True,
                "opening_in_days": opening_in_days,
            },
        )
    if datetime.now(timezone.utc) > registration_closing_date:
        return template.TemplateResponse(
            request=request,
            name="registration_closed.html",
            context={
                "year": year,
                "call_to_action": "registration",
                "intro_message": "Thank you for your interest in attending PyCon Togo 2025. Registrations are now closed.",
            },
        )
    return template.TemplateResponse(
        request=request,
        name="registration.html",
        context={
            "year": year,
            "event_date": event_date_str,
            "registration_open": False,
        },
    )


@router_2025.post("/register")
def register(request: Request):
    if registration_date > datetime.now(timezone.utc):
        return template.TemplateResponse(
            request=request,
            name="registration.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "registration_open": True,
                "opening_in_days": opening_in_days,
            },
        )

    if datetime.now(timezone.utc) > registration_closing_date:
        return template.TemplateResponse(
            request=request,
            name="registration_closed.html",
            context={
                "year": year,
                "call_to_action": "registration",
                "intro_message": "Thank you for your interest in attending PyCon Togo 2025. Registrations are now closed.",
            },
        )


@router_2025.get("/schedule")
def schedule(request: Request):
    if datetime.now(timezone.utc) < schedule_release_date:
        return RedirectResponse(url="/2025/coming-soon")
    schedule_data = get_schedule()
    speaker_images = get_speaker_images()
    event_info = get_event_info()

    return template.TemplateResponse(
        request=request,
        name="schedule.html",
        context={
            "schedule": schedule_data,
            "speaker_images": speaker_images,
            "event_info": event_info,
            "year": year,
        },
    )


@router_2025.get("/health-safety")
def health_safety(request: Request):

    return template.TemplateResponse(
        request=request,
        name="health-safety.html",
        context={
            "year": year,
        },
    )


@router_2025.post("/volunteer")
def volunteer_post(request: Request):
    return template.TemplateResponse(
        request=request,
        name="call_to_action_close.html",
        context={
            "year": year,
            "call_to_action": "volunteers",
            "intro_message": "Thank you for your interest in volunteering for PyCon Togo 2025. We appreciate your enthusiasm and support!",
        },
    )


@router_2025.get("/volunteer")
def volunteer(request: Request):

    if datetime.now(timezone.utc) > close_volunteer_date:

        return template.TemplateResponse(
            request=request,
            name="call_to_action_close.html",
            context={
                "year": year,
                "call_to_action": "volunteers",
                "intro_message": "Thank you for your interest in volunteering for PyCon Togo 2025. We appreciate your enthusiasm and support!",
            },
        )

    return template.TemplateResponse(
        request=request,
        name="volunteer.html",
        context={
            "year": year,
        },
    )


@router_2025.get("/waitlist")
def waitlist(request: Request):
    return RedirectResponse(url="/2025/register")


@router_2025.get("/speakers")
def speakers(request: Request):
    speaker_release_date = datetime(2025, 7, 10, 16, 0, 0)
    release_speaker_theme_date = datetime(2025, 7, 20, 16, 0, 0)
    speaker_release_date = speaker_release_date.replace(tzinfo=timezone.utc)
    release_speaker_theme_date = release_speaker_theme_date.replace(
        tzinfo=timezone.utc)
    release_speaker_theme = False

    if speaker_release_date > datetime.now(timezone.utc):
        return template.TemplateResponse(
            request=request,
            name="coming-soon.html",
            context={
                "year": year,
                "message": "Speakers will be announced soon!",
                "event_date": event_date_str,
            },
        )

    if datetime.now(timezone.utc) > release_speaker_theme_date:
        release_speaker_theme = True
    return template.TemplateResponse(
        request=request,
        name="speakers.html",
        context={
            "year": year,
            "event_date": event_date_str,
            "speakers": speakers_list,
            "is_themes_released": release_speaker_theme,
        },
    )


@router_2025.get("/proposal")
def proposal(request: Request):
    cfp_opening_in_days = datetime(2025, 6, 2, 16, 0, 0)
    cfp_closing_in_days = datetime(2025, 7, 1, 16, 0, 0)
    cfp_opening_in_days = cfp_opening_in_days.replace(tzinfo=timezone.utc)
    cfp_closing_in_days = cfp_closing_in_days.replace(tzinfo=timezone.utc)

    if cfp_opening_in_days > datetime.now(timezone.utc):
        return template.TemplateResponse(
            request=request,
            name="cfp.html",
            context={
                "year": year,
                "event_date": event_date_str,
                "registration_open": True,
                "opening_in_days": cfp_opening_in_days,
            }
        )
    elif cfp_closing_in_days < datetime.now(timezone.utc):
        return template.TemplateResponse(
            request=request,
            name="call_to_action_close.html",
            context={
                "year": year,
                "call_to_action": "Proposals",
                "intro_message": "Thank you for your interest in speaking at PyCon Togo 2025. The Call for Proposals is now closed.",
            }
        )

    return template.TemplateResponse(
        request=request,
        name="speaker.html",
        context={
            "year": year,
        }
    )


@router_2025.post("/proposal")
def submit_proposal(request: Request):
    return template.TemplateResponse(
        request=request,
        name="call_to_action_close.html",
        context={
            "year": year,
            "call_to_action": "Proposals",
            "intro_message": "Thank you for your interest in speaking at PyCon Togo 2025. The Call for Proposals is now closed.",
        }
    )


@router_2025.get("/sponsor")
def sponsor(request: Request):
    return RedirectResponse(url="/2025/contact")


@router_2025.get("/sponsors")
def sponsors(request: Request):
    return template.TemplateResponse(
        request=request,
        name="sponsors.html",
        context={
            "year": year,
            "gold_sponsors": gold_sponsors,
            "silver_sponsors": silver_sponsors,
            "bronze_sponsors": bronze_sponsors,
            "headline_sponsors": headline_sponsors,
            "inkind_sponsors": inkind_sponsors,
            "community_sponsors": community_sponsors,
            "media_sponsors": media_sponsors,
            "educational_supporters": educational_supporters,
        },
    )


@router_2025.get("/contact")
def contact(request: Request):
    return template.TemplateResponse(
        request=request,
        name="contact.html",
        context={
            "year": year,
            "sponsor_tiers": sponsor_tiers,
        },
    )


@router_2025.get("/about")
def about_us(request: Request):
    return template.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "year": year,
            "sponsor_tiers": sponsor_tiers,
        },
    )


@router_2025.get("/code-of-conduct")
def code_of_conduct(request: Request):
    return template.TemplateResponse(
        request=request,
        name="coc.html",
        context={
            "year": year,
            "sponsor_tiers": sponsor_tiers,
        },
    )


@router_2025.get("/team")
def team(request: Request):
    return template.TemplateResponse(
        request=request,
        name="team.html",
        context={
            "year": year,
            "sponsor_tiers": sponsor_tiers,
        },
    )


@router_2025.get("/feedback")
def feedback(request: Request):
    return template.TemplateResponse(
        request=request,
        name="feedback.html",
        context={
            "year": year,
        },
    )


@router_2025.get("/staff-feedback")
def staff_feedback(request: Request):
    return template.TemplateResponse(
        request=request,
        name="staff_feedback.html",
        context={
            "year": year,
        },
    )
