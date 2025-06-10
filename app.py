
from flask import Flask, request, jsonify, send_from_directory
import os
from flask_cors import CORS


app = Flask(__name__, static_url_path='')
CORS(app)

# マッピング定義（0 or 1 で特徴を持っているかを示す）
FABRIC_DB = {
    "サテン":      {"gloss": 1, "diagonal": 0, "breathable": 0, "surface": 0, "luxury": 1, "stretch": 0},
    "ツイル（綾織）": {"gloss": 0, "diagonal": 1, "breathable": 1, "surface": 0, "luxury": 0, "stretch": 0},
    "鹿の子":      {"gloss": 0, "diagonal": 0, "breathable": 1, "surface": 1, "luxury": 0, "stretch": 1},
    "平織":       {"gloss": 0, "diagonal": 0, "breathable": 1, "surface": 0, "luxury": 0, "stretch": 0},
    "ジャカード":   {"gloss": 1, "diagonal": 0, "breathable": 0, "surface": 1, "luxury": 1, "stretch": 0}
}

def to_vector(answer_dict):
    """yes/noの回答を0 or 1 に変換"""
    return {k: 1 if v == "yes" else 0 for k, v in answer_dict.items()}

def similarity(vec1, vec2):
    """単純な一致数によるスコア"""
    return sum(1 for k in vec1 if vec1[k] == vec2.get(k, -1))

@app.route("/api/infer", methods=["POST"])
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

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



    
