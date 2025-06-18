from flask import Flask, request, jsonify, send_from_directory
import os, psycopg2, json
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
CORS(app)

# PostgreSQL に接続
DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# テーブルがなければ作成
cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    expected TEXT,
    predicted TEXT,
    answers JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# --- 省略（FABRIC_DB, to_vector, similarity, infer関数など）---

@app.route("/api/feedback", methods=["POST"])
def feedback():
    data = request.json
    expected = data.get("expected")
    predicted = data.get("predicted")
    answers = data.get("answers")

    cursor.execute(
        "INSERT INTO feedback (expected, predicted, answers) VALUES (%s, %s, %s)",
        (expected, predicted, json.dumps(answers))
    )
    conn.commit()

    return jsonify({"status": "ok"})
