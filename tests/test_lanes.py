import unittest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.db.database import Base, get_db
from src.db.seed import seed_content_lanes
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


class TestContentServiceLanes(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        app.dependency_overrides[get_db] = override_get_db

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()

    async def asyncSetUp(self):
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with TestSessionLocal() as session:
            await seed_content_lanes(session)

    async def asyncTearDown(self):
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

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
