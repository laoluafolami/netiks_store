# Netiks Store Intern Quickstart Guide

## What This Project Is

Netiks Store is a multi-vendor e-commerce application.

It includes:

- a public storefront
- a seller registration and login flow
- a seller dashboard
- product publishing
- checkout
- stock and sales tracking

## Architecture At A Glance

The project is made up of:

- `apps/web`
  The frontend application customers and sellers use in the browser.
- `apps/gateway`
  The API gateway used by the frontend.
- `services/identity-service`
  Handles registration, login, and user identity.
- `services/vendor-service`
  Handles stores and seller data.
- `services/catalog-service`
  Handles categories, products, checkout, and order records.
- `services/media-service`
  Handles uploaded images.
- `services/admin-service`
  Reserved for admin features.
- `postgres`
  Main database.
- `redis`
  Supporting service.

## First Task

Your first task is to run the project locally and prove that it is working.

You must submit proof that:

- Docker containers started successfully
- the website opened in the browser
- the application is reachable at `http://localhost:3001`

## How To Run The Project

1. Install Docker Desktop.
2. Open Docker Desktop and wait until Docker is running.
3. Open the project folder in your terminal.
4. Copy `.env.example` to `.env` if `.env` does not already exist.
5. Run:

```bash
docker compose up --build -d
```

6. Wait for the containers to finish starting.
7. Open:

```text
http://localhost:3001
```

## How To Confirm It Is Running

Run:

```bash
docker compose ps
```

You should see containers for:

- `web`
- `gateway`
- `identity-service`
- `vendor-service`
- `catalog-service`
- `media-service`
- `admin-service`
- `postgres`
- `redis`

You can also test these URLs:

- Frontend: `http://localhost:3001`
- API health: `http://localhost:8000/health/live`

## Proof To Submit

You can submit:

- a screenshot of `docker compose ps`
- a screenshot of the home page or market page
- a short note saying the app opened successfully at `http://localhost:3001`

## If You Want Fresh Marketplace Data

After the stack is running, use:

```bash
npm run seed:demo
```

This loads:

- seller accounts
- stores
- categories
- products
- product images
- starter order activity

## Basic User Flow To Understand

### Customer flow

1. Open the market page.
2. Browse products.
3. Open a product details page.
4. Continue to checkout.
5. Place an order.

### Seller flow

1. Register a seller account.
2. Log in.
3. Create a store.
4. Create a category.
5. Publish a product.
6. Confirm the product appears on the market page.
7. Track orders and sales in the dashboard.

## If Something Goes Wrong

Try these steps:

1. Make sure Docker Desktop is running.
2. Run:

```bash
docker compose ps
```

3. If containers are not running, run:

```bash
docker compose up --build -d
```

4. If you want to stop everything:

```bash
docker compose down
```

5. Then start again:

```bash
docker compose up --build -d
```

## Expected Outcome

By the end of the first task, you should be able to:

- start the project with Docker
- open the frontend in your browser
- explain the main services in simple terms
- show proof that the application is running correctly
