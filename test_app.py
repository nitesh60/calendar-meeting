import unittest
import json
from app import app, db, Meeting

class TestCalendarAPI(unittest.TestCase):

    def setUp(self):
        # Set up test environment
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        # Clean up after each test
        db.session.remove()
        db.drop_all()

    def test_add_meeting(self):
        # Test adding a meeting
        data = {
            'day': '2024-03-20',
            'start_time': '09:00',
            'end_time': '10:00',
            'attendees': ['John', 'Alice']
        }
        response = self.app.post('/add_meeting', json=data)
        self.assertEqual(response.status_code, 200)
        expected_output = {"message": "Meeting scheduled successfully."}

        # Test adding a meeting with missing data
        data_missing = {
            'day': '2024-03-20',
            'start_time': '09:00',
            'end_time': '10:00',
        }
        response_missing = self.app.post('/add_meeting', json=data_missing)
        self.assertEqual(response_missing.status_code, 400)
        expected_output_missing = {"message": "Failed to schedule meeting. Missing required data."}

        # Ensure that the response contains the expected error message
        response_data = json.loads(response_missing.get_data(as_text=True))
        self.assertEqual(response_data['message'], expected_output_missing['message'])

    def test_display_schedule(self):
        # Test displaying schedule when no meetings are added
        response = self.app.get('/schedule')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        expected_output = {"schedule": []}

        # Test displaying schedule after adding meetings
        meeting1 = Meeting(day='2024-03-20', start_time='09:00', end_time='10:00', attendees='John,Alice')
        meeting2 = Meeting(day='2024-03-21', start_time='10:00', end_time='11:00', attendees='Bob,Eve')
        db.session.add(meeting1)
        db.session.add(meeting2)
        db.session.commit()
        response = self.app.get('/schedule')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        expected_output = {
            "schedule": [
                {"day": "2024-03-20", "start_time": "09:00", "end_time": "10:00", "attendees": ["John", "Alice"]},
                {"day": "2024-03-21", "start_time": "10:00", "end_time": "11:00", "attendees": ["Bob", "Eve"]}
            ]
        }

if __name__ == '__main__':
    unittest.main()