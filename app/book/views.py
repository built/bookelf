from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import MediaItemEditor
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from library.models import *
from built import to_previous_page

#----------------------------------------------------------------------------
# Helper Functions
#----------------------------------------------------------------------------

def to_my_library():
	return HttpResponseRedirect('../../library/mine/')


#----------------------------------------------------------------------------
# Views
#----------------------------------------------------------------------------

@login_required
def show_new_book_form(request):
	return render_to_response("library/book/editor.html", {"book_form": MediaItemEditor() }, context_instance=RequestContext(request))

@login_required
def save_book(request):
	
	if request.method != "POST": return HttpResponseRedirect('../add/')
	
	book_form = MediaItemEditor(request.POST)

	if not book_form.is_valid():
		
		return HttpResponse("Error: " + str(book_form.errors ) )
	
	# TO DO: Fix this problem: Should be getting data from cleaned_data hash instead of just data.
	# For some reason neither cleaned_data nor clean_data are available. Doesn't appear to be a versioning issue. 
	# Running Python 2.5.2 and Django 1.0.2. Puzzling.
	
	book = []

	# Look for a book with that ISBN. If it doesn't exist, add it.
	isbn = book_form.data['isbn'].upper()
	
	if MediaItem.objects.filter(isbn__exact = isbn).count() > 0:
		book = MediaItem.objects.filter(isbn__exact = isbn)[0]

	else:
		book = MediaItem()
		# TO DO: There must be a way for a model to be initialized with a form. That would make more sense here.
		book.title = book_form.data['title']
		
		# Deal with the possibility that the new item doesn't have an ISBN. Many older books and non-book media lack an ISBN.
		# As an alternate, we'll create a substitute value in for the ISBN. All substitutions will start with the character 'V' or 'T'

		if 'no_isbn_available' in book_form.data and book_form.data['no_isbn_available'] == 'on':
			# We need to synthesize an ISBN-like number. We'll use the hashcode from the title.
			book_id = str(book.title.__hash__()).replace('-', 'V')
			
			if len(book_id) < 13:
				
				book_id = book_id.rjust(13, 'Q')
				
			book.isbn = book_id

		else:
			book.isbn = book_form.data['isbn'].upper() # Standardize any lingering X or x character.
		
		
		
		book.author = book_form.data['author']
		book.amazon_link = book_form.data['amazon_link']
		book.save()

	# Create an ownership between the current user and the book.

	users_copy_of_book = MediaItemOwnership()
	
	users_copy_of_book.item = book
	users_copy_of_book.owner = request.user
	users_copy_of_book.note = book_form.data['notes']
	users_copy_of_book.save()
	
	return HttpResponseRedirect('../../library/mine/')


def book_exists(isbn):
	return MediaItem.objects.filter(isbn__exact=isbn.upper()).count() > 0


class AvailableBook:
	book = None
	owner_profile = None
	twitter = None

	def __init__(self, book):

		
		self.book = book
		self.title = book.item.title
		self.username = book.owner.username

		from emailconfirmation.models import EmailAddress

		try:

			self.email = EmailAddress.objects.filter(user=book.owner)[0].email
			
		except:
			self.email = ''

		from basic_profiles.models import Profile
		self.twitter = self.make_twitter(Profile.objects.get(user=book.owner).website)

	def make_twitter(self, url):
	
		if not url: return ''
	
		url_marker = 'twitter.com/'
	
		start = url.lower().find(url_marker)
	
		if start < 0: return '' # No twitter found, don't bother.
	
		end = start + len(url_marker)
	
		return url[end:]


#@login_required
def view_book(request, isbn):
	
	parameters = {}

	isbn = isbn.upper()

	if book_exists( isbn ):

		book = parameters['book_info'] = MediaItem.objects.get(isbn__exact=isbn.upper())

		# We look for copies of the specified book that aren't currently loaned out.
		available_copies = parameters['books_available'] = [AvailableBook(book) for book in MediaItemOwnership.objects.filter(item = book).exclude(medialoan__item__item=book)]

		# Indicate if the current user has already borrowed this book.
		# (Which can only be told if the user is logged in.)
		if request.user.is_authenticated():
			parameters['existing_loan'] = MediaLoan.objects.filter(borrower=request.user, item__item=book).count() > 0
			
		my_copies = [book for book in available_copies if book.username == request.user.username]
		
		if my_copies:
			parameters['my_copies'] = my_copies[0]
			
	return render_to_response("library/book/viewer.html", parameters, context_instance=RequestContext(request))




	
@login_required
def remove_book(request, ownership_id):

	try:
		# We delete the ownership, not the book itself.
		MediaItemOwnership.objects.get(id = ownership_id).delete()
	
		# TO DO: Send the user a message in the UI (with an event/signal)
		
	except:
		pass # Throwing an exception for not finding something is just stupid. We fall through.

	return to_previous_page(request)
		

@login_required
def show_loan_form(request, ownership_id):

	try:
		ownership = MediaItemOwnership.objects.get(id=ownership_id)
	except: 
		return HttpResponse("You don't own that?")

	users = User.objects.all()
	
	return render_to_response("library/book/loan.html", {'ownership': ownership, 'users': users }, context_instance=RequestContext(request))


@login_required
def loan_book(request, ownership_id):

	if request.method == "POST":

		# Make sure the item hasn't already been loaned out.
		if MediaLoan.objects.filter(item__id=ownership_id).count() > 0: return HttpResponseRedirect('../../../library/mine/')

		ownership = MediaItemOwnership.objects.get(id=ownership_id)

		user = User.objects.get(username=request.POST['borrower'])

		loan = MediaLoan()
		loan.item = ownership
		loan.borrower = user
		loan.save()
		
		return HttpResponseRedirect('../../../library/mine/')

	else:
		return show_loan_form(request, ownership_id)


@login_required
def return_book(request, loan_id):

	if request.method == "GET":
		
		try:
			MediaLoan.objects.get(id=loan_id, item__owner=request.user).delete()
		except:
			pass

	return to_previous_page(request)










