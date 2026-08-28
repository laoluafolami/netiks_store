# Netiks Store PRD

## 1. Document Control

- Product Name: Netiks Store
- Version: 1.0
- Date: 2026-06-14
- Status: Draft for implementation
- Primary Goal: Build a realistic multi-vendor e-commerce platform that doubles as a hands-on DevOps learning project for interns.

## 2. Product Summary

Netiks Store is a multi-vendor marketplace where independent vendors can create storefronts, add products, manage pricing and inventory, and publish items to a shared marketplace. Shoppers can browse products from multiple vendors, filter by category, and view store details before making purchase decisions.

The product is intentionally designed to be complex enough to teach practical software delivery and DevOps skills. Interns should be able to work on the platform locally, containerize it, automate tests, deploy it to AWS, observe it in production-like environments, and understand the full lifecycle from commit to deployment.

## 3. Problem Statement

Many DevOps learners understand cloud and CI/CD concepts only at a theoretical level. They rarely get exposure to a realistic application with multiple services, authentication, data storage, file uploads, environment management, background jobs, and deployment pipelines.

Netiks Store solves this by providing:

- A real application with frontend, backend, database, storage, and auth.
- A deployment target with meaningful operational concerns.
- Enough product complexity to justify infrastructure, monitoring, automation, and security practices.
- A codebase that can be expanded incrementally by interns without becoming overwhelming on day one.

## 4. Goals

### Business and learning goals

- Create a believable production-style marketplace application.
- Teach interns modern full-stack and DevOps workflows using a single project.
- Keep infrastructure choices as low-cost or free-tier-friendly as possible.
- Provide enough scope for CI/CD, containerization, reverse proxying, observability, and AWS deployments.
- Produce documentation that supports onboarding and independent execution.

### Product goals

- Allow vendors to sign up and create stores.
- Allow vendors to create, edit, publish, and manage products.
- Display products from all vendors on a shared home page.
- Support filtering by category, price, and keyword search.
- Provide secure authentication and authorization.
- Support image upload for store logos and product images.
- Offer a clean admin and vendor management experience.

## 5. Non-Goals For Initial Release

- Full payment processing.
- Live order fulfillment and shipping integration.
- Coupons, loyalty points, gift cards, or advanced promotions.
- Complex recommendation engines.
- Real-time chat between buyers and vendors.
- Native mobile apps.
- Full multi-language and multi-currency support.

These can be added later as stretch goals for interns.

## 6. Target Users

### Primary internal users

- DevOps interns using the project to learn deployment, automation, environments, and operations.
- Engineering mentors reviewing infrastructure and code quality.

### External-style product users

- Marketplace shoppers browsing products.
- Vendors creating stores and listing products.
- Platform admins moderating stores, products, and users.

## 7. User Roles

### Guest

- View home page and public product listings.
- Search and filter products.
- View store pages and product detail pages.

### Shopper

- Register and log in.
- Maintain a profile.
- Save favorites in a future phase.

### Vendor

- Register and log in.
- Create exactly one store in initial version.
- Edit store profile, description, category focus, and branding.
- Create, update, delete, draft, and publish products.
- Upload store logo and product images.
- Manage stock quantity and availability.

### Admin

- View all users, stores, and products.
- Suspend or deactivate stores or products.
- Manage product categories.
- Review platform health from an operational perspective in future admin tooling.

## 8. Core User Stories

### Marketplace browsing

- As a guest, I want to see featured and latest products on the home page so I can discover items quickly.
- As a guest, I want to filter products by category so I can find relevant items.
- As a guest, I want to search by name or keyword so I can locate a product faster.
- As a guest, I want to open a product page to see details, price, images, and vendor information.

### Vendor onboarding

- As a new user, I want to register securely so I can access vendor tools.
- As an authenticated user, I want to create my store so I can begin selling.
- As a vendor, I want to upload a store logo and description so my storefront looks credible.

### Product management

- As a vendor, I want to add products with title, description, price, stock, category, and images.
- As a vendor, I want to save a product as draft before publishing.
- As a vendor, I want to edit or archive products that are no longer available.
- As a vendor, I want to see my product list and status at a glance.

### Platform administration

- As an admin, I want to review all stores and products so I can moderate the marketplace.
- As an admin, I want to disable abusive or invalid listings.

### DevOps learning

- As an intern, I want to run the entire application locally with one setup guide.
- As an intern, I want automated tests and CI checks so I can validate changes safely.
- As an intern, I want containerized services so I can learn deployment workflows.
- As an intern, I want AWS deployment docs and infrastructure patterns so I can practice real operations.

## 9. Functional Requirements

## 9.1 Authentication and authorization

- Users can register with name, email, and password.
- Users can log in and log out securely.
- Passwords must be hashed.
- Token-based authentication will be used between frontend and backend.
- Role-based access control must distinguish shoppers, vendors, and admins.
- Protected routes must prevent unauthorized dashboard access.
- Session persistence must work across page reloads.

## 9.2 Store management

- A vendor can create one store in v1.
- Store fields:
  - Store name
  - Slug
  - Description
  - Contact email
  - Optional phone
  - Logo image
  - Banner image
  - Status
- A store page must show:
  - Store branding
  - Store description
  - Public product grid
  - Vendor profile basics

## 9.3 Product management

- Vendors can create products with:
  - Name
  - Slug
  - Description
  - Category
  - Price
  - Currency
  - Stock quantity
  - SKU
  - Status: draft, published, archived
  - Featured image
  - Additional images
- Vendors can edit and delete their own products.
- Only published products appear on public marketplace pages.
- Products must belong to a store.

## 9.4 Marketplace browsing

- Public home page must display products from multiple stores.
- Product cards must show image, title, price, category, and vendor/store name.
- Marketplace must support:
  - Category filter
  - Search by keyword
  - Sort by latest and price
  - Pagination
- Product detail page must include:
  - Product images
  - Description
  - Price
  - Availability
  - Store information
  - Related products from same store

## 9.5 Categories

- Admins can manage categories.
- Each product belongs to one primary category in v1.
- Category pages can list products under that category.

## 9.6 Media uploads

- Vendors can upload store logos, store banners, and product images.
- Backend must validate file type and size.
- Uploaded assets should use object storage compatible workflow.
- Local development should support local file storage or MinIO-style emulation if desired.

## 9.7 Admin management

- Admin can view all users.
- Admin can view all stores and products.
- Admin can change store or product status.
- Admin can review basic platform metrics in later phases.

## 9.8 Auditability and operations

- Application should log key events:
  - Authentication attempts
  - Store creation
  - Product creation and updates
  - Admin actions
- Environment-based configuration must be supported.
- Health check endpoints must exist for backend and frontend readiness.

## 10. Non-Functional Requirements

### Security

- Password hashing with a strong algorithm.
- JWT or secure session tokens with expiration.
- Input validation at API boundaries.
- CORS configured by environment.
- Basic rate limiting recommended for auth endpoints.
- Secrets must come from environment variables or secret managers, not source control.

### Performance

- Home page should load public products quickly with pagination.
- Image delivery should be optimized on frontend.
- Backend queries should support filtering and sorting efficiently.

### Reliability

- Application must recover cleanly after container restarts.
- Database migrations must be repeatable and versioned.
- Deployment should support rollback strategy.

### Maintainability

- Clear project structure for frontend and backend.
- API schema documented.
- Automated tests for key flows.
- Consistent linting and formatting.

### Observability

- Structured logs preferred.
- Error tracking integration should be easy to add.
- Metrics and uptime checks should be possible in deployment environments.

## 11. Proposed Tech Stack

### Frontend

- Next.js App Router
- TypeScript
- Tailwind CSS
- TanStack Query for API state
- Zod for client-side schema validation where useful

### Backend

- FastAPI
- SQLAlchemy or SQLModel
- Alembic migrations
- Pydantic validation
- JWT-based auth

### Data and storage

- PostgreSQL for primary database
- S3-compatible object storage for media
- Redis optional for caching and rate limiting in later phases

### DevOps and platform

- Docker and Docker Compose for local orchestration
- GitHub Actions for CI/CD
- Nginx or Caddy as reverse proxy in deployment setups
- AWS for deployment practice

## 12. Free-Tier-Friendly Service Strategy

The project should prefer low-cost or free options during development and training:

- Local Docker Compose for everyday development.
- PostgreSQL in Docker locally.
- Local file storage in development, S3-compatible storage abstraction in production.
- GitHub Actions free tier for CI where available.
- AWS Free Tier for:
  - EC2 for app hosting
  - S3 for media
  - RDS only if budget allows; otherwise PostgreSQL can run on EC2 for training environments
- Cloudflare free tier can optionally help with DNS and CDN later.

For intern training, local-first architecture is preferred so the team can learn without incurring constant cloud costs.

## 13. Proposed System Modules

### Frontend modules

- Public home page
- Product listing and filters
- Product detail page
- Store page
- Auth pages
- Vendor dashboard
- Admin dashboard

### Backend modules

- Auth service
- User service
- Store service
- Product service
- Category service
- Media upload service
- Admin moderation service

### Infrastructure modules

- Container definitions
- Environment configuration
- Reverse proxy
- CI pipeline
- Deployment scripts
- Monitoring hooks

## 14. Suggested Repository Structure

```text
netiks-store/
  apps/
    web/                 # Next.js frontend
    api/                 # FastAPI backend
  packages/
    shared-types/        # Optional shared types/contracts
  infra/
    docker/
    nginx/
    aws/
  docs/
    PRD.md
    PROJECT_DOCUMENTATION.md
    RUNBOOKS/
  scripts/
  .github/
    workflows/
```

## 15. Key Screens and Pages

- Landing/home page
- Marketplace product listing page
- Product detail page
- Store profile page
- Sign up page
- Sign in page
- Vendor onboarding page
- Vendor dashboard home
- Product create/edit page
- Store settings page
- Admin dashboard

## 16. API Scope For V1

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `POST /stores`
- `GET /stores/{slug}`
- `PATCH /stores/{id}`
- `POST /products`
- `GET /products`
- `GET /products/{slug}`
- `PATCH /products/{id}`
- `DELETE /products/{id}`
- `GET /categories`
- `POST /uploads`
- `GET /health`

Admin-only endpoints can be added under `/admin`.

## 17. Data Model Overview

### User

- id
- full_name
- email
- password_hash
- role
- is_active
- created_at
- updated_at

### Store

- id
- owner_id
- name
- slug
- description
- contact_email
- phone
- logo_url
- banner_url
- status
- created_at
- updated_at

### Category

- id
- name
- slug
- description

### Product

- id
- store_id
- category_id
- name
- slug
- description
- price
- currency
- stock_quantity
- sku
- status
- featured_image_url
- created_at
- updated_at

### ProductImage

- id
- product_id
- image_url
- alt_text
- sort_order

## 18. MVP Definition

The MVP is complete when:

- Users can register and log in.
- Vendors can create stores.
- Vendors can create and publish products with images.
- The home page shows products from multiple stores.
- Users can filter by category and search by keyword.
- Admin has basic moderation capabilities.
- The app runs locally with Docker Compose.
- Core setup, usage, and architecture are documented.

## 19. Milestones

### Phase 1: Product foundation

- PRD and documentation
- Repo scaffolding
- Local development environment
- Design system direction

### Phase 2: Core application

- Auth
- Store management
- Product management
- Public marketplace pages
- Category filtering

### Phase 3: Quality and operations

- Tests
- Seed data
- API docs
- Logging and health checks
- Container hardening

### Phase 4: DevOps enablement

- CI pipelines
- Deployment configs
- AWS environment setup
- Reverse proxy and TLS guidance
- Monitoring and runbooks

## 20. Acceptance Criteria

- A new vendor can create an account, log in, create a store, and publish a product without manual DB changes.
- A guest can visit the home page and see products from different stores.
- A guest can search and filter products.
- Unauthorized users cannot access vendor-only or admin-only pages.
- Product and store images upload successfully in supported environments.
- The application can be started locally from documented steps.

## 21. Risks and Mitigations

- Risk: Scope becomes too large for an intern project.
  - Mitigation: Ship MVP first and label stretch goals clearly.
- Risk: AWS costs increase unexpectedly.
  - Mitigation: Prefer local development and free-tier-aware architecture.
- Risk: Auth and file uploads add hidden complexity.
  - Mitigation: Implement them early and test them thoroughly.
- Risk: DevOps learning gets overshadowed by application coding.
  - Mitigation: Keep architecture explicit and create infrastructure tasks alongside app tasks.

## 22. Stretch Features

- Shopping cart
- Checkout and payment integration
- Order management
- Favorites or wishlists
- Product reviews
- Vendor analytics dashboard
- Email notifications
- Background jobs
- CDN-backed image processing
- Terraform or OpenTofu infrastructure as code

## 23. Success Metrics

### Product metrics

- Vendors can publish products successfully.
- Public catalog loads reliably.
- Search and filtering return useful results.

### Learning metrics

- Interns can run the platform locally in under 30 minutes.
- Interns can complete a deployment exercise from docs.
- CI catches common mistakes before merge.
- Team can trace issues via logs and health endpoints.

## 24. Open Decisions For Implementation Phase

- Whether shoppers should be able to place orders in v1 or only browse.
- Whether store ownership should remain one-store-per-vendor or support multiple stores.
- Whether media should begin with local disk storage and later swap to S3 abstraction.
- Whether deployment should target one EC2 host first or a more distributed architecture.

Recommended default:

- Browsing-only marketplace for v1
- One store per vendor
- Local media in development, S3-compatible storage abstraction in production
- Single EC2 deployment first, then expand
