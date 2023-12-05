from django import forms
from .models import WebAppModel, UserProfile, UserComments
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class AddPhotoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # User'ı kwargs'tan çıkartıp class attribute olarak sakla
        self.user = kwargs.pop('user', None)
        super(AddPhotoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = WebAppModel
        fields = ["image", "description"]

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class UserCustimizationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserCustimizationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        fields =  ["bio","profile_picture","hobies"]

class UserProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)

    # def save(self, commit=True):
    #     instance = super(UserProfileUpdateForm, self).save(commit=False)
    #     instance.user = self.user
    #     if commit:
    #         instance.save()
    #     return instance


    class Meta:
        model = UserProfile
        fields = ["bio","profile_picture","hobies"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = UserComments
        fields = ['comment']