"""
WorkspaceLogger: A logger that writes to its own log file per workspace session.
"""
import logging
import os
from datetime import datetime

class WorkspaceLogger:
    def __init__(self, log_dir="logs"):
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = os.path.join(log_dir, f"workspace_{timestamp}.log")
        self.logger = logging.getLogger(f"WorkspaceLogger_{timestamp}")
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.log_path = log_path

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def get_log_path(self):
        return self.log_path
