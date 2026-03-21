from flask import Flask, request, render_template, jsonify
from deepface import DeepFace

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/verify", methods=["POST"])
def verify_faces():
    photo1 = request.files["photo1"]
    photo2 = request.files["photo2"]

    result = DeepFace.verify(photo1, photo2)

    similarity = (1 - result["distance"]) * 100
    return jsonify({
        "verified": result["verified"],
        "similarity": f"{similarity:.2f}%"
    })

if __name__ == "__main__":
    app.run()