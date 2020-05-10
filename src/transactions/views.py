from datetime import date
from datetime import datetime as dt
import pandas as pd

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.views import View
from django.contrib import messages

from .forms import TransactionCreateForm, RawTransactionCreateForm
from .models import Transaction

# Create your views here.

####################
# Mixin Stuff
# Currently, this isn't being used.
####################


class CourseObjectMixin(object):
    model = Transaction
    url_lookup = 'id'

    def get_object(self):
        requested_id = self.kwargs.get(self.url_lookup)
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=requested_id)
        return obj


####################
# View Transaction Details
####################
def transaction_detail_view(request, requested_id):
    obj = get_object_or_404(Transaction, id=requested_id)

    context = {
        "page_title": "Transaction Search Result",
        "object": obj
    }

    return render(request, "transactions/transaction_detail.html", context)


####################
# Manually Create a Single, New Transaction Record
####################
# Raw Class Based Method
class TransactionCreateClassView(View):
    template_name = "transactions/transaction_create.html"

    # GET

    def get(self, request, *args, **kwargs):
        form = TransactionCreateForm()
        context = {
            "page_title": "Create a New Record",
            "form": form
        }
        return render(request, self.template_name, context)

    # POST
    def post(self, request, *args, **kwargs):
        # NOTE: Allegedly, there is a way to provide a default value
        # initial_data= {
        #     "date": date.today()
        # }
        # , initial= initial_data)
        form = TransactionCreateForm(request.POST or None)
        # form.fields["date"].initial= date.today()
        if form.is_valid():
            form.save()
        context = {
            "page_title": "Create a New Record",
            "form": form
        }
        return render(request, self.template_name, context)


####################
# Import a CSV File with Multiple Transaction Records
####################
def transaction_upload(request):
    template = "transactions/transaction_upload.html"
    data = Transaction.objects.all()

    prompt = {
        "order": "The CSV should be ordered as follows: Date, Check No., Description, Category, tbSubCat, Sub Category, Type, Memo, Debit, ABS(Debit), Credit, Balance",
        "transactions": data
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith(".csv"):
        messages.error(
            "Invalid file-type. Please upload a valid CSV file. (extension: '.csv')")

    # data_set= csv_file.read().decode("UTF-8")
    data_set = pd.read_csv(csv_file, encoding="UTF-8")

    # io_string= io.StringIO(data_set)
    # next(io_string)

    # Function to determine if the transaction was a debit or credit
    def debit_credit(row):
        if not pd.isnull(row["Debit"]):
            return row["Debit"]
        elif not pd.isnull(row["Credit"]):
            return row["Credit"]
        else:
            return 0

    # for record in csv.reader(io_string, delimiter= ","):
    for i in range(0, len(data_set)):
        if not pd.isnull(data_set.loc[i, "Date"]):
            transaction_amount = debit_credit(data_set.loc[i])
            _, created = Transaction.objects.get_or_create(
                amount=transaction_amount,
                category=data_set.loc[i, "tbSubCat"],
                date=dt.strptime(data_set.loc[i, "Date"], "%m/%d/%Y"),
                description=data_set.loc[i, "Description"]
            )
            print(
                f"Record {i}: {transaction_amount} - {data_set.loc[i, 'tbSubCat']} - {dt.strptime(data_set.loc[i, 'Date'], '%m/%d/%Y')} - {data_set.loc[i, 'Description']}")
            print("*"*5)

    context = {
        "page_title": "CSV Upload"
    }

    return render(request, template, context)


####################
# Update a Transaction Record
####################
def transaction_update_view(request, requested_id):
    obj = get_object_or_404(Transaction, id=requested_id)
    form = TransactionCreateForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    context = {
        "page_title": "Update a Record",
        "form": form
    }
    return render(request, "transactions/transaction_create.html", context)


####################
# Delete a Transaction Record and Confirm
####################
def transaction_delete_view(request, requested_id):
    obj = get_object_or_404(Transaction, id=requested_id)
    # POST Request
    if request.method == "POST":
        # confirming the delete
        obj.delete()
        return redirect("../../")
    context = {
        "page_title": "Delete Transaction Record",
        "object": obj
    }
    return render(request, "transactions/transaction_delete.html", context)


####################
# Return List of Transaction Records
####################
class TransactionListClassView(View):
    template_name = "transactions/transaction_record_list.html"
    queryset = Transaction.objects.all()

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {
            'object_list': self.get_queryset  # ,
            # "the_rest": super(TransactionListClassView, self).get_context_data(**kwargs)
        }
        return render(request, self.template_name, context)


class TransactionFilteredListClassView(TransactionListClassView):
    # year = context["the_rest"]["year"]
    # month = context["the_rest"]["month"]
    # day = context["the_rest"]["day"]
    # queryset = Transaction.objects.filter(date__gt, date(year, month, day))
    queryset = Transaction.objects.filter()
