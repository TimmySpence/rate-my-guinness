from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import pytest

app = Flask(__name__)
CORS(app)


# Use SQLite for tests, otherwise use environment variables for Postgres
if app.config.get("TESTING"):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    DB_USER = os.environ.get("DB_USER", "rmgadmin")
    DB_PASS = os.environ.get("DB_PASS", "")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_NAME = os.environ.get("DB_NAME", "rate_my_guinness")  # Use underscores
    DB_PORT = os.environ.get("DB_PORT", "5432")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define your model
class Rating(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    rating = db.Column(db.Integer, nullable=False)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/ratings", methods=["POST"])
def submit_rating():
    data = request.json
    place = data.get("place", {})
    rating_value = data.get("rating")

    if not place or rating_value is None:
        return jsonify({"error": "Missing place or rating"}), 400

    new_rating = Rating(
        place_id=place.get("place_id"),
        name=place.get("name"),
        lat=place.get("lat"),
        lng=place.get("lng"),
        rating=rating_value
    )
    db.session.add(new_rating)
    db.session.commit()

    return jsonify({"message": "Rating submitted successfully"})

@app.route("/api/ratings", methods=["GET"])
def get_ratings():
    results = (
        db.session.query(
            Rating.place_id,
            Rating.name,
            Rating.lat,
            Rating.lng,
            db.func.avg(Rating.rating).label("avg_rating"),
            db.func.count(Rating.rating).label("count")
        )
        .group_by(Rating.place_id, Rating.name, Rating.lat, Rating.lng)
        .all()
    )

    return jsonify([
        {
            "place_id": r.place_id,
            "name": r.name,
            "lat": r.lat,
            "lng": r.lng,
            "average_rating": round(r.avg_rating, 2),
            "rating_count": r.count
        }
        for r in results
    ])

@app.route("/create_tables")
def create_tables():
    try:
        db.create_all()
        return "Tables created!"
    except Exception as e:
        return f"Error: {e}"

# Ensure tables are created before app starts serving requests
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
