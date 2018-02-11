#!/usr/bin/python
import os, sys
import os.path
import re
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

# basic static pages
def index(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	return render(request, 'index.html', context)

def dlist(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	return render(request, 'dlist.html', context)

def dtable(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	return render(request, 'dtable.html', context)

def participant(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	return render(request, 'participant.html', context)

def sample(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)    
	return render(request, 'sample.html', context)

def dmap(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	return render(request, 'dmap.html', context)

def publication(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	return render(request, 'publication.html', context)

def link(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	return render(request, 'link.html', context)

def data_interpreting(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	return render(request, 'data_interpreting.html', context)

def evaluating_alignment(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	return render(request, 'evaluating_alignment.html', context)

def boot(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	return render(request, 'pages/index.html', context)

