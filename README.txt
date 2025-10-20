Ottawa IT Jobs - Railway-ready (basic)
-------------------------------------
This project scrapes IT jobs from Indeed (Ottawa) and exposes a simple Flask app.
It supports web-push notifications via pywebpush (VAPID).

BEFORE DEPLOY:
1. Generate VAPID keys (see instructions below) and paste them into app.py:
   VAPID_PRIVATE_KEY and VAPID_PUBLIC_KEY.

2. Create a GitHub repository and push this project, then connect to Railway:
   - railway.app -> New Project -> Deploy from GitHub repo

VAPID key generation (Python):
  from pywebpush import generate_vapid_key
  priv, pub = generate_vapid_key()
  print(priv); print(pub)

Note: For production use persist subscriptions in a database; this demo uses in-memory list.