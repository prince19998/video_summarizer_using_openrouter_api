from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
    key_points = db.Column(db.Text, nullable=False)
    action_items = db.Column(db.Text, nullable=False)
    generated_at = db.Column(db.DateTime, nullable=False)
    
    meeting = db.relationship('Meeting', backref=db.backref('summary', uselist=False))