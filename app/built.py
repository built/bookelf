# A collection of utility functions for Built projects.

def to_previous_page(request):
	from django.http import HttpResponseRedirect
	"""
	Returns the user to the previous page (where their request started) or to the site root if no previous page is known.
	"""
	return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
