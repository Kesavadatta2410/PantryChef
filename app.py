from flask import Flask, render_template, request, jsonify, url_for
import os
from werkzeug.utils import secure_filename
import predict  # Import ML model functions
import generate  # Gemini API for recipes
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("firebaseConfig.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Function to check allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    try:
        user = auth.create_user(email=email, password=password)
        return jsonify({"message": "User created successfully", "uid": user.uid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    try:
        user = auth.get_user_by_email(email)
        return jsonify({"message": "Login successful", "uid": user.uid}), 200
    except Exception as e:
        return jsonify({"error": "Invalid email or password"}), 401


@app.route("/")
def home():
    return render_template("generator.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format"}), 400

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Predict using ML model
        detected_ingredient, confidence = predict.predict_image(file_path)
        if "Error" in detected_ingredient:
            return jsonify({"error": detected_ingredient}), 500

        # Get manual ingredients
        manual_ingredients = request.form.get("manual_ingredients", "").strip()
        all_ingredients = detected_ingredient
        if manual_ingredients:
            all_ingredients = f"{manual_ingredients}, {detected_ingredient}"

        # Generate recipes
        recipes = generate.get_recipes(all_ingredients)

        return jsonify({
            "image_url": url_for("static", filename=f"uploads/{filename}"),
            "ingredients": all_ingredients,
            "recipes": recipes
        })
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
