from django import forms

class NewPostForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control row-md-8 col-lg-8', 'rows': 1, 'placeholder': 'Title'}), label="")
    body = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows': 3, 'placeholder': 'Body of the post'}), label="")
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(),required=False)


class PutForm(forms.Form):
    follow = forms.BooleanField(initial=True, widget=forms.HiddenInput(),required=False)


class EditPostForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={'id': 'edit_title','class' : 'form-control row-md-8 col-lg-8', 'rows': 1, 'placeholder': 'Title'}), label="")
    body = forms.CharField(widget=forms.Textarea(attrs={'id': 'edit_body','class' : 'form-control col-md-8 col-lg-8', 'rows': 3, 'placeholder': 'Body of the post'}), label="")
    pk = forms.IntegerField(widget=forms.HiddenInput(),required=False)

