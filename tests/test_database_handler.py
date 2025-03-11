# tests/test_database_handler.py
import unittest
import os
import sqlite3
from modules.database_handler import connect_db, initialize_db, validate_date, validate_time, add_meeting, get_all_meetings, search_meetings
from modules.logger import logger

# Test database and log file paths
TEST_DB_FILE = "database/test_meetings.db"
TEST_LOG_FILE = "logs/test.log"

class TestDatabaseHandler(unittest.TestCase):
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
        initialize_db()

    @classmethod
    def tearDownClass(cls):
        """Clean up the test database and log file after all tests are done."""
        if os.path.exists(TEST_DB_FILE):
            os.remove(TEST_DB_FILE)
        if os.path.exists(TEST_LOG_FILE):
            os.remove(TEST_LOG_FILE)

    def setUp(self):
        """Clear the database before each test."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM meetings")
        conn.commit()
        conn.close()

    def test_validate_date(self):
        """Test the date validation function."""
        self.assertTrue(validate_date("2023-10-01"), "Valid date should return True")
        self.assertFalse(validate_date("2023/10/01"), "Invalid date format should return False")
        self.assertFalse(validate_date("2023-13-01"), "Invalid date should return False")

    def test_validate_time(self):
        """Test the time validation function."""
        self.assertTrue(validate_time("14:30"), "Valid time should return True")
        self.assertFalse(validate_time("25:00"), "Invalid time format should return False")
        self.assertFalse(validate_time("14:60"), "Invalid time should return False")

    def test_add_meeting(self):
        """Test adding a meeting to the database."""
        success, message = add_meeting("2023-10-01", "14:30", "Test Topics", "Test Referrals")
        self.assertTrue(success, "Meeting should be added successfully")
        self.assertEqual(message, "Meeting added successfully!", "Success message should match")

        # Test invalid date format
        success, message = add_meeting("2023/10/01", "14:30", "Test Topics")
        self.assertFalse(success, "Invalid date format should return False")
        self.assertEqual(message, "Invalid date format: 2023/10/01. Expected format: YYYY-MM-DD.", "Error message should match")

        # Test invalid time format
        success, message = add_meeting("2023-10-01", "25:00", "Test Topics")
        self.assertFalse(success, "Invalid time format should return False")
        self.assertEqual(message, "Invalid time format: 25:00. Expected format: HH:MM.", "Error message should match")

    def test_get_all_meetings(self):
        """Test retrieving all meetings from the database."""
        add_meeting("2023-10-01", "14:30", "Test Topics 1")
        add_meeting("2023-10-02", "15:30", "Test Topics 2")

        meetings = get_all_meetings()
        self.assertEqual(len(meetings), 2, "There should be 2 meetings in the database")
        self.assertEqual(meetings[0][2], "14:30", "First meeting time should match")
        self.assertEqual(meetings[1][2], "15:30", "Second meeting time should match")

    def test_search_meetings(self):
        """Test searching meetings by keyword."""
        add_meeting("2023-10-01", "14:30", "Test Topics 1", "Referral 1")
        add_meeting("2023-10-02", "15:30", "Test Topics 2", "Referral 2")

        meetings = search_meetings("Test Topics 1")
        self.assertEqual(len(meetings), 1, "There should be 1 meeting matching the keyword")
        self.assertEqual(meetings[0][3], "Test Topics 1", "Meeting topic should match")

        meetings = search_meetings("Referral 2")
        self.assertEqual(len(meetings), 1, "There should be 1 meeting matching the keyword")
        self.assertEqual(meetings[0][4], "Referral 2", "Meeting referral should match")

if __name__ == "__main__":
    unittest.main()