# Calendar Meeting Scheduler
This is a simple Flask application for scheduling meetings and displaying the schedule.

# Setup

```bash
# Clone the repository
git clone https://github.com/nitesh60/calendar-meeting.git

# Navigate to the project directory
cd calendar-meeting

# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python app.py
```
Clone the repository to your local machine:

```bash
Copy code
git clone <repository_url>
Navigate to the project directory:
```
# bash
Copy code
cd calendar-meeting
Install the required dependencies:

# bash
Copy code
pip install -r requirements.txt
Run the Flask application:

```bash
Copy code
python app.py
Usage
Adding a Meeting
To add a meeting, send a POST request to the /add_meeting endpoint with the meeting details in JSON format.
```
# Example:

```bash
Copy code
curl -X POST -H "Content-Type: application/json" -d '{"day":"2024-03-20", "start_time":"09:00", "end_time":"10:00", "attendees":["John", "Alice"]}' http://127.0.0.1:5000/add_meeting
Displaying Schedule
To display the schedule of all meetings, send a GET request to the /schedule endpoint.
```
Example:

```bash
Copy code
curl http://127.0.0.1:5000/schedule
Technologies Used
Flask: A micro web framework for Python.
SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
SQLite: A lightweight disk-based database engine.
```
