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
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500

from cipsite import pageDisplay 
from cipsite import listViews

from . import views

urlpatterns = [
    url(r'^$',listViews.index),
    url(r'^index',listViews.index),
    url(r'^tables',listViews.tables),
    url(r'^participant',listViews.participant),
    url(r'^publication',listViews.publication),
    url(r'^pabout',listViews.pabout),
    url(r'^rabout',listViews.rabout),
    url(r'^vabout',listViews.vabout),
    url(r'^contact',listViews.contact),
    url(r'^downloadr',listViews.downloadr),
    url(r'^dtabler',listViews.dtabler),   
    url(r'^dmapr',listViews.dmapr),         
    url(r'^downloadp',listViews.downloadp),
    url(r'^dtablep',listViews.dtablep),   
    url(r'^dtablehp',listViews.dtablehp), 
    url(r'^dtablev',listViews.dtablev),  
    url(r'^dmapp',listViews.dmapp),  
    url(r'^map',listViews.map),  
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^list_samplefield', pageDisplay.list_samplefield),
    url(r'^plist_samplefield', pageDisplay.plist_samplefield),
    url(r'^hplist_samplefield', pageDisplay.hplist_samplefield),
    url(r'^vlist_samplefield', pageDisplay.vlist_samplefield),
    url(r'^load_map', pageDisplay.load_map_all),
    url(r'^p_summary', pageDisplay.p_summary),    
    url(r'^flist', pageDisplay.flist),
    url(r'^sinfo', pageDisplay.sinfo),
    url(r'^psinfo', pageDisplay.sinfop),
    url(r'^vsinfo', pageDisplay.sinfov),
    url(r'^pflist', pageDisplay.flistp),
    url(r'^vflist', pageDisplay.flistv),
    url(r'^sctg',  pageDisplay.sctg),
    url(r'^upload', listViews.upload),
    url(r'^help', listViews.help),
]

handler404 = 'listViews.error_404'
handler500 = 'listViews.error_500'

