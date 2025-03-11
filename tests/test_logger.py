import unittest
import os
import time
import sqlite3
import tkinter as tk
from modules.gui import MISGUI
from modules.meeting_manager import MeetingManager
from modules.logger import logger

# Test database and log file paths
TEST_DB_FILE = "database/test_meetings.db"
TEST_LOG_FILE = "logs/test.log"

class TestMISGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test database and log file before running any tests."""
        os.makedirs(os.path.dirname(TEST_DB_FILE), exist_ok=True)
        os.makedirs(os.path.dirname(TEST_LOG_FILE), exist_ok=True)

        # Initialize the database
        cls.manager = MeetingManager()
        cls.manager.connect_db = lambda: sqlite3.connect(TEST_DB_FILE)
        cls.manager.initialize_db()

        # Initialize the Tkinter root window
        cls.root = tk.Tk()
        cls.gui = MISGUI(cls.root)

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
        cursor.execute("DELETE FROM meetings")  # Clear existing data
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='meetings'")  # Reset auto-increment IDs
        conn.commit()
        conn.close()

    def test_add_meeting(self):
        """Test adding a meeting through the GUI."""
        self.gui.date_entry.insert(0, "2023-10-01")
        self.gui.time_entry.insert(0, "14:30")
        self.gui.topics_entry.insert(0, "Test Topics 1")
        self.gui.referrals_entry.insert(0, "Test Referrals")

        self.gui.add_meeting()
        time.sleep(0.5)  # Ensure database update propagates

        # Fetch meetings from the database
        meetings = self.manager.view_all_meetings()
        print("Meetings in DB after add_meeting:", meetings)  # Debugging output

        self.assertEqual(len(meetings), 1, "There should be 1 meeting in the database")
        self.assertEqual(meetings[0][3], "Test Topics 1", "Meeting topic should match")

    def test_view_all_meetings(self):
        """Test viewing all meetings through the GUI."""
        self.manager.add_meeting("2023-10-01", "14:30", "Test Topics 1", "Referral 1")
        self.manager.add_meeting("2023-10-02", "15:30", "Test Topics 2", "Referral 2")

        self.gui.view_all_meetings()

        # Verify the result text area contains the meetings
        result_text = self.gui.result_text.get(1.0, tk.END)
        print("Result text:", repr(result_text))  # Debugging output

        self.assertIn("Test Topics 1", result_text, "Result text should contain 'Test Topics 1'")
        self.assertIn("Test Topics 2", result_text, "Result text should contain 'Test Topics 2'")

if __name__ == "__main__":
    unittest.main()