from django import forms

class ImageForm(forms.Form):
   name = forms.CharField(max_length = 100)
   picture = forms.ImageField()




