# Tiny URL system Design - Hands On

## 1. System Architecture

- Backend Microservice: Handles URL shortening and redirection.
- SQLite Database: Stores URL mappings (local-first for simplicity).
- Docker Compose: Manages containers for the app and database.
- HTTP API Endpoints:
  - `POST /api/shorten`: Accepts a long URL and returns a short URL.
  - `GET /<short_code>`: Redirects to the original URL.

## 2. Code Structure

Create a directory structure:

```bash
tiny-url-system/
├── app.py             # Flask backend
├── Dockerfile         # Docker configuration
├── requirements.txt   # Python dependencies
└── docker-compose.yml # Docker orchestration
```

## 3. Usage

1. \*\* Start the system:

```bash
❯ docker-compose up --build -d
```

2. ** Check the status of the running service **

```bash
❯ docker-compose ps
NAME             IMAGE          COMMAND           SERVICE   CREATED          STATUS          PORTS
tiny-url-app-1   tiny-url-app   "python app.py"   app       19 seconds ago   Up 18 seconds   0.0.0.0:5000->5000/tcp
```

3. ** Tail the logs **

```bash
❯ docker-compose logs -f --tail=200 app
app-1  |  * Serving Flask app 'app'
app-1  |  * Debug mode: on
app-1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
app-1  |  * Running on all addresses (0.0.0.0)
app-1  |  * Running on http://127.0.0.1:5000
app-1  |  * Running on http://172.19.0.2:5000
app-1  | Press CTRL+C to quit
app-1  |  * Restarting with stat
app-1  |  * Debugger is active!
app-1  |  * Debugger PIN: 167-628-980
```

4. ** Test the endpoints **
   - Shorten a URL:

   ```bash
   curl -X POST -H "Content-Type: application/json" -d
   ```

   - Check the short URL from the result of the above `curl` command:

   ```bash
   curl http://localhost:5000/abc123
   ```

# TinyURL System Architecture Diagram

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
