# -*- coding: utf-8 -*-

from django import forms
from django.shortcuts import render, redirect
from aikiblog.models import Training, User
from PIL import Image

import datetime
from annoying.functions import get_object_or_None
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from os.path import join, dirname, realpath

from django.http.response import HttpResponseRedirect

from datetime import date
from django.forms import widgets
from aikiblog.models import TechTren, TrainingComment

CUR_YEAR = datetime.datetime.now().year
START_YEAR_CHOICES = tuple(
    [(year, year) for year in range(CUR_YEAR, CUR_YEAR - 30, -1)])
K = 'K'
M = 'M'
SEX_CHOICES = (
    (K, u'kobieta'),
    (M, u'mężczyzna')
)


def _get_techniques_by_user(user):
    techniques = TechTren.objects.filter(user__id=user.id).order_by('-date')
    choices = []
    for t in techniques:
        choices.append((t.id, t.slug))
    return choices


class AddTrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['date', 'place', 'sensei', 'techniques', 'notes']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddTrainingForm, self).__init__(*args, **kwargs)
        if self.request.user.is_authenticated():
            self.fields['techniques'].choices = \
                _get_techniques_by_user(self.request.user)


class AddTechniquesForm(forms.ModelForm):
    class Meta:
        model = TechTren
        fields = ['date', 'stand', 'attack', 'technique', 'mistakes']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddTechniquesForm, self).__init__(*args, **kwargs)


class SaveUserDataForm(forms.Form):
    first_name = forms.CharField(initial='')
    last_name = forms.CharField(initial='')
    start_year = forms.ChoiceField(choices=START_YEAR_CHOICES, initial=2015)
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


class TrainingCommentForm(forms.ModelForm):

    class Meta:
        model = TrainingComment
        fields = ['training', 'text']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TrainingCommentForm, self).__init__(*args, **kwargs)
