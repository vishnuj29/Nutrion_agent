from flask import Flask, render_template, request
from utils import (
    get_nutrition_facts, generate_meal_plan,
    explain_food_choice, extract_text_from_image
)
from models import db, UserFeedback
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    data = {}
    if request.method == "POST":
        dish = request.form.get("dish", "")
        goal = request.form.get("goal", "")
        feedback = request.form.get("feedback", "")
        image = request.files.get("image")

        # OCR: extract dish name from image
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            data["image_path"] = image_path
            ocr_text = extract_text_from_image(image_path)
            dish = ocr_text or dish

        if dish:
            data["nutrition"] = get_nutrition_facts(dish)
            data["explanation"] = explain_food_choice(dish)

        if goal:
            data["meal_plan"] = generate_meal_plan(goal)

        # Store user feedback
        if feedback:
            new_entry = UserFeedback(dish=dish, goal=goal, feedback=feedback)
            db.session.add(new_entry)
            db.session.commit()

        data["feedback_history"] = UserFeedback.query.order_by(UserFeedback.id.desc()).limit(5).all()

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
