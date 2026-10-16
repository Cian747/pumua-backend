# Breath Connection: Backend API

Django backend and database for the Breath Connection web app (installable PWA). It provides authentication, role-based access, breathing assessment video handling, practice categories and techniques, session and progress tracking, and the admin review workflow.

> **Status:** MVP in development. Update this section as milestones are reached.

## Contents

- [Tech stack](#tech-stack)
- [Features](#features)
- [Data model](#data-model)
- [Getting started](#getting-started)
- [Environment variables](#environment-variables)
- [Common commands](#common-commands)
- [API documentation](#api-documentation)
- [Project structure](#project-structure)
- [Testing](#testing)
- [Security and privacy](#security-and-privacy)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Tech stack

| Area | Technology |
|---|---|
| Language and framework | Python 3.12, Django 5, Django REST Framework |
| Database | PostgreSQL 16 |
| Background jobs | Celery with Redis |
| File storage | S3-compatible private bucket via `django-storages` |
| API docs | `drf-spectacular` (OpenAPI 3) |
| Authentication | Token or session auth with role-based permissions |
| Testing | `pytest`, `pytest-django`, `factory_boy` |
| Code quality | `ruff`, `black`, `mypy` (optional), `pre-commit` |

Adjust versions to match your `requirements.txt` or `pyproject.toml`.

## Features

- User accounts with three roles: participant, coach, and admin
- Recorded consent for video review, with timestamp and version
- Resumable video upload using short-lived presigned links; videos are never public
- Practice categories (for example calm and relaxation, sleep, focus and energy, stress relief, breath control) and breathing techniques with configurable timing
- Session logging and progress tracking (streaks, totals, monthly goals)
- Coach feedback on assessment videos
- Audit log of who accessed which video and when
- Account deletion and data export endpoints

## Data model

```mermaid
erDiagram
    USER ||--o{ CONSENT_RECORD : gives
    USER ||--o{ ASSESSMENT : submits
    USER ||--o{ SESSION_LOG : completes
    PRACTICE_CATEGORY ||--o{ TECHNIQUE : contains
    TECHNIQUE ||--o{ SESSION_LOG : used_in
    ASSESSMENT ||--o{ COACH_FEEDBACK : receives
    USER ||--o{ COACH_FEEDBACK : writes
    USER ||--o{ AUDIT_LOG : triggers

    USER {
        uuid id
        string email
        string role
        datetime created_at
    }
    CONSENT_RECORD {
        uuid id
        string consent_type
        string version
        datetime agreed_at
    }
    ASSESSMENT {
        uuid id
        string video_key
        string status
        datetime submitted_at
    }
    PRACTICE_CATEGORY {
        uuid id
        string name
        string description
    }
    TECHNIQUE {
        uuid id
        string name
        json timing_pattern
        int duration_minutes
    }
    SESSION_LOG {
        uuid id
        datetime completed_at
        int duration_seconds
    }
    COACH_FEEDBACK {
        uuid id
        text note
        string decision
    }
    AUDIT_LOG {
        uuid id
        string action
        string object_type
        datetime occurred_at
    }
```

Adjust the entities and fields to match your final models.

## Getting started

### Prerequisites

- Python 3.12 or later
- PostgreSQL 16 or later
- Redis (for background jobs)
- An S3-compatible bucket (or local storage for development)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your environment file
cp .env.example .env
# Edit .env with your local values (see the table below)

# 5. Create the database and run migrations
createdb breath_connection
python manage.py migrate

# 6. Create an admin user
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/`.

To run background jobs in a second terminal:

```bash
celery -A config worker --loglevel=info
```

### Optional: Docker

If you add a `docker-compose.yml` with Django, PostgreSQL and Redis services:

```bash
docker compose up --build
docker compose exec web python manage.py migrate
```

## Environment variables

Copy `.env.example` to `.env`. Never commit `.env` or any real secrets.

| Variable | Description | Example |
|---|---|---|
| `DJANGO_SECRET_KEY` | Secret key for cryptographic signing | long random string |
| `DJANGO_DEBUG` | Debug mode, `False` in production | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | PostgreSQL connection string | `postgres://user:pass@localhost:5432/breath_connection` |
| `REDIS_URL` | Redis connection for Celery | `redis://localhost:6379/0` |
| `AWS_STORAGE_BUCKET_NAME` | Private bucket for assessment videos | `breath-connection-videos` |
| `AWS_S3_ENDPOINT_URL` | S3-compatible endpoint | provider URL |
| `AWS_ACCESS_KEY_ID` | Storage access key | from your provider |
| `AWS_SECRET_ACCESS_KEY` | Storage secret key | from your provider |
| `CORS_ALLOWED_ORIGINS` | Frontend origins allowed to call the API | `http://localhost:3000` |
| `VIDEO_RETENTION_DAYS` | Days before assessment videos are deleted | agreed with client |

## Common commands

```bash
python manage.py makemigrations     # create migrations after model changes
python manage.py migrate            # apply migrations
python manage.py createsuperuser    # create an admin account
python manage.py seed_demo_data     # load fake categories and techniques (custom command)
pytest                              # run the test suite
ruff check . && black --check .     # lint and format check
```

Always use **fake data** in development and staging. Never copy real user data or videos into a non-production environment.

## API documentation

With the server running:

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

The API is versioned under `/api/v1/`.

## Project structure

```
.
├── config/                 # Django settings, URLs, Celery configuration
├── apps/
│   ├── accounts/           # users, roles, authentication
│   ├── consent/            # consent records
│   ├── assessments/        # video upload, status, coach feedback
│   ├── practices/          # categories and breathing techniques
│   ├── sessions_log/       # completed sessions and progress
│   └── audit/              # audit logging
├── tests/                  # test suite
├── requirements.txt
├── .env.example
└── manage.py
```

Adjust to your actual layout.

## Testing

```bash
pytest
pytest --cov=apps          # with coverage, if pytest-cov is installed
```

Priority tests: permission checks (a user must never access another user's data or video), upload link generation, consent recording, and progress calculations.

## Security and privacy

- All access control is enforced on the server for every request.
- Assessment videos live in a private bucket and are only served through short-lived signed links.
- Admin and coach accounts should use multi-factor authentication.
- Rate limiting is applied to login, sign-up and password reset.
- Secrets are loaded from environment variables and are never committed.
- Dependencies are scanned regularly (`pip-audit`, Dependabot).
- Logs record events, not personal data, passwords, tokens or video links.
- Data retention and deletion follow the policy agreed with the client and applicable data protection law.

To report a security issue, contact `<security email>` rather than opening a public issue.

## Deployment

1. Set `DJANGO_DEBUG=False` and configure all production environment variables.
2. Run `python manage.py migrate` and `python manage.py collectstatic --noinput`.
3. Serve the app with Gunicorn behind a reverse proxy with HTTPS and HSTS enabled.
4. Run at least one Celery worker.
5. Enable automated database backups and test a restore before launch.

Hosting accounts and infrastructure belong to the client.

## Contributing

1. Create a branch from `main`: `git checkout -b feature/short-description`
2. Make your changes with tests.
3. Run linting and tests locally.
4. Open a pull request with a clear description.

## License

Copyright (c) 2026 `Breath Connection`. All rights reserved.

Replace this with the licence agreed in your contract. Note that ownership of the code is set by the development agreement.