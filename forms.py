from .models import Card
from .models import Board
from .models import Stage
from django.forms import ModelForm

class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'quantity', 'notes']

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'desc', 'active']g

class StageForm(ModelForm):
    class Meta:
        model = Stage
        fields = ['name', 'index', 'archived']
