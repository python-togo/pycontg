import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["2027"])

templates = Jinja2Templates(directory="app/templates/2027")


@router.get("/", response_class=HTMLResponse)
async def get_2027(request: Request):
    """
    Endpoint to handle GET requests for the 2027 route.
    """
    try:
        return templates.TemplateResponse("home.html", {"request": request})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error: Unable to process the request.") from e
