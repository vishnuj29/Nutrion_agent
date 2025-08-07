from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish = db.Column(db.String(100))
    goal = db.Column(db.String(100))
    feedback = db.Column(db.Text)
