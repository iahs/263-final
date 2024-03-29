"""hackmelists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^$', views.entry, name='entry'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^list/$', views.index, name='index'),
    url(r'^list/text_box/$', views.text_box, name='text_box'),
    url(r'^list/text_area/$', views.text_area, name='text_area'),
    url(r'^list/content_editable/$', views.content_editable, name='content_editable'),
    url(r'^list/onclick/$', views.onclick, name='onclick'),
    url(r'^query/$', views.query, name='query'),
]
