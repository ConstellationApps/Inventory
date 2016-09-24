from django.forms import formset_factory
from django.shortcuts import render
from django.http import HttpResponse

from .forms import ItemForm
from .models import Item

def index(request):
    ItemFormSet = formset_factory(ItemForm)
    if request.method == 'POST':
        formset = ItemFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                myobject = form.save()
    formset = ItemFormSet()

    allCards = []
    for phase in Item.LIFECYCLE_STAGES:
        phaseDict = {}
        phaseDict['name'] = phase[1]
        phaseDict['cards'] = []
        for item in Item.objects.filter(stage=phase[0]):
            cardDict = {}
            cardDict['id'] = item.pk
            cardDict['name'] = item.name
            cardDict['quantity'] = item.quantity
            cardDict['notes'] = item.notes
            phaseDict['cards'].append(cardDict)
        allCards.append(phaseDict)

    return render(request, 'orderboard/index.html', {'formset': formset, 'stage_list':allCards})


def new_item(request):
    form = ItemForm()
    return HttpResponse(form)
