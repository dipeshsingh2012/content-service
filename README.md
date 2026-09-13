# Content Service (`content-service`)

> **Headless CMS & Merchandising Content Engine for Hiljhil Cafe**

`content-service` is a high-speed FastAPI service running on port **8006** providing content presentation models for storefront micro-frontends and the unified Refine `pim-ui` cockpit.

---

## 🎯 Features
1. **Content & Product Lanes**: Full CRUD for circular category lanes and curated product sliders.
2. **Placement & Display Targeting**: Filter lanes by page placement (`homepage`, `discovery`, `all`).
3. **Card Styles**: Native support for circular category cards with navigation arrows.
4. **Relational Item Merchandising**: Links to catalog products with custom overrides and promo badges.
5. **CMS Global Site Shell**: Full CRUD for site promo banner, header navigation hierarchy, and footer links.
6. **CMS Multi-Page Experience Builder**: Multi-page layout engine for Flagship Homepage, Collections, Discovery, and Custom Editorial pages.

---

## 🚀 API Endpoints

### Health & Readiness
- `GET /api/v1/health` — Service readiness

### Content & Merchandising Lanes
- `GET /api/v1/lanes` — List & filter lanes (placement, status, search)
- `GET /api/v1/lanes/{id}` — Get lane details by ID or slug
- `POST /api/v1/lanes` — Create new lane
- `PATCH /api/v1/lanes/{id}` — Update lane
- `DELETE /api/v1/lanes/{id}` — Delete lane

### CMS Global Site Shell & Reusable Chrome
- `GET /api/v1/cms/shell` — Retrieve active global site shell (promo bar, header, footer)
- `PUT /api/v1/cms/shell` — Update or upsert global site shell configuration
- `GET /api/v1/cms/shell/promo-bar` — Retrieve only the active promo bar configuration
- `PUT /api/v1/cms/shell/promo-bar` — Update only the active promo bar configuration
- `GET /api/v1/cms/shell/header` — Retrieve only the active header navigation configuration
- `PUT /api/v1/cms/shell/header` — Update only the active header navigation configuration
- `GET /api/v1/cms/shell/footer` — Retrieve only the active footer configuration
- `PUT /api/v1/cms/shell/footer` — Update only the active footer configuration


### CMS Pages & Sections
- `GET /api/v1/cms/pages` — List & filter CMS pages (`page_type`, `is_published`, `q`)
- `GET /api/v1/cms/pages/{page_id}` — Get single page by ID or slug
- `POST /api/v1/cms/pages` — Create new CMS page
- `PATCH /api/v1/cms/pages/{page_id}` — Update CMS page
- `DELETE /api/v1/cms/pages/{page_id}` — Delete CMS page
- `POST /api/v1/cms/reset-defaults` — Reset CMS pages and site shell to default showcase state

