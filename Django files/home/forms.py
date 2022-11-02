from email.policy import default
from tkinter import Widget
from django import forms

class Moviedata(forms.Form):
    movie =forms.CharField(label=("") ,widget=forms.TextInput(attrs={'class':'form-control',}))
    year = forms.IntegerField(label=(""),widget=forms.NumberInput(attrs={'class':'form-control',}))

    
