from forms import MediaItemSearchForm
from models import MediaItem, MediaItemOwnership, MediaLoan

#----------------------------------------------------------------------------
# Utility Functions
#----------------------------------------------------------------------------
def count_books_in_library():
	return MediaItemOwnership.objects.all().count()


def count_books_borrowed():
	return MediaLoan.objects.all().count()


def count_books_loaned():
	return MediaLoan.objects.all().count()


