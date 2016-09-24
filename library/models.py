from datetime import date
import datetime

from django.db import models
from django.db.models import Q


# Create your models here.
class Book(models.Model):
    book_id = models.CharField(max_length=20, primary_key=True)
    title = models.TextField()

    class Meta:
        db_table = 'book'


class BookAuthors(models.Model):
    book = models.ForeignKey(Book)
    author_name = models.TextField()

    class Meta:
        db_table = 'book_authors'


class LibraryBranch(models.Model):
    branch_id = models.IntegerField(primary_key=True)
    branch_name = models.TextField()
    address = models.TextField()

    class Meta:
        db_table = 'library_branch'


class BookCopies(models.Model):
    book = models.ForeignKey(Book)
    branch = models.ForeignKey(LibraryBranch)
    no_of_copies = models.IntegerField()

    class Meta:
        db_table = 'book_copies'


class Borrower(models.Model):
    card_no = models.IntegerField(primary_key=True)
    fname = models.TextField(verbose_name="First Name")
    lname = models.TextField(verbose_name="Last Name")
    address = models.TextField(verbose_name="Address")
    phone = models.TextField(verbose_name="Phone Number")

    class Meta:
        db_table = 'borrower'


class BookLoans(models.Model):
    book = models.ForeignKey(Book)
    branch = models.ForeignKey(LibraryBranch)
    card_no = models.ForeignKey(Borrower, db_column='card_no')
    date_out = models.DateField()
    due_date = models.DateField()
    date_in = models.DateField(null=True)

    class Meta:
        db_table = 'book_loans'
        unique_together = ('book', 'branch', 'card_no',)

    def is_late(self):
        delta = date.today() - self.due_date
        if (delta.days > 0) and (self.date_in is None):
            return True
        elif self.date_in is not None:
            deltar = self.date_in - self.due_date
            if deltar.days > 0:
                return True
        else:
            return False



class Fines(models.Model):
    loan = models.ForeignKey(BookLoans, primary_key=True)
    fine_amt = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)

    class Meta:
        db_table = 'fines'



"""
for loan in BookLoans.objects.iterator():
    if loan.is_late():

        # check if fine row exists
        try:
            fine = Fines.objects.get(loan=loan)
        except Fines.DoesNotExist:
            # create new fine
            fine = Fines.objects.create(loan=loan)

        if not fine.paid:
            # calculate the fine and save the fine row
            pass
"""
