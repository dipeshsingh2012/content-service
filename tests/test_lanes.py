import unittest
from httpx import AsyncClient, ASGITransport
import src.db.database as db_module
from src.main import app


class TestContentServiceLanes(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        if db_module._engine is not None:
            await db_module._engine.dispose()
            db_module._engine = None
            db_module._AsyncSessionLocal = None

    async def asyncTearDown(self):
        if db_module._engine is not None:
            await db_module._engine.dispose()
            db_module._engine = None
            db_module._AsyncSessionLocal = None

    async def test_health(self):

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res = await client.get("/api/v1/health")
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json()["status"], "ok")

    async def test_list_lanes_seeded(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            res = await client.get("/api/v1/lanes")
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertIn("items", data)
            self.assertIn("total", data)
            self.assertGreaterEqual(data["total"], 2)

    async def test_create_and_delete_lane(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            payload = {
                "title": "Seasonal Feature",
                "slug": "seasonal-feature-unit-test",
                "lane_type": "category_lane",
                "placement": "discovery",
                "card_style": "circular",
                "has_navigation_arrows": True,
                "status": "active",
                "sort_order": 10,
                "items": [
                    {
                        "id": "tile-1",
                        "title": "Cold Brew Reserve",
                        "image_url": "https://example.com/photo.jpg",
                        "target_url": "#/cold-brew",
                        "badge": "NEW",
                        "sort_order": 0,
                    }
                ],
            }
            res = await client.post("/api/v1/lanes", json=payload)
            self.assertEqual(res.status_code, 201)
            created = res.json()
            self.assertEqual(created["title"], "Seasonal Feature")
            self.assertEqual(len(created["items"]), 1)

            # Delete
            del_res = await client.delete(f"/api/v1/lanes/{created['id']}")
            self.assertEqual(del_res.status_code, 204)


if __name__ == "__main__":
    unittest.main()
