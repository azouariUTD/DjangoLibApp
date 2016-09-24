# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(sql="CREATE SEQUENCE borrower_id_seq", reverse_sql="DROP SEQUENCE borrower_id_seq"),
        migrations.RunSQL("SELECT setval('borrower_id_seq', max(card_no)) FROM borrower"),
    ]
