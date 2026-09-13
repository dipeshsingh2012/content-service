import unittest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.db.database import Base, get_db
from src.main import app

test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def override_get_db():
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


class TestCMSPimUIContract(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        app.dependency_overrides[get_db] = override_get_db

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()

    async def asyncSetUp(self):
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def asyncTearDown(self):
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def test_01_promo_bar_contract(self):
        """Verify dedicated promo bar endpoint contract matches PIM UI PromoBarConfig."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # 1. Fetch initial promo bar
            res = await client.get("/api/v1/cms/shell/promo-bar")
            self.assertEqual(res.status_code, 200)
            promo = res.json()
            self.assertIn("enabled", promo)
            self.assertIn("text", promo)
            self.assertIn("theme", promo)
            self.assertIn("dismissible", promo)

            # 2. PIM UI payload shape for promo bar
            pim_promo_payload = {
                "enabled": True,
                "text": "Flash Roast: Complimentary shipping on orders over $45",
                "cta_text": "Taste Seasonal Lots",
                "cta_url": "#/coffees?sort=harvest",
                "theme": "emerald",
                "badge": "FRESH CROP",
                "dismissible": True,
            }
            put_res = await client.put("/api/v1/cms/shell/promo-bar", json=pim_promo_payload)
            self.assertEqual(put_res.status_code, 200)
            updated = put_res.json()
            self.assertEqual(updated["text"], pim_promo_payload["text"])
            self.assertEqual(updated["theme"], "emerald")
            self.assertEqual(updated["badge"], "FRESH CROP")

    async def test_02_header_and_nav_nodes_contract(self):
        """Verify header navigation contract matches PIM UI HeaderConfig and NavNode hierarchy."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            pim_header_payload = {
                "brand_name": "Hiljhil Micro-Roastery",
                "brand_tagline": "Precision Roasted Specialty Lots",
                "brand_badge": "FLAGSHIP",
                "show_search": True,
                "show_cart": True,
                "show_spatial_finder": True,
                "sticky": True,
                "nodes": [
                    {
                        "id": "nav_coffees",
                        "label": "Coffees",
                        "url": "#/coffees",
                        "badge": "HOT",
                        "children": [
                            {"id": "nav_single", "label": "Single Origin", "url": "#/coffees?type=single"},
                            {"id": "nav_blends", "label": "Espresso Blends", "url": "#/coffees?type=blend"},
                        ],
                    },
                    {
                        "id": "nav_equipment",
                        "label": "Gear",
                        "url": "#/equipment",
                        "children": [],
                    },
                ],
            }
            res = await client.put("/api/v1/cms/shell/header", json=pim_header_payload)
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertEqual(data["brand_name"], "Hiljhil Micro-Roastery")
            self.assertEqual(len(data["nodes"]), 2)
            self.assertEqual(len(data["nodes"][0]["children"]), 2)

    async def test_03_footer_contract(self):
        """Verify footer contract matches PIM UI FooterConfig."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            pim_footer_payload = {
                "brand_name": "HILJHIL ROASTERS",
                "brand_description": "Direct Trade Micro-Lot Coffee Roasters.",
                "show_newsletter": True,
                "newsletter_title": "Join the Cupping Club",
                "newsletter_placeholder": "Enter your email",
                "copyright": "© 2026 Hiljhil Roasters Inc.",
                "columns": [
                    {
                        "id": "col_coffees",
                        "title": "Coffees",
                        "links": [
                            {"label": "Single Origin", "url": "#/coffees"},
                            {"label": "Producer Reserve", "url": "#/coffees?cat=producer"},
                        ],
                    }
                ],
                "social_links": [
                    {"platform": "Instagram", "url": "https://instagram.com"},
                ],
            }
            res = await client.put("/api/v1/cms/shell/footer", json=pim_footer_payload)
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertEqual(data["newsletter_title"], "Join the Cupping Club")
            self.assertEqual(len(data["columns"]), 1)

    async def test_04_pages_and_all_section_types_contract(self):
        """Verify CMS pages endpoint accepts all section types supported by PIM UI."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            pim_page_payload = {
                "id": "page_contract_test",
                "page_type": "home",
                "title": "Flagship Homepage 2026",
                "slug": "/home-2026",
                "description": "Comprehensive test with all section types",
                "is_published": True,
                "sections": [
                    {
                        "id": "sec_hero",
                        "type": "hero_banner",
                        "title": "Hero Section",
                        "sort_order": 1,
                        "is_active": True,
                        "config": {
                            "headline": "Fresh Crop Arrival",
                            "subheadline": "Direct trade microlots from Oromia and Huila.",
                            "primary_cta_text": "Order Now",
                            "primary_cta_url": "#/coffees",
                            "background_image": "https://example.com/hero.jpg",
                            "overlay_opacity": 50,
                            "text_align": "center",
                        },
                    },
                    {
                        "id": "sec_category_lane",
                        "type": "category_lane",
                        "title": "Browse by Roast Style",
                        "sort_order": 2,
                        "is_active": True,
                        "config": {"card_style": "circular", "columns": 4, "categories": []},
                    },
                    {
                        "id": "sec_prod_lane",
                        "type": "product_lane",
                        "title": "CounterCheck Verified Gear",
                        "sort_order": 3,
                        "is_active": True,
                        "config": {"display_count": 6, "show_badges": True, "enable_quick_add": True},
                    },
                    {
                        "id": "sec_testimonials",
                        "type": "testimonials",
                        "title": "What Baristas Say",
                        "sort_order": 4,
                        "is_active": True,
                        "config": {"reviews": [{"author": "James H.", "rating": 5, "quote": "Incredible extraction."}]},
                    },
                    {
                        "id": "sec_promo_callout",
                        "type": "promo_callout",
                        "title": "Subscription Offer",
                        "sort_order": 5,
                        "is_active": True,
                        "config": {"headline": "Save 15% Monthly", "button_text": "Subscribe Now"},
                    },
                ],
            }

            # 1. Create page
            create_res = await client.post("/api/v1/cms/pages", json=pim_page_payload)
            self.assertEqual(create_res.status_code, 201)
            created = create_res.json()
            self.assertEqual(created["id"], "page_contract_test")
            self.assertEqual(len(created["sections"]), 5)

            # 2. Get page by ID
            get_res = await client.get("/api/v1/cms/pages/page_contract_test")
            self.assertEqual(get_res.status_code, 200)
            self.assertEqual(get_res.json()["title"], "Flagship Homepage 2026")

            # 3. Patch page
            patch_res = await client.patch(
                "/api/v1/cms/pages/page_contract_test",
                json={"title": "Updated Flagship 2026", "is_published": False},
            )
            self.assertEqual(patch_res.status_code, 200)
            self.assertEqual(patch_res.json()["title"], "Updated Flagship 2026")
            self.assertFalse(patch_res.json()["is_published"])

            # 4. Delete page
            del_res = await client.delete("/api/v1/cms/pages/page_contract_test")
            self.assertEqual(del_res.status_code, 204)

    async def test_05_reset_defaults_contract(self):
        """Verify reset-defaults endpoint contract returns both shell and pages."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res = await client.post("/api/v1/cms/reset-defaults")
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertIn("message", data)
            self.assertIn("shell", data)
            self.assertIn("pages", data)
            self.assertIn("promo_bar", data["shell"])
            self.assertIn("header", data["shell"])
            self.assertIn("footer", data["shell"])
            self.assertGreaterEqual(len(data["pages"]), 4)


if __name__ == "__main__":
    unittest.main()

