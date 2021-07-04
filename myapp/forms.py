from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment", widget=forms.Textarea)
