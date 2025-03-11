import re
import sqlite3
from modules.logger import logger

class MeetingManager:
    def __init__(self):
        self.initialize_db()  # Ensure the table exists when the class is instantiated

    def connect_db(self):
        """Connect to the SQLite database."""
        try:
            conn = sqlite3.connect("database/meetings.db")  # Update with your database path
            logger.info("Connected to the database.")
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise

    # validate the date format
    @staticmethod
    def validate_date(date):
        """Validate the date format (YYYY-MM-DD)."""
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        return bool(date_pattern.match(date))

    # validate the time format
    @staticmethod
    def validate_time(time):
        """Validate the time format (HH:MM)."""
        time_pattern = re.compile(r"^\d{2}:\d{2}$")
        return bool(time_pattern.match(time))

    def initialize_db(self):
        """Initialize the database with the required tables."""
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS meetings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    topics TEXT NOT NULL,
                    referrals TEXT
                )
            """)
            conn.commit()
            logger.info("Database initialized successfully.")
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {e}")
            raise
        finally:
            conn.close()

    # function to add meeting to db also includes validation of input
    def add_meeting(self, date, time, topics, referrals=""):
        """Add a new meeting to the database."""
        # Validate input data
        if not date or not time or not topics:
            return False, "Invalid input: date, time, and topics are required."

        if not self.validate_date(date):
            return False, f"Invalid date format: {date}. Expected format: YYYY-MM-DD."

        if not self.validate_time(time):
            return False, f"Invalid time format: {time}. Expected format: HH:MM."

        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO meetings (date, time, topics, referrals)
                VALUES (?, ?, ?, ?)
            """, (date, time, topics, referrals))
            conn.commit()
            logger.info(f"Added meeting: {date}, {time}, {topics}, {referrals}")
            return True, "Meeting added successfully!"
        except sqlite3.Error as e:
            logger.error(f"Error adding meeting: {e}")
            return False, f"Failed to add meeting: {e}"
        finally:
            conn.close()

    # function to view all meeting from the db
    def view_all_meetings(self):
        """Retrieve all meetings from the database."""
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, date, time, topics, referrals FROM meetings")
            meetings = cursor.fetchall()
            logger.info("Retrieved all meetings.")
            return meetings
        except sqlite3.Error as e:
            logger.error(f"Error retrieving meetings: {e}")
            raise
        finally:
            conn.close()

    # function to search a specific meeting from the db
    def search_meetings(self, keyword):
        """Search meetings by keyword in topics or referrals."""
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, date, time, topics, referrals FROM meetings
                WHERE topics LIKE ? OR referrals LIKE ?
            """, (f"%{keyword}%", f"%{keyword}%"))
            meetings = cursor.fetchall()
            logger.info(f"Found {len(meetings)} meetings matching '{keyword}'.")
            return meetings
        except sqlite3.Error as e:
            logger.error(f"Error searching meetings: {e}")
            raise
        finally:
            conn.close()