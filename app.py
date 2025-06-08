
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_url_path='')

woven_data = [
    {"name": "平織", "gloss": "low"},
    {"name": "朱子織", "gloss": "high"},
]

@app.route("/api/infer", methods=["POST"])
def infer():
    data = request.json
    result = "不明"
    for item in woven_data:
        if item.get("gloss") == data.get("gloss"):
            result = item["name"]
            break
    return jsonify({"result": result})

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    app.run(debug=True)
