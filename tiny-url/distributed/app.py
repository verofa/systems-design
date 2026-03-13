import os
import random
import string
from urllib.parse import urlparse

from flask import Flask, jsonify, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Config - reads from env variable set in docker-compose
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# --- Model ---
class Url(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String, nullable=False, unique=True)
    short_code = db.Column(db.String(6), nullable=False, unique=True)


# Create tables on startUp
with app.app_context():
    db.create_all()


# --- Helpers ---
# Generate short code - 6 alphanumeric characters
def generate_short_code():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))


# --- Routes ---
@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing URL"}), 400

    long_url = data["url"]
    parsed = urlparse(long_url)
    if not parsed.scheme or not parsed.netloc:
        return jsonify({"error": "Invalid URL"}), 400

    try:
        # Check if URL already exists
        existing = Url.query.filter_by(long_url=long_url).first()
        if existing:
            return (
                jsonify({"short_url": f"http://localhost:5000/{existing.short_code}"}),
                200,
            )

        # Create new short code
        short_code = generate_short_code()
        new_url = Url(long_url=long_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()

        return jsonify({"short_url": f"http://localhost:5000/{short_code}"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    url = Url.query.filter_by(short_code=short_code).first()
    if url:
        return redirect(url.long_url)
    return jsonify({"error": "URL not found"}), 404


@app.route("/api/urls", methods=["GET"])
def list_urls():
    """
    Return a list of all shortened URLs with their original URLs.
    """
    urls = Url.query.all()
    urls_list = []
    for url in urls:
        urls_list.append(
            {
                "short_code": url.short_code,
                "long_url": url.long_url,
            }
        )
    return jsonify({"count": len(urls_list), "urls": urls_list}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
