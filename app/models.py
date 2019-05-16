from .db import db

class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer)
    minutes_reported = db.Column(db.Integer)
    # One of the submitters is a beginner
    has_beginner = db.Column(db.Boolean)
