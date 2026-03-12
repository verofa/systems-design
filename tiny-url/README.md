# Tiny URL system Desing - Hands On

1. System Architecture

- Backend Microservice: Handles URL shortening and redirection.
- SQLite Database: Stores URL mappings (local-first for simplicity).
- Docker Compose: Manages containers for the app and database.
- HTTP API Endpoints:

```bash
POST /api/shorten: Accepts a long URL and returns a short URL.
GET /<short_code>: Redirects to the original URL.
```

Code Structure

Create a directory structure:

```bash
tiny-url-system/
├── app.py          # Flask backend
├── Dockerfile      # Docker configuration
├── requirements.txt # Python dependencies
└── docker-compose.yml # Docker orchestration
```
