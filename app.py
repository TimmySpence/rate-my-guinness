from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Create DB if not exists
DB_FILE = "ratings.db"

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                place_id TEXT,
                name TEXT,
                lat REAL,
                lng REAL,
                rating INTEGER
            );
        """)
        conn.commit()
        conn.close()

init_db()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/ratings", methods=["POST"])
def submit_rating():
    data = request.json

    place = data.get("place", {})
    rating = data.get("rating")

    if not place or not rating:
        return jsonify({"error": "Missing place or rating"}), 400

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ratings (place_id, name, lat, lng, rating)
        VALUES (?, ?, ?, ?, ?)
    """, (
        place.get("place_id"),
        place.get("name"),
        place.get("lat"),
        place.get("lng"),
        rating
    ))
    conn.commit()
    conn.close()

    return jsonify({"message": "Rating submitted successfully"})

# Optional: Get average ratings per place
@app.route("/api/ratings", methods=["GET"])
def get_ratings():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT place_id, name, lat, lng, AVG(rating) as avg_rating, COUNT(*) as count
        FROM ratings
        GROUP BY place_id
    """)
    results = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "place_id": row[0],
            "name": row[1],
            "lat": row[2],
            "lng": row[3],
            "average_rating": round(row[4], 2),
            "rating_count": row[5]
        } for row in results
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)