import unittest
from httpx import AsyncClient, ASGITransport
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


class TestCMSService(unittest.IsolatedAsyncioTestCase):
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

    async def test_get_and_update_shell(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # 1. Get default shell
            res = await client.get("/api/v1/cms/shell")
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertIn("promo_bar", data)
            self.assertIn("header", data)
            self.assertIn("footer", data)
            self.assertEqual(data["header"]["brand_name"], "Hiljhil Roasters")

            # 2. Update shell
            update_payload = {
                "promo_bar": {
                    "enabled": True,
                    "text": "Special Harvest 20% Off",
                    "cta_text": "Shop Now",
                    "cta_url": "#/coffees",
                    "theme": "emerald",
                    "badge": "LIMITED",
                },
                "header": {
                    "brand_name": "Hiljhil Flagship Roastery",
                    "nodes": [],
                    "show_search": True,
                    "show_cart": True,
                    "show_spatial_finder": True,
                    "sticky": True,
                },
            }
            put_res = await client.put("/api/v1/cms/shell", json=update_payload)
            self.assertEqual(put_res.status_code, 200)
            updated = put_res.json()
            self.assertEqual(updated["header"]["brand_name"], "Hiljhil Flagship Roastery")
            self.assertEqual(updated["promo_bar"]["text"], "Special Harvest 20% Off")
            self.assertEqual(updated["promo_bar"]["theme"], "emerald")

            # 3. Get promo bar directly
            pb_get = await client.get("/api/v1/cms/shell/promo-bar")
            self.assertEqual(pb_get.status_code, 200)
            pb_data = pb_get.json()
            self.assertEqual(pb_data["text"], "Special Harvest 20% Off")

            # 4. Update promo bar directly
            pb_put = await client.put(
                "/api/v1/cms/shell/promo-bar",
                json={
                    "enabled": True,
                    "text": "Flash Sale: Buy 2 Get 1 Free",
                    "theme": "amber",
                    "badge": "FLASH",
                },
            )
            self.assertEqual(pb_put.status_code, 200)
            self.assertEqual(pb_put.json()["text"], "Flash Sale: Buy 2 Get 1 Free")
            self.assertEqual(pb_put.json()["theme"], "amber")

            # 5. Get and update header directly
            h_get = await client.get("/api/v1/cms/shell/header")
            self.assertEqual(h_get.status_code, 200)
            self.assertIn("brand_name", h_get.json())

            h_put = await client.put(
                "/api/v1/cms/shell/header",
                json={
                    "brand_name": "Hiljhil Roasters NYC",
                    "nodes": [],
                    "show_search": False,
                    "show_cart": True,
                    "show_spatial_finder": True,
                    "sticky": False,
                },
            )
            self.assertEqual(h_put.status_code, 200)
            self.assertEqual(h_put.json()["brand_name"], "Hiljhil Roasters NYC")
            self.assertFalse(h_put.json()["show_search"])

            # 6. Get and update footer directly
            f_get = await client.get("/api/v1/cms/shell/footer")
            self.assertEqual(f_get.status_code, 200)
            self.assertIn("copyright", f_get.json())

            f_put = await client.put(
                "/api/v1/cms/shell/footer",
                json={
                    "brand_name": "HILJHIL ROASTERS",
                    "brand_description": "Artisan micro-lots.",
                    "columns": [],
                    "show_newsletter": False,
                    "social_links": [],
                    "copyright": "© 2026 Test Cafe",
                },
            )
            self.assertEqual(f_put.status_code, 200)
            self.assertEqual(f_put.json()["copyright"], "© 2026 Test Cafe")

    async def test_cms_pages_crud(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # 1. Initially empty
            list_res = await client.get("/api/v1/cms/pages")
            self.assertEqual(list_res.status_code, 200)
            self.assertEqual(list_res.json()["total"], 0)

            # 2. Create a page
            new_page = {
                "id": "page_test_brew",
                "page_type": "static",
                "title": "Brewing Guides & Calibration",
                "slug": "/brewing-guides",
                "description": "Step by step recipes for espresso, pour-over and immersion brewing.",
                "is_published": True,
                "sections": [
                    {
                        "id": "sec_brew_hero",
                        "type": "hero_banner",
                        "title": "Brew Guide Hero",
                        "is_active": True,
                        "sort_order": 1,
                        "config": {
                            "headline": "Dial In Your Daily Extraction",
                            "subheadline": "Water ratios and grind sizes.",
                            "primary_cta_text": "View Recipes",
                            "primary_cta_url": "#/recipes",
                            "background_image": "https://example.com/brew.jpg",
                            "overlay_opacity": 50,
                            "text_align": "center",
                        },
                    }
                ],
            }
            create_res = await client.post("/api/v1/cms/pages", json=new_page)
            self.assertEqual(create_res.status_code, 201)
            created = create_res.json()
            self.assertEqual(created["id"], "page_test_brew")
            self.assertEqual(created["title"], "Brewing Guides & Calibration")
            self.assertEqual(len(created["sections"]), 1)

            # 3. Duplicate slug returns 409
            dup_res = await client.post("/api/v1/cms/pages", json=new_page)
            self.assertEqual(dup_res.status_code, 409)

            # 4. Get page by ID
            get_res = await client.get("/api/v1/cms/pages/page_test_brew")
            self.assertEqual(get_res.status_code, 200)
            self.assertEqual(get_res.json()["slug"], "/brewing-guides")

            # 5. Get page by slug
            slug_res = await client.get("/api/v1/cms/pages/brewing-guides")
            self.assertEqual(slug_res.status_code, 200)
            self.assertEqual(slug_res.json()["id"], "page_test_brew")

            # 6. Update page
            patch_res = await client.patch(
                "/api/v1/cms/pages/page_test_brew",
                json={"title": "Master Brewing Guides 2026", "is_published": False},
            )
            self.assertEqual(patch_res.status_code, 200)
            patched = patch_res.json()
            self.assertEqual(patched["title"], "Master Brewing Guides 2026")
            self.assertFalse(patched["is_published"])

            # 7. List pages with filter
            filter_res = await client.get("/api/v1/cms/pages?page_type=static")
            self.assertEqual(filter_res.status_code, 200)
            self.assertEqual(filter_res.json()["total"], 1)

            # 8. Delete page
            del_res = await client.delete("/api/v1/cms/pages/page_test_brew")
            self.assertEqual(del_res.status_code, 204)

            # 9. Verify deleted
            not_found_res = await client.get("/api/v1/cms/pages/page_test_brew")
            self.assertEqual(not_found_res.status_code, 404)

    async def test_reset_defaults(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res = await client.post("/api/v1/cms/reset-defaults")
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertIn("message", data)
            self.assertIn("shell", data)
            self.assertIn("pages", data)
            self.assertGreaterEqual(len(data["pages"]), 4)

            # Check that pages can be listed
            pages_res = await client.get("/api/v1/cms/pages")
            self.assertEqual(pages_res.status_code, 200)
            self.assertGreaterEqual(pages_res.json()["total"], 4)


if __name__ == "__main__":
    unittest.main()
