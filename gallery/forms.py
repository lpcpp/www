from django.forms import ModelForm
from gallery.models import Album
from gallery.models import Photo
from django import forms 


class AlbumForm(ModelForm):
    front_cover = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'init'}))
    path = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'init'}))
    class Meta:
        model = Album
        

class PhotoForm(ModelForm):
    url = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'init'}))
    class Meta:
        model = Photo
