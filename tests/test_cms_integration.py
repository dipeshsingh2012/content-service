import unittest
from httpx import ASGITransport, AsyncClient

from src.config import settings
import src.db.database as db_module
from src.main import app


class TestCMSRealDBIntegration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        if not settings.DATABASE_URL:
            self.skipTest("No DATABASE_URL configured")
        if db_module._engine is not None:
            await db_module._engine.dispose()
            db_module._engine = None
            db_module._AsyncSessionLocal = None

    async def asyncTearDown(self):
        if db_module._engine is not None:
            await db_module._engine.dispose()
            db_module._engine = None
            db_module._AsyncSessionLocal = None

    async def test_01_health(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res = await client.get("/api/v1/health")
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertEqual(data["status"], "ok")
            self.assertEqual(data["service"], "content-service")

    async def test_02_get_shell_from_db(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res = await client.get("/api/v1/cms/shell")
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertIn("promo_bar", data)
            self.assertIn("header", data)
            self.assertIn("footer", data)
            self.assertEqual(data["header"]["brand_name"], "Hiljhil Roasters")

    async def test_03_promo_bar_dedicated_endpoint(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # 1. Fetch promo bar
            res = await client.get("/api/v1/cms/shell/promo-bar")
            self.assertEqual(res.status_code, 200)
            promo = res.json()
            self.assertTrue(promo["enabled"])

            # 2. Update promo bar
            update_payload = {
                "enabled": True,
                "text": "Live Neon DB Verified Promo Bar",
                "cta_text": "Taste Fresh Harvest",
                "cta_url": "#/coffees",
                "theme": "amber",
                "badge": "VERIFIED",
                "dismissible": True,
            }
            put_res = await client.put("/api/v1/cms/shell/promo-bar", json=update_payload)
            self.assertEqual(put_res.status_code, 200)
            updated = put_res.json()
            self.assertEqual(updated["text"], "Live Neon DB Verified Promo Bar")
            self.assertEqual(updated["badge"], "VERIFIED")

            # 3. Read back to confirm persistence in PostgreSQL
            verify_res = await client.get("/api/v1/cms/shell/promo-bar")
            self.assertEqual(verify_res.status_code, 200)
            self.assertEqual(verify_res.json()["text"], "Live Neon DB Verified Promo Bar")

    async def test_04_cms_pages_real_db(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # 1. List seeded pages from real DB
            res = await client.get("/api/v1/cms/pages")
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertGreaterEqual(data["total"], 4)

            # 2. Verify seeded homepage exists
            slugs = [p["slug"] for p in data["items"]]
            self.assertIn("/", slugs)

            # 3. Create a test page in real DB
            page_payload = {
                "id": "page_integration_test_live",
                "page_type": "discovery",
                "title": "Integration Test Page",
                "slug": "/test-integration-live",
                "description": "Live DB integration test page",
                "is_published": True,
                "sections": [],
            }
            create_res = await client.post("/api/v1/cms/pages", json=page_payload)
            self.assertIn(create_res.status_code, [201, 409])
            if create_res.status_code == 201:
                created = create_res.json()
                self.assertEqual(created["title"], "Integration Test Page")

            # 4. Fetch by slug
            get_res = await client.get("/api/v1/cms/pages/test-integration-live")
            self.assertEqual(get_res.status_code, 200)
            self.assertEqual(get_res.json()["id"], "page_integration_test_live")

            # 5. Clean up test page
            del_res = await client.delete("/api/v1/cms/pages/page_integration_test_live")
            self.assertEqual(del_res.status_code, 204)


if __name__ == "__main__":
    unittest.main()

