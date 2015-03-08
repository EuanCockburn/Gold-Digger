import os
import logging

work_dir = os.getcwd()
log_file = os.path.join(work_dir, 'logs/log')
event_logger = logging.getLogger('event_log')
event_logger_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s %(message)s')
event_logger_handler.setFormatter(formatter)
event_logger.addHandler(event_logger_handler)
event_logger.setLevel(logging.INFO)