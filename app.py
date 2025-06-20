from flask import Flask, request, jsonify, render_template
import os, psycopg2, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# PostgreSQL 接続設定
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("❌ DATABASE_URL is not set in environment variables.")

conn = psycopg2.connect(DATABASE_URL + "?sslmode=require")
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

# ✅ index.html を返す
@app.route("/")
def index():
    return render_template("index.html")

# ✅ ユーザーフィードバック保存エンドポイント
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

# ✅ 推論エンドポイント（仮）
@app.route("/api/infer", methods=["POST"])
def infer():
    # 仮で "ツイル（綾織）" を返すように
    return jsonify({"result": "ツイル（綾織）"}), 200
