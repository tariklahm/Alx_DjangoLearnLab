from django import forms

class ExampleForm(forms.Form):
    firstField=forms.CharField()
    secondField=forms.CharField(widget=forms.PasswordInput)