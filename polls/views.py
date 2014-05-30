from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from polls.models import Poll, Choice

"""List View abstracts displaying a list of objects,
	and Detail View abstracts displaying a detail page for
	a particular kind of object

	Generic views need to know what model they are acting upon.
		*Provided with model attribute

	Detail Views expect primary key captured from url to be pk, so change poll_id to pk.

	Detail Views use <app name>/<model name>_detail.html. template_name overrides this.

	For a Detail View, poll variable supplied automatically

	For List View, generated context variable is poll_list...override with context_object_name"""

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_poll_list'

	def get_queryset(self):
		#Return 5 most recent polls
		return Poll.objects.order_by('-pub_date')[:5]

#Below is the 'hard way' to do what is above. Got rid of it to reduce code reduncdancy
"""def index(request):
	latest_poll_list = Poll.objects.order_by('pub_date')[:5]
	context = {'latest_poll_list': latest_poll_list}
	return render(request, 'polls/index.html', context)
	
	#Below is the same, more or less, as above
	#template = loader.get_template('polls/index.html')
	#context = RequestContext(request, {
	#	'latest_poll_list': latest_poll_list
	#	})
	#return HttpResponse(template.render(context))"""

class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.html'

#'hard way'
"""def detail(request, poll_id): 
	
	poll = get_object_or_404(Poll, pk=poll_id) 
	
	#Above line does the exact same thing as the code below.
	#try:
	#	poll = Poll.objects.get(pk=poll_id)
	#except Poll.DoesNotExist:
	#	raise Http404
	
	return render(request, 'polls/detail.html', {'poll': poll})"""

class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'polls/results.html'

#'hard way'
"""def results(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	return render(request, 'polls/results.html', {'poll': p})"""

def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except(KeyError, Choice.DoesNotExist):
		#Show Poll detail page.
		return render(request, 'polls/detail.html', {
			'poll': p,
			'error_message': "You didn't vote on a choice"
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		#When dealing with post data, always use HttpResponseRedirect
		#Prevents data from being posted twice!! (good thing)!!

		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))




