# -*- coding: utf-8 -*-

from django import forms
from django.shortcuts import render, redirect
from aikiblog.models import Training, User, TempAvatar
from PIL import Image

import datetime
from annoying.functions import get_object_or_None
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from os.path import join, dirname, realpath


class AddTrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['user', 'date', 'place', 'techniques']


def add_training(request):
    form = AddTrainingForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'add_training.html', {'form': form.as_p()})


_current_dir = dirname(realpath(__file__))
CUR_YEAR = datetime.datetime.now().year
START_YEAR_CHOICES = tuple(
    [(year, year) for year in range(CUR_YEAR, CUR_YEAR - 30, -1)])
K = 'K'
M = 'M'
SEX_CHOICES = (
    (K, u'kobieta'),
    (M, u'mężczyzna')
)


class SaveUserDataForm(forms.Form):
    first_name = forms.CharField(initial='')
    last_name = forms.CharField(initial='')
    start_year = forms.ChoiceField(choices=START_YEAR_CHOICES, initial=2004)
    sex = forms.ChoiceField(widget=forms.RadioSelect, choices=SEX_CHOICES)
    avatar = forms.ImageField()
    about_me = forms.CharField(widget=forms.Textarea(), required=False, initial='')

    def __init__(self, *args, **kwargs):
        super(SaveUserDataForm, self).__init__(*args, **kwargs)

    def save(self, user_id):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        start_year = self.cleaned_data.get('start_year')
        sex = self.cleaned_data.get('sex')
        about_me = self.cleaned_data.get('about_me')
        avatar = self.cleaned_data.get('avatar')
        user = get_user_model().objects.get(id=user_id)
        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.start_year = start_year
            user.sex = K if sex == 'K' else M
            if avatar:
                user.avatar = SimpleUploadedFile(avatar.name, avatar.read(), content_type='image/jpeg')
                user.save()
                im = Image.open(str(user.avatar))
                a = im.size[0]
                b = im.size[1]
                size = (300, 300)
                if a > b:
                    c = (a - b)/2
                    d = a - c
                    box = (c, 0, d, b)
                elif b > a:
                    c = (b - a)/2
                    d = b - c
                    box = (0, c, a, d)
                else:
                    box = (0, 0, a, a)

            region = im.crop(box)
            region.thumbnail(size)
            region.save(str(user.avatar), "JPEG")

        if about_me:
            user.about_text = about_me

        user.save()

