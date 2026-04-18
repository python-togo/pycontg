from app.schemas.models import SponsorTier
from app.database.config import supabase
from app.utils.logger import setup_logger


logger = setup_logger()

community_supporter = SponsorTier(
    name="Community Supporter",
    title="community",
    availability=255,
    available=255,
    amount_cfa=50000,
    amount_usd=85,
    advantages=[
        "Logo on website",
        "Mention during opening ceremony",
        "Social media recognition",
    ],
)

bronze_sponsor = SponsorTier(
    name="Bronze Sponsor",
    title="bronze",
    availability=10,
    available=10,
    amount_cfa=150000,
    amount_usd=255,
    advantages=[
        "Logo on website and printed materials",
        "Mention during opening ceremony",
        "Social media recognition",
        "Distribution of company materials",
    ],
)


silver_sponsor = SponsorTier(
    name="Silver Sponsor",
    title="silver",
    availability=5,
    available=5,
    amount_cfa=300000,
    amount_usd=500,
    advantages=[
        "Logo on website and printed materials",
        "Mention during opening ceremony",
        "Enhanced social media recognition",
        "Distribution of company materials",
        "Banner placement at venue",
        "Brief company introduction (2 min)",
    ],
)

gold_sponsor = SponsorTier(
    name="Gold Sponsor",
    title="gold",
    availability=3,
    available=3,
    amount_cfa=600000,
    amount_usd=1000,
    advantages=[
        "Premium logo placement on all materials",
        "Special recognition during ceremonies",
        "Comprehensive social media campaign",
        "Small exhibit space",
        "Multiple banner placements",
        "3-minute speaking opportunity",
    ],
)


headline_sponsor = SponsorTier(
    name="Headline Sponsor",
    title="headline",
    availability=2,
    available=2,
    amount_cfa=1000000,
    amount_usd=1680,
    advantages=[
        'Event naming rights: "PyCon Togo 2025 powered by [Your Company]"',
        "Prominent logo placement on all conference materials and website",
        "Dedicated social media campaign highlighting your support",
        "Premium exhibit space at the venue entrance",
        "Opening keynote opportunity (10 minutes)",
        "Four banners placed strategically throughout the venue",
        "Opportunity to distribute branded items to all attendees",
        "First access to recruitment opportunities with participants",
    ],
)


in_kind_sponsor = SponsorTier(
    name="In-Kind Sponsor",
    title="inkind",
    availability=255,
    available=255,
    amount_cfa=0,
    amount_usd=0,
    advantages=[
        "Recognition on website and conference materials",
        "Social media recognition",
        "Mention during opening ceremony",
        "Custom benefits based on contribution value",
    ],
)


def create_sponsor_tiers():
    existing_tiers = supabase.table("sponsortiers").select("*").execute()
    if existing_tiers.data:
        logger.info("Sponsor tiers already exist. Skipping creation.")
        return

    sponsor_tiers = [
        community_supporter,
        bronze_sponsor,
        silver_sponsor,
        gold_sponsor,
        headline_sponsor,
        in_kind_sponsor,
    ]

    for tier in sponsor_tiers:
        supabase.table("sponsortiers").insert(tier.dict()).execute()
        logger.info(tier)
    logger.info("Sponsor tiers created successfully.")


if __name__ == "__main__":
    # create_sponsor_tiers()
    pass
