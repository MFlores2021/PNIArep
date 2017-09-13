#!/usr/bin/python
import os, sys
import os.path
import re
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

currentdir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(currentdir)
import loadData


# download pages
def download(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	return render(request, 'download.html', context)

# dynamic pages
def flist(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	fid = request.GET.get('fid', '')
	sid_list = request.GET.get('sid', '')
	vname = request.GET.get('vname', '')
	data = loadData.load_data_samplefield()
	if sid_list:
		context['select'] = []
		context['select'] = sid_list.split(",")
		context['vname'] = 'unknown virus'
		if vname:
			context['vname'] = vname
	if fid:
		if fid in data:
			context['fid'] = fid
			context['prefix'] = fid[:3]
			context['departament'] = data[fid]['attr'][0]
			context['province'] = data[fid]['attr'][1]
			context['district'] = data[fid]['attr'][2]
			context['locality'] = data[fid]['attr'][3]
			context['lat'] = data[fid]['attr'][4]
			context['lng'] = data[fid]['attr'][5]
			context['alt'] = data[fid]['attr'][6]
			#context['reference'] = data[fid]['attr'][7]
			# context['img'] = data[fid]['attr'][7]
			context['sample'] = data[fid]['samp']
		else:
			context['ERRMSG'] = 'field ID ' + fid + ' is not correct'
	else:
		context['ERRMSG'] = 'no field was selected'
	return render(request, 'flist.html', context)

def sinfo(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	sid = request.GET.get('sid', '')
	if sid:
		context['sid'] = sid
		# parse known html and import it to virome page
		html_known = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/sample/result_" + sid + "/blastn.html"
		html_known_info = ""
		if os.path.exists(html_known):
			dh = open(html_known, "r")
			for i in range(6):
				next(dh)
			for line in dh:
				line = re.sub(r'width: 780px;', "", line)
				#line = re.sub(r'table-bordered', "table-striped", line)
				matchObj = re.search( r'blastn_references/(.*)\.html', line) # convet the link
				if matchObj:
					link = "/virome/sctg?vtp=blastn&sid=" + sid + "&vid=" + matchObj.group(1)
					line = re.sub(r'blastn_references/.*html', link, line)
				html_known_info = html_known_info + line + "\n"
		else:
			html_info = "None of virus was identified by nucleotide similarity (BLASTN)"

		context['html_known'] = html_known
		context['html_known_info'] = html_known_info

		# parse novel html and import it to virome page
		html_novel = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/sample/result_" + sid + "/blastx.html"
		html_novel_info = ""
		if os.path.exists(html_novel):
			dh = open(html_novel, "r")
			for i in range(6):
				next(dh)
			for line in dh:
				line = re.sub(r'width: 780px;', "", line)
				#line = re.sub(r'table-bordered', "table-striped", line)
				matchObj = re.search( r'blastx_references/(.*)\.html', line) # convet the link
				if matchObj:
					link = "/virome/sctg?vtp=blastx&sid=" + sid + "&vid=" + matchObj.group(1)
					line = re.sub(r'blastx_references/.*html', link, line)
				html_novel_info = html_novel_info + line + "\n"
		else:
			html_novel_info = "None of virus was identified by translated protein similarity (BLASTX)"

		context['html_novel'] = html_novel
		context['html_novel_info'] = html_novel_info

		# get sample clean information 
		context['total']   = 'NA'
		context['clean']   = 'NA'
		context['cleanP']  = 'NA'
		context['rRNA']    = 'NA'
		context['tsnoRNA'] = 'NA'
		context['final']   = 'NA'
		context['finalP']  = 'NA'

		data_clean = loadData.load_data_clean()
		if sid in data_clean:
			context['total']   = data_clean[sid]['total']
			context['clean']   = data_clean[sid]['clean']
			context['cleanP']  = data_clean[sid]['cleanP']
			context['rRNA']    = str(data_clean[sid]['chlo']) + '/' + str(data_clean[sid]['rRNA'])
			context['tsnoRNA'] = str(data_clean[sid]['tRNA']) + '/' + str(data_clean[sid]['snoRNA']) + '/' + str(data_clean[sid]['snRNA'])
			context['final']   = data_clean[sid]['final']
			context['finalP']  = data_clean[sid]['finalP']
	else:
		context['ERRMSG'] = 'no sample was selected'
	return render(request, 'sinfo.html', context)

# For phytoptora
def flistp(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	fid = request.GET.get('fid', '')
	sid_list = request.GET.get('sid', '')
	vname = request.GET.get('vname', '')
	data = loadData.pload_data_samplefield()
	
	if sid_list:
		context['select'] = []
		context['select'] = sid_list.split(",")
		context['vname'] = 'unknown virus'
		if vname:
			context['vname'] = vname
	if fid:
		if fid in data:
			context['fid'] = fid
			context['prefix'] = fid[:3]
			context['isolateid'] = data[fid]['attr'][0]
			context['region'] = data[fid]['attr'][1]
			context['province'] = data[fid]['attr'][2]
			context['district'] = data[fid]['attr'][3]
			context['locality'] = data[fid]['attr'][4]
			context['lat'] = data[fid]['attr'][5]
			context['lng'] = data[fid]['attr'][6]
			context['alt'] = data[fid]['attr'][7]
			context['reference'] = data[fid]['attr'][8]
			context['img'] = data[fid]['attr'][8]
			context['sample'] = data[fid]['sampl']
			print context['sample']
		else:
			context['ERRMSG'] = 'field ID ' + fid + ' is not correct'
	else:
		context['ERRMSG'] = 'no field was selected'
	return render(request, 'flistp.html', context)

def sinfop(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	sid = request.GET.get('sid', '')
	if sid:
		context['sid'] = sid
		# parse known html and import it to virome page
		html_known = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/sample/result_" + sid + "/blastn.html"
		html_known_info = ""
		if os.path.exists(html_known):
			dh = open(html_known, "r")
			for i in range(6):
				next(dh)
			for line in dh:
				line = re.sub(r'width: 780px;', "", line)
				#line = re.sub(r'table-bordered', "table-striped", line)
				matchObj = re.search( r'blastn_references/(.*)\.html', line) # convet the link
				if matchObj:
					link = "/virome/sctg?vtp=blastn&sid=" + sid + "&vid=" + matchObj.group(1)
					line = re.sub(r'blastn_references/.*html', link, line)
				html_known_info = html_known_info + line + "\n"
		else:
			html_info = "None of virus was identified by nucleotide similarity (BLASTN)"

		context['html_known'] = html_known
		context['html_known_info'] = html_known_info

		# parse novel html and import it to virome page
		html_novel = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/sample/result_" + sid + "/blastx.html"
		html_novel_info = ""
		if os.path.exists(html_novel):
			dh = open(html_novel, "r")
			for i in range(6):
				next(dh)
			for line in dh:
				line = re.sub(r'width: 780px;', "", line)
				#line = re.sub(r'table-bordered', "table-striped", line)
				matchObj = re.search( r'blastx_references/(.*)\.html', line) # convet the link
				if matchObj:
					link = "/virome/sctg?vtp=blastx&sid=" + sid + "&vid=" + matchObj.group(1)
					line = re.sub(r'blastx_references/.*html', link, line)
				html_novel_info = html_novel_info + line + "\n"
		else:
			html_novel_info = "None of virus was identified by translated protein similarity (BLASTX)"

		context['html_novel'] = html_novel
		context['html_novel_info'] = html_novel_info

		# get sample clean information 
		context['total']   = 'NA'
		context['clean']   = 'NA'
		context['cleanP']  = 'NA'
		context['rRNA']    = 'NA'
		context['tsnoRNA'] = 'NA'
		context['final']   = 'NA'
		context['finalP']  = 'NA'

		data_clean = loadData.load_data_clean()
		if sid in data_clean:
			context['total']   = data_clean[sid]['total']
			context['clean']   = data_clean[sid]['clean']
			context['cleanP']  = data_clean[sid]['cleanP']
			context['rRNA']    = str(data_clean[sid]['chlo']) + '/' + str(data_clean[sid]['rRNA'])
			context['tsnoRNA'] = str(data_clean[sid]['tRNA']) + '/' + str(data_clean[sid]['snoRNA']) + '/' + str(data_clean[sid]['snRNA'])
			context['final']   = data_clean[sid]['final']
			context['finalP']  = data_clean[sid]['finalP']
	else:
		context['ERRMSG'] = 'no sample was selected'
	return render(request, 'sinfop.html', context)

def sctg(request):
	context = {}
	context.update(settings.GLOBAL_SETTINGS)
	sid = request.GET.get('sid', '')
	vid = request.GET.get('vid', '')
	vtp = request.GET.get('vtp', '')
	if sid and vid and vtp:
		html = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/sample/result_" + sid + "/" + vtp + "_references/" + vid + ".html"
		html_info = ""
		dh = open(html, "r")
		for i in range(5):
			next(dh)
		for line in dh:
			line = re.sub(r'table-bordered', "", line)
			#line = re.sub(r'<table.*center', "<table class=\"table table\-striped\"", line) # adjust table style
			matchObj = re.search(r'img src="(.*)\.png', line) # convet the png
			if matchObj:
				link = "img src =\"/static/sample/result_" + sid + "/" + vtp + "_references/" + matchObj.group(1) + ".png\" \""
				line = re.sub(r'img src.*\.png"', link, line)
			html_info = html_info + line + "\n"
		context['html'] = html
		context['html_info'] = html_info
		context['sid'] = sid
		context['vid'] = vid
	else:
		context['ERRMSG'] = 'no sample or virus was selected'
	return render(request, 'sctg.html', context)

def geo_list(request):
	data = loadData.load_data()
	return JsonResponse(data)

def list_samplefield(request):
	data = loadData.load_data_samplefield()
	return JsonResponse(data)

def plist_samplefield(request):
	data = loadData.pload_data_samplefield()
	return JsonResponse(data)