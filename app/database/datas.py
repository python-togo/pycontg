from app.database.config import supabase
from app.database.migration import create_sponsor_tiers
from app.utils.logger import setup_logger

logger = setup_logger()


swags = [
    {
        "name": "Black PyCon Togo 2025 T-Shirt",
        "description": "Proudly represent the Python Togo community with our official t-shirt. Made from high-quality cotton.",
        "price": 3000,
        "priceDollar": 6,
        "originalPrice": 5000,
        "images": [
            "static/images/swags/unisex-lightweight-t-shirt-black-front-688a5d3c5ed2a.png",
        ],
    },
    {
        "name": "White Python Togo T-Shirt",
        "description": "Proudly represent the Python Togo community with our official t-shirt. Made from high-quality cotton.",
        "price": 3000,
        "priceDollar": 6,
        "originalPrice": 5000,
        "images": [
            "static/images/swags/1pythontogo.png",

            "static/images/swags/tshirt5.png",
        ],
    },
    {
        "name": "Python Togo T-Shirt",
        "description": "Proudly represent the Python Togo community with our official t-shirt. Made from high-quality cotton.",
        "price": 3000,
        "priceDollar": 6,
        "originalPrice": 5000,
        "images": [
            "static/images/swags/2pythontogo.png",

            "static/images/swags/tshirt5.png",
        ],
    },

    {
        "name": "Red Python Togo 2025 T-Shirt",
        "description": "Proudly represent the Python Togo community with our official t-shirt. Made from high-quality cotton.",
        "price": 3000,
        "priceDollar": 6,
        "originalPrice": 5000,
        "images": [
            "static/images/swags/3pythontogo.png",
            "static/images/swags/tshirt1.png",
            "static/images/swags/tshirt2.png",
            "static/images/swags/tshirt3.png",
            "static/images/swags/tshirt6.png",
            "static/images/swags/tshirt7.png",
            "static/images/swags/tshirt4.png",
            "static/images/swags/tshirt5.png",
        ],
    },
    {
        "name": "White PyCon Togo 2025 T-Shirt",
        "description": "Proudly represent the Python Togo community with our official t-shirt. Made from high-quality cotton.",
        "price": 3000,
        "priceDollar": 6,
        "originalPrice": 5000,
        "images": [
            "static/images/swags/unisex-lightweight-t-shirt-white-left-front-688a5d3d9259d.png",
            "static/images/swags/tshirt1.png",
            "static/images/swags/tshirt2.png",
            "static/images/swags/tshirt3.png",
            "static/images/swags/tshirt6.png",
            "static/images/swags/tshirt7.png",
            "static/images/swags/tshirt4.png",
            "static/images/swags/tshirt5.png",
        ],
    },
    {
        "name": "Black Python Togo Hoodie",
        "description": "Stay warm with our Python Togo hoodie. Perfect for coding nights and meetups.",
        "price": 12000,
        "priceDollar": 25,
        "originalPrice": 15000,
        "images": [
            "static/images/swags/hoodie4.png",
            "static/images/swags/hoodie5.png",
            "static/images/swags/hoodie6.png",
        ],
    },
    {
        "name": "Python Togo Travel Mugs & Tumblers",
        "description": "This tumbler boasts a large capacity and an ergonomic handle for a comfortable hold.",
        "price": 14000,
        "priceDollar": 25,
        "originalPrice": 15000,
        "images": [
            "static/images/swags/bottlewater_silver-whitecover.jpg",
            "static/images/swags/bootle2.png",
            "static/images/swags/bootle3.png",
            "static/images/swags/bootle4.png",
        ],
    },
    {
        "name": "Python Togo Stickers",
        "description": "Decorate your laptop, phone, and more with our Python Togo stickers. Durable and waterproof.",
        "price": 1000,
        "priceDollar": 2,
        "originalPrice": 1000,
        "images": [
            "static/images/swags/stickers1.png",
            "static/images/swags/stickers.png",
            "static/images/swags/stickers2.png",
        ],
    },
    {
        "name": "PyCon Togo 2025 Stickers",
        "description": "Decorate your laptop, phone, and more with our PyCon Togo 2025 stickers. Durable and waterproof.",
        "price": 1000,
        "priceDollar": 2,
        "originalPrice": 1000,
        "images": [
            "static/images/swags/kiss-cut-stickers-white-4x4-default-688a608b163f1.png",
            "static/images/swags/stickers.png",
            "static/images/swags/stickers2.png",
        ],
    },
    {
        "name": "PyCon Togo 2025 Stickers",
        "description": "Decorate your laptop, phone, and more with our PyCon Togo 2025 stickers. Durable and waterproof.",
        "price": 1000,
        "priceDollar": 2,
        "originalPrice": 1000,
        "images": [
            "static/images/swags/kiss-cut-stickers-white-4x4-default-688a60dee3beb.png",
            "static/images/swags/stickers.png",
            "static/images/swags/stickers2.png",
        ],
    },
    {
        "name": "Python all over print",
        "description": "This all-over print is a unique and stylish way to show your love for Python.",
        "price": 15000,
        "priceDollar": 30,
        "originalPrice": 20000,
        "images": [
            "static/images/swags/allover3.png",
            "static/images/swags/allover1.png",
            "static/images/swags/allover2.png",
            "static/images/swags/allover4.png",
            "static/images/swags/allover5.png",
            "static/images/swags/allover6.png",
        ],
    },
    {
        "name": "White Python Togo Hoodie",
        "description": "Stay warm with our Python Togo hoodie. Perfect for coding nights and meetups.",
        "price": 12000,
        "priceDollar": 25,
        "originalPrice": 15000,
        "images": [
            "static/images/swags/hoodie8.png",
            "static/images/swags/hoodie2.png",
            "static/images/swags/hoodie.png",
            "static/images/swags/hoodie1.png",
            "static/images/swags/hoodie7.png",
            "static/images/swags/hoodie4.png",
            "static/images/swags/hoodie5.png",
            "static/images/swags/hoodie6.png",
        ],
    },
    {
        "name": "Black PyCon Togo 2025 Cap",
        "description": "Complete your tech look with our exclusive Python Togo cap. Adjustable and comfortable.",
        "price": 3000,
        "priceDollar": 6,
        "originalPrice": 3500,
        "images": [
            "static/images/swags/cap.png",

        ],
    },
    {
        "name": "Python Togo Cap",
        "description": "Complete your tech look with our exclusive Python Togo cap. Adjustable and comfortable.",
        "price": 3000,
        "priceDollar": 6,
        "originalPrice": 3500,
        "images": [
            "static/images/swags/cap7.png",
            "static/images/swags/cap.png",
            "static/images/swags/cap1.png",
            "static/images/swags/cap2.png",
            "static/images/swags/cap3.png",
            "static/images/swags/cap4.png",
            "static/images/swags/cap5.png",
            "static/images/swags/cap6.png",
        ],
    },
    {
        "name": "Red PyCon Togo 2025 Cap",
        "description": "Complete your tech look with our exclusive Red PyCon Togo 2025  cap. Adjustable and comfortable.",
        "price": "SOLD OUT",
        "priceDollar": 6,
        "originalPrice": 3500,
        "images": [
            "static/images/swags/redcap.png",
            "static/images/swags/cap5.png",
            "static/images/swags/cap6.png",
        ],
    }
]


def get_swags():
    return swags


def get_sponsorteirs():
    """
    Fetch all sponsor tiers from the database.
    """
    create_sponsor_tiers()
    response = supabase.table("sponsortiers").select("*").execute()
    data = response.data
    if len(data) == 0:
        logger.info("No sponsor tiers found.")
        return []

    for tier in data:
        tier["amount_cfa"] = int(tier["amount_cfa"])
        tier["amount_usd"] = int(float(tier["amount_usd"]))
        tier["availability"] = int(tier["availability"])

    return data


def get_sponsortirtbytitle(title):
    """
    Fetch a specific sponsor tier by its title.
    """
    create_sponsor_tiers()
    response = supabase.table("sponsortiers").select(
        "*").eq("title", title).execute()
    data = response.data
    if len(data) == 0:
        logger.info(f"No sponsor tier found with title: {title}")
        return None
    data[0]["amount_cfa"] = int(data[0]["amount_cfa"])
    data[0]["amount_usd"] = int(float(data[0]["amount_usd"]))
    data[0]["availability"] = int(data[0]["availability"])

    return data[0]


def get_something_email(table, email):
    """
    Fetch a specific entry by email from a given table.
    """
    response = supabase.table(table).select("*").eq("email", email).execute()
    data = response.data
    if len(data) == 0:
        logger.info(f"No entry found with email: {email}")
        return None
    return data[0]


def get_something_by_field(table, field, value):
    """
    Fetch a specific entry by a given field and value from a specified table.
    """
    response = supabase.table(table).select("*").eq(field, value).execute()
    data = response.data
    if len(data) == 0:
        logger.info(f"No entry found with {field}: {value}")
        return None
    return data


def get_something_by_email_firstname_lastname(table, email, firstname, lastname):
    """
    Fetch a specific entry by email, first name, and last name from a given table.
    """
    response = supabase.table(table).select(
        "*").eq("email", email).eq("firstname", firstname).eq("lastname", lastname).execute()
    data = response.data
    if len(data) == 0:
        logger.info(
            f"No entry found with email: {email}, firstname: {firstname}, lastname: {lastname}")
        return None
    return data[0]


def insert_something(table, data):
    """
    Insert a new entry into a specified table.
    """
    response = supabase.table(table).insert(data).execute()
    if response:
        logger.info("Data inserted successfully.")
        return True
    else:
        logger.error(f"Failed to insert data: {response.error}")
        return False


def update_something(table, email, data):
    """
    Update an entry in a specified table based on email.
    """
    response = supabase.table(table).update(data).eq("email", email).execute()
    if response.status_code == 200:
        logger.info("Data updated successfully.")
        return True
    else:
        logger.error(f"Failed to update data: {response.error}")
        return False


def get_everything(table):
    """
    Get everything in a particular table
    """
    response = supabase.table(table).select("*").execute()
    data = response.data
    if len(data) == 0:
        return {"message": "No entries found"}
    return data


def get_everything_where(table, field, value):
    """
    Get everything in a particular table where a specific field matches a value
    """
    response = supabase.table(table).select("*").eq(field, value).execute()
    data = response.data
    if len(data) == 0:
        return {"message": "No entries found"}
    return data


if __name__ == "__main__":
    tiers = get_sponsorteirs()
    logger.info(tiers)
