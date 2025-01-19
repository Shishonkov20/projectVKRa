from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import Textarea
from django.http import request

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class AdvUserCreationForm(UserCreationForm):
    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'dolzn', 'first_name', 'last_name')


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())

    password2 = forms.CharField(label='Пароль(повторно)', widget=forms.PasswordInput,
                                help_text="Введите тот же самый пароль для проверки")

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        email = self.cleaned_data['email']
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if AdvUser.objects.filter(email=email).exists():
            errors = {'email': ValidationError(
                'Почта уже зарегистрирована')}
            raise ValidationError(errors)

        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные данные не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'dolzn',)

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            user.is_active = False
            user.is_activated = False
            if commit:
                user.save()
            user_registrated.send(RegistrationForm, instance=user)
            return user


class WorkOnProjectForm(forms.ModelForm):
    class Meta:
        model = WorkOnProject
        fields = ['description', 'type_work', 'dat']
        widgets = {
            'dat': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                       }),
        }

        def save(self, commit=True):
            project = super().save(commit=False)
            project.pk = 2
            return project
