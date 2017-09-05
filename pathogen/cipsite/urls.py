"""cipsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
#from cipsite import static
from cipsite import pageDisplay 
from cipsite import listViews

from . import views

urlpatterns = [
#   url(r'^$',views.index),
    url(r'^$',listViews.index),
    url(r'^index',listViews.index),
    url(r'^tables',listViews.tables),
    url(r'^participant',listViews.participant),
    url(r'^publication',listViews.publication),
    url(r'^pabout',listViews.pabout),
    url(r'^rabout',listViews.rabout),
    url(r'^contact',listViews.contact),
    url(r'^downloadr',listViews.downloadr),
    url(r'^dtabler',listViews.dtabler),   
    url(r'^dmapr',listViews.dmapr),         
    url(r'^downloadp',listViews.downloadp),
    url(r'^dtablep',listViews.dtablep),   
    url(r'^dmapp',listViews.dmapp),  
    url(r'^admin/', admin.site.urls),

    url(r'^list_samplefield', pageDisplay.list_samplefield),
    url(r'^plist_samplefield', pageDisplay.plist_samplefield),
    url(r'^flist', pageDisplay.flist),
    url(r'^sinfo', pageDisplay.sinfo),
    url(r'^pflist', pageDisplay.flistp),
    url(r'^psinfo', pageDisplay.sinfop),
]
