# Exercise 05 — FastAPI REST API

A REST API built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

* Full CRUD operations for posts
* Pagination with `page` and `per_page`
* Filtering by post status (`draft` or `published`)
* API key authentication using `X-API-Key`
* PostgreSQL backend
* SQLAlchemy ORM models
* Pydantic request and response validation
* Automatically generated Swagger/OpenAPI documentation

## Project Structure

```text
app/
├── main.py
├── db.py
├── models.py
├── schemas.py
├── auth.py
├── __init__.py
└── routers/
    ├── __init__.py
    └── posts.py
```

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/exercise04
API_KEY=hireclout-secret-key
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI development server:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

OpenAPI specification:

```text
http://localhost:8000/openapi.json
```

## Example Requests

### Get posts

```bash
curl "http://localhost:8000/posts?page=1&per_page=10&status=draft"
```

### Get a single post

```bash
curl "http://localhost:8000/posts/5"
```

### Create a post

```bash
curl -X POST "http://localhost:8000/posts" \
-H "Content-Type: application/json" \
-H "X-API-Key: hireclout-secret-key" \
-d '{
  "user_id": 1,
  "title": "My First Post",
  "body": "Hello from FastAPI",
  "status": "draft"
}'
```

### Update a post

```bash
curl -X PATCH "http://localhost:8000/posts/5" \
-H "Content-Type: application/json" \
-H "X-API-Key: hireclout-secret-key" \
-d '{
  "status": "published"
}'
```

### Delete a post

```bash
curl -X DELETE "http://localhost:8000/posts/5" \
-H "X-API-Key: hireclout-secret-key"
```

## Status Codes

* `200 OK` — Successful request
* `201 Created` — Resource created successfully
* `204 No Content` — Resource deleted successfully
* `401 Unauthorized` — Missing or invalid API key
* `404 Not Found` — Resource does not exist
* `422 Unprocessable Entity` — Request validation failed
* `500 Internal Server Error` — Unexpected server error

```
```
