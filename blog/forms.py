from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment
class UserRegitserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django import forms
from django.contrib.auth.forms import UserChangeForm

class EditProfileForm(UserChangeForm):
    # Include the fields you want to update for the user model
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "edit_input", "placeholder": "Change your Email"}))
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class": "edit_input", "placeholder": "Change your first name"}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class": "edit_input", "placeholder": "Change your Last name"}))
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class": "edit_input", "placeholder": "Change your Username"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  # Exclude the 'bio' field

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "img", "body",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img'].required = False

class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",) 

        widgets = {
            'body': forms.Textarea(attrs={'class':'text_input'}),
        }
