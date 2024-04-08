from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
db = SQLAlchemy(app)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.String(8), nullable=False)
    end_time = db.Column(db.String(8), nullable=False)
    attendees = db.Column(db.String(255), nullable=False)

@app.route("/add_meeting", methods=["POST"])
def add_meeting():
    data = request.get_json()
    if not all(key in data for key in ["day", "start_time", "end_time", "attendees"]):
        return jsonify({"message": "Failed to schedule meeting. Missing required data."}), 400

    # Check for collision with existing meetings
    existing_meetings = Meeting.query.filter_by(day=data["day"]).all()
    for meeting in existing_meetings:
        if data["start_time"] < meeting.end_time and data["end_time"] > meeting.start_time:
            return jsonify({"message": "Failed to schedule meeting. There is a scheduling conflict."}), 409

    # If no conflict, add the meeting
    meeting = Meeting(day=data["day"], start_time=data["start_time"], end_time=data["end_time"],
                      attendees=",".join(data.get("attendees", [])))
    db.session.add(meeting)
    try:
        db.session.commit()
        return jsonify({"message": "Meeting scheduled successfully."}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "Failed to schedule meeting."}), 500

@app.route("/schedule", methods=["GET"])
def display_schedule():
    meetings = Meeting.query.all()
    schedule = [{"day": meeting.day, "start_time": meeting.start_time, "end_time": meeting.end_time,
                 "attendees": meeting.attendees.split(",")} for meeting in meetings]
    return jsonify({"schedule": schedule}), 200

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
