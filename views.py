from django.forms import formset_factory
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.core import serializers
from django.urls import reverse

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
    '''Return the base template that will call the API to display
    a list of boards'''
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()

    return render(request, 'SimpleInventory/view-list.html', {
        'template_settings': template_settings,
    })

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

def manage_boards(request):
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()
    boardForm = BoardForm()

    return render(request, 'SimpleInventory/manage-boards.html', {
        'form': boardForm,
        'template_settings': template_settings,
    })

def manage_board_edit(request, board_id):
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()
    board = Board.objects.get(pk=board_id)
    boardName = board.name
    boardDesc = board.desc
    boardForm = BoardForm(initial={'name': boardName, 'desc': boardDesc})
    return render(request, 'SimpleInventory/edit-board.html', {
        'form': boardForm,
        'board_id': board_id,
        'template_settings': template_settings,
    })

def manage_stages(request):
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()
    stageForm = StageForm()
    return render(request, "SimpleInventory/manage-stages.html", {
        'form': stageForm,
        'template_settings': template_settings,
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
    boardObjects = Board.objects.all()
    if boardObjects:
        boards = serializers.serialize('json', boardObjects)
        return HttpResponse(boards)
    else:
        return HttpResponseNotFound("You have no boards at this time")

def api_v1_board_create(request):
    '''Create a board, takes a post with a CSRF token, name, and
    description and returns a json object containing the status which will
    be either 'success' or 'fail' and a friendly message'''
    boardForm = BoardForm(request.POST or None)
    if request.POST and boardForm.is_valid():
        newBoard = Board()
        newBoard.name = boardForm.cleaned_data['name']
        newBoard.desc = boardForm.cleaned_data['desc']
        try:
            newBoard.save()
            return HttpResponse(serializers.serialize('json', [newBoard,]))
        except:
            return HttpResponseServerError("Could not save board at this time")
    else:
        return HttpResponseBadRequest("Invalid Form Data!")

def api_v1_board_update(request, boardID):
    '''Update a board, based upon the form data contained in request'''
    boardForm = BoardForm(request.POST or None)
    if request.POST and boardForm.is_valid():
        try:
            board = Board.objects.get(pk=boardID)
            newName = boardForm.cleaned_data['name']
            newDesc = boardForm.cleaned_data['desc']
            board.name = newName
            board.desc = newDesc
            board.save()
            return HttpResponse(json.dumps({"board" : reverse("view_board", args=[boardID,])}))
        except:
            return HttpResponseServerError("Invalid board ID")
    else:
        return HttpResponseBadRequest("Invalid Form Data!")

def api_v1_board_archive(request, boardID):
    '''archives a board, returns status object'''
    board = Board.objects.get(pk=boardID)
    board.archived = True
    try:
        board.save()
        return HttpResponse("Board Archived")
    except:
        return HttpResponseServerError("Board could not be archived at this time")

def api_v1_board_unarchive(request, boardID):
    '''unarchives a board, returns status object'''
    board = Board.objects.get(pk=boardID)
    board.archived = False
    try:
        board.save()
        return HttpResponse("Board Un-Archived")
    except:
        return HttpResponseServerError("Board could not be un-archived at this time")

def api_v1_board_active_cards(request, boardID):
    '''Retrieve all active cards for the stated board'''
    cardObjects = Card.objects.filter(board=Board.objects.get(pk=boardID),
                                      archived=False)
    if cardObjects:
        cards = serializers.serialize('json', cardObjects)
        return HttpResponse(cards)
    else:
        return HttpResponseNotFound("There are no active cards on this board")

def api_v1_board_archived_cards(request, boardID):
    '''Retrieve all archived cards for the stated board'''
    cardObjects = Card.objects.filter(board=Board.objects.get(pk=boardID),
                                      archived=True)
    if cardObjects:
        cards = serializers.serialize('json', cardObjects)
        return HttpResponse(cards)
    else:
        return HttpResponseNotFound("This board has no archived cards")

def api_v1_board_info(request, boardID):
    '''Retrieve the title and description for the stated board'''
    try:
        board = Board.objects.get(pk=boardID)
        response = json.dumps({"title" : board.name, "desc" : board.desc})
        return HttpResponse(response)
    except:
        return HttpResponseNotFound("No board with given ID found")

# -----------------------------------------------------------------------------
# API Functions related to Card Operations
# -----------------------------------------------------------------------------

def api_v1_card_create(request):
    '''Creates a new card from POST data.  Takes in a CSRF token with the
    data as well as card name, quantity, description, board reference, and
    active state'''
    cardForm = CardForm(request.POST or None)
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
            return HttpResponseServerError("Could not create card at this time")
    else:
        return HttpResponseBadRequest("Invalid Form Data!")

def api_v1_card_archive(request, cardID):
    '''Archive a card identified by the given primary key'''
    card = Card.objects.get(pk=cardID)
    card.archived = True
    try:
        card.save()
        return HttpResponse("Card successfully archived")
    except:
        return HttpResponseServerError("Card could not be archived at this time")

def api_v1_card_unarchive(request, cardID):
    '''Unarchive a card identified by the given primary key'''
    card = Card.objects.get(pk=cardID)
    card.archived = False
    try:
        card.save()
        return HttpResponse("Card successfully un-archived")
    except:
        return HttpResponseServerError("Card could not be un-archived at this time")

def api_v1_card_move_right(request, cardID):
    '''Move a card to the next stage to the left'''
    stages = list(Stage.objects.filter(archived=False))
    stages.sort(key=lambda x: x.index)

    card = get_object_or_404(Card, pk=cardID)
    stageID = stages.index(card.stage)

    try:
        card.stage = stages[stageID + 1]
        card.save()
        retVal = {}
        retVal['status'] = "success"
        retVal['msg'] = "Card unarchived successfully"
        retVal['stageName'] = card.stage.name
        retVal['stageID'] = card.stage.pk
        return HttpResponse(json.dumps(retVal))
    except:
        return HttpResponseServerError("Card could not be moved at this time")

def api_v1_card_move_left(request, cardID):
    '''Move a card to the next stage to the left'''
    stages = list(Stage.objects.filter(archived=False))
    stages.sort(key=lambda x: x.index)

    card = get_object_or_404(Card, pk=cardID)
    stageID = stages.index(card.stage)

    try:
        if stageID - 1 < 0:
            raise IndexError
        card.stage = stages[stageID - 1]
        card.save()
        retVal = {}
        retVal['status'] = "success"
        retVal['msg'] = "Card unarchived successfully"
        retVal['stageName'] = card.stage.name
        retVal['stageID'] = card.stage.pk
        return HttpResponse(json.dumps(retVal))
    except:
        return HttpResponseServerError("Card could not be moved at this time")

# -----------------------------------------------------------------------------
# API Functions related to Stage Operations
# -----------------------------------------------------------------------------

def api_v1_stage_list(request):
    '''List all stages, can be filtered by the client, will return a list
    of all stages, including stages that the client is not authorized to
    use.'''
    stageObjects = Stage.objects.all()
    if stageObjects:
        stages = serializers.serialize('json', Stage.objects.all())
        return HttpResponse(stages)
    else:
        return HttpResponseNotFound("There are no stages defined")

def api_v1_stage_create(request):
    '''Creates a new stage from POST data.  Takes in a CSRF token with the
    data as well as stage name, quantity, description, board reference, and
    active state'''
    stageForm = StageForm(request.POST or None)
    if request.POST and stageForm.is_valid():
        newStage = Stage()
        newStage.name = stageForm.cleaned_data['name']
        newStage.index = -1   # The model save function will append the stage
        newStage.archived = False
        try:
            newStage.save()
            return HttpResponse(serializers.serialize('json', [newStage,]))
        except:
            return HttpResponseServerError("Stage could not be created at this time")
    else:
        return HttpResponseBadRequest("Invalid Form Data!")

def api_v1_stage_archive(request, stageID):
    '''Archive a stage identified by the given primary key'''
    stage = Stage.objects.get(pk=stageID)
    stage.archived = True
    try:
        stage.save()
        return HttpResponse("Stage successfully archived")
    except:
        return HttpResponseServerError("Stage could not be archived at this time")

def api_v1_stage_unarchive(request, stageID):
    '''Unarchive a stage identified by the given primary key'''
    stage = Stage.objects.get(pk=stageID)
    stage.archived = False
    try:
        stage.save()
        return HttpResponse("Stage successfully un-archived")
    except:
        return HttpResponse("Stage could not be un-archived at this time")

def api_v1_stage_move_left(request, stageID):
    '''Move a stage to the left'''
    stageCurrent = Stage.objects.get(pk=stageID)
    if stageCurrent.index > 0:
        stageLeft = Stage.objects.get(index=stageCurrent.index-1)
        try:
            stageCurrent.swap(stageLeft)
            return HttpResponse("Stage successfully moved")
        except:
            return HttpResponseServerError("Stage could not be moved at this time")
    else:
        return HttpResponseBadRequest("Stage cannot be moved")

def api_v1_stage_move_right(request, stageID):
    '''Move a stage to the right'''
    stageCurrent = Stage.objects.get(pk=stageID)
    try:
        stageRight = Stage.objects.get(index=stageCurrent.index+1)
        stageCurrent.swap(stageRight)
        return HttpResponse("Stage successfully moved")
    except:
        return HttpResponseServerError("Stage could not be moved at this time")
