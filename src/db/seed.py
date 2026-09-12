from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import ContentLane

SEED_LANES = [
    {
        "id": "lane_homepage_categories",
        "title": "Explore by Category",
        "subtitle": "Single origin estate roasts, espresso machines, and precision barista gear",
        "slug": "explore-by-category",
        "lane_type": "category_lane",
        "placement": "homepage",
        "card_style": "circular",
        "has_navigation_arrows": True,
        "status": "active",
        "sort_order": 1,
        "items": [
            {
                "id": "cat_roasted_coffee",
                "product_id": None,
                "title": "Roasted & Ground Coffee",
                "subtitle": "Fresh roasted single origins & blends",
                "image_url": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=300&h=300&fit=crop&q=80",
                "target_url": "#/coffees",
                "badge": None,
                "price": None,
                "sort_order": 0,
            },
            {
                "id": "cat_espresso_machines",
                "product_id": None,
                "title": "Espresso Machines",
                "subtitle": "Prosumer & compact espresso makers",
                "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=300&h=300&fit=crop&q=80",
                "target_url": "#/equipment",
                "badge": "Popular",
                "price": None,
                "sort_order": 1,
            },
            {
                "id": "cat_brewing_gear",
                "product_id": None,
                "title": "Brewing Equipment",
                "subtitle": "Pour-over, aeropress & cold brew",
                "image_url": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=300&h=300&fit=crop&q=80",
                "target_url": "#/equipment",
                "badge": None,
                "price": None,
                "sort_order": 2,
            },
            {
                "id": "cat_grinders",
                "product_id": None,
                "title": "Burr Grinders",
                "subtitle": "Precision flat & conical burrs",
                "image_url": "https://images.unsplash.com/photo-1589396575653-c09c794ff6a6?w=300&h=300&fit=crop&q=80",
                "target_url": "#/equipment",
                "badge": None,
                "price": None,
                "sort_order": 3,
            },
            {
                "id": "cat_drinkware",
                "product_id": None,
                "title": "Barista Drinkware",
                "subtitle": "Ceramic cups & insulated tumblers",
                "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=300&h=300&fit=crop&q=80",
                "target_url": "#/equipment",
                "badge": None,
                "price": None,
                "sort_order": 4,
            },
            {
                "id": "cat_roast_subscriptions",
                "product_id": None,
                "title": "Roast Subscriptions",
                "subtitle": "Fortnightly doorstep delivery",
                "image_url": "https://images.unsplash.com/photo-1610632380989-680fe40816c6?w=300&h=300&fit=crop&q=80",
                "target_url": "#/subscriptions",
                "badge": "Save 15%",
                "price": None,
                "sort_order": 5,
            },
        ],
    },
    {
        "id": "lane_homepage_bestsellers",
        "title": "Bestseller Coffees",
        "subtitle": "Freshly roasted specialty coffee beans and cold brew drops from India's premier estates",
        "slug": "bestseller-coffees",
        "lane_type": "product_lane",
        "placement": "homepage",
        "card_style": "circular",
        "has_navigation_arrows": True,
        "status": "active",
        "sort_order": 2,
        "items": [
            {
                "id": "prod_baarbara_whiskey",
                "product_id": "prod_breville_barista_touch",
                "title": "BAARBARA ESTATE - WHISKEY BARREL AGED",
                "subtitle": "Ripe banana, Red Plum, Whiskey Oak, Brown Sugar",
                "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&h=600&fit=crop&q=80",
                "target_url": "#/product/prod_breville_barista_touch",
                "badge": None,
                "price": "₹ 1,250",
                "sort_order": 0,
            },
            {
                "id": "prod_elkhill_estates",
                "product_id": "prod_fellow_ode_gen2",
                "title": "ELKHILL ESTATES",
                "subtitle": "Orange, Brown Spice, Roasted Hazelnut, Milk Chocolate",
                "image_url": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=600&h=600&fit=crop&q=80",
                "target_url": "#/product/prod_fellow_ode_gen2",
                "badge": None,
                "price": "₹ 800",
                "sort_order": 1,
            },
            {
                "id": "prod_sea_salt_mocha",
                "product_id": "prod_breville_barista_touch",
                "title": "SEA SALT MOCHA DROP | CONCENTRATE",
                "subtitle": "Specialty Coffee Concentrate ready to stir & sip",
                "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=600&h=600&fit=crop&q=80",
                "target_url": "#/product/prod_breville_barista_touch",
                "badge": "NEW",
                "price": "₹ 250",
                "sort_order": 2,
            },
            {
                "id": "prod_vienna_dark_roast",
                "product_id": "prod_acaia_lunar",
                "title": "VIENNA | DARK ROAST - EASY POUR",
                "subtitle": "Blue Tokai Coffee Easy Pour Box • 5 Single Sachets",
                "image_url": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=600&h=600&fit=crop&q=80",
                "target_url": "#/product/prod_acaia_lunar",
                "badge": None,
                "price": "₹ 300",
                "sort_order": 3,
            },
            {
                "id": "prod_attikan_estate",
                "product_id": "prod_fellow_ode_gen2",
                "title": "ATTIKAN ESTATE - ESPRESSO ROAST",
                "subtitle": "Dark Chocolate, Figs, Roasted Almonds",
                "image_url": "https://images.unsplash.com/photo-1589396575653-c09c794ff6a6?w=600&h=600&fit=crop&q=80",
                "target_url": "#/product/prod_fellow_ode_gen2",
                "badge": None,
                "price": "₹ 550",
                "sort_order": 4,
            },
        ],
    },
]


async def seed_content_lanes(db: AsyncSession):
    for lane_data in SEED_LANES:
        res = await db.execute(select(ContentLane).where(ContentLane.id == lane_data["id"]))
        existing = res.scalar_one_or_none()
        if not existing:
            lane = ContentLane(**lane_data)
            db.add(lane)
    await db.commit()


if __name__ == "__main__":
    import asyncio
    from src.db.database import get_db

    async def main():
        async for session in get_db():
            await seed_content_lanes(session)
            print("Successfully seeded content lanes into PostgreSQL!")
            break

    asyncio.run(main())

