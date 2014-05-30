from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader

from polls.models import Poll

def index(request):
	latest_poll_list = Poll.objects.order_by('pub_date')[:5]
	context = {'latest_poll_list': latest_poll_list}
	return render(request, 'polls/index.html', context)
	
	"""Below is the same, more or less, as above"""
	#template = loader.get_template('polls/index.html')
	#context = RequestContext(request, {
	#	'latest_poll_list': latest_poll_list
	#	})
	#return HttpResponse(template.render(context))

def detail(request, poll_id): 
	
	poll = get_object_or_404(Poll, pk=poll_id) 
	
	#Above line does the exact same thing as the code below.
	#try:
	#	poll = Poll.objects.get(pk=poll_id)
	#except Poll.DoesNotExist:
	#	raise Http404
	
	return render(request, 'polls/detail.html', {'poll': poll})


def results(request, poll_id):
	return HttpResponse("You are looking at the results of poll %s" % poll_id)

def vote(request, poll_id):
	return HttpResponse("You are voting for poll %s" % poll_id)




