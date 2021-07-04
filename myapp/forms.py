from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment", widget=forms.Textarea)
    comment.widget.attrs.update({'id': 'comment'})
