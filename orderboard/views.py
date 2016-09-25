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
        if phase == Item.LIFECYCLE_STAGES[-1]:
            continue
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

def move_left(request, cardID):
    # This is safe to assert since the primary key must only ever return a single result
    item = Item.objects.filter(pk=cardID)[0]

    stageIndex = 0
    for stageTuple in Item.LIFECYCLE_STAGES:
        if item.stage == stageTuple[0]:
            print(str(stageTuple))
            stageIndex = Item.LIFECYCLE_STAGES.index(stageTuple)
            print(stageIndex)
            item.stage = Item.LIFECYCLE_STAGES[stageIndex - 1][0]
            item.save()
            break
    return HttpResponse(Item.LIFECYCLE_STAGES[stageIndex - 1][1])

def move_right(request, cardID):
    # This is safe to assert since the primary key must only ever return a single result
    item = Item.objects.filter(pk=cardID)[0]

    stageIndex = 0
    for stageTuple in Item.LIFECYCLE_STAGES:
        if item.stage == stageTuple[0]:
            print(str(stageTuple))
            stageIndex = Item.LIFECYCLE_STAGES.index(stageTuple)
            print(stageIndex)
            item.stage = Item.LIFECYCLE_STAGES[stageIndex + 1][0]
            item.save()
            break
    return HttpResponse(Item.LIFECYCLE_STAGES[stageIndex + 1][1])

def archive(request, cardID):
    item = Item.objects.filter(pk=cardID)[0]
    item.stage = Item.LIFECYCLE_STAGES[-1][0]
    item.save()
    return HttpResponse("Archived " + str(cardID))
