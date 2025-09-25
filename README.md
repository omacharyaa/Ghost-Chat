# Ghost Chat

Anonymous regional chat with rooms and room codes, Flask + Socket.IO.

## Local Development

1. Python 3.11+
2. Create venv and install deps:
```
pip install -r requirements.txt
```
3. Run:
```
python run.py
```
Open http://localhost:5000

## Environment Variables
- SECRET_KEY (required in prod)
- DATABASE_URL (defaults to sqlite:///ghost_chat.db)
- SOCKETIO_MESSAGE_QUEUE (optional, e.g. Redis URL)
- IPINFO_TOKEN (optional, for geolocation if enabled)

## Deploy on Render
Option A: Blueprint
- Connect repo on Render, add `render.yaml` at repo root
- Render will detect and provision the service

Option B: Manual service
- Create Web Service (Python)
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:$PORT run:app`
- Add env vars: `FLASK_ENV=production`, `SECRET_KEY=<random>`, `DATABASE_URL` (or keep sqlite), optional `IPINFO_TOKEN`

Notes:
- Socket.IO uses eventlet worker; scale to more workers for higher concurrency.
- For multiple instances, set `SOCKETIO_MESSAGE_QUEUE` to a Redis URL for shared pub/sub.
