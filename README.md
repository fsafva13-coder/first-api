# first-api

A minimal FastAPI backend built to understand the request → response cycle from the server side — two JSON endpoints, tested via curl and browser, deployed nowhere fancy on purpose.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Overview

Most backend tutorials start with a framework's opinions before the fundamentals stick. This project strips that away: a health-check endpoint and a query-parameter endpoint, built to confirm a simple thing — that a server can receive an HTTP request, process it, and hand back structured JSON. It's the first rung of a backend track, not a production service, and the README says so on purpose.

## Features

- `GET /` — health-check endpoint returning server status as JSON
- `GET /greet?name=` — accepts a query parameter and returns a dynamic JSON response
- Auto-generated interactive API docs at `/docs` (FastAPI's built-in Swagger UI)
- Zero external dependencies beyond the web framework and server — no database, no auth, nothing to obscure the core request/response mechanics

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Server:** Uvicorn (ASGI)

## Demo

![API docs screenshot](screenshots/docs-ui.png)
*FastAPI's auto-generated `/docs` page, used to test both endpoints without leaving the browser.*

## Installation

```bash
git clone https://github.com/fsafva13-coder/first-api.git
cd first-api
pip install -r requirements.txt
```

## Usage

Start the server:

```bash
uvicorn main:app --reload
```

Test with curl:

```bash
curl http://127.0.0.1:8000/
curl "http://127.0.0.1:8000/greet?name=Safva"
```

Or open directly in a browser:

- `http://127.0.0.1:8000/` — health check
- `http://127.0.0.1:8000/greet?name=Safva` — greeting endpoint
- `http://127.0.0.1:8000/docs` — interactive Swagger UI

## Project Structure

```
first-api/
├── main.py            # App definition and both endpoints
├── requirements.txt    # fastapi, uvicorn
└── README.md
```

## Challenges & Learnings

The hardest part wasn't the code — it was resisting the urge to add scope before understanding the basics. Confirming that a GET request with a query string behaves differently from a POST body, and seeing the browser round-trip a real HTTP request without any client library, made the request/response loop concrete instead of theoretical.

## Future Improvements

- Add a `POST` endpoint to contrast body payloads with query parameters
- Add basic input validation with Pydantic models
- Containerize with Docker
- Deploy to a public URL (Render/Railway) once the next assignment covers deployment

## License

MIT
