from django import forms
from .models import Publisher, Review
SEARCH_CHOICES = (
    ("title", "Title"),
    ("contributor", "Contributor"))
class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields= "__all__"
class SearchForm (forms.Form):
    search= forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(choices=SEARCH_CHOICES, required=False)
class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=0, max_value=5)
    class Meta:
        model = Review
        exclude = ["date_edited", "book"]
