from django import forms

class MediaItemEditor(forms.Form):

	title = forms.CharField(max_length=100, required=True)
	author = forms.CharField(max_length=100, required=True)
	isbn = forms.CharField(max_length=13, required=False)
	amazon_link = forms.URLField(required=False)
	notes = forms.CharField(widget=forms.Textarea, required=False)
	no_isbn_available = forms.BooleanField(required=False)

