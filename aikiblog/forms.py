# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.validators import MinLengthValidator
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from aikiblog.models import Training, User


class RegisterForm(forms.Form):
    login = forms.CharField(label='login')
    password = forms.CharField(
        label='hasło',
        widget=forms.PasswordInput,
        validators=[MinLengthValidator(6)],
        error_messages={'min_length': u'Hasło musi mieć co najmniej 6 znaków'}
    )

    password2 = forms.CharField(
        label='powtórz hasło', widget=forms.PasswordInput)
    email = forms.EmailField(label='e-mail', widget=forms.EmailInput)

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if User.objects.filter(username=login):
            raise forms.ValidationError(u'Podany login istnieje w bazie')
        return login

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError(u'Podane hasła nie są zgodne')
        return password2


def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        username = request.POST.get('login')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.save()
        login(request, user)

        redirect_url = reverse('training-list')
        return redirect(redirect_url)

    return render(request, 'registration.html', {'form': form})


class AddTrainingForm(forms.ModelForm):
    class Meta:
        model=Training
        fields = ['user', 'date', 'place', 'techniques']


def add_training(request):
    form = AddTrainingForm(request.POST or None)
    if form.is_valid():
        form.slug = '1234'
        form.save()

    return render(request, 'add_training.html', {'form': form.as_p()})


class LoginForm(forms.Form):
    login = forms.CharField(label='login')
    password = forms.CharField(label='hasło', widget=forms.PasswordInput)

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if not User.objects.filter(username=login):
            raise forms.ValidationError(u'Podany login nie istnieje w bazie')
        return login