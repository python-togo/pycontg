import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse


router = APIRouter(tags=["2024"])


@router.get("/")
async def get_2024(request: Request):
    """
    Endpoint to handle GET requests for the 2024 route.
    """
    try:

        return RedirectResponse(url="https://luma.com/runpiv8k?tk=YxGTaU", status_code=302)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error: Unable to process the request.") from e
