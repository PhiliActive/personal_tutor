import logging
import os
from configparser import ConfigParser

# Default configurations
DEFAULT_LOG_FILE = "logs/test.log"
DEFAULT_LOG_LEVEL = "INFO"

# Load configuration
config = ConfigParser()
config.read("config/config.ini")

# Get log file and log level from config, or use defaults
log_file = config.get("LOGGING", "log_file", fallback=DEFAULT_LOG_FILE)
log_level = config.get("LOGGING", "log_level", fallback=DEFAULT_LOG_LEVEL)

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=getattr(logging, log_level, logging.INFO),  # Convert string log level to logging level
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Ensure logger instance has the correct level
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, log_level, logging.INFO))  # Explicitly set level
