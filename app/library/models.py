from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class MediaItem(models.Model):
	
	isbn = models.CharField(blank=False, max_length=13, verbose_name="ISBN")
	title = models.CharField(blank=False, max_length=100)
	author = models.CharField(blank=True, max_length=100)
	amazon_link = models.URLField(blank=True, verify_exists=True)
	
	def __unicode__(self):
		return self.title



class MediaItemOwnership(models.Model):

	# We need to have one of these for each copy of a book any user owns. 
	# If they own two, there are two of these.

	owner = models.ForeignKey(User)
	item = models.ForeignKey(MediaItem)

	# A note may contain info on the condition of the item or special requirements.
	note = models.TextField(blank=True)

	def __unicode__(self):
		return "%s => %s" % (self.owner.username, self.item)


class MediaLoan(models.Model):
	
	"""
	This represents a loan of a book or other piece of media. The item's owner is implied.
	"""
	item = models.ForeignKey(MediaItemOwnership)
	borrower = models.ForeignKey(User)
	from datetime import datetime
	date_loaned = models.DateTimeField(default=datetime.now)

	def __unicode__(self):
		return "%s loaned \"%s\" to %s" % (self.item.owner.username, self.item.item.title, self.borrower.username)


# Set up signal handling so a Tweet will be sent whenever a book is added to the database.

MAX_TWEET_LENGTH = 140

from django.db.models.signals import post_save

def tweet_about_new_items(sender, **kwargs):

	if kwargs['created']:

		item = kwargs['instance']

		from twitter import *
#		tweet = twitter.Api("built_test", "123built")
		tweet = twitter.Api("virtlib", "book$yay!")
		
		template = "%s '%s' %s" # Message Title URL

		# TO DO: Make this figure it out from settings instead of hardcoding
		url = "http://virtlib.builtsoftware.com/book/isbn/%s" % item.item.isbn
		
		message = "Just added:"
		
		extra_characters_len = 4  # two spaces and two quotes. Better way to describe this?
		
		max_title_size = MAX_TWEET_LENGTH - len(message) - len(url) - extra_characters_len
		
		# Ellipsize the title if need be. The message and the URL need to take priority.
#		title = item.item.title if len(item.item.title) <= max_title_size else item.item.title[:max_title_size-3] + '...'

		if len(item.item.title) <= max_title_size:
			title = item.item.title  
		else:
			title = item.item.title[:max_title_size-3] + '...'	
		

		tweet.PostUpdate( template % (message, title, url) )


post_save.connect(tweet_about_new_items, sender=MediaItemOwnership)





















