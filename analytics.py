from flask import Blueprint, render_template, jsonify
import jwt
import time

analytics_bp = Blueprint('analytics', __name__)

# ─────────────────────────────────────────────────────────────
# CONFIGURATION
# Get your embed secret from Metabase:
#   Admin Settings → Embedding → Embedding secret key
# ─────────────────────────────────────────────────────────────
METABASE_EMBED_SECRET = "SECRET_KEY_REMOVED_HERE"
METABASE_SITE_URL = "https://dashboard.flumendataanalytics.com"

# Map each dashboard slot (1, 2, ...) to its Metabase dashboard ID.
# Dashboard IDs come from the Metabase URL when viewing a dashboard:
#   e.g. /dashboard/3 → ID is 3
DASHBOARDS = {
    1: {
        "id": 3,
        "embedding_params": {
            "date": "enabled",
            "day_of_week": "enabled",
            "location": "enabled",
            "date_range": "enabled",
            "date_range%3A": "enabled",
            "kpi_month": "enabled"
        }
    },
    2: {
        "id": None,   # ← replace None with your second dashboard's ID
        "embedding_params": {}
    },
}

# ─────────────────────────────────────────────────────────────
# TOKEN GENERATOR
# Tokens expire after 10 minutes. The page fetches a fresh one
# on every load, so this is always up to date.
# ─────────────────────────────────────────────────────────────
def generate_token(dashboard_config):
    now = int(time.time())
    payload = {
        "resource": {"dashboard": dashboard_config["id"]},
        "params": {},
        "iat": now,
        "exp": now + 600,   # 10 minutes
        "_embedding_params": dashboard_config["embedding_params"]
    }
    return jwt.encode(payload, METABASE_EMBED_SECRET, algorithm="HS256")


# ─────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────
@analytics_bp.route('/')
def home():
    return render_template("analytics/index.html",
                           metabase_url=METABASE_SITE_URL)


@analytics_bp.route('/token/<int:slot>')
def get_token(slot):
    """
    Called by the page's JavaScript to get a fresh signed token.
    Example: GET /analytics/token/1  →  {"token": "eyJ..."}
    """
    dashboard = DASHBOARDS.get(slot)
    if not dashboard or dashboard["id"] is None:
        return jsonify({"error": f"Dashboard slot {slot} is not configured yet"}), 404
    token = generate_token(dashboard)
    return jsonify({"token": token})
