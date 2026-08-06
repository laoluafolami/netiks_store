# Netiks Store Architecture Deep Dive & Production Readiness Assessment

**Week 1 Lab Report**  
**Date:** August 4, 2026  
**Project:** Netiks Store - Multi-Vendor E-Commerce Platform  
**Assessment Type:** Architecture Analysis & Cloud Deployment Preparation

---

## Executive Summary

This report provides a comprehensive analysis of the Netiks Store application architecture, examining its microservices design, networking configuration, data persistence strategy, and production deployment readiness. The application consists of 9 interconnected services orchestrated through Docker Compose, implementing a modern microservices architecture suitable for cloud deployment.

**Key Findings:**
- The system follows a well-structured microservices pattern with clear service boundaries
- All services communicate through a central API gateway, providing a single entry point
- Data persistence is managed through Docker volumes for both database and media files
- Several critical security and configuration changes are required before cloud deployment
- The current configuration is optimized for local development and requires significant modifications for production environments

---

## Table of Contents

1. [Part 1 - Architecture Map](#part-1---architecture-map)
2. [Part 2 - Networking Investigation](#part-2---networking-investigation)
3. [Part 3 - State & Storage Audit](#part-3---state--storage-audit)
4. [Part 4 - Configuration & Secrets Review](#part-4---configuration--secrets-review)
5. [Part 5 - Production Readiness Assessment](#part-5---production-readiness-assessment)
6. [Reflections](#reflections)

---

## Part 1 - Architecture Map

### System Architecture Diagram

```
                                    ┌─────────────────┐
                                    │                 │
                                    │  User Browser   │
                                    │                 │
                                    └────────┬────────┘
                                             │
                                             │ HTTP :3001
                                             ▼
                        ┌────────────────────────────────────┐
                        │                                    │
                        │    Web Frontend (Next.js)          │
                        │    Port: 3000 (exposed as 3001)    │
                        │                                    │
                        └─────────┬──────────────────────────┘
                                  │
                                  │ HTTP :8000 (API calls)
                                  │
                                  ▼
                        ┌────────────────────────────────────┐
                        │                                    │
                        │    API Gateway (FastAPI)           │
                        │    Port: 8000                      │
                        │    Central API entry point         │
                        │                                    │
                        └─────────┬──────────────────────────┘
                                  │
                ┌─────────────────┼─────────────────┬───────────────┐
                │                 │                 │               │
                ▼                 ▼                 ▼               ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │   Identity   │  │   Vendor     │  │   Catalog    │  │    Media     │
    │   Service    │  │   Service    │  │   Service    │  │   Service    │
    │   :8001      │  │   :8002      │  │   :8003      │  │   :8004      │
    └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
           │                 │                 │                 │
           │                 │                 │                 │
           └─────────────────┴─────────────────┴─────────────────┘
                             │                 │
                             │                 │
                             ▼                 ▼
                    ┌──────────────┐    ┌────────────┐
                    │  PostgreSQL  │    │   Redis    │
                    │    :5432     │    │   :6379    │
                    │ (exposed as  │    └────────────┘
                    │   :55432)    │
                    └──────────────┘
                             
                    ┌──────────────┐
                    │    Admin     │
                    │   Service    │
                    │    :8005     │
                    └──────┬───────┘
                           │
                           ▼
                    (connects to PostgreSQL)
```
<img width="896" height="1198" alt="Gemini_Generated_Image_d3hl1xd3hl1xd3hl" src="https://github.com/user-attachments/assets/bb1aa2b1-7cf3-4fe6-9090-9634c4eadcd6" />


### Service Responsibilities

**1. Web Frontend (Port 3001)**
- Next.js-based user interface for customers and vendors
- Renders marketplace pages, product listings, and vendor dashboards
- Communicates exclusively with the API Gateway

**2. API Gateway (Port 8000)**
- Central routing hub for all backend services
- Handles authentication validation and user context extraction
- Aggregates and proxies requests to microservices
- Provides a unified API surface for the frontend

**3. Identity Service (Port 8001)**
- Manages user authentication and registration
- Issues and validates JWT tokens
- Stores user credentials securely with password hashing
- Handles login, logout, and session management

**4. Vendor Service (Port 8002)**
- Manages store creation and vendor profiles
- Handles store information updates
- Provides store lookup and vendor-store relationships

**5. Catalog Service (Port 8003)**
- Manages product creation, editing, and publishing
- Handles product categories
- Provides product search and filtering capabilities
- Manages checkout and order processing

**6. Media Service (Port 8004)**
- Handles file uploads for product images and store logos
- Validates file types and sizes
- Manages media storage (currently local disk via Docker volume)

**7. Admin Service (Port 8005)**
- Provides administrative capabilities
- Enables moderation of stores and products
- Manages platform-wide settings

**8. PostgreSQL (Port 5432, exposed as 55432)**
- Primary relational database for all services
- Stores user accounts, stores, products, categories, and orders
- Uses separate schemas for service isolation

**9. Redis (Port 6379)**
- Caching and session management support
- Provides fast data access for frequently used information

---

### Request Journey: "Buy Now" Button Click

**Scenario:** A customer clicks the "Buy Now" button on a product page to place an order.

**Step-by-Step Flow:**

1. **Browser Action**: The customer's browser initiates an HTTP POST request to the Web Frontend at `http://localhost:3001/checkout/[product-slug]` containing product details and customer information.

2. **Frontend Processing**: The Next.js application validates the form data client-side and prepares a checkout request payload containing product ID, quantity, and customer details.

3. **API Gateway Call**: The frontend sends a POST request to `http://gateway:8000/api/v1/checkout` (using the internal API URL since this is a server-side action). The gateway acts as the single entry point for all backend operations.

4. **Gateway Routing**: The API Gateway receives the request and routes it to the Catalog Service at `http://catalog-service:8003/checkout`. The gateway may validate the user's authentication token if the user is logged in.

5. **Catalog Service Processing**: The Catalog Service receives the checkout request and performs the following:
   - Validates product availability and stock levels
   - Checks product pricing and calculates total cost
   - Queries the PostgreSQL database to verify product details
   - Creates an order record in the `catalog` schema of PostgreSQL
   - Updates product stock quantities if needed

6. **Database Transaction**: PostgreSQL processes the INSERT operation to save the order, including customer information, product details, quantities, prices, and order status. This operation is atomic to ensure data consistency.

7. **Response Chain**: The Catalog Service returns a success response with the order ID back to the Gateway, which then forwards it to the Web Frontend.

8. **User Confirmation**: The frontend displays an order confirmation page to the customer with the order details and order number.

**Total Time**: Approximately 200-500ms depending on database load and network latency.

---

## Part 2 - Networking Investigation

### Question 1: Published Ports from Host Machine

**Command Executed:**
```powershell
docker compose ps
```

**Results:**

<img width="1291" height="233" alt="image" src="https://github.com/user-attachments/assets/5e4c80e9-f18b-4fae-a70c-837107a5706e" />


| Service | Container Port | Published Host Port | Accessibility |
|---------|---------------|---------------------|---------------|
| web | 3000 | 3001 | ✅ Accessible |
| gateway | 8000 | 8000 | ✅ Accessible |
| identity-service | 8001 | 8001 | ✅ Accessible |
| vendor-service | 8002 | 8002 | ✅ Accessible |
| catalog-service | 8003 | 8003 | ✅ Accessible |
| media-service | 8004 | 8004 | ✅ Accessible |
| admin-service | 8005 | 8005 | ✅ Accessible |
| postgres | 5432 | 55432 | ✅ Accessible |
| redis | 6379 | 6379 | ✅ Accessible |

**Analysis:**

From the host machine (your laptop), **all 9 services** are directly reachable. This is configured through the `ports:` directive in the `docker-compose.yml` file. Each service publishes its port using the format `"<host_port>:<container_port>"`.

For example:
- The web frontend runs on port 3000 inside its container but is exposed to the host on port 3001
- PostgreSQL runs on port 5432 inside its container but is exposed on port 55432 to avoid conflicts with any existing local PostgreSQL installations

**Key Insight:** This "publish everything" approach is convenient for local development and debugging but represents a **significant security risk** in production environments.

---

### Question 2: Internal Service Discovery

**Command Executed and Result:**

<img width="1240" height="112" alt="image" src="https://github.com/user-attachments/assets/e3e42c34-d89d-4def-b712-0a8182fcb1d4" />

```powershell
docker compose exec gateway python -c "import socket; print('catalog-service resolves to:', socket.gethostbyname('catalog-service')); print('postgres resolves to:', socket.gethostbyname('postgres')); print('redis resolves to:', socket.gethostbyname('redis'))"
```

**Results:**
```
catalog-service resolves to: 172.19.0.6
postgres resolves to: 172.19.0.4
redis resolves to: 172.19.0.2
```

**How Service Discovery Works:**

Docker Compose creates a **private internal network** for all services defined in the compose file. Each service is assigned:
1. A **service name** that acts as a DNS hostname (e.g., `catalog-service`, `postgres`, `redis`)
2. An **internal IP address** from Docker's bridge network (in the 172.19.0.x range in this case)

**Technical Explanation:**

When a service needs to communicate with another service, it uses the service name as the hostname. Docker's embedded DNS server automatically resolves these names to the correct container IP addresses. This happens completely within Docker's internal network and doesn't require any external DNS configuration.

For example, when the gateway needs to call the catalog service, it makes a request to `http://catalog-service:8003`. Docker's DNS resolves `catalog-service` to `172.19.0.7`, and the request reaches the correct container.

**Key Benefits:**
- **Automatic service discovery** - No need to manually configure IP addresses
- **Network isolation** - Internal communication doesn't expose services to the host network unless explicitly published
- **Dynamic IP management** - Container IPs can change; service names remain constant
- **Simplified configuration** - Services reference each other by name, making the configuration portable

---

### Question 3: Frontend API URLs - Two Different Configurations

**Configuration from `.env.example`:**
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
INTERNAL_API_BASE_URL=http://gateway:8000/api/v1
```

**Why Two URLs Are Necessary:**

Next.js applications execute code in **two different environments**:

1. **Client-Side (Browser)**: Code that runs in the user's web browser
2. **Server-Side (Next.js Server)**: Code that runs during Server-Side Rendering (SSR) or API routes

**Detailed Explanation:**

**`NEXT_PUBLIC_API_BASE_URL` (http://localhost:8000/api/v1)**
- **Used by:** Client-side code running in the user's browser
- **Why this URL:** When code runs in the browser, it cannot access Docker's internal network. The browser doesn't know what `gateway` means as a hostname.
- **How it works:** The browser makes HTTP requests from the user's machine to `localhost:8000`, which is the published port that maps to the gateway service.
- **Example use case:** When a user clicks a button to fetch products, the JavaScript running in their browser uses this URL.

**`INTERNAL_API_BASE_URL` (http://gateway:8000/api/v1)**
- **Used by:** Server-side code running inside the Next.js container
- **Why this URL:** The Next.js container runs within Docker's internal network and can directly communicate with other containers using service names.
- **How it works:** During server-side rendering, the Next.js container makes requests to `http://gateway:8000`, which Docker's DNS resolves to the gateway container.
- **Example use case:** When Next.js pre-renders a product page on the server, it uses this URL to fetch data before sending HTML to the browser.

**Why One URL Cannot Work for Both:**

- If we only used `http://localhost:8000` for server-side code, it wouldn't work because `localhost` inside a container refers to that container itself, not the host machine or other containers.
- If we only used `http://gateway:8000` for client-side code, it wouldn't work because the user's browser cannot resolve the Docker service name `gateway`.

**Cloud Deployment Impact:**

In production, both URLs would likely point to the same public domain:
```
NEXT_PUBLIC_API_BASE_URL=https://api.netiks.com/api/v1
INTERNAL_API_BASE_URL=https://api.netiks.com/api/v1
```

Or maintain internal networking:
```
NEXT_PUBLIC_API_BASE_URL=https://api.netiks.com/api/v1
INTERNAL_API_BASE_URL=http://gateway:8000/api/v1
```

---

### Question 4: Database Port Configuration - 5432 vs 55432

**Configuration from `docker-compose.yml`:**
```yaml
postgres:
  ports:
    - "${POSTGRES_EXPOSE_PORT:-55432}:5432"
```

**Why Both Ports Exist Simultaneously:**

This is a **port mapping** configuration where:
- **5432** is the internal container port (left side of the colon after the first colon)
- **55432** is the external host port (left side of the mapping)

**Detailed Explanation:**

**Inside Docker's Network (Port 5432):**
- All services within the Docker Compose network connect to PostgreSQL on port **5432**
- For example, the catalog-service uses the connection string: `postgresql://postgres:postgres@postgres:5432/netiks_store`
- The hostname `postgres` resolves to the PostgreSQL container, and port 5432 is PostgreSQL's default port
- This is the "native" port that PostgreSQL listens on within its container

**From Host Machine (Port 55432):**
- Your laptop can connect to PostgreSQL on port **55432**
- For example: `psql -h localhost -p 55432 -U postgres -d netiks_store`
- This is the "published" port that Docker maps to the container's internal port 5432

**Why Use Port 55432 Instead of 5432?**

1. **Conflict Avoidance**: Many developers have PostgreSQL installed locally, which typically runs on port 5432. Using 55432 prevents port conflicts.
2. **Multiple Projects**: If you run multiple projects with PostgreSQL containers, each can expose a different host port (55432, 55433, etc.) while all internally use 5432.
3. **Security Consideration**: Using non-standard ports can provide a minor security-through-obscurity benefit.

**Analogy for Non-Technical Understanding:**

Think of this like an apartment building:
- **Port 5432** is the apartment number where PostgreSQL lives inside the building (Docker network)
- **Port 55432** is the street address where visitors from outside (your host machine) can find the building entrance
- Residents inside the building (other containers) use the apartment number (5432) directly
- Visitors from outside (your laptop) use the street address (55432), which the building's reception (Docker) redirects to the correct apartment

---

## Part 3 - State & Storage Audit

### Named Volumes Inventory

**Command Executed:**
```powershell
docker volume ls
docker volume inspect netiks_store_postgres_data
docker volume inspect netiks_store_media_uploads
```

<img width="1004" height="348" alt="image" src="https://github.com/user-attachments/assets/2b4cc09c-8f0a-4d77-932a-61bf67db66ad" />

<img width="1004" height="358" alt="image" src="https://github.com/user-attachments/assets/6e45ba97-f819-4085-ae03-0674a38cc60b" />


**Identified Volumes:**

| Volume Name | Storage Purpose | Service Owner | Location | Critical Data |
|-------------|----------------|---------------|----------|---------------|
| `netiks_store_postgres_data` | Database files | postgres | `/var/lib/postgresql/data` | ✅ Yes - All application data |
| `netiks_store_media_uploads` | Uploaded media files | media-service | `/app/uploads` | ✅ Yes - Product images, store logos |

---

### Volume 1: postgres_data

**What It Stores:**
- All PostgreSQL database files including:
  - User accounts and credentials (identity schema)
  - Store information and vendor profiles (vendor schema)
  - Product catalog, categories, and inventory (catalog schema)
  - Order history and transaction records
  - Admin moderation logs
  - Database indexes and system tables

**Why It Matters:**
This volume contains **100% of the application's structured data**. Without it, the application would be completely empty - no users, no stores, no products, no orders.

**Mount Configuration:**
```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

**Physical Location on Host:**
```
/var/lib/docker/volumes/netiks_store_postgres_data/_data
```

---

### Volume 2: media_uploads

**What It Stores:**
- Product images uploaded by vendors
- Store logos and banners
- Any other media assets

**Why It Matters:**
This volume contains all the visual content that makes the marketplace appealing and functional. Without it, all products would appear without images, and stores would lack branding.

**Mount Configuration:**
```yaml
media-service:
  volumes:
    - media_uploads:/app/uploads
```

**Physical Location on Host:**
```
/var/lib/docker/volumes/netiks_store_media_uploads/_data
```

---

### Data Persistence Proof

**Test Procedure:**
1. Verify current application state by checking the marketplace page at `http://localhost:3001/market`

<img width="1004" height="668" alt="image" src="https://github.com/user-attachments/assets/41ff660e-ed77-41ca-ae06-72e60edc4622" />

2. Execute `docker compose down` (WITHOUT the `-v` flag)

<img width="933" height="347" alt="image" src="https://github.com/user-attachments/assets/8828cba9-7909-41d2-b331-9178369a34d3" />

3. Execute `docker compose up -d` to restart the stack

<img width="952" height="455" alt="image" src="https://github.com/user-attachments/assets/ab8aaaf0-f591-4b1c-93d1-d44f9241a27c" />

4. Re-check the marketplace page

**Expected Result:**
All seeded products, stores, and uploaded images remain intact after the restart. The application state is fully preserved.

<img width="1004" height="668" alt="image" src="https://github.com/user-attachments/assets/fa84fec5-cf62-4976-a451-9b44ea1c9271" />

**Why This Works:**

When you run `docker compose down`:
- Containers are **stopped and removed**
- Container filesystems are **deleted**
- **Named volumes are preserved** (unless `-v` flag is used)
- Volume data persists on the host filesystem

When you run `docker compose up -d`:
- New containers are created
- Named volumes are **reattached** to the new containers
- The PostgreSQL container finds all its existing database files
- The media-service container finds all existing uploaded images
- The application resumes with all previous data intact

**What Would Happen With `docker compose down -v`:**

The `-v` flag tells Docker to delete volumes along with containers. This would:
1. **Delete** `netiks_store_postgres_data` → All database records lost
2. **Delete** `netiks_store_media_uploads` → All uploaded images lost
3. Require complete **re-seeding** of the database
4. Require **re-uploading** all product images and store logos
5. Reset the application to a **fresh installation state**

**Critical Takeaway:** Named volumes are Docker's solution for persistent data. They survive container restarts, updates, and recreations—but they can be destroyed with the `-v` flag.

---

### Product Image Storage Location

**Where Uploaded Files End Up:**

When a vendor uploads a product image through the media-service:

1. **Upload Path**: `POST http://localhost:8004/uploads`
2. **Storage Location**: Files are written to `/app/uploads` inside the media-service container
3. **Volume Mapping**: This directory is backed by the `media_uploads` Docker volume
4. **Physical Location**: Actual files reside in `/var/lib/docker/volumes/netiks_store_media_uploads/_data` on the host machine

**Cloud Deployment Implications:**

**Current Approach (Local Disk Storage):**
- ✅ Simple and works well for development
- ✅ No external dependencies or costs
- ❌ **Critical Risk**: If the VM's disk fails, all images are permanently lost
- ❌ **Scaling Issue**: Cannot easily share images across multiple server instances
- ❌ **Backup Complexity**: Requires file-level backups in addition to database backups

**Recommended Cloud Approach:**

Use **object storage services** like Amazon S3, Google Cloud Storage, or Azure Blob Storage:
- ✅ **Durability**: 99.999999999% (11 nines) durability - files are replicated across multiple data centers
- ✅ **Availability**: Accessible from multiple servers, enabling horizontal scaling
- ✅ **Automatic Backups**: Cloud providers handle redundancy and backups
- ✅ **Cost-Effective**: Pay only for storage used; no need to provision disk space
- ✅ **CDN Integration**: Can serve images through Content Delivery Networks for faster global access

**What Happens If VM Disk Dies:**

With current local storage:
1. All uploaded product images are **permanently lost**
2. Products will display without images (broken image links)
3. Vendors must **re-upload all media**
4. Customer experience severely degraded
5. No recovery possible unless you have external backups

With S3 or similar object storage:
1. Images remain **safe and accessible** even if the VM is completely destroyed
2. Simply point a new VM to the same S3 bucket
3. Application continues serving images without interruption
4. Zero data loss scenario

---

### Redis Storage Analysis

**What Redis Stores in Netiks Store:**

Based on the configuration, Redis is available for:
1. **Session caching** (if implemented)
2. **Rate limiting data** for API endpoints
3. **Temporary cached data** to reduce database queries
4. **Background job queues** (if implemented in future)

**Current Usage:**
Redis is provisioned but appears to be **lightly used or reserved for future features**. The current architecture primarily relies on PostgreSQL for all persistent data.

**Data Loss Impact Analysis:**

**If Redis Container Is Deleted:**

**Potential Losses:**
- Cached data would be lost (needs to be rebuilt from database)
- Active sessions might be interrupted
- Rate limiting counters would reset
- Background job queues would be cleared

**Is This Loss Acceptable?**

**Yes, for most scenarios:**
- ✅ Redis data is **ephemeral by design** - it's meant to be rebuilt
- ✅ No permanent business data is stored in Redis
- ✅ Application can regenerate cached data from PostgreSQL
- ✅ User impact is minimal - worst case is slightly slower performance while cache rebuilds
- ✅ Sessions can be re-established through new logins

**When It Becomes Critical:**
- ⚠️ If Redis is used for critical rate limiting (e.g., preventing abuse), resets could allow rate limit bypass
- ⚠️ If background job queues contain time-sensitive tasks, those tasks would be lost
- ⚠️ High-traffic periods could see performance degradation while cache rebuilds

**Best Practice:**
- Redis should **never** be the primary storage for any data you cannot afford to lose
- Always design Redis usage to be **recoverable from other sources**
- Consider Redis persistence (RDB snapshots or AOF logs) for production environments if uptime is critical

---

## Part 4 - Configuration & Secrets Review

### Environment Variables Configuration Table

| Variable | What it controls | Safe to commit to Git? | Must change for cloud? |
|----------|------------------|------------------------|------------------------|
| `NEXT_PUBLIC_API_BASE_URL` | Public API endpoint for browser requests | ✅ Yes (example only) | ✅ Yes - Change to cloud domain |
| `INTERNAL_API_BASE_URL` | Server-side API endpoint | ✅ Yes (example only) | ⚠️ Maybe - Depends on architecture |
| `GATEWAY_PORT` | Gateway service port number | ✅ Yes | ❌ No - Internal port |
| `IDENTITY_SERVICE_PORT` | Identity service port | ✅ Yes | ❌ No - Internal port |
| `VENDOR_SERVICE_PORT` | Vendor service port | ✅ Yes | ❌ No - Internal port |
| `CATALOG_SERVICE_PORT` | Catalog service port | ✅ Yes | ❌ No - Internal port |
| `MEDIA_SERVICE_PORT` | Media service port | ✅ Yes | ❌ No - Internal port |
| `ADMIN_SERVICE_PORT` | Admin service port | ✅ Yes | ❌ No - Internal port |
| `MEDIA_SERVICE_URL` | Internal media service URL | ✅ Yes | ❌ No - Service name consistent |
| `IDENTITY_SERVICE_URL` | Internal identity service URL | ✅ Yes | ❌ No - Service name consistent |
| `VENDOR_SERVICE_URL` | Internal vendor service URL | ✅ Yes | ❌ No - Service name consistent |
| `CATALOG_SERVICE_URL` | Internal catalog service URL | ✅ Yes | ❌ No - Service name consistent |
| `POSTGRES_DB` | Database name | ✅ Yes | ❌ No - Can remain same |
| `POSTGRES_USER` | Database username | ❌ **NO - SECURITY RISK** | ✅ **YES - CRITICAL** |
| `POSTGRES_PASSWORD` | Database password | ❌ **NO - SECURITY RISK** | ✅ **YES - CRITICAL** |
| `POSTGRES_HOST` | Database hostname | ✅ Yes | ❌ No - Service name consistent |
| `POSTGRES_PORT` | Internal database port | ✅ Yes | ❌ No - Internal port |
| `POSTGRES_EXPOSE_PORT` | Host-exposed database port | ✅ Yes | ✅ Yes - Should NOT be exposed |
| `WEB_EXPOSE_PORT` | Host port for web frontend | ✅ Yes | ✅ Yes - Behind reverse proxy |
| `REDIS_URL` | Redis connection string | ✅ Yes | ❌ No - Service name consistent |
| `JWT_SECRET` | Secret key for JWT signing | ❌ **NO - SECURITY RISK** | ✅ **YES - CRITICAL** |
| `JWT_ALGORITHM` | JWT signing algorithm | ✅ Yes | ❌ No - Standard algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | ✅ Yes | ⚠️ Maybe - Consider shortening |
| `UPLOAD_DIR` | Media upload directory path | ✅ Yes | ✅ Yes - Change to S3 config |

---

### Security Problems with Current Configuration

**Critical Security Issues for Cloud Deployment:**

#### 1. Default Database Credentials
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

**Problem:**
- Using the default username "postgres" with the simple password "postgres" is a well-known default
- Attackers routinely scan for databases with default credentials
- If the database port is exposed, it can be compromised in minutes

**Risk Level:** 🔴 **CRITICAL**

**Recommended Fix:**
- Generate a strong, random password (minimum 20 characters, mixed case, numbers, symbols)
- Use a non-default username
- Store in environment-specific secret management (AWS Secrets Manager, Azure Key Vault, etc.)

Example:
```
POSTGRES_USER=netiks_prod_db_admin_2026
POSTGRES_PASSWORD=Xk9#mP2$vL8qR5@nB3wT7&hF4*dC6!jN
```

---

#### 2. Weak JWT Secret
```
JWT_SECRET=change-this-to-a-32-char-minimum-secret
```

**Problem:**
- The value literally says "change-this", indicating it's a placeholder
- Even though it meets the 32-character minimum, it's predictable
- A weak JWT secret allows attackers to forge authentication tokens

**What JWT_SECRET Controls:**

The JWT_SECRET is used to **cryptographically sign** authentication tokens. When a user logs in:
1. The identity-service generates a JWT token containing user information
2. This token is **signed** using the JWT_SECRET
3. The signature proves the token hasn't been tampered with
4. Services verify the signature before trusting the token's contents

**What An Attacker Could Do With The Secret:**

If an attacker discovers the JWT_SECRET, they can:
- ✅ **Forge valid tokens** for any user account, including administrators
- ✅ **Bypass authentication** entirely by creating their own tokens
- ✅ **Impersonate any user** without knowing passwords
- ✅ **Access all protected endpoints** and perform administrative actions
- ✅ **Create new admin accounts** or modify existing data
- ✅ **Steal customer information, vendor data, and order history**

**Real-World Attack Scenario:**
1. Attacker finds JWT_SECRET in a misconfigured cloud environment or GitHub repository
2. Attacker creates a JWT token with `{"user_id": "admin", "role": "admin"}`
3. Attacker signs it with the stolen JWT_SECRET
4. Attacker uses this forged token to access all admin endpoints
5. Entire platform is compromised without any login attempts

**Risk Level:** 🔴 **CRITICAL**

**Recommended Fix:**
- Generate a cryptographically strong random secret (64+ characters)
- Never use readable words or patterns
- Store in secure secret management system
- Rotate periodically (every 90 days)

Example generation:
```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(64))"

# Using OpenSSL
openssl rand -base64 64 | tr -d '\n'
```

---

#### 3. Exposed Database Port
```
POSTGRES_EXPOSE_PORT=55432
```

**Problem:**
- The database is configured to be accessible from outside Docker
- In production, this means anyone on the internet could attempt to connect
- Combined with weak credentials, this is a disaster waiting to happen

**Risk Level:** 🔴 **CRITICAL in production**

**Recommended Fix:**
- Remove the port mapping entirely in production
- Database should **only** be accessible from within the Docker network
- Use SSH tunneling or VPN for administrative access
- Never expose databases directly to the internet

---

### Variables Requiring Changes for Cloud Deployment

**Must Change for Public Access:**

1. **`NEXT_PUBLIC_API_BASE_URL`**
   - **From:** `http://localhost:8000/api/v1`
   - **To:** `https://api.netiks.com/api/v1` or `https://yourdomain.com/api/v1`
   - **Reason:** Users' browsers need to reach the actual cloud server, not localhost

2. **`POSTGRES_PASSWORD` and `POSTGRES_USER`**
   - **From:** Default credentials
   - **To:** Strong, unique credentials stored in secrets manager
   - **Reason:** Security requirement for production environments

3. **`JWT_SECRET`**
   - **From:** Placeholder value
   - **To:** Cryptographically strong random string
   - **Reason:** Secure authentication system

4. **`UPLOAD_DIR` or add S3 Configuration**
   - **From:** `/app/uploads` (local disk)
   - **To:** S3 bucket configuration with credentials
   - **Reason:** Durable, scalable media storage

**Should Remove/Not Expose:**

5. **`POSTGRES_EXPOSE_PORT`**
   - **Action:** Remove port mapping from docker-compose
   - **Reason:** Database should never be directly accessible from internet

---

## Part 5 - Production Readiness Assessment

# What Must Change Before Netiks Store Runs in the Cloud

---

### 1. Service Exposure and Security Boundaries

**Current Issue:**

In the local development environment, all 9 services publish their ports to the host machine:
- Web frontend: 3001
- Gateway: 8000
- Identity service: 8001
- Vendor service: 8002
- Catalog service: 8003
- Media service: 8004
- Admin service: 8005
- PostgreSQL: 55432
- Redis: 6379

On a cloud VM with a public IP, **every single port would be accessible from the internet**. This means anyone could directly access any service, bypassing intended security controls.

**Why This Matters:**

1. **Direct Database Access:** Exposing PostgreSQL port 55432 allows attackers to attempt database connections, potentially compromising all application data
2. **Service Bypass:** Attackers could skip the gateway and directly call internal services, bypassing authentication checks
3. **Attack Surface:** Each exposed service is a potential entry point for attacks, DOS, or exploitation
4. **No Access Control:** Internal services lack robust authentication because they're designed to trust requests from the gateway

**Which Services Should Be Publicly Accessible:**

✅ **ONLY the Web Frontend** (currently port 3001)
- This is the user-facing application
- Should be accessed through a reverse proxy on standard ports (80/443)

**Which Services MUST NOT Be Publicly Accessible:**

❌ **Gateway (8000)** - Should only be accessible from the web frontend container  
❌ **All Microservices (8001-8005)** - Should only be accessible from the gateway  
❌ **PostgreSQL (55432)** - Should only be accessible from service containers  
❌ **Redis (6379)** - Should only be accessible from service containers

**Proposed Direction:**

1. **Remove all port mappings** from docker-compose.yml except for the web service
2. Implement a **reverse proxy** (Nginx or Caddy) to handle public traffic
3. Configure the reverse proxy to:
   - Listen on ports 80 (HTTP) and 443 (HTTPS)
   - Route requests to the web frontend
   - Route API requests to the gateway
   - Reject all other traffic
4. Services communicate only through Docker's internal network
5. Use **firewall rules** (AWS Security Groups, UFW, iptables) to block direct access to service ports

**Configuration Example:**
```yaml
# Production docker-compose.yml - No exposed ports except through reverse proxy
services:
  web:
    # No ports section - accessed only through reverse proxy
  gateway:
    # No ports section - internal only
  postgres:
    # No ports section - internal only
```

---

### 2. Traffic Entry Point and Reverse Proxy

**Current Issue:**

Local development uses `http://localhost:3001` to access the application. This doesn't work in the cloud because:
- Users are accessing from different locations worldwide
- `localhost` refers to their own computer, not your server
- Port numbers (3001, 8000) look unprofessional and confusing
- No HTTPS/TLS encryption

**What Is A Reverse Proxy:**

A reverse proxy is a server that sits between users and your application, acting as an intermediary that:
- Receives all incoming traffic from the internet
- Routes requests to the appropriate internal services
- Returns responses back to users
- Can handle SSL/TLS termination for HTTPS
- Can implement rate limiting, caching, and load balancing

**Analogy:** Think of a reverse proxy like a hotel concierge. Guests (users) don't know the internal layout of the hotel (your microservices). They ask the concierge (reverse proxy) for what they need, and the concierge knows exactly which internal department to contact.

**Why You Need It:**

1. **Single Entry Point:** Users connect to one domain (e.g., netiks.com)
2. **Standard Ports:** Access via port 80 (HTTP) or 443 (HTTPS), not custom ports
3. **SSL/TLS Termination:** Handles HTTPS encryption so internal services can use plain HTTP
4. **Request Routing:** Routes `/` to web frontend, `/api/v1/` to gateway
5. **Security Layer:** Can filter malicious requests before they reach your application
6. **Static Content:** Can serve static files efficiently without hitting application servers

**Proposed Direction:**

1. **Install Nginx or Caddy** on the cloud VM
2. **Configure routing rules:**
   ```nginx
   # Nginx example
   server {
       listen 80;
       server_name netiks.com www.netiks.com;
       
       location / {
           proxy_pass http://localhost:3000;  # Web frontend
       }
       
       location /api/v1/ {
           proxy_pass http://localhost:8000;  # Gateway
       }
   }
   ```

3. **Domain Setup:**
   - Register a domain name (e.g., netiks.com)
   - Point DNS A records to your VM's public IP address
   - Configure reverse proxy to accept requests for that domain

4. **Traffic Flow:**
   ```
   User → netiks.com:443 → Reverse Proxy → Web Frontend (3000)
   User → netiks.com/api/v1 → Reverse Proxy → Gateway (8000) → Services
   ```

**Benefits:**
- Professional domain-based access
- Secure HTTPS connections
- Internal services remain hidden
- Centralized security and monitoring

---

### 3. Secrets Management and Credential Security

**Current Issue:**

All secrets are stored in plain text in a `.env` file:
- Database credentials
- JWT signing secret
- API keys (if any)

In development, this is acceptable, but in production:
- The `.env` file might be accidentally committed to Git
- Server administrators can read all secrets
- Backup systems might expose secrets
- No audit trail of who accessed secrets
- Secrets aren't rotated or versioned

**Why This Matters:**

Compromised secrets mean:
- **Database breach:** Full access to all application data
- **Authentication bypass:** Ability to forge user tokens
- **Data theft:** Customer information, vendor data, orders
- **Service disruption:** Ability to delete or modify data
- **Regulatory violations:** GDPR, PCI-DSS, and other compliance failures

**Proposed Direction:**

**Option 1: Basic - Environment Variables from Secure Source**
1. Store secrets in server environment variables (not in files)
2. Load them when starting Docker Compose
3. Use SSH key-based access to the server
4. Implement file permissions to restrict .env access

**Option 2: Recommended - Cloud Secret Management**
1. Use **AWS Secrets Manager** or **AWS Systems Manager Parameter Store**
2. Store all secrets encrypted in AWS
3. Configure services to fetch secrets at startup
4. Rotate secrets regularly (automated)
5. Audit all secret access

**Implementation Approach:**
```yaml
# docker-compose.yml
services:
  identity-service:
    environment:
      JWT_SECRET: ${JWT_SECRET_FROM_AWS}
      POSTGRES_PASSWORD: ${DB_PASSWORD_FROM_AWS}
```

**Script to fetch secrets on startup:**
```bash
#!/bin/bash
# fetch-secrets.sh
export JWT_SECRET=$(aws secretsmanager get-secret-value --secret-id prod/jwt-secret --query SecretString --output text)
export POSTGRES_PASSWORD=$(aws secretsmanager get-secret-value --secret-id prod/db-password --query SecretString --output text)
docker-compose up -d
```

**Benefits:**
- Encrypted storage of sensitive data
- Access logging and auditing
- Automatic rotation capabilities
- No secrets in code repositories
- Compliance-ready

---

### 4. Data Protection and Backup Strategy

**Current Issue:**

All data resides on the VM's local disk:
- PostgreSQL data in Docker volume
- Uploaded media files in Docker volume

**Risks:**

1. **Hardware Failure:** If the VM's disk fails, all data is permanently lost
2. **Accidental Deletion:** Running `docker compose down -v` destroys everything
3. **Ransomware:** Malware could encrypt or delete volumes
4. **No Disaster Recovery:** Cannot restore to a previous state
5. **Single Point of Failure:** One disk failure = complete business shutdown

**Why This Matters:**

A single disk failure could result in:
- Loss of all customer accounts
- Loss of all vendor stores and products
- Loss of all order history
- Loss of all uploaded product images
- Complete business continuity failure
- Potential legal liability

**Proposed Direction:**

**For PostgreSQL Database:**

1. **Automated Backups:**
   ```bash
   # Daily backup script
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   docker exec netiks_store-postgres-1 pg_dump -U postgres netiks_store | gzip > backup_$DATE.sql.gz
   aws s3 cp backup_$DATE.sql.gz s3://netiks-backups/database/
   ```

2. **Schedule with Cron:**
   ```cron
   0 2 * * * /home/ubuntu/backup-database.sh  # Daily at 2 AM
   ```

3. **Retention Policy:**
   - Keep daily backups for 7 days
   - Keep weekly backups for 4 weeks
   - Keep monthly backups for 12 months

4. **Alternative - Managed Database:**
   - Consider **AWS RDS for PostgreSQL**
   - Automated backups included
   - Point-in-time recovery
   - Multi-AZ replication for high availability
   - Higher cost but much better reliability

**For Media Files:**

1. **Migration to S3:**
   - Move from local storage to **Amazon S3**
   - S3 provides 99.999999999% durability (11 nines)
   - Automatic replication across multiple data centers
   - Versioning capabilities
   - No backup needed - S3 handles redundancy

2. **Configuration Changes:**
   ```python
   # media-service update
   import boto3
   
   s3_client = boto3.client('s3')
   bucket_name = 'netiks-media-uploads'
   ```

**Testing Recovery:**

Regular disaster recovery drills:
1. Restore database from backup to a test environment
2. Verify data integrity
3. Test application functionality with restored data
4. Document recovery time and process

**Benefits:**
- Protection against hardware failures
- Ability to recover from mistakes
- Compliance with data protection regulations
- Business continuity assurance
- Peace of mind

---

### 5. Container Restart Policies and Service Availability

**Current Issue:**

Checking the `docker-compose.yml` file reveals **no restart policies** are configured. This means:

```yaml
services:
  web:
    build: ...
    # NO restart policy
```

**What Happens When the VM Reboots:**

1. VM shuts down (planned maintenance, crash, or update)
2. All Docker containers stop
3. VM comes back online
4. Docker daemon starts
5. **Containers DO NOT start automatically**
6. Application is completely down
7. Requires manual intervention: `docker compose up -d`

**Why This Matters:**

- **Unplanned Outages:** Surprise reboots mean extended downtime
- **Maintenance Windows:** Every OS update requires manual container restart
- **Service Level Failures:** Cannot meet uptime commitments
- **Manual Dependency:** Always requires someone to manually restart services

**Proposed Direction:**

Add restart policies to all services in `docker-compose.yml`:

```yaml
services:
  web:
    build: ...
    restart: unless-stopped
    
  gateway:
    build: ...
    restart: unless-stopped
    
  identity-service:
    build: ...
    restart: unless-stopped
    
  vendor-service:
    build: ...
    restart: unless-stopped
    
  catalog-service:
    build: ...
    restart: unless-stopped
    
  media-service:
    build: ...
    restart: unless-stopped
    
  admin-service:
    build: ...
    restart: unless-stopped
    
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    
  redis:
    image: redis:7-alpine
    restart: unless-stopped
```

**Restart Policy Options:**

- **`no`** (default): Never restart automatically
- **`always`**: Always restart, even if manually stopped
- **`on-failure`**: Only restart if container exits with error
- **`unless-stopped`**: Always restart unless explicitly stopped by admin

**Recommended: `unless-stopped`**

This policy ensures:
- ✅ Containers restart after VM reboot
- ✅ Containers restart after crashes
- ✅ Manual stops are respected (for maintenance)
- ✅ Automatic recovery from failures

**Additional Boot Configuration:**

Ensure Docker itself starts on boot:
```bash
sudo systemctl enable docker
```

**Testing:**
1. Add restart policies to docker-compose.yml
2. Start the stack: `docker compose up -d`
3. Reboot the VM: `sudo reboot`
4. After reboot, verify all containers are running: `docker compose ps`

   <img width="1236" height="171" alt="image" src="https://github.com/user-attachments/assets/d3650008-a310-467b-978a-9d9e8209030f" />

**Expected Result:**
All containers should automatically come back online within 30-60 seconds of VM boot completion.

---

### 6. HTTPS/TLS Encryption

**Current Issue:**

All communication currently uses **plain HTTP**:
- Browser to web frontend: `http://localhost:3001`
- Web to gateway API: `http://localhost:8000`
- No encryption means all data travels in plain text

**Why HTTPS Matters:**

1. **Data Privacy:** Without encryption:
   - Login credentials sent in plain text
   - JWT tokens visible to network attackers
   - Customer personal information exposed
   - Credit card details (future feature) unprotected

2. **Man-in-the-Middle Attacks:**
   - Attackers on the same network can intercept traffic
   - Passwords can be stolen
   - Session tokens can be hijacked
   - Data can be modified in transit

3. **Browser Security Warnings:**
   - Modern browsers show "Not Secure" for HTTP sites
   - Users lose trust in the application
   - Some browsers block certain features on HTTP

4. **SEO Penalties:**
   - Google ranks HTTPS sites higher
   - HTTP sites marked as "Not Secure" in search results

5. **Compliance Requirements:**
   - PCI-DSS requires HTTPS for payment processing
   - GDPR requires encryption of personal data in transit
   - Many regulations mandate HTTPS

**What HTTPS Provides:**

- **Encryption:** All data scrambled during transmission
- **Authentication:** Proof that you're connecting to the real server, not an imposter
- **Integrity:** Guarantee that data hasn't been modified in transit
- **Trust:** Green padlock icon, "Secure" label in browsers

**Proposed Direction:**

**Step 1: Obtain SSL/TLS Certificate**

**Option A - Let's Encrypt (Free, Recommended):**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d netiks.com -d www.netiks.com
```

**Option B - AWS Certificate Manager (If using AWS Load Balancer):**
- Free certificates managed by AWS
- Automatic renewal
- Integrated with ALB/CloudFront

**Step 2: Configure Nginx with HTTPS**

```nginx
server {
    listen 80;
    server_name netiks.com www.netiks.com;
    return 301 https://$server_name$request_uri;  # Redirect HTTP to HTTPS
}

server {
    listen 443 ssl http2;
    server_name netiks.com www.netiks.com;
    
    ssl_certificate /etc/letsencrypt/live/netiks.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/netiks.com/privkey.pem;
    
    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    location / {
        proxy_pass http://localhost:3000;
    }
    
    location /api/v1/ {
        proxy_pass http://localhost:8000;
    }
}
```

**Step 3: Update Application Configuration**

```env
NEXT_PUBLIC_API_BASE_URL=https://netiks.com/api/v1
```

**Step 4: Enable Automatic Certificate Renewal**

Let's Encrypt certificates expire after 90 days. Automate renewal:

```bash
# Test renewal
sudo certbot renew --dry-run

# Automatic renewal via cron (already installed by certbot)
sudo systemctl status certbot.timer
```

**What It Takes At Basic Level:**

1. **Domain Name:** Register and point DNS to your server (~$10-15/year)
2. **Certificate:** Free with Let's Encrypt
3. **Configuration:** 10-20 lines of Nginx configuration
4. **Time Investment:** 1-2 hours for first-time setup
5. **Maintenance:** Fully automated with certbot

**Benefits:**
- ✅ Secure data transmission
- ✅ User trust and browser confidence
- ✅ Compliance with security standards
- ✅ Better SEO rankings
- ✅ Protection against common attacks

---

### 7. Additional Production Concerns

**Logging and Monitoring:**

**Current State:**
- Logs go to container stdout
- No centralized log collection
- No alerting on errors

**Needed:**
- Centralized logging (AWS CloudWatch, ELK Stack, or Loki)
- Application performance monitoring
- Error tracking (Sentry, Rollbar)
- Uptime monitoring (UptimeRobot, Pingdom)

**Resource Limits:**

**Current State:**
- No memory or CPU limits on containers
- One service can consume all resources
- Potential for cascading failures

**Needed:**
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

**Health Checks:**

**Current State:**
- Only PostgreSQL has health checks
- Other services may start before they're ready

**Needed:**
```yaml
services:
  gateway:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Rate Limiting:**

**Current State:**
- No rate limiting
- Vulnerable to DOS attacks
- API abuse possible

**Needed:**
- Implement rate limiting at reverse proxy level
- Configure per-endpoint rate limits
- Add IP-based throttling

---

## Summary of Critical Changes

### Must-Have Before Cloud Deployment

| Priority | Change | Impact | Effort |
|----------|--------|--------|--------|
| 🔴 Critical | Remove database port exposure | Security | Low |
| 🔴 Critical | Change default database credentials | Security | Low |
| 🔴 Critical | Generate strong JWT secret | Security | Low |
| 🔴 Critical | Implement reverse proxy with HTTPS | Security & Functionality | Medium |
| 🔴 Critical | Add restart policies to all services | Reliability | Low |
| 🟡 High | Configure secrets management | Security | Medium |
| 🟡 High | Migrate media to S3 | Durability | Medium |
| 🟡 High | Implement database backup strategy | Data Protection | Medium |
| 🟢 Medium | Add health checks to all services | Reliability | Low |
| 🟢 Medium | Configure resource limits | Stability | Low |
| 🟢 Medium | Set up centralized logging | Observability | Medium |

### Deployment Readiness Checklist

- [ ] All services configured with restart: unless-stopped
- [ ] Database credentials changed from defaults
- [ ] JWT secret replaced with cryptographically strong value
- [ ] Port mappings removed (except through reverse proxy)
- [ ] Nginx/Caddy configured as reverse proxy
- [ ] SSL/TLS certificate obtained and configured
- [ ] Domain name registered and DNS configured
- [ ] HTTPS enforced for all traffic
- [ ] Secrets stored in AWS Secrets Manager or equivalent
- [ ] Media uploads configured to use S3
- [ ] Database backup script created and scheduled
- [ ] Backup restore procedure tested
- [ ] Monitoring and alerting configured
- [ ] Firewall rules configured on VM
- [ ] Security group rules configured (AWS)
- [ ] Health checks implemented for all services
- [ ] Resource limits defined for containers
- [ ] Documentation updated for production environment

---

## Reflections

### What I Found Hardest This Week

The most challenging aspect of this week's deep dive was fully understanding the **security implications of the current configuration** and how seemingly innocent development conveniences become critical vulnerabilities in production environments.

Initially, having all services expose their ports seemed logical for development - it makes debugging easy and allows direct access to each service. However, realizing that this same configuration on a public cloud VM would expose the database, all microservices, and Redis directly to the internet was eye-opening. The concept of "default secure" vs. "default convenient" became very clear.

The second challenge was grasping the **dual-environment nature of Next.js** and why two different API URLs are necessary. Understanding that JavaScript executes in fundamentally different contexts (browser vs. server) and that Docker's internal DNS is only available within the container network required mental shifting between these two perspectives.

Finally, working through the **data persistence concepts** with Docker volumes highlighted how easy it is to accidentally destroy data with a single flag (`-v`). This reinforced the critical importance of backup strategies and durable storage solutions like S3 for production environments.

This week transformed my understanding from "how to run the application locally" to "how to architect for production safely and reliably." The knowledge gained will be essential for Week 2's cloud deployment.

---

## Appendix: Quick Reference Answers

### Three Critical Questions

**1. Which containers must never be exposed to the public internet, and why?**

**Answer:** PostgreSQL, Redis, and ALL backend microservices (identity, vendor, catalog, media, admin services) must never be directly exposed. 

- **PostgreSQL** contains all application data and credentials - exposure allows direct database access and potential data theft
- **Redis** may contain session data and cache - exposure allows session hijacking and cache poisoning
- **Backend microservices** lack robust authentication since they trust the gateway - direct exposure bypasses security controls and allows unauthorized access to sensitive operations

Only the web frontend should be accessible publicly, and only through a reverse proxy with HTTPS.

---

**2. Where does the data live, and what single command would destroy it?**

**Answer:** Data lives in two Docker named volumes:

1. **`netiks_store_postgres_data`** - Contains all database records (users, stores, products, orders)
2. **`netiks_store_media_uploads`** - Contains all uploaded images and media files

**The command that would destroy all data:**
```bash
docker compose down -v
```

The `-v` flag tells Docker to delete volumes along with containers, resulting in:
- Complete loss of all database records
- Permanent deletion of all uploaded media
- No recovery possible without external backups
- Application reset to fresh installation state

**Safe command to restart without data loss:**
```bash
docker compose down     # Without -v flag
docker compose up -d
```

---

**3. What three things would you change in `.env` before deploying tomorrow?**

**Answer:**

**Change 1: Database Credentials**
```bash
# FROM (INSECURE):
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# TO (SECURE):
POSTGRES_USER=netiks_prod_admin_2026
POSTGRES_PASSWORD=Xk9#mP2$vL8qR5@nB3wT7&hF4*dC6!jN
# Generated with: openssl rand -base64 32
```

**Change 2: JWT Secret**
```bash
# FROM (INSECURE):
JWT_SECRET=change-this-to-a-32-char-minimum-secret

# TO (SECURE):
JWT_SECRET=c3VwZXJfc2VjcmV0X2tleV90aGF0X2lzX3ZlcnlfbG9uZ19hbmRfcmFuZG9tXzIwMjY=
# Generated with: python -c "import secrets; print(secrets.token_urlsafe(64))"
```

**Change 3: API Base URL**
```bash
# FROM (LOCAL):
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1

# TO (CLOUD):
NEXT_PUBLIC_API_BASE_URL=https://api.netiks.com/api/v1
# Or whatever your actual domain will be
```

**Why These Matter:**
- **Database credentials:** Prevent unauthorized database access and data breaches
- **JWT secret:** Prevent authentication bypass and user impersonation
- **API URL:** Enable browsers to connect to the actual cloud server instead of localhost

---

## Conclusion

Netiks Store is a well-architected microservices application that demonstrates modern cloud-native principles. The current implementation works excellently for local development, providing clear service boundaries, proper data persistence, and a realistic multi-vendor marketplace experience.

However, transitioning from local development to production cloud deployment requires significant configuration and architectural changes. The primary concerns center around:

1. **Security:** Removing exposed services, implementing strong credentials, and adding HTTPS
2. **Reliability:** Configuring automatic restarts, implementing backups, and using durable storage
3. **Accessibility:** Setting up proper domain-based routing through a reverse proxy

None of these changes require fundamental architectural redesign. The microservices structure is sound and production-ready. The required changes are primarily operational and configurational in nature, which is exactly what Week 2's deployment exercises will address.

The knowledge gained this week provides a solid foundation for understanding not just how to deploy the application, but **why** each production configuration exists and what problems it solves. This understanding is essential for maintaining and troubleshooting the application in real-world cloud environments.

---

**Report Prepared By:** Afolami Olaoluwa   
**Date:** August 6, 2026  
**Next Steps:** Week 2 - Cloud VM Deployment  

---

*End of Report*


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
