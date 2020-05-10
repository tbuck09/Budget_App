from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home_view(request, *args, **kwargs):
    context_dict = {
        "page_title": "Home"
    }
    return render(request, "home.html", context_dict)


def data_entry_view(request, *args, **kwargs):
    context_dict = {
        "title_text": "This is my title. There are many like it, but this one is mine.",
        "page_title": "Data Entry",
        "my_list": ["testa", "testb", "testc"]
    }
    return render(request, "manual_entry.html", context_dict)


####################
# Test for passing variables through the URL
####################
def url_test(request, year, month, day):
    context = {}
    return render(request, "filters.html", context)
