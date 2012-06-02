#----------------------------------------------------------------------------
# Functions to provide book-search for the virtual library.
#----------------------------------------------------------------------------
from django.db.models import Q
from models import MediaItem

def book_search(request):
	return MediaItem.objects.filter(  *query( *search_parameters(request) )  )


def query(isbn, title, author):
	query = []
	
	if isbn:
		query += [ Q(isbn__exact = isbn.upper()) ]

	if title:
		query += [ Q(title__icontains=title) ]

	if author:
		query += [ Q(author__icontains=author) ]
		
	return query
	

def search_parameters(request):
	return [ field(request, fieldname) for fieldname in ['isbn', 'title', 'author'] ]

	
def field(request, fieldname):
	return request.GET[fieldname].strip() if fieldname in request.GET else ''
