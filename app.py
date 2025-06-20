from flask import Flask, request, jsonify, send_from_directory
import os, psycopg2, json
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
CORS(app)

# PostgreSQL に接続
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("❌ DATABASE_URL is not set in environment variables.")

conn = psycopg2.connect(DATABASE_URL + "?sslmode=require")  # SSL required by Render
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

# ✅ トップページルートを追加（ここがポイント！）
@app.route("/")
def index():
    return "🚀 Flask app is running. Try POSTing to /api/feedback."

# ユーザーフィードバックAPI
@app.route("/api/feedback", methods=["POST"])
def feedback():
    data = request.json
    expected = data.get("expected")       # ユーザーが正解と思ったもの
    predicted = data.get("predicted")     # 推定結果
    answers = data.get("answers")         # ユーザーのyes/no回答

    cursor.execute(
        "INSERT INTO feedback (expected, predicted, answers) VALUES (%s, %s, %s)",
        (expected, predicted, json.dumps(answers))
    )
    conn.commit()

    return jsonify({"status": "ok"})
