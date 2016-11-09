from .models import Item
from .models import Board
from .models import Stage
from django.forms import ModelForm

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'notes']

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'desc']

class StageForm(ModelForm):
    class Meta:
        model = Stage
        fields = ['name', 'index', 'active']
