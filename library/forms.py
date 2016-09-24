from django import forms

from library.models import BookLoans, Borrower, LibraryBranch, Book, Fines


class SearchForm(forms.Form):
    query = forms.CharField(label="Search", max_length=80, required=True)


class BookCheckoutForm(forms.Form):
    card_no = forms.IntegerField(label="Borrower Card Number", required=True)
    branch_id = forms.IntegerField(label="Branch", required=True)
    book_id = forms.CharField(label="Book ID", required=True)

    def clean(self):
        cleaned_data = super(BookCheckoutForm, self).clean()

        # get form values
        card_no = cleaned_data.get('card_no')
        branch_id = cleaned_data.get('branch_id')
        book_id = cleaned_data.get('book_id')

        # validate borrower
        try:
            borrower = Borrower.objects.get(pk=card_no)
        except Borrower.DoesNotExist:
            raise forms.ValidationError('Invalid borrower card number')

        # validate branch
        try:
            branch = LibraryBranch.objects.get(pk=branch_id)
        except LibraryBranch.DoesNotExist:
            raise forms.ValidationError('Invalid branch ID')

        # validate borrower
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise forms.ValidationError('Invalid book ID')

        # check existing loans for the card
        loan_count = BookLoans.objects.filter(
            card_no=card_no,
            date_in__isnull=True
        ).count()
        if loan_count >= 3:
            raise forms.ValidationError('Borrower has 3 books already checked out')

        # add model objects to form
        self.borrower = borrower
        self.branch = branch
        self.book = book


class CardCheckoutsForm(forms.Form):
    card_no = forms.IntegerField(label="Borrower Card Number", required=True)

    def clean(self):
        cleaned_data = super(CardCheckoutsForm, self).clean()

        # get form values
        card_no = cleaned_data.get('card_no')

        # validate borrower
        try:
            borrower = Borrower.objects.get(pk=card_no)
        except Borrower.DoesNotExist:
            raise forms.ValidationError('Invalid borrower card number')

        self.borrower = borrower


class ListFineForm(forms.Form):
    card_no = forms.IntegerField(label="Borrower Card Number", required=True)

    def clean(self):
        cleaned_data = super(ListFineForm, self).clean()

        # get form values

        card_no = cleaned_data.get('card_no')

        # validate borrower
        try:
            bookloans = BookLoans.objects.filter(card_no=card_no)
        except BookLoans.DoesNotExist:
            raise forms.ValidationError('No Book Loans for entered card no')

        self.bookloans = bookloans


class CheckFines(forms.Form):
    fine_id = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super(CheckFines, self).clean()

        # get form values
        fine_id = cleaned_data.get('fine_id')

        # validate borrower
        try:
            fine = Fines.objects.get(pk=fine_id)
        except BookLoans.DoesNotExist:
            raise forms.ValidationError('Invalid Fine')

        self.fine = fine


class BookCheckinForm(forms.Form):
    loan_id = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super(BookCheckinForm, self).clean()

        # get form values
        loan_id = cleaned_data.get('loan_id')

        # validate borrower
        try:
            loan = BookLoans.objects.get(pk=loan_id)
        except BookLoans.DoesNotExist:
            raise forms.ValidationError('Invalid book loan')

        self.loan = loan


class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ['fname', 'lname', 'address', 'phone']

    def clean(self):
        cleaned_data = super(BorrowerForm, self).clean()

        # get form values
        fname = cleaned_data.get('fname', '')
        lname = cleaned_data.get('lname', '')
        address = cleaned_data.get('address', '')

        # check if user already exists with same first, last and address
        try:
            Borrower.objects.get(
                fname__iexact=fname.strip(),
                lname__iexact=lname.strip(),
                address__iexact=address.strip()
            )
            exists = True
        except Borrower.DoesNotExist:
            exists = False

        if exists:
            raise forms.ValidationError('Borrower with the same first name, last name and address exists!')
