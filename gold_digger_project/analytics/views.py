from django.template import RequestContext
from django.shortcuts import render_to_response
from GChartWrapper import Pie

def index(request):
    context = RequestContext(request)
    context_dict = {'pie': Pie([10,10]).title('Male/Female ratio').color('red','lime').label('male', 'female')}
    return render_to_response('analytics/index.html', context_dict, context)
