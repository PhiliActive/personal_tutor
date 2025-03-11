import re
import sqlite3
import os
from configparser import ConfigParser
from modules.logger import logger

# Load configuration
config = ConfigParser()
config.read("config/config.ini")
db_path = config["DATABASE"]["db_path"]

def connect_db():
    """Connect to the SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        logger.info("Connected to the database.")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise

def initialize_db():
    """Initialize the database with the required tables."""
    # Create the database directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = connect_db()
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

def validate_date(date):
    """Validate the date format (YYYY-MM-DD)."""
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    return bool(date_pattern.match(date))

def validate_time(time):
    """Validate the time format (HH:MM)."""
    time_pattern = re.compile(r"^\d{2}:\d{2}$")
    return bool(time_pattern.match(time))

def add_meeting(date, time, topics, referrals=""):
    """Add a new meeting to the database."""
    # Validate input data
    if not date or not time or not topics:
        return False, "Invalid input: date, time, and topics are required."

    if not validate_date(date):
        return False, f"Invalid date format: {date}. Expected format: YYYY-MM-DD."

    if not validate_time(time):
        return False, f"Invalid time format: {time}. Expected format: HH:MM."

    conn = connect_db()
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

def get_all_meetings():
    """Retrieve all meetings from the database."""
    conn = connect_db()
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

    def search_meetings(keyword):
        """Search meetings by keyword in topics or referrals."""
        conn = connect_db()
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