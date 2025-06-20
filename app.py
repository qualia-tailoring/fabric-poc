from flask import Flask, request, jsonify, send_from_directory
import os, psycopg2, json
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
CORS(app)

# PostgreSQL に接続
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT") ,
    sslmode="require" 
)
cursor = conn.cursor()
print("DB_HOST:", os.getenv("DB_HOST"))  # デバッグ用に一時的に出力

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
    expected = data.get("expected")       # ユーザーが正解と思ったもの
    predicted = data.get("predicted")     # 推定結果
    answers = data.get("answers")         # ユーザーのyes/no回答

    cursor.execute(
        "INSERT INTO feedback (expected, predicted, answers) VALUES (%s, %s, %s)",
        (expected, predicted, json.dumps(answers))
    )
    conn.commit()

    return jsonify({"status": "ok"})
