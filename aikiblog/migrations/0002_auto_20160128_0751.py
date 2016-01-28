# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('aikiblog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'static/galleries/%Y/%m/%d', verbose_name=b'Zdj\xc4\x99cie')),
                ('thumbnail', models.ImageField(null=True, upload_to=b'static/galleries/thumbnails/%Y/%m/%d', blank=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Data dodania')),
                ('description', models.CharField(max_length=160, null=True, verbose_name=b'Opis zdj\xc4\x99cia', blank=True)),
            ],
            options={
                'verbose_name': 'Zdj\u0119cie',
                'verbose_name_plural': 'Zdj\u0119cia',
            },
        ),
        migrations.AlterModelOptions(
            name='training',
            options={'ordering': ['-date'], 'verbose_name': 'Trening', 'verbose_name_plural': 'Treningi'},
        ),
        migrations.AddField(
            model_name='image',
            name='training',
            field=models.ForeignKey(to='aikiblog.Training'),
        ),
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.ForeignKey(verbose_name=b'\xc4\x86wicz\xc4\x85cy', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
