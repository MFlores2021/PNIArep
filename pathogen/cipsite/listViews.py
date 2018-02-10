from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

import loadData
import scripts

def index(request):
    return render(request, "index.html")

def map(request):
    return render(request, "map.html")

def tables(request):
    return render(request, "tables.html")

def participant(request):
    return render(request, "participant.html")

def publication(request):
    return render(request, "publication.html")

def contact(request):
    return render(request, "contact.html")

def pabout(request):
    return render(request, "pabout.html")

def rabout(request):
    return render(request, "rabout.html")

def downloadr(request):
    return render(request, "downloadr.html")

def upload(request):
    if request.method == 'POST' and request.FILES['xlsxfile']:
    	dbase = ""
    	if 'optradio' in request.POST:
   			dbase = request.POST['optradio']
   			
        myfile = request.FILES['xlsxfile']
        fs = FileSystemStorage(location='./static/data') 
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        result = scripts.upload_sql_xlsx('./static/data/' + filename,dbase)
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        }, result)
    return render(request, 'upload.html')

def dtabler(request):
	data = loadData.load_data_samplefield()
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	fid = request.GET.get('fid', '')
	if fid:
		if fid in data:
			context['fid'] = fid
			context['prefix'] = fid[0] + fid[1]
			context['region'] = data[fid]['attr'][0]
			context['district'] = data[fid]['attr'][1]
			context['locality'] = data[fid]['attr'][2]
			context['lat'] = data[fid]['attr'][3]
			context['lng'] = data[fid]['attr'][4]
			context['alt'] = data[fid]['attr'][5]
			context['fsize'] = data[fid]['attr'][6]
			context['img'] = data[fid]['attr'][7]
			context['sample'] = data[fid]['samp']
		else:
			context['ERRMSG'] = 'field ID ' + fid + ' is not correct'
	else:
		context['ERRMSG'] = 'no field was selected'
	return render(request, 'dtabler.html', context)

def dmapr(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	return render(request, 'dmapr.html', context)


def downloadp(request):
    return render(request, "downloadp.html")


def dtablep(request):
	data = loadData.pload_data_samplefield()
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	fid = request.GET.get('fid', '')
	if fid:
		if fid in data:
			context['fid'] = fid
			context['prefix'] = fid[0] + fid[1]
			context['region'] = data[fid]['attr'][0]
			context['district'] = data[fid]['attr'][1]
			context['locality'] = data[fid]['attr'][2]
			context['lat'] = data[fid]['attr'][3]
			context['lng'] = data[fid]['attr'][4]
			context['alt'] = data[fid]['attr'][5]
			context['fsize'] = data[fid]['attr'][6]
			context['img'] = data[fid]['attr'][7]
			context['sample'] = data[fid]['samp']
		else:
			context['ERRMSG'] = 'field ID ' + fid + ' is not correct'
	else:
		context['ERRMSG'] = 'no field was selected'
	return render(request, 'dtablep.html', context)

def dtablev(request):
	data = loadData.vload_data_samplefield()
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	fid = request.GET.get('fid', '')
	if fid:
		if fid in data:
			context['fid'] = fid
			context['prefix'] = fid[0] + fid[1]
			context['region'] = data[fid]['attr'][0]
			context['district'] = data[fid]['attr'][1]
			context['locality'] = data[fid]['attr'][2]
			context['lat'] = data[fid]['attr'][3]
			context['lng'] = data[fid]['attr'][4]
			context['alt'] = data[fid]['attr'][5]
			context['fsize'] = data[fid]['attr'][6]
			context['img'] = data[fid]['attr'][7]
			context['sample'] = data[fid]['samp']
		else:
			context['ERRMSG'] = 'field ID ' + fid + ' is not correct'
	else:
		context['ERRMSG'] = 'no field was selected'
	return render(request, 'dtablev.html', context)

def dmapp(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	return render(request, 'dmapp.html', context)
	