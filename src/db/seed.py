from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import ContentLane, CMSPage, CMSSiteShell, CMSThemePreset

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
                "target_url": "/coffees",
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
                "target_url": "/equipment",
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
                "target_url": "/equipment",
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
                "target_url": "/equipment",
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
                "target_url": "/equipment",
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
                "target_url": "/subscriptions",
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
                "target_url": "/product/prod_breville_barista_touch",
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
                "target_url": "/product/prod_fellow_ode_gen2",
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
                "target_url": "/product/prod_breville_barista_touch",
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
                "target_url": "/product/prod_acaia_lunar",
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
                "target_url": "/product/prod_fellow_ode_gen2",
                "badge": None,
                "price": "₹ 550",
                "sort_order": 4,
            },
        ],
    },
]


DEFAULT_GLOBAL_SHELL = {
    "promo_bar": {
        "enabled": True,
        "text": "Complimentary express delivery on whole bean harvest orders over $50 · Small-batch roasted daily",
        "cta_text": "Explore Fresh Roasts",
        "cta_url": "/coffees",
        "theme": "amber",
        "badge": "FRESH HARVEST",
        "dismissible": True,
    },
    "header": {
        "brand_name": "Hiljhil Roasters",
        "brand_tagline": "Specialty Sourced & Micro-Lot Roasted",
        "brand_badge": "FLAGSHIP ROASTERY",
        "logo_url": "/logo.jpg",
        "show_search": True,
        "show_cart": True,
        "show_spatial_finder": True,
        "sticky": True,
        "nodes": [
            {
                "id": "nav_coffees",
                "label": "Whole Bean Coffees",
                "url": "/coffees",
                "badge": "FRESH",
                "children": [
                    {
                        "id": "nav_single_origin",
                        "label": "Single Origin Lots",
                        "url": "/coffees?category=single_origin",
                    },
                    {
                        "id": "nav_producer_series",
                        "label": "Producer Series Nano-Lots",
                        "url": "/coffees?category=producer_series",
                        "badge": "EXCLUSIVE",
                    },
                    {
                        "id": "nav_espresso_blends",
                        "label": "House & Espresso Blends",
                        "url": "/coffees?category=espresso_blend",
                    },
                    {
                        "id": "nav_decaf",
                        "label": "Mountain Water Decaf",
                        "url": "/coffees?category=decaf",
                    },
                ],
            },
            {
                "id": "nav_equipment",
                "label": "Espresso & Brewing Gear",
                "url": "/equipment",
                "children": [
                    {
                        "id": "nav_machines",
                        "label": "Espresso Machines",
                        "url": "/equipment?category=espresso_machine",
                    },
                    {
                        "id": "nav_grinders",
                        "label": "Precision Burr Grinders",
                        "url": "/equipment?category=grinder",
                    },
                    {
                        "id": "nav_accessories",
                        "label": "Barista Tools & Drinkware",
                        "url": "/equipment?category=accessories",
                    },
                ],
            },
            {
                "id": "nav_discovery",
                "label": "Discovery (CounterCheck™)",
                "url": "/discovery",
                "badge": "SPATIAL 3D",
            },
            {
                "id": "nav_subscriptions",
                "label": "Roast Subscriptions",
                "url": "/subscriptions",
                "badge": "SAVE 15%",
            },
            {
                "id": "nav_cafes",
                "label": "Roasteries & Cafes",
                "url": "/cafes",
            },
            {
                "id": "nav_about",
                "label": "Our Story",
                "url": "/about",
            },
        ],
    },
    "footer": {
        "brand_name": "HILJHIL ROASTERS",
        "brand_description": "Artisan specialty coffee roasters dedicated to direct trade sourcing, anaerobic fermentation nano-lots, and precision-engineered brewing equipment.",
        "show_newsletter": True,
        "newsletter_title": "Join the Roasters Circle",
        "newsletter_placeholder": "Enter your email for private lot access & brew recipes...",
        "columns": [
            {
                "id": "col_shop",
                "title": "Shop Experience",
                "links": [
                    {"label": "Whole Bean Coffees", "url": "/coffees"},
                    {"label": "Espresso Machines", "url": "/equipment?category=espresso_machine"},
                    {"label": "Precision Grinders", "url": "/equipment?category=grinder"},
                    {"label": "Roast Subscriptions", "url": "/subscriptions"},
                    {"label": "Barista Drinkware", "url": "/equipment"},
                ],
            },
            {
                "id": "col_roastery",
                "title": "Roastery & Craft",
                "links": [
                    {"label": "Sourcing Philosophy", "url": "/about"},
                    {"label": "Anaerobic Fermentation", "url": "/about"},
                    {"label": "Direct Trade Transparency", "url": "/about"},
                    {"label": "CounterCheck™ Clearance Guarantee", "url": "/discovery"},
                ],
            },
            {
                "id": "col_guides",
                "title": "Learn & Brew",
                "links": [
                    {"label": "Espresso Extraction Guide", "url": "/about"},
                    {"label": "V60 & Chemex Ratio Calculator", "url": "/about"},
                    {"label": "Water Mineralization Science", "url": "/about"},
                    {"label": "Roast Schedule & Freshness", "url": "/coffees"},
                ],
            },
            {
                "id": "col_support",
                "title": "Customer Care & Legal",
                "links": [
                    {"label": "Orders & Express Shipping", "url": "/about"},
                    {"label": "3-Year Equipment Warranty", "url": "/about"},
                    {"label": "Privacy Policy", "url": "/privacy"},
                    {"label": "Terms of Service", "url": "/terms"},
                ],
            },
        ],
        "social_links": [
            {"platform": "Instagram", "url": "https://instagram.com"},
            {"platform": "YouTube", "url": "https://youtube.com"},
            {"platform": "X / Twitter", "url": "https://x.com"},
        ],
        "copyright": "© 2026 Hiljhil Roasters Co. All rights reserved. Precision-crafted for specialty coffee devotees.",
    },
    "theme": {
        "id": "theme_hill_jhil_alpine",
        "name": "Hill Jhil Alpine Tarn",
        "preset": "alpine",
        "mode": "light",
        "primary_color": "#085454",
        "accent_color": "#0d9488",
        "surface_color": "#ffffff",
        "background_color": "#f0fdfa",
        "text_color": "#042f2e",
        "font_family": "serif",
        "border_radius": "rounded-2xl",
        "badge_text": "ALPINE ESTATE HARVEST",
        "is_active": True,
    },
}

DEFAULT_THEME_PRESETS_LIST = [
    {
        "id": "theme_hill_jhil_alpine",
        "name": "Hill Jhil Alpine Tarn",
        "preset": "alpine",
        "mode": "light",
        "primary_color": "#085454",
        "accent_color": "#0d9488",
        "surface_color": "#ffffff",
        "background_color": "#f0fdfa",
        "text_color": "#042f2e",
        "font_family": "serif",
        "border_radius": "rounded-2xl",
        "badge_text": "ALPINE ESTATE HARVEST",
        "is_active": True,
        "sort_order": 1,
    },
    {
        "id": "theme_warm_amber",
        "name": "Warm Amber Roast",
        "preset": "amber",
        "mode": "light",
        "primary_color": "#92400e",
        "accent_color": "#f59e0b",
        "surface_color": "#ffffff",
        "background_color": "#fbf9f6",
        "text_color": "#1c1917",
        "font_family": "serif",
        "border_radius": "rounded-2xl",
        "badge_text": "FLAGSHIP HARVEST",
        "is_active": False,
        "sort_order": 2,
    },
    {
        "id": "theme_midnight_espresso",
        "name": "Midnight Espresso",
        "preset": "espresso",
        "mode": "dark",
        "primary_color": "#1c1917",
        "accent_color": "#d97706",
        "surface_color": "#18181b",
        "background_color": "#09090b",
        "text_color": "#f4f4f5",
        "font_family": "sans",
        "border_radius": "rounded-xl",
        "badge_text": "BARISTA NIGHTS",
        "is_active": False,
        "sort_order": 3,
    },
    {
        "id": "theme_highland_emerald",
        "name": "Highland Emerald",
        "preset": "emerald",
        "mode": "light",
        "primary_color": "#064e3b",
        "accent_color": "#10b981",
        "surface_color": "#ffffff",
        "background_color": "#f0fdf4",
        "text_color": "#064e3b",
        "font_family": "sans",
        "border_radius": "rounded-2xl",
        "badge_text": "ESTATE ORIGINS",
        "is_active": False,
        "sort_order": 4,
    },
    {
        "id": "theme_berry_crimson",
        "name": "Berry Crimson Velvet",
        "preset": "crimson",
        "mode": "light",
        "primary_color": "#881337",
        "accent_color": "#f43f5e",
        "surface_color": "#ffffff",
        "background_color": "#fff1f2",
        "text_color": "#4c0519",
        "font_family": "serif",
        "border_radius": "rounded-2xl",
        "badge_text": "LIMITED NANO-LOT",
        "is_active": False,
        "sort_order": 5,
    },
    {
        "id": "theme_modern_slate",
        "name": "Modern Minimal Slate",
        "preset": "slate",
        "mode": "light",
        "primary_color": "#0f172a",
        "accent_color": "#64748b",
        "surface_color": "#ffffff",
        "background_color": "#f8fafc",
        "text_color": "#0f172a",
        "font_family": "sans",
        "border_radius": "rounded-lg",
        "badge_text": "PRECISION LAB",
        "is_active": False,
        "sort_order": 6,
    },
]

DEFAULT_CMS_PAGES = [
    {
        "id": "page_home",
        "page_type": "home",
        "title": "Hill Jhil Homepage",
        "slug": "/",
        "description": "Main flagship landing experience featuring hero banner, origin lanes, and spatial discovery.",
        "is_published": True,
        "sections": [
            {
                "id": "sec_home_hero",
                "type": "hero_banner",
                "title": "Flagship Roastery Hero Banner",
                "subtitle": "Primary high-impact hero introducing autumn reserve micro-lots",
                "is_active": True,
                "sort_order": 1,
                "config": {
                    "headline": "Rare Harvests. Uncompromising Extraction.",
                    "subheadline": "Direct-trade micro-lots roasted with scientific precision and paired with CounterCheck™ space-fit verified espresso gear.",
                    "badge": "AUTUMN 2026 RESERVE",
                    "primary_cta_text": "Explore Fresh Harvests",
                    "primary_cta_url": "/coffees",
                    "secondary_cta_text": "CounterCheck™ Spatial Finder",
                    "secondary_cta_url": "/discovery",
                    "background_image": "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=1600&auto=format&fit=crop&q=85",
                    "overlay_opacity": 65,
                    "text_align": "center",
                },
            },
            {
                "id": "sec_home_category_lane",
                "type": "category_lane",
                "title": "Curated Origin & Gear Collections",
                "subtitle": "Circular origin discovery rail",
                "is_active": True,
                "sort_order": 2,
                "config": {
                    "card_style": "circular",
                    "has_navigation_arrows": True,
                    "categories": [
                        {
                            "id": "cat_coffee",
                            "title": "Roasted Coffee",
                            "image_url": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=300&h=300&fit=crop&q=80",
                            "url": "/coffees",
                            "badge": "FRESH ROAST",
                        },
                        {
                            "id": "cat_espresso",
                            "title": "Espresso Machines",
                            "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=300&h=300&fit=crop&q=80",
                            "url": "/equipment",
                            "badge": "POPULAR",
                        },
                        {
                            "id": "cat_brewing",
                            "title": "Brewing Equipment",
                            "image_url": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=300&h=300&fit=crop&q=80",
                            "url": "/equipment",
                        },
                        {
                            "id": "cat_grinders",
                            "title": "Burr Grinders",
                            "image_url": "https://images.unsplash.com/photo-1589396575653-c09c794ff6a6?w=300&h=300&fit=crop&q=80",
                            "url": "/equipment",
                        },
                        {
                            "id": "cat_drinkware",
                            "title": "Barista Drinkware",
                            "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=300&h=300&fit=crop&q=80",
                            "url": "/equipment",
                        },
                        {
                            "id": "cat_subs",
                            "title": "Roast Subscriptions",
                            "image_url": "https://images.unsplash.com/photo-1610632380989-680fe40816c6?w=300&h=300&fit=crop&q=80",
                            "url": "/subscriptions",
                            "badge": "SAVE 15%",
                        },
                    ],
                },
            },
            {
                "id": "sec_home_product_lane",
                "type": "product_lane",
                "title": "Featured Roaster Harvests",
                "subtitle": "Direct trade anaerobic lots and competition roast profiles",
                "is_active": True,
                "sort_order": 3,
                "config": {
                    "filter_badge": "NANO LOT",
                    "card_style": "slider",
                    "limit": 6,
                },
            },
            {
                "id": "sec_home_promo_callout",
                "type": "promo_callout",
                "title": "CounterCheck™ Guarantee Highlight",
                "subtitle": "Spatial dimension fitment guarantee callout",
                "is_active": True,
                "sort_order": 4,
                "config": {
                    "headline": "Guaranteed Kitchen Fit Before You Buy",
                    "body": "Never return an espresso machine that does not clear your kitchen cabinets. CounterCheck™ calculates machine height, top water-reservoir clearance, and portafilter swing radius in real-time.",
                    "badge": "PATENTED SPATIAL TECH",
                    "button_text": "Launch CounterCheck™ Finder",
                    "button_url": "/discovery",
                    "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&auto=format&fit=crop&q=80",
                    "layout": "image_right",
                },
            },
            {
                "id": "sec_home_product_grid",
                "type": "product_grid",
                "title": "Verified Bestsellers & Espresso Gear",
                "subtitle": "Flagship equipment with 3-year roastery warranty and complimentary dial-in session",
                "is_active": True,
                "sort_order": 5,
                "config": {
                    "columns": 3,
                    "limit": 6,
                    "show_quick_add": True,
                },
            },
            {
                "id": "sec_home_testimonials",
                "type": "testimonials",
                "title": "Devotee Reviews & Barista Feedback",
                "subtitle": "What coffee champions and home baristas say about our roasts",
                "is_active": True,
                "sort_order": 6,
                "config": {
                    "testimonials": [
                        {
                            "id": "test_1",
                            "author": "Elena Rostova",
                            "role": "National Barista Finalist 2025",
                            "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
                            "rating": 5,
                            "quote": "The Mooleh Manay Excelsa is a revelation. The carbonic maceration preserves vibrant berry acidity while delivering deep body and delicate floral jasmine aromatics.",
                            "verified_purchase": True,
                        },
                        {
                            "id": "test_2",
                            "author": "Marcus Vance",
                            "role": "Home Barista Devotee",
                            "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
                            "rating": 5,
                            "quote": "CounterCheck™ saved me from purchasing an espresso machine that would have hit my under-cabinet lighting. The machine fit with millimeter accuracy, and the coffee is world-class.",
                            "verified_purchase": True,
                        },
                        {
                            "id": "test_3",
                            "author": "Dr. Sarah Lin",
                            "role": "Specialty Coffee Roaster",
                            "avatar_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&auto=format&fit=crop&q=80",
                            "rating": 5,
                            "quote": "Hiljhil sets the bar for ethical sourcing in specialty coffee. Transparent farm pricing, zero defects, and roast consistency that never falters across seasonal harvests.",
                            "verified_purchase": True,
                        },
                    ],
                },
            },
        ],
    },
    {
        "id": "page_collection_coffees",
        "page_type": "collection",
        "title": "Whole Bean Coffees Collection (PLP)",
        "slug": "/coffees",
        "description": "Category listing page for single origins, espresso blends, and seasonal harvest releases.",
        "is_published": True,
        "sections": [
            {
                "id": "sec_coll_hero",
                "type": "hero_banner",
                "title": "Coffees Collection Banner",
                "subtitle": "Collection header banner for coffees",
                "is_active": True,
                "sort_order": 1,
                "config": {
                    "headline": "Single Origin & Producer Series Harvests",
                    "subheadline": "From the high-altitude volcanic soils of Guji to the mist-shrouded hills of Coorg. Direct trade, single-farm traceability.",
                    "badge": "CROP HARVEST 2026",
                    "primary_cta_text": "Shop All Beans",
                    "primary_cta_url": "/coffees",
                    "background_image": "https://images.unsplash.com/photo-1587734195503-904fca47e0e9?w=1600&auto=format&fit=crop&q=80",
                    "overlay_opacity": 60,
                    "text_align": "left",
                },
            },
            {
                "id": "sec_coll_grid",
                "type": "category_grid",
                "title": "Explore by Roast Profile",
                "subtitle": "Choose your ideal flavor profile",
                "is_active": True,
                "sort_order": 2,
                "config": {
                    "columns": 4,
                    "categories": [
                        {
                            "id": "cat_light",
                            "title": "Light-Medium Terroir Roasts",
                            "image_url": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400&h=300&fit=crop&q=80",
                            "url": "/coffees?roast=light",
                            "badge": "FLORAL & BRIGHT",
                        },
                        {
                            "id": "cat_medium",
                            "title": "House & Balanced Roasts",
                            "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=400&h=300&fit=crop&q=80",
                            "url": "/coffees?roast=medium",
                            "badge": "CHOCOLATE & CARAMEL",
                        },
                        {
                            "id": "cat_anaerobic",
                            "title": "Anaerobic Nano-Lots",
                            "image_url": "https://images.unsplash.com/photo-1610632380989-680fe40816c6?w=400&h=300&fit=crop&q=80",
                            "url": "/coffees?process=anaerobic",
                            "badge": "WINE & TROPICAL",
                        },
                        {
                            "id": "cat_decaf",
                            "title": "Mountain Water Decaf",
                            "image_url": "https://images.unsplash.com/photo-1587734195503-904fca47e0e9?w=400&h=300&fit=crop&q=80",
                            "url": "/coffees?category=decaf",
                            "badge": "CHEMICAL FREE",
                        },
                    ],
                },
            },
            {
                "id": "sec_coll_products",
                "type": "product_grid",
                "title": "All Active Coffee Offerings",
                "subtitle": "Full ground-truth coffee beans from catalog",
                "is_active": True,
                "sort_order": 3,
                "config": {
                    "columns": 3,
                    "filter_category": "coffee_beans",
                    "limit": 12,
                    "show_quick_add": True,
                },
            },
        ],
    },
    {
        "id": "page_product_default",
        "page_type": "product",
        "title": "Product Detail Page (PDP)",
        "slug": "/products/:id",
        "description": "Universal product page layout template automatically rendered across all catalog items (espresso gear, whole bean coffees, accessories).",
        "is_published": True,
        "sections": [
            {
                "id": "sec_pdp_overview",
                "type": "product_lane",
                "title": "Product Media Showcase & Specs",
                "subtitle": "High-res media carousel, buy box, and CounterCheck™ clearance metrics",
                "is_active": True,
                "sort_order": 1,
                "config": {
                    "card_style": "slider",
                    "display_count": 4,
                    "show_badges": True,
                    "enable_quick_add": True,
                },
            },
            {
                "id": "sec_pdp_pairing",
                "type": "product_lane",
                "title": "Recommended Roaster Pairings",
                "subtitle": "Fresh whole bean lots and precision companion tools",
                "is_active": True,
                "sort_order": 2,
                "config": {
                    "filter_category": "coffee_beans",
                    "card_style": "slider",
                    "limit": 4,
                },
            },
            {
                "id": "sec_pdp_reviews",
                "type": "testimonials",
                "title": "Devotee Extraction Reviews",
                "subtitle": "Grind calibration notes and home barista feedback",
                "is_active": True,
                "sort_order": 3,
                "config": {
                    "testimonials": [
                        {
                            "id": "pdp_test_1",
                            "author": "Marcus V.",
                            "role": "Verified Home Barista",
                            "rating": 5,
                            "quote": "Extremely consistent extraction with zero channeling. The spatial tolerance matched my kitchen cabinet height exactly.",
                        }
                    ]
                },
            },
        ],
    },
    {
        "id": "page_discovery",
        "page_type": "discovery",
        "title": "CounterCheck™ Spatial Fitment Discovery",
        "slug": "/discovery",
        "description": "Spatial dimension verification workbench and under-cabinet clearance finder.",
        "is_published": True,
        "sections": [
            {
                "id": "sec_disc_hero",
                "type": "hero_banner",
                "title": "Discovery Experience Hero",
                "subtitle": "Dimensional clearance hero",
                "is_active": True,
                "sort_order": 1,
                "config": {
                    "headline": "Precision Spatial Clearance Engine",
                    "subheadline": "Measure your kitchen counter space once. Discover premium espresso gear guaranteed to fit under your cabinets with full reservoir access.",
                    "badge": "PATENTED FITMENT TECH",
                    "primary_cta_text": "Enter Kitchen Dimensions",
                    "primary_cta_url": "/discovery",
                    "background_image": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=1600&auto=format&fit=crop&q=85",
                    "overlay_opacity": 70,
                    "text_align": "center",
                },
            },
            {
                "id": "sec_disc_lane",
                "type": "product_lane",
                "title": "CounterCheck™ Verified Slim Machines",
                "subtitle": "Under 35cm total height for tight overhead cabinets",
                "is_active": True,
                "sort_order": 2,
                "config": {
                    "filter_category": "espresso_machine",
                    "card_style": "slider",
                    "limit": 6,
                },
            },
            {
                "id": "sec_disc_callout",
                "type": "promo_callout",
                "title": "How CounterCheck™ Spatial Verification Works",
                "subtitle": "3-point measurement explanation",
                "is_active": True,
                "sort_order": 3,
                "config": {
                    "headline": "3-Point Counter Clearance Guarantee",
                    "body": "Every machine in our catalog has been 3D scanned in our roastery test lab. We measure operational clearances for top hopper lids, side steam wand reach, and front portafilter insertion.",
                    "badge": "VERIFIED TOLERANCE",
                    "button_text": "Read Fitment Whitepaper",
                    "button_url": "/about",
                    "image_url": "https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=800&auto=format&fit=crop&q=80",
                    "layout": "image_left",
                },
            },
        ],
    },
    {
        "id": "page_about",
        "page_type": "static",
        "title": "About Hiljhil Roasters & Philosophy",
        "slug": "/about",
        "description": "Our sourcing transparency, roasting manifesto, and engineering standards.",
        "is_published": True,
        "sections": [
            {
                "id": "sec_about_hero",
                "type": "hero_banner",
                "title": "Story Hero Banner",
                "subtitle": "Introduction to roasting manifesto",
                "is_active": True,
                "sort_order": 1,
                "config": {
                    "headline": "Sourcing with Integrity. Roasting with Science.",
                    "subheadline": "Founded by coffee obsessives and precision engineers, Hiljhil bridges experimental agricultural fermentation with uncompromising home extraction.",
                    "badge": "ROASTERY MANIFESTO",
                    "primary_cta_text": "Explore Harvest Lots",
                    "primary_cta_url": "/coffees",
                    "background_image": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=1600&auto=format&fit=crop&q=80",
                    "overlay_opacity": 65,
                    "text_align": "center",
                },
            },
            {
                "id": "sec_about_callout_1",
                "type": "promo_callout",
                "title": "Direct Trade Promise",
                "subtitle": "Sourcing ethics",
                "is_active": True,
                "sort_order": 2,
                "config": {
                    "headline": "Direct Farm Transparency",
                    "body": "We reject commoditized coffee supply chains. We partner directly with estate owners in Karnataka and Oromia, financing raised drying beds and anaerobic fermentation tanks.",
                    "badge": "FARM DIRECT",
                    "button_text": "View Estate Harvests",
                    "button_url": "/coffees",
                    "image_url": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800&auto=format&fit=crop&q=80",
                    "layout": "image_right",
                },
            },
            {
                "id": "sec_about_testimonials",
                "type": "testimonials",
                "title": "Industry Accolades & Roaster Recognition",
                "subtitle": "Celebrated by international coffee judges",
                "is_active": True,
                "sort_order": 3,
                "config": {
                    "testimonials": [
                        {
                            "id": "accolade_1",
                            "author": "Specialty Coffee Guild 2025",
                            "role": "Award for Fermentation Innovation",
                            "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
                            "rating": 5,
                            "quote": "Hiljhil demonstrates what happens when scientific rigor meets artisanal micro-lot farming. The flavor clarity is unmatched.",
                            "verified_purchase": True,
                        },
                    ],
                },
            },
            {
                "id": "sec_about_pillars",
                "type": "feature_grid",
                "title": "Our Heritage Pillars",
                "subtitle": "Direct trade, precision small-batch roasting, and welcoming community",
                "is_active": True,
                "sort_order": 4,
                "config": {
                    "columns": 3,
                    "items": [
                        {
                            "id": "pillar_direct_trade",
                            "title": "100% Direct Trade",
                            "description": "Zero middlemen. We work side-by-side with farmers at origin, sharing cupping feedback and funding post-harvest processing experiments.",
                            "badge": "ETHICAL SOURCING",
                        },
                        {
                            "id": "pillar_roasting",
                            "title": "Small-Batch Roasting",
                            "description": "Every estate lot has its own signature roast curve designed to bring out intrinsic terroir notes of fruit, chocolate, and spices.",
                            "badge": "CRAFT ROAST",
                        },
                        {
                            "id": "pillar_community",
                            "title": "Community & Craft",
                            "description": "From free home barista masterclasses to sensory cuppings, our mission is to make specialty coffee welcoming, approachable, and fun.",
                            "badge": "COMMUNITY FIRST",
                        },
                    ],
                },
            },
        ],
    },
    {
        "id": "page_cafes",
        "page_type": "static",
        "title": "Visit Our Cafes & Espresso Bars",
        "slug": "/cafes",
        "description": "Step into our spaces designed for the love of coffee. Precision espresso, pour-overs, and sensory cuppings.",
        "is_published": True,
        "sections": [
            {
                "id": "sec_cafes_hero",
                "type": "hero_banner",
                "title": "Cafe Experience Hero",
                "subtitle": "Introduction to our flagships",
                "is_active": True,
                "sort_order": 1,
                "config": {
                    "headline": "Visit Our Cafes & Roasteries",
                    "subheadline": "Step into spaces designed for the love of craft coffee. From manual pour-overs to single-origin cold brews and fresh bakery pairings.",
                    "badge": "THE CAFE EXPERIENCE",
                    "primary_cta_text": "Find Nearest Cafe",
                    "primary_cta_url": "#sec_cafes_list",
                    "background_image": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1600&auto=format&fit=crop&q=80",
                    "overlay_opacity": 60,
                    "text_align": "center",
                },
            },
            {
                "id": "sec_cafes_list",
                "type": "feature_grid",
                "title": "Flagship Cafes & Espresso Bars",
                "subtitle": "Explore our roasting flagships and neighborhood espresso bars across India",
                "is_active": True,
                "sort_order": 2,
                "config": {
                    "columns": 2,
                    "items": [
                        {
                            "id": "highland-flagship",
                            "title": "Highland District Flagship & Roastery",
                            "subtitle": "Bangalore, 560038",
                            "description": "104 Roasters Lane, Highland District • Open Daily: 7:00 AM – 9:00 PM • +91 (080) 4122-8901",
                            "image_url": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800&fit=crop&q=80",
                            "badge": "Open Now",
                            "tags": ["Modbar Pour-Over Bar", "Bakery Kitchen", "Outdoor Patio", "Roastery Tours"],
                            "action_text": "Order Ahead for Pickup",
                            "action_url": "/coffees",
                        },
                        {
                            "id": "indiranagar",
                            "title": "Indiranagar 12th Main",
                            "subtitle": "Bangalore, 560008",
                            "description": "842, 12th Main Rd, HAL 2nd Stage • Open Daily: 7:30 AM – 10:30 PM • +91 (080) 4953-2210",
                            "image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800&fit=crop&q=80",
                            "badge": "Open Now",
                            "tags": ["Cold Brew Tap", "Sourdough Toast Bar", "High-Speed Wi-Fi"],
                            "action_text": "Order Ahead for Pickup",
                            "action_url": "/coffees",
                        },
                        {
                            "id": "bandra-west",
                            "title": "Bandra West • Pali Hill",
                            "subtitle": "Mumbai, 400050",
                            "description": "Plot 12, Gasper Enclave, Dr Ambedkar Rd • Open Daily: 7:00 AM – 11:00 PM • +91 (022) 6744-1189",
                            "image_url": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=800&fit=crop&q=80",
                            "badge": "Open Now",
                            "tags": ["Espresso Tasting Flights", "Pet-Friendly", "Artisan Pastries"],
                            "action_text": "Order Ahead for Pickup",
                            "action_url": "/coffees",
                        },
                        {
                            "id": "connaught-place",
                            "title": "Connaught Place • Inner Circle",
                            "subtitle": "New Delhi, 110001",
                            "description": "M-Block 24, Middle Circle • Open Daily: 8:00 AM – 10:00 PM • +91 (011) 4309-8800",
                            "image_url": "https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=800&fit=crop&q=80",
                            "badge": "Open Now",
                            "tags": ["Manual Brew Bar", "Reserve Estate Coffees", "Heritage Architecture"],
                            "action_text": "Order Ahead for Pickup",
                            "action_url": "/coffees",
                        },
                    ],
                },
            },
            {
                "id": "sec_cafes_cupping",
                "type": "promo_callout",
                "title": "Weekend Cupping Sessions",
                "subtitle": "Live barista sensory tastings",
                "is_active": True,
                "sort_order": 3,
                "config": {
                    "headline": "Join a Live Barista Coffee Tasting",
                    "body": "Every Saturday at 11:00 AM across all flagships. Taste single-origin micro-lots, learn the SCA flavor wheel, and calibrate your palate with our head roasters.",
                    "badge": "SATURDAY 11 AM",
                    "button_text": "RSVP for Cupping",
                    "button_url": "#cupping-rsvp",
                    "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&fit=crop&q=80",
                    "layout": "card_banner",
                },
            },
        ],
    },
    {
        "id": "page_offers",
        "page_type": "static",
        "title": "Special Offers & Tasting Bundles",
        "slug": "/offers",
        "description": "Exclusive seasonal perks, promo coupon codes, and curated explorer bundles.",
        "is_published": True,
        "sections": [
            {
                "id": "sec_offers_hero",
                "type": "hero_banner",
                "title": "Offers Banner",
                "subtitle": "Seasonal discounts and starter bundles",
                "is_active": True,
                "sort_order": 1,
                "config": {
                    "headline": "Exclusive Roastery Perks & Bundles",
                    "subheadline": "Unlock seasonal discounts, starter explorer bundles, and complimentary perks designed to elevate your home brewing.",
                    "badge": "EXCLUSIVE OFFERS",
                    "primary_cta_text": "Shop Bundles",
                    "primary_cta_url": "/coffees",
                    "background_image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=1600&auto=format&fit=crop&q=80",
                    "overlay_opacity": 60,
                    "text_align": "center",
                },
            },
            {
                "id": "sec_offers_coupons",
                "type": "feature_grid",
                "title": "Active Promo Codes",
                "subtitle": "Click to copy code and apply directly at checkout",
                "is_active": True,
                "sort_order": 2,
                "config": {
                    "columns": 3,
                    "items": [
                        {
                            "id": "coupon_coffee10",
                            "title": "First Coffee Purchase Special",
                            "subtitle": "10% OFF",
                            "description": "Get 10% off your first single-origin roast bag, easy pour box, or concentrate drop.",
                            "badge": "COFFEE10",
                            "terms": "Valid for new customers. No minimum spend.",
                            "action_text": "Copy Code: COFFEE10",
                            "action_url": "/coffees",
                        },
                        {
                            "id": "coupon_roastclub",
                            "title": "Recurring Roasters Subscription",
                            "subtitle": "15% OFF",
                            "description": "Subscribe to regular deliveries of fresh beans and receive an ongoing 15% discount on every dispatch.",
                            "badge": "ROASTCLUB",
                            "terms": "Applies automatically to recurring coffee subscriptions.",
                            "action_text": "Copy Code: ROASTCLUB",
                            "action_url": "/subscriptions",
                        },
                        {
                            "id": "coupon_gearship",
                            "title": "Espresso Hardware Free Shipping",
                            "subtitle": "FREE SHIPPING",
                            "description": "Complimentary insured white-glove shipping on all espresso machines, burr grinders, and barista tools over ₹ 2,500.",
                            "badge": "GEARSHIP",
                            "terms": "Valid on all hardware orders across India.",
                            "action_text": "Copy Code: GEARSHIP",
                            "action_url": "/equipment",
                        },
                    ],
                },
            },
            {
                "id": "sec_offers_bundles",
                "type": "feature_grid",
                "title": "Curated Tasting Bundles",
                "subtitle": "Handpicked roast pairings and home barista starter kits",
                "is_active": True,
                "sort_order": 3,
                "config": {
                    "columns": 2,
                    "items": [
                        {
                            "id": "bundle_explorer",
                            "title": "Explorer Starter Duo",
                            "subtitle": "₹ 800 (Save ₹ 150)",
                            "description": "1x Attikan Estate Espresso (250g) + 1x Easy Pour Vienna Box (5 Sachets)",
                            "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600&fit=crop&q=80",
                            "badge": "Save ₹ 150",
                            "action_text": "Shop Bundle",
                            "action_url": "/coffees",
                        },
                        {
                            "id": "bundle_coldbrew",
                            "title": "Cold Brew Lover Bundle",
                            "subtitle": "₹ 850 (Save ₹ 200)",
                            "description": "2x Sea Salt Mocha Drops Concentrate + 1x Glass Barista Tumbler",
                            "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=600&fit=crop&q=80",
                            "badge": "Save ₹ 200",
                            "action_text": "Shop Bundle",
                            "action_url": "/coffees",
                        },
                    ],
                },
            },
        ],
    },
    {
        "id": "page_subscriptions",
        "page_type": "static",
        "title": "Personalized Coffee Subscriptions",
        "slug": "/subscriptions",
        "description": "Never run out of freshly roasted estate coffee with flexible automated deliveries.",
        "is_published": True,
        "sections": [
            {
                "id": "sec_sub_hero",
                "type": "hero_banner",
                "title": "Roasters Club Hero",
                "subtitle": "Subscription club intro",
                "is_active": True,
                "sort_order": 1,
                "config": {
                    "headline": "The Roasters Club",
                    "subheadline": "Never run out of freshly roasted estate coffee. Enjoy up to 20% savings, complimentary surprise micro-lots, and total control to pause or cancel anytime.",
                    "badge": "DOORSTEP ROASTERY DISPATCH",
                    "primary_cta_text": "Build Your Subscription",
                    "primary_cta_url": "#builder",
                    "background_image": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=1600&auto=format&fit=crop&q=80",
                    "overlay_opacity": 65,
                    "text_align": "center",
                },
            },
            {
                "id": "sec_sub_perks",
                "type": "feature_grid",
                "title": "Club Perks & Guarantees",
                "subtitle": "Why coffee lovers subscribe to Hiljhil Roasters",
                "is_active": True,
                "sort_order": 2,
                "config": {
                    "columns": 3,
                    "items": [
                        {
                            "id": "perk_fresh",
                            "title": "Roasted to Order",
                            "description": "Shipped within 24h of roasting for peak flavor development and degassing.",
                            "badge": "PEAK DEGASSING",
                        },
                        {
                            "id": "perk_flexible",
                            "title": "Flexible Cadence",
                            "description": "Skip, swap roast profiles, or cancel anytime directly from your dashboard.",
                            "badge": "TOTAL FREEDOM",
                        },
                        {
                            "id": "perk_delivery",
                            "title": "Free Priority Delivery",
                            "description": "Complimentary insured delivery directly from the roastery floor to your kitchen.",
                            "badge": "FREE SHIPPING",
                        },
                    ],
                },
            },
            {
                "id": "sec_sub_plans",
                "type": "feature_grid",
                "title": "Select Roast Profiles",
                "subtitle": "Choose your signature taste profile for recurring deliveries",
                "is_active": True,
                "sort_order": 3,
                "config": {
                    "columns": 2,
                    "items": [
                        {
                            "id": "roast_espresso",
                            "title": "Attikan Espresso Roast",
                            "subtitle": "Bestseller",
                            "description": "Dark chocolate, roasted almonds & sweet figs. Formulated for dense crema.",
                            "badge": "₹ 468 / 250g (Save 15%)",
                            "action_text": "Subscribe Weekly",
                            "action_url": "/cart",
                        },
                        {
                            "id": "roast_medium",
                            "title": "Silver Oak Cafe Blend",
                            "subtitle": "Balanced",
                            "description": "Hazelnut, mild stone fruit citrus & wild honey.",
                            "badge": "₹ 468 / 250g (Save 15%)",
                            "action_text": "Subscribe Bi-Weekly",
                            "action_url": "/cart",
                        },
                        {
                            "id": "roast_filter",
                            "title": "Single-Origin Estate Filter",
                            "subtitle": "Artisanal",
                            "description": "Stone fruit, wild jasmine & raw sugarcane sweetness.",
                            "badge": "₹ 468 / 250g (Save 15%)",
                            "action_text": "Subscribe Bi-Weekly",
                            "action_url": "/cart",
                        },
                        {
                            "id": "roast_coldbrew",
                            "title": "Cold Brew Blend Reserve",
                            "subtitle": "Summer Pick",
                            "description": "Deep cocoa, rich caramel & spiced molasses.",
                            "badge": "₹ 468 / 250g (Save 15%)",
                            "action_text": "Subscribe Monthly",
                            "action_url": "/cart",
                        },
                    ],
                },
            },
        ],
    },
    {
        "id": "page_privacy",
        "page_type": "static",
        "title": "Privacy Policy",
        "slug": "/privacy",
        "description": "Hiljhil Cafe customer privacy policy and data governance practices.",
        "is_published": True,
        "sections": [
            {
                "id": "sec_privacy_content",
                "type": "rich_text",
                "title": "Hiljhil Privacy & Data Governance",
                "subtitle": "Last updated: September 10, 2026",
                "is_active": True,
                "sort_order": 1,
                "config": {
                    "badge": "LEGAL & COMPLIANCE",
                    "headline": "Privacy Policy",
                    "last_updated": "September 10, 2026",
                    "clauses": [
                        {
                            "title": "1. Information We Collect",
                            "body": "When you visit Hiljhil Cafe (hiljhil.cafe) or purchase coffee beans and espresso hardware, we collect necessary customer details including your name, shipping address, billing details, phone number, and email. We also log browser analytics, anonymized session fitment inputs, and device cookies to optimize store navigation.",
                        },
                        {
                            "title": "2. How We Use Your Data",
                            "body": "Your information is used strictly to fulfill roastery orders, coordinate white-glove hardware delivery, process subscription recurring renewals, and send roast notifications. We never sell, rent, or trade your personal data to third-party brokers.",
                        },
                        {
                            "title": "3. Computer Vision & CounterCheck Diagnostics",
                            "body": "When using CounterCheck Spatial AI to verify overhead kitchen cabinet clearance, images captured by your camera are processed on-device in WebAssembly or securely via our computer vision pipeline. Fitment snapshots are never retained beyond your session without explicit permission.",
                        },
                        {
                            "title": "4. Your Data Rights",
                            "body": "You may request full export, deletion, or modification of your account credentials and order history at any time by contacting privacy@hiljhil.cafe.",
                        },
                    ],
                },
            },
        ],
    },
    {
        "id": "page_terms",
        "page_type": "static",
        "title": "Terms of Service",
        "slug": "/terms",
        "description": "Storefront purchase agreement, warranty details, and customer policies.",
        "is_published": True,
        "sections": [
            {
                "id": "sec_terms_content",
                "type": "rich_text",
                "title": "Storefront Terms & Sales Conditions",
                "subtitle": "Last updated: September 10, 2026",
                "is_active": True,
                "sort_order": 1,
                "config": {
                    "badge": "LEGAL & COMPLIANCE",
                    "headline": "Terms of Service",
                    "last_updated": "September 10, 2026",
                    "clauses": [
                        {
                            "title": "1. Storefront & Purchase Agreement",
                            "body": "By placing an order for roasted coffee beans, brewing equipment, or recurring subscriptions through Hiljhil Cafe, you agree to our standard terms and conditions. All prices are listed in Indian Rupees (INR) and include applicable GST taxes unless stated otherwise.",
                        },
                        {
                            "title": "2. Roasted-to-Order & Perishable Goods",
                            "body": "Our coffees are roasted in micro-batches and shipped within 24 to 48 hours of degas. Because coffee is an artisanal perishable product, returns on opened bean bags cannot be accepted. If you receive damaged packaging or notice a defect, our customer care team will dispatch an immediate replacement.",
                        },
                        {
                            "title": "3. White-Glove Hardware Warranty & Fitment Guarantee",
                            "body": "All espresso machines (Breville, Gaggia, etc.) include official manufacturer warranty coverage. When verified through our CounterCheck spatial fitment tool with a Verified Fitment Badge, customers are protected with complimentary 30-day hassle-free exchange if the physical unit cannot clear kitchen cabinets.",
                        },
                        {
                            "title": "4. Subscriptions & Billing",
                            "body": "The Roasters Club recurring subscriptions can be modified, paused, or canceled anytime via your account dashboard or by reaching out to support@hiljhil.cafe before your next dispatch date.",
                        },
                    ],
                },
            },
        ],
    },
    {
        "id": "page_not_found",
        "page_type": "static",
        "title": "Page Not Found",
        "slug": "/not-found",
        "description": "404 page recovery banner and navigation assistance.",
        "is_published": True,
        "sections": [
            {
                "id": "sec_404_hero",
                "type": "hero_banner",
                "title": "404 Hero",
                "subtitle": "Lost brew notification",
                "is_active": True,
                "sort_order": 1,
                "config": {
                    "headline": "Bean There, Lost That",
                    "subheadline": "We couldn't find the page or brew you were looking for. The roast might have sold out or moved to a new shelf.",
                    "badge": "404 ERROR",
                    "primary_cta_text": "Back to Home",
                    "primary_cta_url": "/",
                    "secondary_cta_text": "Browse All Coffees",
                    "secondary_cta_url": "/coffees",
                    "background_image": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=1600&auto=format&fit=crop&q=80",
                    "overlay_opacity": 75,
                    "text_align": "center",
                },
            },
            {
                "id": "sec_404_links",
                "type": "feature_grid",
                "title": "Popular Destinations",
                "subtitle": "Jump back to one of our favorite roastery spots",
                "is_active": True,
                "sort_order": 2,
                "config": {
                    "columns": 3,
                    "items": [
                        {
                            "id": "nav_coffees",
                            "title": "Specialty Coffees",
                            "description": "Single-origin micro-lots, signature espresso blends, and easy-pour drippers.",
                            "badge": "EXPLORE ROASTS",
                            "action_text": "Browse Coffees",
                            "action_url": "/coffees",
                        },
                        {
                            "id": "nav_equipment",
                            "title": "Espresso Hardware",
                            "description": "Space-verified espresso machines and precision conical burr grinders.",
                            "badge": "COUNTERCHECK VERIFIED",
                            "action_text": "Explore Equipment",
                            "action_url": "/equipment",
                        },
                        {
                            "id": "nav_cafes",
                            "title": "Visit Our Cafes",
                            "description": "Step into our flagship cafes in Bangalore, Mumbai, and New Delhi.",
                            "badge": "FLAGSHIPS & BARS",
                            "action_text": "Find a Cafe",
                            "action_url": "/cafes",
                        },
                    ],
                },
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


async def seed_cms_data(db: AsyncSession, force_reset: bool = False):
    # 1. Seed or reset CMSSiteShell singleton
    shell_res = await db.execute(select(CMSSiteShell).where(CMSSiteShell.id == "default"))
    existing_shell = shell_res.scalar_one_or_none()
    if force_reset and existing_shell:
        existing_shell.promo_bar = DEFAULT_GLOBAL_SHELL["promo_bar"]
        existing_shell.header = DEFAULT_GLOBAL_SHELL["header"]
        existing_shell.footer = DEFAULT_GLOBAL_SHELL["footer"]
        existing_shell.theme = DEFAULT_GLOBAL_SHELL["theme"]
    elif not existing_shell:
        shell = CMSSiteShell(
            id="default",
            promo_bar=DEFAULT_GLOBAL_SHELL["promo_bar"],
            header=DEFAULT_GLOBAL_SHELL["header"],
            footer=DEFAULT_GLOBAL_SHELL["footer"],
            theme=DEFAULT_GLOBAL_SHELL["theme"],
        )
        db.add(shell)

    # 2. Seed or reset CMSPages
    if force_reset:
        pages_res = await db.execute(select(CMSPage))
        for p in pages_res.scalars().all():
            await db.delete(p)
        await db.flush()

    for page_data in DEFAULT_CMS_PAGES:
        res = await db.execute(select(CMSPage).where(CMSPage.id == page_data["id"]))
        existing_page = res.scalar_one_or_none()
        if not existing_page:
            page = CMSPage(**page_data)
            db.add(page)

    # 3. Seed or reset CMSThemePresets
    if force_reset:
        presets_res = await db.execute(select(CMSThemePreset))
        for p in presets_res.scalars().all():
            await db.delete(p)
        await db.flush()

    for preset_data in DEFAULT_THEME_PRESETS_LIST:
        res = await db.execute(select(CMSThemePreset).where(CMSThemePreset.preset == preset_data["preset"]))
        existing_preset = res.scalar_one_or_none()
        if not existing_preset:
            preset = CMSThemePreset(**preset_data)
            db.add(preset)
        elif force_reset:
            for key, val in preset_data.items():
                setattr(existing_preset, key, val)

    await db.commit()


if __name__ == "__main__":
    import asyncio
    from sqlalchemy import text
    from src.db.database import get_db, engine, Base

    async def main():
        async with engine.begin() as conn:
            await conn.execute(text("ALTER TABLE cms_site_shell ADD COLUMN IF NOT EXISTS theme JSONB DEFAULT '{}'::jsonb;"))
            await conn.run_sync(Base.metadata.create_all)
        print("Schema verified: cms_site_shell.theme & cms_theme_presets table ready.")

        async for session in get_db():
            await seed_content_lanes(session)
            print("Successfully seeded content lanes into PostgreSQL!")
            await seed_cms_data(session, force_reset=True)
            print("Successfully seeded CMS site shell, theme presets & pages into PostgreSQL!")
            break

    asyncio.run(main())

