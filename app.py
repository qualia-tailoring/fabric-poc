from flask import Flask, request, jsonify, render_template
import os, psycopg2, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# マッピング定義（0 or 1 で特徴を持っているかを示す）
FABRIC_DB = {
    "サテン":      {"gloss": 1, "diagonal": 0, "breathable": 0, "surface": 0, "luxury": 1, "stretch": 0},
    "ツイル（綾織）": {"gloss": 0, "diagonal": 1, "breathable": 1, "surface": 0, "luxury": 0, "stretch": 0},
    "鹿の子":      {"gloss": 0, "diagonal": 0, "breathable": 1, "surface": 1, "luxury": 0, "stretch": 1},
    "ブロード(平織)":       {"gloss": 0, "diagonal": 0, "breathable": 1, "surface": 0, "luxury": 0, "stretch": 0},
    "ジャカード":   {"gloss": 1, "diagonal": 0, "breathable": 0, "surface": 1, "luxury": 1, "stretch": 0}
}


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
def infer():
    user_input = request.json
    user_vector = to_vector(user_input)

    # 類似度を計算
    best_match = None
    best_score = -1
    for fabric, features in FABRIC_DB.items():
        score = similarity(user_vector, features)
        if score > best_score:
            best_score = score
            best_match = fabric

    return jsonify({"result": best_match})
