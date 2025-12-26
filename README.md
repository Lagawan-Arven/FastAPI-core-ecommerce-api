# 🛒 FastAPI Mini E-Commerce API

A production-ready **backend e-commerce REST API** built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, featuring JWT authentication, role-based access control, transactional checkout, pagination, logging, testing, and Dockerized deployment.

This project is designed as a **backend portfolio project** showcasing real-world API architecture and best practices.

---

## 🚀 Features

### 🔐 Authentication & Authorization
- JWT-based authentication
- OAuth2 password flow
- Role-based access control (`user`, `admin`)
- Admin-only endpoints

### 👤 Users
- User registration & login
- Admin user creation
- View users (admin only)
- Delete users (admin only)

### 🛍 Products
- Create, update, delete products (admin)
- View products (authenticated users)
- Stock management

### 🛒 Cart
- Add/remove products to cart
- View cart contents
- Checkout selected items
- Checkout all items
- Stock validation

### 📦 Orders
- Create orders
- View all orders (admin)
- Order-product many-to-many relationship

### 🧱 Architecture & Quality
- SQLAlchemy ORM with relationships
- Pydantic schemas (request/response models)
- Dependency injection
- Database transactions for critical operations
- Pagination on list endpoints
- Structured logging
- Integration tests with pytest
- Docker & Docker Compose support

---

## 🧰 Tech Stack

- **Python 3.11**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **JWT (python-jose)**
- **Passlib (bcrypt)**
- **Pytest**
- **Docker & Docker Compose**
- **Uvicorn**

---

## ⚙️ Environment Variables

Create a `.env` file at the project root:
- DB_USER=postgres
- DB_PASSWORD=postgres
- DB_HOST=db
- DB_PORT=5432
- DB_NAME=ecommerce_db

- SECRET_KEY=supersecretkey
- ALGORITHM=HS256

- POSTGRES_USER =postgres
- POSTGRES_PASSWORD =postgres
- POSTGRES_DB =ecommerce_db

> ⚠️ **Do not commit `.env` files to GitHub**

---

## 🐳 Docker Setup (Recommended)

### Build & Run API + PostgreSQL
- docker compose up --build

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

---

## 🗄 Database Migrations

This project is designed to work with **Alembic**.

After starting containers:
- docker compose exec api alembic upgrade head

> Database tables should NOT be created automatically in production.

---

## 🧪 Running Tests

A separate test database is recommended.
- pytest -v

Tests include:
- App startup
- User registration
- Login & JWT issuance
- Protected endpoints
- Admin authorization

---

## 📄 API Documentation

FastAPI automatically generates interactive API docs:

- Swagger UI → `/docs`
- ReDoc → `/redoc`

---

## 🔎 Pagination

All list endpoints support pagination using `page` and `limit` query parameters.

Example:
- GET /products?page=2&limit=10

Response includes:
- {
- "total": 42,
- "page": 2,
- "limit": 10,
- "items": [...]
- }

---

## 🧾 Logging

The application uses structured logging to track:
- Startup & shutdown events
- Authentication attempts
- Admin actions
- Checkout transactions
- Unexpected errors

Logs are printed to stdout (Docker-friendly).

---

## 🔐 Roles & Permissions

| Role  | Permissions |
|------|-------------|
| User | View products, manage cart, place orders |
| Admin | Manage users, products, view all orders |

---

## 🧠 Design Decisions

- **JWT Authentication** for stateless security
- **Dependency Injection** for testability
- **Database Transactions** for checkout consistency
- **Pagination** for scalability
- **Dockerized Services** for deployment parity

---

## 📌 Future Improvements

- Payment gateway integration (Stripe)
- Order cancellation & refunds
- Product categories
- Rate limiting
- Caching (Redis)
- Async DB support
- CI/CD pipeline

---

## 👨‍💻 Author

**Arven Lagawan**  
Backend Developer (FastAPI / Python)

This project was built as a **portfolio demonstration of real-world backend development practices**.

---

## ⭐️ Why This Project

This API was intentionally designed to reflect:
- Real e-commerce workflows
- Production-grade backend structure
- Clean, maintainable code
- Readiness for deployment and scaling

If you’re a recruiter or reviewer:  
👉 This project represents how I build backend systems in real environments.
