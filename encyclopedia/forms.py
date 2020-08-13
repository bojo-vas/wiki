from django import forms


class SearchForm(forms.Form):
    searched = forms.CharField(label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}), max_length=100)


class NewPage(forms.Form):
    title = forms.CharField(label='Title:', widget=forms.TextInput(
        attrs={'placeholder': 'Entry Title', 'class': 'title'}), max_length=100)
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'You can use "Markup" or plain text to write your entry', 'class': 'content'}))
