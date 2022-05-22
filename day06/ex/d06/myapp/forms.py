from django.forms import ModelForm
from django import forms
from django.forms.widgets import HiddenInput
from django.contrib.auth.forms import UserCreationForm
from .models import TipModel, UserTip


class NewUserForm(UserCreationForm):
    class Meta:
        model = UserTip
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class TipForm(ModelForm):
    class Meta:
        model = TipModel
        fields = ['content']


class DeleteTipForm(forms.Form):
    _method = forms.CharField(widget=HiddenInput(), initial='delete')
    id = forms.IntegerField(widget=HiddenInput())

    def __init__(self, id, *args, **kwargs):
        super(DeleteTipForm, self).__init__(*args, **kwargs)
        if id:
            self.fields['id'].initial = id


class VoteForm(forms.Form):
    _method = forms.CharField(widget=HiddenInput(), initial='put')
    id = forms.IntegerField(widget=HiddenInput())
    type = forms.BooleanField(required=False)

    def __init__(self, id, *args, **kwargs):
        super(VoteForm, self).__init__(auto_id='%s', *args, **kwargs)
        if id:
            self.fields['id'].initial = id
