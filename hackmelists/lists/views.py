from django.shortcuts import render
from .models import ListItem
from urlparse import parse_qs

def entry(request):
    return render(request, 'lists/request.html')

def welcome(request):
    name = "User"
    if (request.method == 'POST' and request.POST.get("name", False)):
        name = request.POST["name"]
    return render(request, 'lists/welcome.html', {'name':name})

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

def query(request):
    items = ListItem.objects.order_by('id')
    try:
        name = parse_qs(request.META['QUERY_STRING'])['name'][0]
    except KeyError:
        name = "Default"
    return render(request, 'lists/query.html', {'items':items, 'name': name})
