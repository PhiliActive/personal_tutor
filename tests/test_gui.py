# In tests/test_gui.py
import unittest
import os
import sys
import sqlite3
import tkinter as tk

# Adjust the Python path to include the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import the gui module from the modules folder
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
        cursor.execute("DELETE FROM meetings")
        conn.commit()
        conn.close()

    def test_add_meeting(self):
        """Test adding a meeting through the GUI."""
        # Simulate user input
        self.gui.date_entry.insert(0, "2023-10-01")
        self.gui.time_entry.insert(0, "14:30")
        self.gui.topics_entry.insert(0, "Test Topics")
        self.gui.referrals_entry.insert(0, "Test Referrals")

        # Trigger the add_meeting method
        self.gui.add_meeting()

        # Verify the meeting was added to the database
        meetings = self.manager.view_all_meetings()
        self.assertEqual(len(meetings), 1, "There should be 1 meeting in the database")

        # Verify the input fields are cleared
        self.assertEqual(self.gui.date_entry.get(), "", "Date entry should be cleared")
        self.assertEqual(self.gui.time_entry.get(), "", "Time entry should be cleared")
        self.assertEqual(self.gui.topics_entry.get(), "", "Topics entry should be cleared")
        self.assertEqual(self.gui.referrals_entry.get(), "", "Referrals entry should be cleared")

    def test_view_all_meetings(self):
        """Test viewing all meetings through the GUI."""
        # Add test meetings to the database
        self.manager.add_meeting("2023-10-01", "14:30", "Test Topics 1")
        self.manager.add_meeting("2023-10-02", "15:30", "Test Topics 2")

        # Trigger the view_all_meetings method
        self.gui.view_all_meetings()

        # Verify the result text area contains the meetings
        result_text = self.gui.result_text.get(1.0, tk.END)
        self.assertIn("Test Topics 1", result_text, "Result text should contain 'Test Topics 1'")
        self.assertIn("Test Topics 2", result_text, "Result text should contain 'Test Topics 2'")

    def test_search_meetings(self):
        """Test searching meetings through the GUI."""
        # Add test meetings to the database
        self.manager.add_meeting("2023-10-01", "14:30", "Test Topics 1", "Referral 1")
        self.manager.add_meeting("2023-10-02", "15:30", "Test Topics 2", "Referral 2")

        # Simulate user input in the search entry
        self.gui.search_entry.insert(0, "Test Topics 1")

        # Trigger the search_meetings method
        self.gui.search_meetings()

        # Verify the result text area contains the correct meeting
        result_text = self.gui.result_text.get(1.0, tk.END)
        self.assertIn("Test Topics 1", result_text, "Result text should contain 'Test Topics 1'")
        self.assertNotIn("Test Topics 2", result_text, "Result text should not contain 'Test Topics 2'")

    def test_clear_results(self):
        """Test clearing the result text area."""
        # Add some text to the result text area
        self.gui.result_text.insert(tk.END, "Test Text")

        # Trigger the clear_results method
        self.gui.clear_results()

        # Verify the result text area is cleared
        result_text = self.gui.result_text.get(1.0, tk.END)
        self.assertEqual(result_text, "\n", "Result text area should be cleared")

if __name__ == "__main__":
    unittest.main()