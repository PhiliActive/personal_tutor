import logging
import os
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read("config/config.ini")

# Set up logging
log_file = config["LOGGING"]["log_file"]
log_level = config["LOGGING"]["log_level"]

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=log_level,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)