# DVM ERP Full

DVM ERP Full is a lesson planning and curriculum management platform built for school operations.
It includes a FastAPI backend, a Vue frontend, role-based portal access, and public chapter browsing.

Current deployment model:
1. Backend API on Ubuntu VPS (Nginx + systemd + PostgreSQL)
2. Frontend on Netlify

## Core Features

1. Public academic content browsing
- Browse classes, subjects, chapters, and concepts
- Chapter detail pages with concept breakdown
- Public PDF access for chapter documents

2. Portal for staff users
- Secure login with JWT auth
- Role support: teacher, subject_head, mentor, hm, principal, super_admin
- Subject-wise chapter management
- Concept and exhibit management
- Chapter PDF upload and update
- XLSX upload/re-upload workflows

3. Operational hardening
- Rate limiting on auth endpoints
- Upload validation and file size caps
- Alembic migrations for schema changes
- Static uploads served from API

## Tech Stack

Backend:
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL (production)
- SQLite fallback (local if DATABASE_URL is not set)

Frontends:
- `frontend` (Lesson Planning): Vue 3, Vite, Vue Router, Pinia, Axios
- `erp` (ERP Portal): Vue 3, Vite, Vue Router, Pinia, Axios
- `website` (Public Website): Vue 3, Vite
- `library` (Digital Library): Vue 3, Vite, Axios

Infra:
- Ubuntu VPS (Live)
- Dual systemd services:
    1. `dvmapi`: FastAPI backend (uvicorn)
    2. `dvmbot`: Telegram AI Agent (python)
- Nginx reverse proxy (SSL via Certbot)
- Netlify for frontend hosting

## Repository Structure

- backend: API, models, routers, migrations, seeding
- frontend: lesson planning app (existing app)
- erp: dedicated ERP frontend app
- website: dedicated public website app
- library: dedicated digital library app
- dvm-telegram-bot: AI agent for student/staff lookup
- deploy: VPS deployment configs and scripts
- uploads: runtime uploaded files (not committed)

## Quick Start (Local Development)

Prerequisites:
1. Python 3.10+
2. Node.js 18+
3. npm

### 1) Backend Setup

1. Open terminal in backend folder.
2. Create and activate virtual environment.
3. Install dependencies.
4. Copy backend/.env.example to backend/.env and fill values.
5. Run migrations.
6. Seed sample data.
7. Start API server.

Commands:

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
python seed.py
uvicorn main:app --reload

API default URL: http://localhost:8000

### 2) Lesson Planning Frontend Setup

1. Open terminal in frontend folder.
2. Install dependencies.
3. Copy frontend/.env.example to frontend/.env and set VITE_API_BASE_URL.
4. Start dev server.

Commands:

cd frontend
npm install
copy .env.example .env
npm run dev

Lesson planning frontend default URL: http://localhost:5173

### 3) ERP Frontend Setup

1. Open terminal in erp folder.
2. Install dependencies.
3. Create .env with VITE_API_BASE_URL.
4. Start dev server.

Commands:

cd erp
npm install
echo VITE_API_BASE_URL=http://localhost:8000 > .env
npm run dev

### 4) Website Frontend Setup

Commands:

cd website
npm install
npm run dev

### 5) Library Frontend Setup

Commands:

cd library
npm install
echo VITE_API_BASE_URL=http://localhost:8000 > .env
npm run dev

## Environment Variables

Backend (.env):
- SECRET_KEY: required JWT signing secret
- DATABASE_URL: production PostgreSQL URL
- ALLOWED_ORIGINS: comma-separated frontend origins

Frontend env (.env) for apps that call API:
- VITE_API_BASE_URL: public API base URL

## Default Super Admin Account (Seed)

- Email: admin@dalmiatrusts.in
- Password: admin123

Change this immediately in production.

Seed behavior notes:
- `seed.py` creates/updates role metadata and ensures these roles exist in users: `teacher`, `subject_head`, `mentor`, `hm`, `principal`, `super_admin`
- Existing user passwords are not reset unless `SEED_FORCE_PASSWORD_RESET=1`
- Optional env vars:
	- `SEED_SUPER_ADMIN_EMAIL`
	- `SEED_SUPER_ADMIN_PASSWORD`
	- `SEED_CREATE_ROLE_USERS` (`1` by default)
	- `SEED_DEFAULT_USER_PASSWORD` (for optional role bootstrap users)
	- `SEED_FORCE_PASSWORD_RESET` (`0` by default)

## Deployment (VPS + Netlify)

Production target:
- API domain: https://fastapi.dvmchirawa.ac.in
- Frontend host: Netlify

### VPS First-Time Setup

Use the script at deploy/setup.sh after updating repository URL placeholders.

Typical flow:
1. Clone repository on VPS
2. Create Python virtual environment
3. Install backend dependencies
4. Create PostgreSQL database and user
5. Configure backend .env
6. Run Alembic migrations
7. Seed initial data
8. Install systemd service from deploy/dvmapi.service
9. Install Nginx config from deploy/fastapi.dvmchirawa.ac.in.conf
10. Enable SSL using certbot

### Ongoing Deployment

Use deploy/deploy.sh on VPS:
1. Pull latest main
2. Install/update dependencies
3. Run migrations
4. Restart API service

To run seed during deploy:
- `RUN_SEED=1 bash deploy/deploy.sh`

### Telegram Bot Deployment
The AI agent runs as a separate service on the same VPS:
1. Directory: `dvm-telegram-bot`
2. Service Name: `dvmbot.service`
3. Log View: `journalctl -u dvmbot -f`

## API Overview

Main router groups:
- /api/public: public academic content
- /api/portal: authenticated portal operations
- /api/users: auth and user management

Health/root:
- /

## Data and File Storage

- Uploaded files are served from /uploads
- Chapter PDF URL is exposed as pdf_url in chapter responses
- Uploads directory should be backed up as persistent data

## Testing

Backend tests are available under backend/tests.

Run from backend folder:

pytest

## Security Notes

1. Never commit real .env files.
2. Use strong SECRET_KEY in production.
3. Restrict ALLOWED_ORIGINS to actual frontend domains only.
4. Replace default super_admin password after first login.
5. Keep server packages and Python dependencies updated.

## ERP Scale Roadmap (Next Phase)

Planned evolution toward full ERP:
1. Academic planning beyond chapters (annual plans, assessments, outcomes)
2. Staff workflows and approvals
3. Student and class operations integration
4. Reporting and analytics dashboards
5. AI-assisted teaching tools

AI note:
- Chapter PDFs are intended to be used as reference content for future AI features.

## License

Proprietary internal project for DVM operations unless updated by repository owner.
