from django.template import RequestContext
from django.shortcuts import render_to_response
from GChartWrapper import Pie

import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(levelname)s %(asctime)s%(module)s%(process)d%(message)s%(pathname)s$(lineno)d$(funcName)s')
handler.setFormatter(formatter)
logging.basicConfig(filename='logs/example.log')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.debug('ASD')

def index(request):
    context = RequestContext(request)
    context_dict = {'pie': Pie([10,10]).title('Male/Female ratio').color('red','lime').label('male', 'female')}
    return render_to_response('analytics/index.html', context_dict, context)
