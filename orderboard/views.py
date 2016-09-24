from django.forms import formset_factory
from django.shortcuts import render
from django.http import HttpResponse

from .forms import ItemForm

# Create your views here.

def index(request):
    ItemFormSet = formset_factory(ItemForm)
    if request.method == 'POST':
        formset = ItemFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                myobject = form.save()
    formset = ItemFormSet()
    return render(request, 'orderboard/index.html', {'formset': formset})


def new_item(request):
    form = ItemForm()
    return HttpResponse(form)
