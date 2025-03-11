import unittest
import os
import logging
import importlib
from modules.logger import logger

# Test log file path
TEST_LOG_FILE = "logs/test.log"

class TestLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test log file before running any tests."""
        os.makedirs(os.path.dirname(TEST_LOG_FILE), exist_ok=True)
        
        # Ensure the log file exists before testing
        with open(TEST_LOG_FILE, "w") as f:
            f.write("")  # Create an empty log file
        
        # Reload logger module to ensure fresh configuration
        import modules.logger
        importlib.reload(modules.logger)
        from modules.logger import logger
        cls.logger = logger
        
        # Clear existing handlers and reconfigure logging
        cls.logger.handlers.clear()

        # Create a file handler manually and attach it
        file_handler = logging.FileHandler(TEST_LOG_FILE)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        
        cls.logger.addHandler(file_handler)
        cls.logger.setLevel(logging.INFO)

    @classmethod
    def tearDownClass(cls):
        """Clean up the test log file after all tests are done."""
        # Close all handlers before deleting the log file
        for handler in cls.logger.handlers[:]:
            handler.close()
            cls.logger.removeHandler(handler)
        
        if os.path.exists(TEST_LOG_FILE):
            os.remove(TEST_LOG_FILE)

    def test_logger_initialization(self):
        """Test if the logger is initialized correctly."""
        self.assertIsNotNone(self.logger, "Logger should be initialized")
        self.assertEqual(self.logger.getEffectiveLevel(), logging.INFO, "Logger level should be INFO")

    def test_logger_output(self):
        """Test if the logger writes to the log file."""
        test_message = "This is a test log message."
        self.logger.info(test_message)

        # Verify the log file contains the test message
        with open(TEST_LOG_FILE, "r") as log_file:
            log_content = log_file.read()
            self.assertIn(test_message, log_content, "Log file should contain the test message")

if __name__ == "__main__":
    unittest.main()