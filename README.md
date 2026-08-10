# Republic of Kandhla - Backend System

A hyper-local virtual political ecosystem app backend built with Django, DRF, Celery, Redis, and PostgreSQL.

## Prerequisites
- Python 3.10+
- PostgreSQL
- Redis Server (for Celery & Vote Queue)

## Local Setup

### 1. Clone & Install
```bash
git clone <repository-url>
cd "Democratic Republic"
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the root directory (optional for local dev if default ports match):
```ini
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/kandhla_db
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
```

### 3. Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run the Servers

Start the **Django Development Server**:
```bash
python manage.py runserver
```

Start the **Celery Worker** (for background tasks like ban expiry, vote processing):
```bash
celery -A kandhla worker -l INFO --pool=solo
```

Start the **Celery Beat Scheduler** (for periodic automation):
```bash
celery -A kandhla beat -l INFO
```

## Features Implemented
- **Phase 1**: Database Models (Accounts, Ecosystem, Content, Election)
- **Phase 2**: Serializers, RBAC Permissions, API Views
- **Phase 3**: Celery Automations, Middleware, Signals
- **Phase 4**: Firebase Integration Module (FCM Notifications, Realtime DB Sync)

## API Endpoints Overview
- `POST /api/auth/google/`: Google Login
- `PATCH /api/auth/profile/setup/`: Profile Setup (City/Mohalla)
- `GET /api/feed/{mohalla_id}/`: View Mohalla Feed
- `POST /api/election/cast-vote/`: Secure Voting via Redis Queue
- `GET /api/elections/{id}/results/`: Election Results (Phase-gated)

*For more details, check `INSTRUCTIONS.md`, `REQUIREMENTS.md`, and `SCHEMA.md`.*
