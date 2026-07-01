# Project Execution Report: Netiks Store Microservices Platform.
## 1. Project Overview.
The objective of this task was to successfully deploy and run the Netiks Store, a multi-vendor e-commerce microservices platform, locally using Docker. This project utilizes a distributed architecture consisting of a Next.js frontend, a Python FastAPI backend ecosystem, and supporting infrastructure (PostgreSQL and Redis).

## 2. Starting the Project with Docker.
To ensure a clean and reproducible environment, the application was orchestrated using Docker Compose. The following steps were executed in the terminal:
### Step 1: Environment Configuration.
Created the local environment variables file required by the Docker containers:

![alt text](image.png)

### Step 2: Building and Starting the Containers.
Launched the entire microservices stack in detached (background) mode. This command built the custom Docker images for the Next.js frontend and Python services, and pulled the official images for the database and cache:

<img width="349" height="85" alt="image" src="https://github.com/user-attachments/assets/638292c0-0279-4f41-ba1d-17a5ed3a97a5" />


### Step 3: Seeding the Database.
To populate the empty database with demo vendors, categories, and products, the seeding script was executed. (Note: An environment variable DOCKER_BIN=docker was prepended to resolve a hardcoded macOS file path in the original script, adapting it for my Linux/WSL environment).

![alt text](image-2.png)

## 3. Explanation of Main Services.
The Netiks Store is built on a Microservices Architecture. Instead of one massive application doing everything, the system is broken down into specialized, independent services that talk to each other. Here is what each main service does in simple terms:
### Frontend (Next.js) - The Storefront.
This is the visual part of the application that the customer interacts with. It displays the products, handles the shopping cart UI, and provides a responsive, fast user experience.
### API Gateway (FastAPI) - The Traffic Cop.
The frontend doesn't talk to the database directly. Instead, it sends all its requests to the API Gateway. The Gateway acts like a receptionist, looking at the request and directing it to the correct backend service (e.g., "You want product details? Go talk to the Catalog Service.").
### Identity Service - The Security Guard.
This service handles everything related to users. It manages registration, logins, password hashing, and session tokens to ensure only authorized users can access certain features.
### Catalog Service - The Inventory Manager.
This is the brain behind the products. It stores and retrieves information about items, categories, prices, and stock levels. When you view a product page, the Catalog Service is providing that data.
### Vendor Service - The Landlord.
Because this is a multi-vendor marketplace (like Amazon or Etsy), this service manages the sellers. It keeps track of which store owns which products, store names, and vendor profiles.
### PostgreSQL - The Filing Cabinet.
This is the relational database where all the permanent, structured data lives. Every product, user, and order is safely stored in organized tables here.
### Redis - The Sticky Note / Whiteboard.
This is an in-memory data store. It is incredibly fast and is used to store temporary data that needs to be accessed quickly, such as active user sessions, caching frequently viewed products, or managing shopping carts.

## 4. Proof of Execution.
### A. Docker Container Status.
The following output verifies that all microservices and infrastructure components are successfully built, running, and healthy.

![alt text](image-3.png)

![alt text](image-4.png)

## B. Application Frontend Verification
The application was accessed via a web browser to verify that the frontend is successfully communicating with the API Gateway and rendering the seeded demo data.

![alt text](image-5.png)
![alt text](image-6.png)
![alt text](image-7.png)
## Market
![alt text](image-8.png)
![alt text](image-9.png)
## Vendor Access
![alt text](image-10.png)
### C. Access URLs
The application was successfully verified using the following local URLs:
- Main Storefront (Frontend): http://localhost:3001
- API Gateway (Backend Entry Point): http://localhost:8000
- Database (PostgreSQL): localhost:55432

## 5. Conclusion
The Netiks Store microservices platform was successfully deployed locally. All containers initialized correctly, database migrations were applied seamlessly, and the frontend successfully rendered the seeded marketplace data, proving that the service-to-service communication is fully operational.

#
# Netiks Store

Netiks Store is a multi-vendor e-commerce platform with a storefront, seller dashboard, checkout flow, and supporting backend services.

## Workspace Layout

```text
apps/
  web/
  gateway/
services/
  identity-service/
  vendor-service/
  catalog-service/
  media-service/
  admin-service/
packages/
  shared-python/
  shared-types/
infra/
  docker/
  nginx/
  aws/
docs/
```

## Quick Start

1. Copy `.env.example` to `.env`.
2. Install frontend dependencies with `npm install`.
3. Sync Python workspaces with `uv sync`.
4. Start Docker Desktop and wait until it shows that Docker is running.
5. Start the stack with `docker compose up --build -d`.
6. Open `http://localhost:3001`.

## First Task For Interns

The first task is to run the project locally with Docker and show proof that it is working.

Suggested proof:

- a screenshot of Docker Desktop or `docker compose ps`
- a screenshot of the home page or market page in the browser
- a short note showing the URL used: `http://localhost:3001`

## Demo Data Reset

Run `npm run seed:demo` while the Docker stack is up to load the default marketplace data:

- 3 vendor accounts with storefronts
- 3 stores and categories
- 6 published products with real product photos
- starter order history that updates stock and sold counts

## Current Working Backend Surface

The following flows are implemented and have been smoke-tested locally:

- Auth: register, login, `me`, refresh-token rotation
- Vendor: create store, get my store, public store lookup, store update
- Catalog: create/list categories, create/update products, public published-product lookup, owner product listing
- Media: authenticated upload through the gateway, direct media retrieval

Services that still need further expansion:

- richer admin moderation flows
- full product search/filtering
- cross-service ownership verification between catalog and vendor domains

## Local Service Endpoints

- Frontend: `http://localhost:3001` by default in Docker Compose
- Gateway: `http://localhost:8000`
- Identity: `http://localhost:8001`
- Vendor: `http://localhost:8002`
- Catalog: `http://localhost:8003`
- Media: `http://localhost:8004`

## Docker Notes

- Each backend service runs Alembic migrations on container startup.
- The repo includes a root `.dockerignore` to keep build contexts smaller for GitHub and CI.
- If port `5432` is already in use on a machine, set `POSTGRES_EXPOSE_PORT` in `.env` before running Compose.
- If the stack has already been run before and you want clean marketplace data again, use `npm run seed:demo`.
- If you change code and want to rebuild everything, run `docker compose up --build -d` again.

## Documentation

- [Intern Quickstart Guide](/Users/woron/Documents/netiks-store/docs/INTERN_QUICKSTART_GUIDE.md)
- [PRD](/Users/woron/Documents/netiks-store/docs/PRD.md)
- [Project Documentation](/Users/woron/Documents/netiks-store/docs/PROJECT_DOCUMENTATION.md)
- [Technical Plan](/Users/woron/Documents/netiks-store/docs/TECHNICAL_PLAN.md)
- [Deployment Challenge Lab](/Users/woron/Documents/netiks-store/docs/DEPLOYMENT_CHALLENGE_LAB.md)
