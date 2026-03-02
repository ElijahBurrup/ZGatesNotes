import os
from flask import Flask, Blueprint, send_from_directory

URL_PREFIX = os.environ.get("URL_PREFIX", "")

# --- Blueprint for all routes (supports URL_PREFIX) ---
bp = Blueprint("main", __name__)

# ── Catalog ──────────────────────────────────────────────
@bp.route("/")
def index():
    return send_from_directory("static", "index.html")

# ── Slug-based reader route ──────────────────────────────
slug_to_file = {
    "carnality-vs-divinity": "Carnality_Vs_Divinity.html",
}

@bp.route("/read/<slug>")
def read_note(slug):
    filename = slug_to_file.get(slug)
    if not filename:
        return "Note not found", 404
    return send_from_directory("assets", filename)

# ── Landing pages (static HTML per note) ─────────────────
# Each note gets a route like /the-message-title
# Add new routes here as notes are created


def create_app():
    static_path = f"{URL_PREFIX}/static" if URL_PREFIX else ""
    flask_app = Flask(__name__, static_folder="static", static_url_path=static_path)

    flask_app.register_blueprint(bp, url_prefix=URL_PREFIX or None)

    @flask_app.context_processor
    def inject_prefix():
        return {"url_prefix": URL_PREFIX}

    @flask_app.after_request
    def rewrite_urls(response):
        if URL_PREFIX and response.content_type and "text/html" in response.content_type:
            content = response.get_data(as_text=True)
            content = content.replace('href="/', f'href="{URL_PREFIX}/')
            content = content.replace("href='/", f"href='{URL_PREFIX}/")
            content = content.replace('src="/', f'src="{URL_PREFIX}/')
            content = content.replace("src='/", f"src='{URL_PREFIX}/")
            content = content.replace('action="/', f'action="{URL_PREFIX}/')
            content = content.replace("action='/", f"action='{URL_PREFIX}/")
            response.set_data(content)
        return response

    return flask_app


# ── Run ──────────────────────────────────────────────────
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=7000)
