from datetime import date, timedelta
from django.contrib import messages
from django.db import connection
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from time import sleep

from library.forms import SearchForm, BookCheckoutForm, CardCheckoutsForm, BookCheckinForm, BorrowerForm
from library.forms import ListFineForm, CheckFines
from library.models import BookLoans, Fines


def fines(request):
    for loan in BookLoans.objects.iterator():
        if loan.is_late():
            try:
                fine = Fines.objects.get(loan=loan)
            except Fines.DoesNotExist:
                fine = Fines.objects.create(loan=loan)

            if not fine.paid:
                if loan.date_in is not None:
                    no_of_late_days = (loan.date_in - loan.due_date)
                    fine_amount = no_of_late_days.days * 0.25
                    fine.fine_amt = fine_amount
                    fine.save()
                else:
                    no_of_late_days = (date.today() - loan.due_date)
                    fine_amount = no_of_late_days.days * 0.25
                    fine.fine_amt = fine_amount
                    fine.save()

    return redirect('index')


def index(request):
    form = CardCheckoutsForm()

    template = 'library/index.html'
    data = {
        'form': form,
    }

    return render(request, template, data)


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            search_sql = """
                select
                    book.book_id,
                    book.title,
                    book_authors.author_name,
                    book_copies.branch_id,
                    book_copies.no_of_copies ,
                    COALESCE(check_out_books.check_out_copies , 0 ) as check_out_copies,
                    book_copies.no_of_copies - COALESCE(check_out_books.check_out_copies , 0 ) as available_copies

                from book
                join book_authors_v book_authors on (book.book_id = book_authors.book_id )
                join book_copies on (book.book_id = book_copies.book_id)
                left join (SELECT BOOK_ID , BRANCH_ID , COUNT(*) AS check_out_copies FROM Book_Loans
                where date_in is null
                group by BOOK_ID , BRANCH_ID) check_out_books on ( check_out_books.book_id = book_copies.book_id and check_out_books.branch_id = book_copies.branch_id)
                where
                lower(book_authors.author_name) like lower('%{query}%')
                or
                lower(book.title) like lower('%{query}%')
                or
                lower(book.book_id) like lower('%{query}%')
            """.format(query=query)

            cursor = connection.cursor()
            cursor.execute(search_sql)
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row)) for row in cursor.fetchall()
                ]
    else:
        form = SearchForm()
        results = None

    template = 'library/search.html'
    data = {
        'form': form,
        'results': results,
    }

    return render(request, template, data)


def checkout(request):
    if request.method == 'POST':
        form = BookCheckoutForm(request.POST)
        if form.is_valid():
            card_no = form.cleaned_data.get('card_no')
            branch_id = form.cleaned_data.get('branch_id')
            book_id = form.cleaned_data.get('book_id')

            try:
                BookLoans.objects.create(
                    card_no=form.borrower,
                    branch_id=form.branch.pk,
                    book_id=form.book.pk,
                    date_out=date.today(),
                    due_date=date.today() + timedelta(days=14)
                )

                messages.add_message(request, messages.SUCCESS, 'Book successfully checked out!')
            except Exception, e:
                messages.add_message(request, messages.ERROR, 'Book could not be checked out... %s' % str(e))

            # redirect back to search page
            return redirect('search')

    else:
        form = BookCheckoutForm(initial={
            'branch_id': request.GET.get('branch_id'),
            'book_id': request.GET.get('book_id'),
        })

    template = 'library/checkout.html'
    data = {
        'form': form,
    }

    return render(request, template, data)


@require_POST
def checkouts(request):
    form = CardCheckoutsForm(request.POST)
    if form.is_valid():
        loans = BookLoans.objects.filter(
            card_no=form.borrower,
            date_in__isnull=True
        )
    else:
        loans = BookLoans.objects.none()

    template = 'library/checkouts.html'
    data = {
        'form': form,
        'loans': loans,
    }

    return render(request, template, data)


@require_POST
def listfines(request):
    form = ListFineForm(request.POST)
    unpaidfines = []
    if form.is_valid():
        for loan in form.bookloans:
            if Fines.objects.filter(loan=loan).exists():
                fine = Fines.objects.get(loan=loan)
                if not fine.paid:
                    unpaidfines.append(fine)

    template = 'library/listfines.html'
    data = {
        'form': form,
        'unpaidfines': unpaidfines,
    }

    return render(request, template, data)


@require_GET
def payfines(request):
    form = CheckFines(request.GET)
    if form.is_valid():
        form.fine.paid = True
        try:
            form.fine.save()
        except Exception, e:
            messages.add_message(request, messages.ERROR, 'Error while paying the fine: %s' % str(e))
        messages.add_message(request, messages.SUCCESS, 'Fine Paid')
    else:
        messages.add_message(request, messages.ERROR, 'Invalid entry')

    sleep(2)

    return redirect('index')


@require_GET
def checkin(request):
    form = BookCheckinForm(request.GET)
    if form.is_valid():
        form.loan.date_in = date.today()
        try:
            form.loan.save()
        except Exception, e:
            messages.add_message(request, messages.ERROR, 'Error while checking in book: %s' % str(e))
        messages.add_message(request, messages.SUCCESS, 'Book successfully checked in!')
    else:
        messages.add_message(request, messages.ERROR, 'Invalid book loan!')

    # redirect back to home page
    sleep(2)
    return redirect('index')


def add_borrower(request):
    if request.method == 'POST':
        form = BorrowerForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            cursor = connection.cursor()
            cursor.execute("SELECT nextval('borrower_id_seq')")
            instance.card_no = long(cursor.fetchone()[0])
            instance.save()

            # set message and redirect
            messages.add_message(request, messages.SUCCESS, 'Borrower succesfully added!')
            return redirect('index')
    else:
        form = BorrowerForm()

    template = 'library/add_borrower.html'
    data = {
        'form': form,
    }

    return render(request, template, data)
