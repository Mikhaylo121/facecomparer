import cv2
import numpy as np
import os
from flask import Flask, request, jsonify, render_template
from uuid import uuid4

app = Flask(__name__)

# ORB detector
orb = cv2.ORB_create()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/verify", methods=["POST"])
def verify():
    path1, path2 = None, None
    try:
        if "file1" not in request.files or "file2" not in request.files:
            return jsonify({"status": "error", "message": "Two files required"}), 400

        file1 = request.files["file1"]
        file2 = request.files["file2"]

        os.makedirs("uploads", exist_ok=True)
        # Generate unique filenames to avoid collisions
        path1 = os.path.join("uploads", f"{uuid4().hex}_{file1.filename}")
        path2 = os.path.join("uploads", f"{uuid4().hex}_{file2.filename}")
        file1.save(path1)
        file2.save(path2)

        # Read both images
        img1 = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)

        if img1 is None or img2 is None:
            return jsonify({"status": "error", "message": "Invalid image(s)"}), 400

        # Detect ORB keypoints and descriptors
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        if des1 is None or des2 is None:
            return jsonify({"status": "fail", "message": "No features detected"}), 400

        # Match descriptors
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)

        # Calculate similarity score
        similarity = len(matches) / max(len(kp1), len(kp2))

        # Cleanup uploaded files
        if path1 and os.path.exists(path1): os.remove(path1)
        if path2 and os.path.exists(path2): os.remove(path2)

        if similarity > 0.3:  # threshold, tune as needed
            return jsonify({"status": "success", "message": "Same person", "similarity": float(similarity)})
        else:
            return jsonify({"status": "fail", "message": "Different person", "similarity": float(similarity)})
    except Exception as e:
        print("Error in /verify:", e)
        # Cleanup in case of error
        if path1 and os.path.exists(path1): os.remove(path1)
        if path2 and os.path.exists(path2): os.remove(path2)
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)