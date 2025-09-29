from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Tag

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'image')

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, label='Tags',
            help_text='Separate tags with commas (e.g. django, python)')

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})
        if instance:
            initial['tags'] = ', '.join([t.name for t in instance.tags.all()])
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
        max_length=2000,
        label=''
    )

    class Meta:
        model = Comment
        fields = ['content']