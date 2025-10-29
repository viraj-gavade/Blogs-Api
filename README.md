# 🔥 Blogs API

A minimal and opinionated blogging API built with FastAPI. It supports user registration, authentication (cookie-based JWT), creating/updating/deleting blogs, comments, and likes. The API returns consistent JSON responses via a custom response helper.

---

## ⚡ Overview

This project is a simple Blogs API implemented using FastAPI. It provides endpoints for:
- User signup, login (cookie-based JWT), and logout.
- CRUD for blog posts (create, read, update, delete).
- Adding, updating, and deleting comments on blogs.
- Liking/unliking blogs (toggle).
- User profile operations (view, update, change password) and retrieving user's blogs/comments/likes.

The API is designed for learning and small projects. It uses SQLAlchemy for ORM models and Pydantic (via schemas) for validation.

---

## 🚀 Tech Stack

- FastAPI — web framework
- Uvicorn — ASGI server
- SQLAlchemy — ORM
- Pydantic — request/response schemas
- python-dotenv — environment variables
- passlib[bcrypt] — password hashing
- python-jose — JWT handling

---

## 🧭 Quick start (setup & installation)

> These instructions assume you're on Windows (PowerShell). Adjust activation commands for other shells or platforms.

1. Clone the repo

```powershell
# from the folder where you want the project
git clone <your-repo-url>
cd "Blogs Api"
```

2. Create and activate a virtual environment

```powershell
python -m venv .venv
# PowerShell activation
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies

```powershell
pip install fastapi uvicorn sqlalchemy python-dotenv passlib[bcrypt] python-jose
```

(Optionally pin versions and put them into a `requirements.txt`.)

4. Create a `.env` file in the project root and add required variables (example):

```
DB_URL=sqlite:///./test.db
SECRETE_KEY=your_secret_key_here
ALGORITHM=HS256
```

Notes:
- The code expects environment variables `DB_URL`, `SECRETE_KEY`, and `ALGORITHM` loaded by `utils/imports.py`.
- `DB_URL` can point to any SQLAlchemy-supported database; the example above is SQLite for local testing.

5. Run the server

```powershell
uvicorn main:app --reload --port 8000
```

Open Swagger UI at http://127.0.0.1:8000/docs or ReDoc at http://127.0.0.1:8000/redoc

---

## 🧩 API Endpoints (summary)

All responses use a `CustomResponse` wrapper with the following shapes:

- Success: `{ "status": "success", "message": "...", "data": { ... } }`
- Error: `{ "status": "error", "message": "..." }`

Base URL: `/`

### Auth 🔑
- POST `/auth/register` — Register a new user
  - Body (SignupUser): `{ "fullName": "string", "email": "email", "password": "string", "username": "string" }`
  - Success: 201 Created, data: public user object (username, email, fullName).

- POST `/auth/login` — Login user and set cookie
  - Body (SignInUser): `{ "username": "string", "password": "string" }`
  - Success: 200 OK, sets `accessToken` cookie and returns token in data.

- GET `/auth/logout` — Logout user
  - Clears cookie; returns success message.

### User 👤
(All routes under `/user` require an authenticated cookie — `accessToken`)

- GET `/user/me` — Get profile
  - Success: 200, data: user public info (id, username, email)

- PUT `/user/me/update` — Update profile
  - Body (UpdateUser): optionally `{ "fullName", "email", "username" }`
  - Success: 200, returns updated public user

- PUT `/user/me/changepass` — Change password
  - Body (ChangePassword): `{ "current_pass": "...", "new_password": "..." }`
  - Success: 200, password updated

- GET `/user/me/comments` — Get blogs the user has commented on
  - Success: 200, data: list of blogs

- GET `/user/me/likes` — Get blogs the user has liked
  - Success: 200, data: list of blogs

- GET `/user/me/blogs` — Get blogs created by the user
  - Success: 200, data: list of blogs

### Blog 📝
- GET `/blog/` — Get all blogs
  - Success: 200, data: list of blogs

- POST `/blog/` — Create a blog (auth required)
  - Body (Blog): `{ "title": "...", "content": "..." }` (id, dates are optional/handled by server)
  - Success: 201, data: created blog

- GET `/blog/{id}` — Get single blog with comments and likes
  - Success: 200, data: object: { Blog, Comments, Likes }

- PUT `/blog/{id}` — Update blog (auth + ownership) 
  - Body (UpdateBlog): `{ "title"?, "content"? }`
  - Success: 200, returns updated blog

- DELETE `/blog/{id}` — Delete blog (auth + ownership)
  - Success: 200, success message

### Comment 💬
- POST `/comment/{blog_id}` — Add comment to a blog (auth required)
  - Body (CommentSchema): `{ "content": "..." }`
  - Success: 201, returns created comment

- PUT `/comment/{comment_id}` — Update a comment (auth + ownership)
  - Body (UpdateCommentSchema): `{ "content": "..." }`
  - Success: 200, returns updated comment

- DELETE `/comment/{comment_id}` — Delete a comment (auth + ownership)
  - Success: 200, success message

### Like 👍
- GET `/like/toggle/{id}` — Toggle like on a blog (auth required)
  - Success: 200, message indicates liked/unliked

---

## 📚 API documentation links

- Swagger UI: https://your-domain/docs
- ReDoc: https://your-domain/redoc

(For local development, these are available at `http://127.0.0.1:8000/docs` and `/redoc`.)

---

## 🧠 Features

- ✅ User registration/login using hashed passwords (bcrypt)
- ✅ JWT-based auth (stored in an `accessToken` cookie)
- ✅ CRUD for blogs with ownership checks
- ✅ Comment creation, update, delete with ownership checks
- ✅ Toggle-like functionality for blogs
- ✅ Consistent JSON response wrapper via `utils/response.py`
- ✅ Validation and schemas (Pydantic models) for inputs and outputs

---

## 📁 Folder structure

```
/ (project root)
├─ main.py                    # FastAPI app and router registration
├─ Auth/                      # Auth helpers (hashing, JWT)
│  └─ auth.py
├─ Controllers/               # Business logic for each resource
│  ├─ auth_controllers.py
│  ├─ blog_controllers.py
│  ├─ comment_controllers.py
│  ├─ like_controllers.py
│  └─ user_controllers.py
├─ DataBase/                  # DB connection / session factory
│  └─ connect.py
├─ Midddlewares/              # Request middlewares (JWT verification)
│  └─ auth_middleware.py
├─ Models/                    # SQLAlchemy models
│  └─ sql_models.py
├─ Routes/                    # APIRouter definitions
│  ├─ auth_routes.py
│  ├─ blog_routes.py
│  ├─ comment_routes.py
│  ├─ like_routes.py
│  └─ user_routes.py
├─ Schemas/                   # Pydantic models (request/response shapes)
│  ├─ blog_schemas.py
│  ├─ comment_schemas.py
│  ├─ like_schemas.py
│  └─ user_schemas.py
└─ utils/                     # helpers
   ├─ imports.py              # env loader & settings
   └─ response.py             # CustomResponse wrapper
```

---

## 💡 Example requests & responses

Example: Register a user

Request (POST `/auth/register`)

```json
{
  "fullName": "Jane Doe",
  "email": "jane@example.com",
  "password": "Password123!",
  "username": "jane_doe"
}
```

Response (201)

```json
{
  "status": "success",
  "message": "User Registered Successfully!",
  "data": {
    "username": "jane_doe",
    "email": "jane@example.com",
    "Full Name": "Jane Doe"
  }
}
```

Example: Login (POST `/auth/login`)

Request body:

```json
{ "username": "jane_doe", "password": "Password123!" }
```

Response (200) — cookie `accessToken` is set and token returned in `data`.

General response format for success and error is shown above in the API Endpoints section.


Thanks for building with FastAPI — enjoy the project! 🚀
