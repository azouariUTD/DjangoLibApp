# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('title', models.TextField()),
            ],
            options={
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='BookAuthors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author_name', models.TextField()),
                ('book', models.ForeignKey(to='library.Book')),
            ],
            options={
                'db_table': 'book_authors',
            },
        ),
        migrations.CreateModel(
            name='BookCopies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('no_of_copies', models.IntegerField()),
                ('book', models.ForeignKey(to='library.Book')),
            ],
            options={
                'db_table': 'book_copies',
            },
        ),
        migrations.CreateModel(
            name='BookLoans',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_out', models.DateField()),
                ('due_date', models.DateField()),
                ('date_in', models.DateField(null=True)),
            ],
            options={
                'db_table': 'book_loans',
            },
        ),
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('card_no', models.IntegerField(serialize=False, primary_key=True)),
                ('fname', models.TextField()),
                ('lname', models.TextField()),
                ('address', models.TextField()),
                ('phone', models.TextField()),
            ],
            options={
                'db_table': 'borrower',
            },
        ),
        migrations.CreateModel(
            name='LibraryBranch',
            fields=[
                ('branch_id', models.IntegerField(serialize=False, primary_key=True)),
                ('branch_name', models.TextField()),
                ('address', models.TextField()),
            ],
            options={
                'db_table': 'library_branch',
            },
        ),
        migrations.CreateModel(
            name='Fines',
            fields=[
                ('loan', models.ForeignKey(primary_key=True, serialize=False, to='library.BookLoans')),
                ('fine_amt', models.DecimalField(max_digits=19, decimal_places=2)),
                ('paid', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'fines',
            },
        ),
        migrations.AddField(
            model_name='bookloans',
            name='book',
            field=models.ForeignKey(to='library.Book'),
        ),
        migrations.AddField(
            model_name='bookloans',
            name='branch',
            field=models.ForeignKey(to='library.LibraryBranch'),
        ),
        migrations.AddField(
            model_name='bookloans',
            name='card_no',
            field=models.ForeignKey(to='library.Borrower', db_column=b'card_no'),
        ),
        migrations.AddField(
            model_name='bookcopies',
            name='branch',
            field=models.ForeignKey(to='library.LibraryBranch'),
        ),
        migrations.AlterUniqueTogether(
            name='bookloans',
            unique_together=set([('book', 'branch', 'card_no')]),
        ),
    ]
