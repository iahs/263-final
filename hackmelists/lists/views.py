from django.shortcuts import render
from .models import ListItem

def index(request):
    items = ListItem.objects.order_by('id')
    return render(request, 'lists/index.html', {'items':items})

def text_box(request):
    items = ListItem.objects.order_by('id')
    return render(request, 'lists/list.html', {'items':items, 'type':'text_box'})

def text_area(request):
    items = ListItem.objects.order_by('id')
    return render(request, 'lists/list.html', {'items':items, 'type':'text_area'})

def content_editable(request):
    items = ListItem.objects.order_by('id')
    return render(request, 'lists/list.html',
                  {'items':items, 'type':'content_editable'})

def onclick(request):
    items = ListItem.objects.order_by('id')
    return render(request, 'lists/list.html', {'items':items, 'type':'onclick'})
