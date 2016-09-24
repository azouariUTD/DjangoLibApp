# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20151025_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrower',
            name='address',
            field=models.TextField(verbose_name=b'Address'),
        ),
        migrations.AlterField(
            model_name='borrower',
            name='fname',
            field=models.TextField(verbose_name=b'First Name'),
        ),
        migrations.AlterField(
            model_name='borrower',
            name='lname',
            field=models.TextField(verbose_name=b'Last Name'),
        ),
        migrations.AlterField(
            model_name='borrower',
            name='phone',
            field=models.TextField(verbose_name=b'Phone Number'),
        ),
        migrations.AlterField(
            model_name='fines',
            name='fine_amt',
            field=models.DecimalField(default=0.0, max_digits=19, decimal_places=2),
        ),
    ]
