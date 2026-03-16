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

### 1.1 High Level Overview

<p align="center">
<img src="images/system-architecture.jpg" alt="Tiny-URL-Architecture" style="width:80%; height:auto;">
</p>

### 1.2 Low Level Overview

#### 1.2.1 Code (Python) Overview

<p align="center">
<img src="images/system-architecture-l.jpg" alt="Tiny-URL-Architecture" style="width:80%; height:auto;">
</p>

#### 1.2.2 Docker Services Overview

<p align="center">
<img src="images/system-architecture-docker.jpg" alt="Docker-Architecture" style="width:80%; height:auto;">
</p>

## 📁 2. Code Structure

**Directory structure**

```bash
tiny-url/
├── app.py             # Flask backend
├── Dockerfile         # Docker configuration
├── requirements.txt   # Python dependencies
└── docker-compose.yml # Docker orchestration
```

## 📁 3. Usage

### 3.1 💻 Software Requirements

Before running the TinyURL system, ensure you have the following installed on
your machine:

🐳 **Docker**

- **Description**: A platform for developing and shipping software with containers
- **Installation Guide**: [Get Started with Docker]
- **Command to Verify**: `🦄❯ docker --version`

🐳📄 **Docker Compose**

- **Description**: A tool for defining and running multi-container Docker applications
- **Installation Guide**: [Set up Docker Compose]
- **Command to Verify**: `🦄❯ docker-compose --version`

🌱 **Git**

- **Description**: A version control system for tracking changes in source code
- **Installation Guide**: [Install Git]
- **Command to Verify**: `🦄❯ git --version`

### 3.2 🌐 Cloning the GitHub Repository

To get started with the TinyURL system, clone the GitHub repository:

```bash
# Option 1: HTTPS
🦄❯ git clone https://github.com/verofa/systems-design.git

# Option 2: SSH (requires SSH keys set up)
🦄❯ git clone git@github.com:verofa/systems-design.git
```

After cloning, change into the project directory:

```bash
🦄❯ cd systems-design/tiny-url/distributed
```

### 3.3 **Start the system**

```bash
🦄❯ docker-compose up --build -d
```

**Check the status of the running service**

```bash
🦄❯ docker-compose ps
NAME             IMAGE          COMMAND           SERVICE   CREATED          STATUS          PORTS
NAME                IMAGE                COMMAND                  SERVICE   CREATED       STATUS                 PORTS
distributed-app-1   distributed-app      "python app.py"          app       4 hours ago   Up 4 hours             0.0.0.0:5000->5000/tcp
distributed-db-1    postgres:16-alpine   "docker-entrypoint.s…"   db        4 hours ago   Up 4 hours (healthy)   5432/tcp
```

**Tail the logs**

- a) Check service `app` logs:

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

- b) Check service `db` logs:

```bash
🦄❯ docker-compose logs -f --tail=200 db
...
db-1  |
db-1  | PostgreSQL init process complete; ready for start up.
db-1  |
db-1  | 2026-03-16 00:23:41.342 UTC [1] LOG:  starting PostgreSQL 16.13 on aarch64-unknown-linux-musl, compiled by gcc (Alpine 15.2.0) 15.2.0, 64-bit
db-1  | 2026-03-16 00:23:41.342 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db-1  | 2026-03-16 00:23:41.342 UTC [1] LOG:  listening on IPv6 address "::", port 5432
db-1  | 2026-03-16 00:23:41.343 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db-1  | 2026-03-16 00:23:41.344 UTC [57] LOG:  database system was shut down at 2026-03-16 00:23:41 UTC
db-1  | 2026-03-16 00:23:41.346 UTC [1] LOG:  database system is ready to accept connections
db-1  | 2026-03-16 00:28:41.451 UTC [55] LOG:  checkpoint starting: time
```

**Test the endpoints**

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

- Check All the processed URLs:

```bash
 🦄❯ curl -v http://localhost:5000/api/urls
```

[Accepts JSON and expect `url` field]: https://github.com/verofa/systems-design/blob/e4b8b55b9297435c062eda8f4b43f4ee5e114241/tiny-url/app.py#L15-L22
[Redirect to original URL]: https://github.com/verofa/systems-design/blob/e4b8b55b9297435c062eda8f4b43f4ee5e114241/tiny-url/app.py#L56-L59
[Get Started with Docker]: https://docs.docker.com/get-started/get-docker/
[Set up Docker Compose]: https://docs.docker.com/compose/install/
[Install Git]: https://git-scm.com/install/
