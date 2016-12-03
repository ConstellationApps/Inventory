from django.forms import formset_factory
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core import serializers

import json
import operator

from SimpleBase.models import GlobalTemplateSettings

from .forms import CardForm
from .forms import StageForm
from .forms import BoardForm

from .models import Card
from .models import Stage
from .models import Board


# =============================================================================
# View Functions
# =============================================================================

def view_list(request):
    return HttpResponse("Rendered list of boards")

def view_board(request, board_id):
    '''Return the base template that will call the API to display the
    entire board with all the cards'''
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()
    form = CardForm()

    return render(request, 'SimpleInventory/board.html', {
        'form': form,
        'id': board_id,
        'template_settings': template_settings,
    })

def view_board_archive(request, board_id):
    '''Return the base template that will call the API to display the
    board's archived cards'''
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()

    return render(request, 'SimpleInventory/archive.html', {
        'id': board_id,
        'template_settings': template_settings,
    })

# =============================================================================
# Management Functions
# =============================================================================

def manage_create_board(request):
    boardForm = BoardForm()
    return render(request, "create-board.html", {'form':boardForm})

def manage_stages(request):
    stageForm = StageForm()
    return render(request, "SimpleInventory/manage-stages.html", {
        'form': stageForm
    })

# =============================================================================
# API Functions for the v1 API
# =============================================================================

    # The functions in this section handle API calls for creating,
    # activating, and deactivating boards, creating, moving, and archiving
    # cards, and creating, activating, deactivating, and updating states.

# -----------------------------------------------------------------------------
# API Functions related to Board Operations
# -----------------------------------------------------------------------------

def api_v1_board_list(request):
    '''List all boards, can be filtered by the client, will return a list
    of all boards, including boards that the client is not authorized to
    use.'''
    boards = serializers.serialize('json', Board.objects.all())
    return HttpResponse(boards)

def api_v1_board_create(request):
    '''Create a board, takes a post with a CSRF token, name, and
    description and returns a json object containing the status which will
    be either 'success' or 'fail' and a friendly message'''
    boardForm = BoardForm(request.POST or None)
    retVal = {}
    if request.POST and boardForm.is_valid():
        newBoard = Board()
        newBoard.name = boardForm.cleaned_data['name']
        newBoard.desc = boardForm.cleaned_data['desc']
        try:
            newBoard.save()
            retVal['status'] = "success"
            retVal['msg'] = "Board created successfully"
        except:
            retVal['status'] = "fail"
            retVal['msg'] = "Could not create board"
    else:
        retVal['status'] = "fail"
        retVal['msg'] = "Invalid form data"
    return HttpResponse(json.dumps(retVal))

def api_v1_board_deactivate(request, boardID):
    '''deactivates a board, returns status object'''
    board = Board.objects.get(pk=boardID)
    board.active = False
    retVal = {}
    try:
        board.save()
        retVal['status'] = "success"
        retVal['msg'] = "Board deactivated successfully"
    except:
        retVal['status'] = "fail"
        retVal['msg'] = "Could not deactivate board"

    return HttpResponse(json.dumps(retVal))

def api_v1_board_activate(request, boardID):
    '''activates a board, returns status object'''
    board = Board.objects.get(pk=boardID)
    board.active = True
    retVal = {}
    try:
        board.save()
        retVal['status'] = "success"
        retVal['msg'] = "Board activated successfully"
    except:
        retVal['status'] = "fail"
        retVal['msg'] = "Could not activate board"

    return HttpResponse(json.dumps(retVal))

def api_v1_board_active_cards(request, boardID):
    '''Retrieve all active cards for the stated board'''
    cards = serializers.serialize('json',
                                  Card.objects.filter(
                                      board=Board.objects.get(pk=boardID),
                                      archived=False
                                  ))
    return HttpResponse(cards)

def api_v1_board_archived_cards(request, boardID):
    '''Retrieve all archived cards for the stated board'''
    cards = serializers.serialize('json',
                                  Card.objects.filter(
                                      board=Board.objects.get(pk=boardID),
                                      archived=True
                                  ))
    return HttpResponse(cards)

# -----------------------------------------------------------------------------
# API Functions related to Card Operations
# -----------------------------------------------------------------------------

def api_v1_card_create(request):
    '''Creates a new card from POST data.  Takes in a CSRF token with the
    data as well as card name, quantity, description, board reference, and
    active state'''
    cardForm = CardForm(request.POST or None)
    retVal = {}
    if request.POST and cardForm.is_valid():
        newCard = Card()
        newCard.name = cardForm.cleaned_data['name']
        newCard.quantity = cardForm.cleaned_data['quantity']
        newCard.notes = cardForm.cleaned_data['notes']
        newCard.stage = cardForm.cleaned_data['stage']
        newCard.board = cardForm.cleaned_data['board']
        newCard.archived = False
        try:
            newCard.save()
            return HttpResponse(serializers.serialize('json', [newCard,]))
        except:
            retVal['status'] = "fail"
            retVal['msg'] = "Could not create card"
    else:
        retVal['status'] = "fail"
        retVal['msg'] = "Invalid form data"
    return HttpResponse(json.dumps(retVal))

def api_v1_card_archive(request, cardID):
    '''Archive a card identified by the given primary key'''
    card = Card.objects.get(pk=cardID)
    card.archived = True
    retVal = {}
    try:
        card.save()
        retVal['status'] = "success"
        retVal['msg'] = "Card archived successfully"
    except:
        retVal['status'] = "fail"
        retVal['msg'] = "Could not archive card"

    return HttpResponse(json.dumps(retVal))

def api_v1_card_unarchive(request, cardID):
    '''Unarchive a card identified by the given primary key'''
    card = Card.objects.get(pk=cardID)
    card.archived = False
    retVal = {}
    try:
        card.save()
        retVal['status'] = "success"
        retVal['msg'] = "Card unarchived successfully"
    except:
        retVal['status'] = "fail"
        retVal['msg'] = "Could not unarchive card"

    return HttpResponse(json.dumps(retVal))

def api_v1_card_move_right(request, cardID):
    '''Move a card to the next stage to the left'''
    stages = list(Stage.objects.filter(archived=False))
    stages.sort(key=lambda x: x.index)

    card = get_object_or_404(Card, pk=cardID)
    stageID = stages.index(card.stage)

    retVal = {}
    try:
        card.stage = stages[stageID + 1]
        card.save()
        retVal['status'] = "success"
        retVal['msg'] = "Card unarchived successfully"
        retVal['stageName'] = card.stage.name
        retVal['stageID'] = card.stage.pk
    except:
        retVal['status'] = "fail"
        retVal['msg'] = "Could not unarchive card"

    return HttpResponse(json.dumps(retVal))

def api_v1_card_move_left(request, cardID):
    '''Move a card to the next stage to the left'''
    stages = list(Stage.objects.filter(archived=False))
    stages.sort(key=lambda x: x.index)

    card = get_object_or_404(Card, pk=cardID)
    stageID = stages.index(card.stage)

    retVal = {}
    try:
        if stageID - 1 < 0:
            raise IndexError
        card.stage = stages[stageID - 1]
        card.save()
        retVal['status'] = "success"
        retVal['msg'] = "Card unarchived successfully"
        retVal['stageName'] = card.stage.name
        retVal['stageID'] = card.stage.pk
    except:
        retVal['status'] = "fail"
        retVal['msg'] = "Could not unarchive card"

    return HttpResponse(json.dumps(retVal))

# -----------------------------------------------------------------------------
# API Functions related to Stage Operations
# -----------------------------------------------------------------------------

def api_v1_stage_list(request):
    '''List all stages, can be filtered by the client, will return a list
    of all stages, including stages that the client is not authorized to
    use.'''
    stages = serializers.serialize('json', Stage.objects.all())
    return HttpResponse(stages)

def api_v1_stage_create(request):
    '''Creates a new stage from POST data.  Takes in a CSRF token with the
    data as well as stage name, quantity, description, board reference, and
    active state'''
    stageForm = StageForm(request.POST or None)
    retVal = {}
    if request.POST and stageForm.is_valid():
        newStage = Stage()
        newStage.name = stageForm.cleaned_data['name']
        newStage.index = stageForm.cleaned_data['index']
        newStage.archived = False
        try:
            newStage.save()
            retVal['status'] = "success"
            retVal['msg'] = "Stage created successfully"
        except:
            retVal['status'] = "fail"
            retVal['msg'] = "Could not create stage"
    else:
        retVal['status'] = "fail"
        retVal['msg'] = "Invalid form data"
    return HttpResponse(json.dumps(retVal))

def api_v1_stage_archive(request, stageID):
    '''Archive a stage identified by the given primary key'''
    stage = Stage.objects.get(pk=stageID)
    stage.archived = True
    retVal = {}
    try:
        stage.save()
        retVal['status'] = "success"
        retVal['msg'] = "Stage archived successfully"
    except:
        retVal['status'] = "fail"
        retVal['msg'] = "Could not archive stage"

    return HttpResponse(json.dumps(retVal))

def api_v1_stage_unarchive(request, stageID):
    '''Unarchive a stage identified by the given primary key'''
    stage = Stage.objects.get(pk=stageID)
    stage.archived = False
    retVal = {}
    try:
        stage.save()
        retVal['status'] = "success"
        retVal['msg'] = "Stage unarchived successfully"
    except:
        retVal['status'] = "fail"
        retVal['msg'] = "Could not unarchive stage"

    return HttpResponse(json.dumps(retVal))

def api_v1_stage_move_left(request, stageID):
    '''Move a stage to the left'''
    stageCurrent = Stage.objects.get(pk=stageID)
    if stageCurrent.index > 0:
        stageLeft = Stage.objects.get(index=stageCurrent.index-1)

        stageLeft.index = stageLeft.index + 1
        stageCurrent.index = stageCurrent.index - 1

        stageLeft.save()
        stageCurrent.save()
        
def api_v1_stage_move_right(request, stageID):
    '''Move a stage to the right'''
    stageCurrent = Stage.objects.get(pk=stageID)
    try:
        stageRight = Stage.objects.get(index=stageCurrent.index+1)

        stageRight.index = stageRight.index - 1
        stageCurrent.index = stageCurrent.index + 1

        stageRight.save()
        stageCurrent.save()
        
    except DoesNotExist as e:
        pass
