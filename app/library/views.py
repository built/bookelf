from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from models import MediaItem, MediaItemOwnership, MediaLoan
from forms import MediaItemSearchForm
from tools import count_books_in_library
from search import book_search
from django.core.paginator import Paginator

#----------------------------------------------------------------------------
# Views
#----------------------------------------------------------------------------
@login_required
def show_search_form(request):
	return render_to_response("library/search.html", {"library_size": count_books_in_library(), "search_form": MediaItemSearchForm() }, context_instance=RequestContext(request))


@require_GET
@login_required
def search(request):
	
	
	items_per_page = 15
	
	items = paginate_items(request, book_search(request), items_per_page)

	return render_to_response('library/list.html', {"items": items}, RequestContext(request))

@require_GET
@login_required
def show_my_library(request):

	items_per_page = 15
	
	items = paginate_items(request, MediaItemOwnership.objects.filter(owner=request.user), items_per_page)

	return render_to_response('library/user/list.html', {"items": items}, RequestContext(request))


def paginate_items(request, items, items_per_page):
	
	page_manager = Paginator(items, items_per_page)

    # Make sure page request is an int. If not, deliver first page.
	try:
		page = int( request.GET.get('page', '1') )
	except ValueError:
		page = 1

    # If page request (9999) is out of range, deliver last page of results.
	try:
		page_of_items = page_manager.page(page)
	except:
		page_of_items = page_manager.page(page_manager.num_pages)

	return page_of_items


@login_required
def show_my_loans(request):
	"""
	Show the books this user has loaned out to other users.
	"""
	return object_list(request, queryset = MediaLoan.objects.filter(item__owner=request.user), template_name="library/user/loaned.html")


@login_required
def show_my_borrows(request):
	"""
	Show the books this user has loaned out to other users.
	"""
	return object_list(request, queryset = MediaLoan.objects.filter(borrower=request.user), template_name="library/user/borrowed.html")


@login_required
def show_new_book_form(request):
	return render_to_response("book/editor.html", {"book_form": BookForm() }, context_instance=RequestContext(request))



from django.contrib.auth.models import User
from operator import itemgetter

@require_GET
@login_required
def show_leaderboard(request):

	""" Show the 5 users who have shared the most titles on the system """
	LEADERS_WANTED = 5

	# This ended up more difficult than I expected.
	# Seems like Django's ORM could do this work for us. 
	# Maybe I've just missed it.

	items = {}
	
	# Map/Reduce username/book pairs into a count for each user.
	for username in [item.owner.username for item in MediaItemOwnership.objects.all()]:
		items[username] = items[username] + 1 if username in items else 1

	# Unpack the top users from the reduce hash and build a 'helper' object with username/bookcount fields.
	top_list = sorted(items.iteritems(), key=itemgetter(1), reverse=True)[:LEADERS_WANTED]
	
	leaders = [ {'username': item[0], 'bookcount': item[1]} for item in top_list ]
	
	return render_to_response('leaderboard.html', {"leaders": leaders}, RequestContext(request))












