import os
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="")

# ── Catalog ──────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# ── Slug-based reader route ──────────────────────────────
slug_to_file = {
    # "slug-name": "Asset_Filename.html",
}

@app.route("/read/<slug>")
def read_note(slug):
    filename = slug_to_file.get(slug)
    if not filename:
        return "Note not found", 404
    return send_from_directory("assets", filename)

# ── Landing pages (static HTML per note) ─────────────────
# Each note gets a route like /the-message-title
# Add new routes here as notes are created

# ── Run ──────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=7000)
