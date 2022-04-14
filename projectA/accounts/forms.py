from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number','full_name', 'password')


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match !')
        return cd['password2']

    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change password using <a href=\"../password/\">this form </a>')

    class Meta:
        model = User
        fields = ('full_name','phone_number','password','last_login')



class UserRegistrationForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    full_name = forms.CharField(label='full name')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('this phone number is exist.')
        return phone

    def clean_full_name(self):
        name = self.cleaned_data['full_name']
        user = User.objects.filter(full_name=name).exists()
        if user:
            raise ValidationError('this name is already exists.')
        return name



class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)