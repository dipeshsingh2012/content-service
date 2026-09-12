# Content Service (`content-service`)

> **Headless CMS & Merchandising Content Engine for Hiljhil Cafe**

`content-service` is a high-speed FastAPI service running on port **8006** providing content presentation models for storefront micro-frontends and the unified Refine `pim-ui` cockpit.

---

## 🎯 Features
1. **Content & Product Lanes**: Full CRUD for circular category lanes and curated product sliders.
2. **Placement & Display Targeting**: Filter lanes by page placement (`homepage`, `discovery`, `all`).
3. **Card Styles**: Native support for circular category cards with navigation arrows.
4. **Relational Item Merchandising**: Links to catalog products with custom overrides and promo badges.

---

## 🚀 API Endpoints
- `GET /api/v1/health` — Service readiness
- `GET /api/v1/lanes` — List & filter lanes (placement, status, search)
- `GET /api/v1/lanes/{id}` — Get lane details
- `POST /api/v1/lanes` — Create new lane
- `PATCH /api/v1/lanes/{id}` — Update lane
- `DELETE /api/v1/lanes/{id}` — Delete lane
