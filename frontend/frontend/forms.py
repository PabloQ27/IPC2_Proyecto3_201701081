from django import forms

class Archivo(forms.Form):
    titulo = forms.CharField(max_length=50)
    file = forms.FileField()