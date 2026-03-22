from flask import Flask, request, render_template, jsonify
import face_recognition

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/verify", methods=["POST"])
def verify_faces():
    photo1 = request.files["photo1"]
    photo2 = request.files["photo2"]

    img1 = face_recognition.load_image_file(photo1)
    img2 = face_recognition.load_image_file(photo2)

    enc1 = face_recognition.face_encodings(img1)[0]
    enc2 = face_recognition.face_encodings(img2)[0]

    distance = face_recognition.face_distance([enc1], enc2)[0]
    similarity = (1 - distance) * 100

    return jsonify({
        "verified": distance < 0.6,
        "similarity": f"{similarity:.2f}%"
    })

if __name__ == "__main__":
    app.run()