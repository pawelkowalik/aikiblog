# -*- coding: utf-8 -*-

import os
from cStringIO import StringIO

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image as ImagePIL


class User(AbstractUser):
    SEX = (
        ('K','Kobieta'),
        ('M','Mężczyzna'),
    )
    avatar = models.ImageField(upload_to='static/avatars/%Y/%m/%d', null=True, blank=True)
    start_year = models.IntegerField(null=True, blank=True, verbose_name='Trenuje od')
    about_text = models.TextField(null=True, blank=True, verbose_name='O mnie')
    sex = models.CharField(max_length=1, choices=SEX, verbose_name='Płeć')


class News(models.Model):
    title = models.CharField('Tytuł', max_length=50)
    slug = models.SlugField('Odnosnik', max_length=50)
    posted_date = models.DateTimeField('Data publikacji')
    image = models.ImageField(upload_to='static/news', null=True, blank=True, verbose_name='Zdjęcie')
    text = models.TextField(null=True, blank=True, verbose_name='Treść')
    author = models.ForeignKey(User, verbose_name='Autor')

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "Newsy"

    def __unicode__(self):
        return self.title


class Sensei(models.Model):
    name = models.CharField('Imię i nazwisko', max_length=50)
    slug = models.SlugField('Odnosnik', max_length=50)

    class Meta:
        verbose_name = "Sensei"
        verbose_name_plural = "Senseje"

    def __unicode__(self):
        return self.name


class Dojo(models.Model):
    name = models.CharField('Nazwa dojo', max_length=50)
    slug = models.SlugField('Odnosnik', max_length=50)
    start_year = models.IntegerField(verbose_name='Rok założenia')
    city = models.CharField('Miasto', max_length=50)
    adress = models.CharField('Adres', max_length=50)
    sensei = models.ForeignKey(Sensei, verbose_name='Sensei')
    image1 = models.ImageField(upload_to='static/dojo', verbose_name='Zdjęcie 1')
    image2 = models.ImageField(upload_to='static/dojo', null=True, blank=True, verbose_name='Zdjęcie 2')
    image3 = models.ImageField(upload_to='static/dojo', null=True, blank=True, verbose_name='Zdjęcie 3')
    story = models.TextField(null=True, blank=True, verbose_name='Historia')
    trainings = models.TextField(null=True, blank=True, verbose_name='Treningi')
    users = models.ManyToManyField(User, blank=True, verbose_name='Byli tutaj')

    class Meta:
        verbose_name = "Dojo"
        verbose_name_plural = "Dojo"

    def __unicode__(self):
        return self.name


class Stand(models.Model):
    name = models.CharField('Nazwa postawy', max_length=50)
    slug = models.SlugField('Odnosnik', max_length=50)

    class Meta:
        verbose_name = "Postawa"
        verbose_name_plural = "Postawy"

    def __unicode__(self):
        return self.name


class Attack(models.Model):
    name = models.CharField('Nazwa ataku', max_length=50)
    slug = models.SlugField('Odnosnik', max_length=50)

    class Meta:
        verbose_name = "Atak"
        verbose_name_plural = "Ataki"

    def __unicode__(self):
        return self.name


class Technique(models.Model):
    name = models.CharField('Nazwa techniki', max_length=50)
    slug = models.SlugField('Odnosnik', max_length=50)

    class Meta:
        verbose_name = "Techika"
        verbose_name_plural = "Techniki"

    def __unicode__(self):
        return self.name


class TechTren(models.Model):
    user = models.ForeignKey(User, verbose_name='Ćwiczący')
    date = models.DateField('Data treningu')
    stand = models.ForeignKey(Stand, verbose_name='Postawa')
    attack = models.ForeignKey(Attack, verbose_name='Atak')
    technique = models.ForeignKey(Technique, verbose_name='Technika')
    mistakes = models.TextField(verbose_name='Błędy')
    slug = models.SlugField('Odnosnik', max_length=50)

    class Meta:
        verbose_name = "Techika z treningu"
        verbose_name_plural = "Techniki z treningu"

    def __unicode__(self):
        return self.slug

    def save(self, force_insert=False, force_update=False, using=None):
        self.slug = slugify(str(self.date) + " " + str(self.stand) + " " + str(self.attack) +
                            " " + str(self.technique) + " " + str(self.user_id))
        super(TechTren, self).save(force_insert, force_update, using)

    def get_absolute_url(self):
        self.training = Training.objects.get(techniques=self.id)
        return reverse('training-detail', kwargs={'slug': self.training})


class Training(models.Model):
    TYPE = (
        ('T','trening'),
        ('S','staż'),
    )
    user = models.ForeignKey(User, verbose_name='Ćwiczący', null=True, blank=True)
    date = models.DateTimeField('Data i godzina treningu')
    place = models.ForeignKey(Dojo, verbose_name='Miejsce treningu')
    sensei = models.ForeignKey(Sensei, verbose_name='Sensei')
    slug = models.SlugField('Odnosnik', max_length=50, null=True, blank=True)
    techniques = models.ManyToManyField(TechTren, verbose_name='Techniki')
    type = models.CharField(max_length=1, choices=TYPE, verbose_name='Typ')
    notes = models.TextField(verbose_name="Notatki")

    class Meta:
        verbose_name = "Trening"
        verbose_name_plural = "Treningi"
        ordering = ['-date']

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('training-detail', kwargs={'slug': self.slug})

    def save(self, force_insert=False, force_update=False, using=None):
        d = self.date
        dt = '{:%Y-%m-%d %H-%M}'.format(d)
        self.slug = slugify(str(self.user) + " " + str(dt) + " " + str(self.place))
        super(Training, self).save(force_insert, force_update, using)


class TrainingComment(models.Model):
    training = models.ForeignKey(Training)
    text = models.CharField(max_length=160, verbose_name='Tekst komentarza')
    posted_date = models.DateTimeField('Data dodania', auto_now_add=True)
    author = models.ForeignKey(User)

    class Meta:
        verbose_name = "Komentarz"
        verbose_name_plural = "Komentarze"


class Image(models.Model):
    image = models.ImageField('Zdjęcie', upload_to='static/galleries/%Y/%m/%d')
    thumbnail = models.ImageField(upload_to='static/galleries/thumbnails/%Y/%m/%d', null=True, blank=True)
    training = models.ForeignKey(Training)
    date = models.DateTimeField('Data dodania', auto_now_add=True)
    description = models.CharField(max_length=160, verbose_name='Opis zdjęcia', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Ćwiczący', null=True, blank=True)

    class Meta:
        verbose_name = "Zdjęcie"
        verbose_name_plural = "Zdjęcia"

    def __unicode__(self):
        return self.training

    def create_thumbnail(self):
        if not self.image:
            return

        THUMBNAIL_SIZE = (100, 75)
        DJANGO_TYPE = self.image.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
        image = ImagePIL.open(StringIO(self.image.read()))
        image.thumbnail(THUMBNAIL_SIZE, ImagePIL.ANTIALIAS)
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)
        self.thumbnail.save('%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        force_update = False
        if self.id:
            force_update = True
        super(Image, self).save(force_update=force_update)
