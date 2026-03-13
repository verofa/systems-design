# 🌟 Tiny URL System Design - Hands On

## 🚀 Introduction

The TinyURL system is a practical implementation of URL shortening technology
that demonstrates core systems design principles. This project provides a
hands-on approach to understanding backend services, database design,
containerization, and API development.

This document serves as both a technical reference and a learning tool,
showcasing how to build a fully functional URL shortening service from scratch
using modern technologies.

## 📚 1. System Architecture

- **Backend Microservice**: Handles URL shortening and redirection.
- **SQLite Database**: Stores URL mappings (local-first for simplicity).
- **Docker Compose**: Manages containers for the app and database.
- **HTTP API Endpoints**:
  - `POST /api/shorten`: Accepts a long URL and returns a short URL.
  - `GET /<short_code>`: Redirects to the original URL.

### 1.1 🧩 TinyURL System Architecture Diagram

```bash
    ┌─────────────┐       ┌─────────────────────┐   ┌───────────────┐
    │             │       │                     │   │               │
    │   User      ├───────► API Gateway         ├───► SQLite DB     │
    │             │       │ (Flask App)         │   │               │
    └─────────────┘       │                     │   └───────────────┘
                          │  HTTP Requests      │
                          │◀───────────────────▲│
                          │                    ││
                          │ POST /api/shorten  ││
                          │                    ││
                          │                    ││
                          └─────────────────────┘
                          │  Response           │
                          │◀───────────────────▲│
                          │                    ││
                          │  GET /<short>      ││
                          │                    ││
                          └─────────────────────┘

```

#### 🔍 Detail Component Breakdown

##### 1. User Interface

- Web Browser
- Command-line tools (`curl`,`Postman`)
- Mobile clients via API calls

##### 2. API Gateway - Flask App

- Endpoints:
  - `POST /api/shorten`: [Accepts JSON and expect `url` field]
  - `GET /<short_code>`: [Redirect to original URL]

- **Core Logic**
  - URL validation
  - Short code generation
  - Database interaction
  - Error handling

##### 3. Database (SQLite)

- Stores URL mappings
- Schema:

```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url TEXT UNIQUE NOT NULL,
    short_code TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

##### 4. Docker Containers

```bash
        ┌───────────────┐       ┌─────────────────┐
        │               │       │                 │
        │ API Container ├───────► Database Vol    │
        │  (Flask)      │       │  (SQLite DB)    │
        │   app.py      │◀──────►  tinyurl.db     │
        │               │       │                 │
        └───────────────┘       └─────────────────┘
```

###### ➜ Data Flow

1. **Shortening a URL**

- a) User sends POST request with long URL
- b) API Validate URL and check if exist in the database
- c) If not found, generates a new short code
- d) And stores the mappings in the database
- e) Returns short URL to the user

2. **Redirection**

- a) User visits the short URL
- b) API extracts short_code
- c) Queries the database to get the long URL
- d) Performs HTTP redirect to original URL

## 📁 2. Code Structure

Create a directory structure:

```bash
tiny-url/
├── app.py             # Flask backend
├── Dockerfile         # Docker configuration
├── requirements.txt   # Python dependencies
└── docker-compose.yml # Docker orchestration
```

## 📁 3. Usage

1. **Start the system**

```bash
🦄❯ docker-compose up --build -d
```

2. **Check the status of the running service**

```bash
🦄❯ docker-compose ps
NAME             IMAGE          COMMAND           SERVICE   CREATED          STATUS          PORTS
tiny-url-app-1   tiny-url-app   "python app.py"   app       19 seconds ago   Up 18 seconds   0.0.0.0:5000->5000/tcp
```

3. **Tail the logs**

```bash
🦄❯ docker-compose logs -f --tail=200 app
app-1  |  * Serving Flask app 'app'
app-1  |  * Debug mode: on
app-1  | WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
app-1  |  * Running on all addresses (0.0.0.0)
app-1  |  * Running on http://127.0.0.1:5000
app-1  |  * Running on http://172.19.0.2:5000
app-1  | Press CTRL+C to quit
app-1  |  * Restarting with stat
app-1  |  * Debugger is active!
app-1  |  * Debugger PIN: 167-628-980
```

4. **Test the endpoints**
   - Shorten a URL:

   ```bash
    🦄❯ curl -X POST \
       -H "Content-Type: application/json" \
       -d '{"url": "https://example.com"}' \
       http://localhost:5000/api/shorten
   ```

   - Check the short URL from the result of the above `curl` command:

   ```bash
    🦄❯ curl http://localhost:5000/abc123
   ```

[Accepts JSON and expect `url` field]: https://github.com/verofa/sysmtems-design/blob/e4b8b55b9297435c062eda8f4b43f4ee5e114241/tiny-url/app.py#L15-L22v
[Redirect to original URL]: https://github.com/verofa/sysmtems-design/blob/e4b8b55b9297435c062eda8f4b43f4ee5e114241/tiny-url/app.py#L56-L59
