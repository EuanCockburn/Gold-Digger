import logging 
from pythonjsonlogger import jsonlogger
import json
import time

class Logger:
	number = 1

	def __init__(self):
		logging.basicConfig(filename='logs/example1.log',level=logging.ERROR)
		self.logger = logging.getLogger()
		self.logHandler = logging.StreamHandler()
		self.formatter = jsonlogger.JsonFormatter()
		self.logHandler.setFormatter(self.formatter)
		self.logger.addHandler(self.logHandler)

	def jdefault(self, object):
	    return object.__dict__

	def log(self, object, type):
		self.logger.error(json.dumps(Log(object, type),  default=self.jdefault))

class Log:
	def __init__(self, object, type):
		self.timestamp = time.time()
		self.type = type
		if type == log_type.START_GAME:
			self.body = object

class log_type:
    START_GAME = 1
    MOVE = 2
    DIG = 3

logger = Logger()