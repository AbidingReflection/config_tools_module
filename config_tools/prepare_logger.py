import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
import sys
import os
from datetime import datetime

class CustomFormatter(logging.Formatter):
    """Custom formatter to handle microsecond-level timestamp logging."""
    
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = datetime.fromtimestamp(record.created).strftime(datefmt)
        else:
            t = datetime.fromtimestamp(record.created)
            s = t.strftime("%Y-%m-%d %H:%M:%S") + ",%03d" % (record.msecs)
        return s

def prepare_logger(log_path: str, output_name_prefix="") -> Logger:
    """Create and configure a logger with both console and file handlers."""
    
    # Ensure the specified log_path directory exists
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # Generate a timestamp string for the log file name
    timestamp_str = datetime.now().strftime('%Y_%m_%d_%H%M%S')
    log_file = os.path.join(log_path, f"{output_name_prefix}{timestamp_str}.log")

    # Create the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Log format with the correct timestamp format
    log_format = CustomFormatter(fmt='%(asctime)s %(levelname)s: %(message)s',
                                 datefmt='%Y-%m-%d %H:%M:%S.%f')

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)

    # File handler (RotatingFileHandler for automatic log rotation)
    file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)

    # Add the handlers to the logger
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
