# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(null=True, upload_to=b'static/avatars/%Y/%m/%d', blank=True)),
                ('start_year', models.IntegerField(null=True, verbose_name=b'Trenuje od', blank=True)),
                ('about_text', models.TextField(null=True, verbose_name=b'O mnie', blank=True)),
                ('sex', models.CharField(max_length=1, verbose_name=b'P\xc5\x82e\xc4\x87', choices=[(b'K', b'Kobieta'), (b'M', b'M\xc4\x99\xc5\xbcczyzna')])),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Attack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Nazwa ataku')),
                ('slug', models.SlugField(verbose_name=b'Odnosnik')),
            ],
            options={
                'verbose_name': 'Atak',
                'verbose_name_plural': 'Ataki',
            },
        ),
        migrations.CreateModel(
            name='Dojo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Nazwa dojo')),
                ('slug', models.SlugField(verbose_name=b'Odnosnik')),
                ('start_year', models.IntegerField(verbose_name=b'Rok za\xc5\x82o\xc5\xbcenia')),
                ('city', models.CharField(max_length=50, verbose_name=b'Miasto')),
                ('adress', models.CharField(max_length=50, verbose_name=b'Adres')),
                ('image1', models.ImageField(upload_to=b'static/dojo', verbose_name=b'Zdj\xc4\x99cie 1')),
                ('image2', models.ImageField(upload_to=b'static/dojo', null=True, verbose_name=b'Zdj\xc4\x99cie 2', blank=True)),
                ('image3', models.ImageField(upload_to=b'static/dojo', null=True, verbose_name=b'Zdj\xc4\x99cie 3', blank=True)),
                ('story', models.TextField(null=True, verbose_name=b'Historia', blank=True)),
                ('trainings', models.TextField(null=True, verbose_name=b'Treningi', blank=True)),
            ],
            options={
                'verbose_name': 'Dojo',
                'verbose_name_plural': 'Dojo',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, verbose_name=b'Tytu\xc5\x82')),
                ('slug', models.SlugField(verbose_name=b'Odnosnik')),
                ('posted_date', models.DateTimeField(verbose_name=b'Data publikacji')),
                ('image', models.ImageField(upload_to=b'static/news', null=True, verbose_name=b'Zdj\xc4\x99cie', blank=True)),
                ('text', models.TextField(null=True, verbose_name=b'Tre\xc5\x9b\xc4\x87', blank=True)),
                ('author', models.ForeignKey(verbose_name=b'Autor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'Newsy',
            },
        ),
        migrations.CreateModel(
            name='Sensei',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Imi\xc4\x99 i nazwisko')),
                ('slug', models.SlugField(verbose_name=b'Odnosnik')),
            ],
            options={
                'verbose_name': 'Sensei',
                'verbose_name_plural': 'Senseje',
            },
        ),
        migrations.CreateModel(
            name='Stand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Nazwa postawy')),
                ('slug', models.SlugField(verbose_name=b'Odnosnik')),
            ],
            options={
                'verbose_name': 'Postawa',
                'verbose_name_plural': 'Postawy',
            },
        ),
        migrations.CreateModel(
            name='Technique',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Nazwa techniki')),
                ('slug', models.SlugField(verbose_name=b'Odnosnik')),
            ],
            options={
                'verbose_name': 'Techika',
                'verbose_name_plural': 'Techniki',
            },
        ),
        migrations.CreateModel(
            name='TechTren',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name=b'Data treningu')),
                ('mistakes', models.TextField(verbose_name=b'B\xc5\x82\xc4\x99dy')),
                ('slug', models.SlugField(verbose_name=b'Odnosnik')),
                ('attack', models.ForeignKey(verbose_name=b'Atak', to='aikiblog.Attack')),
                ('stand', models.ForeignKey(verbose_name=b'Postawa', to='aikiblog.Stand')),
                ('technique', models.ForeignKey(verbose_name=b'Technika', to='aikiblog.Technique')),
                ('user', models.ForeignKey(verbose_name=b'\xc4\x86wicz\xc4\x85cy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Techika z treningu',
                'verbose_name_plural': 'Techniki z treningu',
            },
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name=b'Data i godzina treningu')),
                ('slug', models.SlugField(null=True, verbose_name=b'Odnosnik', blank=True)),
                ('type', models.CharField(max_length=1, verbose_name=b'Typ', choices=[(b'T', b'trening'), (b'S', b'sta\xc5\xbc')])),
                ('notes', models.TextField(verbose_name=b'Notatki')),
                ('place', models.ForeignKey(verbose_name=b'Miejsce treningu', to='aikiblog.Dojo')),
                ('sensei', models.ForeignKey(verbose_name=b'Sensei', to='aikiblog.Sensei')),
                ('techniques', models.ManyToManyField(to='aikiblog.TechTren', verbose_name=b'Techniki')),
                ('user', models.ForeignKey(verbose_name=b'\xc4\x86wicz\xc4\x85cy', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Trening',
                'verbose_name_plural': 'Treningi',
            },
        ),
        migrations.CreateModel(
            name='TrainingComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=160, verbose_name=b'Tekst komentarza')),
                ('posted_date', models.DateTimeField(auto_now_add=True, verbose_name=b'Data dodania')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('training', models.ForeignKey(to='aikiblog.Training')),
            ],
            options={
                'verbose_name': 'Komentarz',
                'verbose_name_plural': 'Komentarze',
            },
        ),
        migrations.AddField(
            model_name='dojo',
            name='sensei',
            field=models.ForeignKey(verbose_name=b'Sensei', to='aikiblog.Sensei'),
        ),
        migrations.AddField(
            model_name='dojo',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'Byli tutaj', blank=True),
        ),
    ]
