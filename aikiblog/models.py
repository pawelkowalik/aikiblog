# -*- coding: utf-8 -*-
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from PIL import Image


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

    def save(self):
        self.slug = slugify(str(self.date) + " " + str(self.user)+ " " + str(self.stand) + " " + str(self.attack) + " " + str(self.technique))
        super(TechTren, self).save()


class Training(models.Model):
    TYPE = (
        ('T','trening'),
        ('S','staż'),
    )
    user = models.ForeignKey(User, verbose_name='Ćwiczący')
    date = models.DateTimeField('Data treningu')
    place = models.ForeignKey(Dojo, verbose_name='Miejsce treningu')
    sensei = models.ForeignKey(Sensei, verbose_name='Sensei')
    slug = models.SlugField('Odnosnik', max_length=50)
    techniques = models.ManyToManyField(TechTren, verbose_name='Techniki')
    type = models.CharField(max_length=1, choices=TYPE, verbose_name='Typ')
    notes = models.TextField(verbose_name="Notatki")

    class Meta:
        verbose_name = "Trening"
        verbose_name_plural = "Treningi"

    def __unicode__(self):
        return self.slug

    def save(self):
        d = self.date
        dt = '{:%Y-%m-%d %H-%M}'.format(d)
        self.slug = slugify(str(self.user) + " " + str(dt) + " " + str(self.place))
        super(Training, self).save()


class TempAvatar(models.Model):
    image_file = models.ImageField(upload_to='temp_avatars/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)