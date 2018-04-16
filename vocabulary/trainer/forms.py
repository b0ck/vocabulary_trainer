from django import forms


class VocabularyForm(forms.Form):
    attrs = {
        'class': 'form-control',
        'placeholder': 'Insert your answer...'
    }
    vocabulary = forms.CharField(widget=forms.TextInput(attrs=attrs), label='', max_length=100, required=True)
