from django.shortcuts import render
from django.http import HttpResponse

from .forms import ItemForm

# Create your views here.

def index(request):
    return HttpResponse("We're Live!")

def new_item(request):
    form = ItemForm()
    return HttpResponse(form)
