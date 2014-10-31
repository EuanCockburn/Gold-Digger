from django.template import RequestContext
from django.shortcuts import render_to_response
from GChartWrapper import Pie

import logging
from logging.config import dictConfig
from pythonjsonlogger import jsonlogger

dictConfig(LOGGING)
logger = logging.getLogger('my_logger')
logger.debug('foo')

def index(request):
    context = RequestContext(request)
    data = [['100',10],['90',9],['80',8]]
    context_dict = {'pie': Pie(data).title('Hello Pie').color('red','lime').label('hello', 'world')}
    return render_to_response('analytics/index.html', context_dict, context)
