# -*- coding: utf-8 -*-

import datetime

from django import forms
from django.forms import models
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage

from .models import TechTren, TrainingComment, Training, Image, User



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


class UpdateTrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['date', 'place', 'sensei', 'techniques', 'notes']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'start_year', 'about_text', 'sex', 'avatar']


class AddTrainingForm(UpdateTrainingForm):
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
        self.request = kwargs.pop('request', None)

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
                im = PILImage.open(str(user.avatar))
                width = im.size[0]
                height = im.size[1]
                size = (300, 300)
                if width > height:
                    lcor = (width - height)/2
                    rcor = width - lcor
                    box = (lcor, 0, rcor, height)
                elif height > width:
                    lcor = (height - width)/2
                    rcor = height - lcor
                    box = (0, lcor, width, rcor)
                else:
                    box = (0, 0, width, width)

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


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = "__all__"


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'description']


def get_image_formset(form, formset=models.BaseInlineFormSet, **kwargs):
    return models.inlineformset_factory(Training, Image, form, formset, **kwargs)