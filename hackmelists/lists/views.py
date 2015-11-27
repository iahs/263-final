from django.shortcuts import render
from .models import ListItem

def list(request):
    items = ListItem.objects.order_by('id')
    return render(request, 'lists/index.html', {'items':items})
