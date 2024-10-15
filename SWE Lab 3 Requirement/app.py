from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "mysecrettoken"

matches = []


@app.before_request
def authenticate_token():
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401
    

@app.route("/add" , methods = ["POST"])
def Add_match():
    match = {

        "id" : len(matches) + 1,
        "score" : request.json.get("score"),
        "title" : request.json.get("title"),
        "location" : request.json.get("location")
    }
    matches.append(match)
    return jsonify(match)

    
@app.route("/match" , methods = ["GET"])
def get_matches():
    match_titles = []
    for i in matches:
        match_titles.append(i["title"])
    return match_titles


@app.route("/matches/<int:id>" , methods = ["PUT"])
def update_match(id):
    match = next((t for t in matches if t["id"] == id) , None)
    if match is None:
        return jsonify({"error" : "Match not found"}), 404
    match["title"] = request.json.get("title" , match["title"])
    match["score"] = request.json.get("score" , match["score"])
    return jsonify(match)


@app.route("/matches/<int:id>" , methods = ["DELETE"])
def delete_match(id):
    global matches
    matches = [t for t in matches if t["id"] != id]
    return '', 204

@app.route("/socres" , methods = ["GET"])
def scores():
    score = []
    for i in matches:
        score.append(i["score"])
    return score

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error" : "Resource not found"}), 404

if __name__ == "__main__":
    app.run(port=3000)
    