"""
Error logging system
Logs errors and important events to file for debugging
"""

import logging
import os
from datetime import datetime

def setup_logger():
	"""Setup application logger"""
	# Create logs directory if it doesn't exist
	if not os.path.exists('logs'):
		os.makedirs('logs')
	
	# Create log filename with date
	log_filename = f"logs/app_log_{datetime.now().strftime('%Y%m%d')}.log"
	
	# Configure logging
	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(levelname)s - %(message)s',
		handlers=[
			logging.FileHandler(log_filename),
			logging.StreamHandler()  # Also print to console
		]
	)
	
	return logging.getLogger('HandMouseController')

# Create logger instance
logger = setup_logger()

def log_info(message):
	"""Log info message"""
	logger.info(message)

def log_error(message, exception=None):
	"""Log error message"""
	if exception:
		logger.error(f"{message}: {str(exception)}", exc_info=True)
	else:
		logger.error(message)

def log_warning(message):
	"""Log warning message"""
	logger.warning(message)

def log_debug(message):
	"""Log debug message"""
	logger.debug(message)