# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='urlsStored',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pagina', models.TextField()),
                ('numPagina', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
