from django import forms

class NewLineupForm(forms.Form):
    zipcode = forms.CharField(label='Zip Code')
    provider = forms.CharField(label='Provider')
    csvdata = forms.CharField(label='CSV', widget=forms.Textarea)
