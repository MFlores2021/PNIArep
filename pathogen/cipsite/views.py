from django.shortcuts import render

def index(request):
    return render(request, "index.html")

# def map(request):
#     return render(request, "map.html")

def tables(request):
    return render(request, "tables.html")

def participant(request):
    return render(request, "participant.html")

def publication(request):
    return render(request, "publication.html")

def contact(request):
    return render(request, "contact.html")

def downloadr(request):
    return render(request, "downloadr.html")