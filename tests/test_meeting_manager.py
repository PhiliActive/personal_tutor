import unittest
import sqlite3
import os
from modules.meeting_manager import MeetingManager
from modules.logger import logger

# Test database and log file paths
TEST_DB_FILE = "database/test_meetings.db"
TEST_LOG_FILE = "logs/test.log"

class TestMeetingManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test database and log file before running any tests."""
        # Override the database and log file paths for testing
        os.environ["DB_PATH"] = TEST_DB_FILE
        os.environ["LOG_FILE"] = TEST_LOG_FILE

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(TEST_DB_FILE), exist_ok=True)
        os.makedirs(os.path.dirname(TEST_LOG_FILE), exist_ok=True)

        # Initialize the database
        cls.manager = MeetingManager()
        cls.manager.connect_db = lambda: sqlite3.connect(TEST_DB_FILE)
        cls.manager.initialize_db()

    @classmethod
    def tearDownClass(cls):
        """Clean up the test database and log file after all tests are done."""
        if os.path.exists(TEST_DB_FILE):
            os.remove(TEST_DB_FILE)
        if os.path.exists(TEST_LOG_FILE):
            os.remove(TEST_LOG_FILE)

    def setUp(self):
        """Clear the database before each test."""
        conn = sqlite3.connect(TEST_DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM meetings")
        conn.commit()
        conn.close()

    def test_validate_date(self):
        """Test the date validation function."""
        self.assertTrue(MeetingManager.validate_date("2023-10-01"), "Valid date should return True")
        self.assertFalse(MeetingManager.validate_date("2023-13-01"), "Invalid date should return False")

    def test_validate_time(self):
        """Test the time validation function."""
        self.assertTrue(MeetingManager.validate_time("14:30"), "Valid time should return True")
        self.assertFalse(MeetingManager.validate_time("25:00"), "Invalid time format should return False")

    def test_add_meeting(self):
        """Test adding a meeting to the database."""
        success, message = self.manager.add_meeting("2023-10-01", "14:30", "Test Topics", "Test Referrals")
        self.assertTrue(success, "Meeting should be added successfully")
        self.assertEqual(message, "Meeting added successfully!", "Success message should match")

    def test_view_all_meetings(self):
        """Test retrieving all meetings from the database."""
        self.manager.add_meeting("2023-10-01", "14:30", "Test Topics 1")
        self.manager.add_meeting("2023-10-02", "15:30", "Test Topics 2")

        meetings = self.manager.view_all_meetings()
        self.assertEqual(len(meetings), 2, "There should be 2 meetings in the database")

    def test_search_meetings(self):
        """Test searching meetings by keyword."""
        self.manager.add_meeting("2023-10-01", "14:30", "Test Topics 1", "Referral 1")
        self.manager.add_meeting("2023-10-02", "15:30", "Test Topics 2", "Referral 2")

        meetings = self.manager.search_meetings("Test Topics 1")
        self.assertEqual(len(meetings), 1, "There should be 1 meeting matching the keyword")

if __name__ == "__main__":
    unittest.main()