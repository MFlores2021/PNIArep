#!/usr/bin/python
import os, sys
import os.path
from django.conf import settings

import MySQLdb

# convert GPS location
# from degree,min,sec to decimal_system
# must be stay with load data
def convert_GPS(gps_unit):
	gps_unit = str(gps_unit)
	ma = gps_unit.split(".")  
	degree = abs(int(ma[0]))
	minute = ma[1][0:2]

	second = '0'
	if ma[1][2:4]:
		second = ma[1][2:4]
	s2 = '0'
	if ma[1][4:]:
		s2 = ma[1][4:]    
	minute = minute + "." + second + s2
	minute = float(minute)

	gps_decimal = degree + (minute / float(60))
	if float(gps_unit) < 0:
		gps_decimal = float(gps_decimal) * float(-1)
	gps_decimal = "%.5f" % gps_decimal
	return gps_decimal

# load dataset
def load_data():
	datafile = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/data.txt"

	# set filter set, only load sample dataset which is cleaned 
	data_clean_obj = load_data_clean();

	# main for load data
	data_obj = {}       # data object for store all data
	sample_uniq = {}    # dict for check the sample uniq
	dh = open(datafile, "r")
	for line in dh:
		if line[0] == "#":
			continue
		line = line.strip("\n")
		m = line.split("\t")
		# print len(m)

		# attribute for sample
		sampleID = m[0]
		prefix = sampleID[0:2]
		sdate = m[1]
		sage  = m[9]
		simgs_exist = []
		slimgs_exist = []
		simgs = m[12].split("/")
		slimgs = m[13].split("/")
		sintercrop = m[14]
		scultivar = m[15]

		for fname in simgs:
			fpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/images/" + prefix + "/" + fname
			if os.path.exists(fpath):
				simgs_exist.append(fname)

		for fname in slimgs:
			fpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/images/" + prefix + "/" + fname
			if os.path.exists(fpath):
				slimgs_exist.append(fname)

		if sampleID in sample_uniq.keys():
			sys.stderr.write('[ERR]dup sample ID ', sampleID, "\n")
		else:
			sample_uniq[sampleID] = 1

		sequenced = 0
		if sampleID in data_clean_obj:
			sequenced = 1

		# attribute for field
		region = m[2]
		district = m[3]
		locality = m[4]
		fid = m[5]
		lng = m[6]
		lat = m[7]
		#lng = convert_GPS(m[6])
		#lat = convert_GPS(m[7])
		alt = m[8]
		fsize = m[10]
		fimgs_exist = []
		fimgs = m[11].split("/")
		for fname in fimgs:
			fpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/images/" + prefix + "/" + fname
			if os.path.exists(fpath):
				fimgs_exist.append(fname)

		if fid not in data_obj.keys():
			data_obj[fid] = {}
			data_obj[fid]['attr'] = [region, district, locality, lat, lng, alt, fsize, fimgs_exist, fid]
			data_obj[fid]['samp'] = []
			data_obj[fid]['samp'].append([sampleID, sdate, sage, simgs_exist, slimgs_exist, sintercrop, scultivar, sequenced])
		else:
			data_obj[fid]['samp'].append([sampleID, sdate, sage, simgs_exist, slimgs_exist, sintercrop, scultivar, sequenced])
	return data_obj

# load data clean
def load_data_clean():
	dataCleanFile = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../static/data_clean.txt"
	dataCleanObj = {}	# data clean obj for store all data clean
	dh=open(dataCleanFile, "r")
	for line in dh:
		if line[0] == "#":
			continue
		line = line.strip("\n")
		m = line.split("\t")

		# title
		# 0		 1      2       3           4          5     6          7       8        9     10    11      12     13   14     15    16   17   18          19
		# sample rename barcode Data-set-ID Library-ID total 3P-unmatch 3P-null 3P-match baseN short cleaned %clean tRNA snoRNA snRNA chol rRNA final-clean %final-clean 
		if m[5] < 10000:
			continue

		sid = m[0];
		if len(m[1])>=3:
			sid = m[1]

		if sid not in dataCleanObj.keys():
			dataCleanObj[sid] = {}
			dataCleanObj[sid]['total'] = m[5]
			dataCleanObj[sid]['clean'] = m[11]
			dataCleanObj[sid]['cleanP']= m[12]
			dataCleanObj[sid]['tRNA']  = m[13]
			dataCleanObj[sid]['snoRNA']= m[14]
			dataCleanObj[sid]['snRNA'] = m[15]
			dataCleanObj[sid]['chlo']  = m[16]
			dataCleanObj[sid]['rRNA']  = m[17]
			dataCleanObj[sid]['final'] = m[18]
			dataCleanObj[sid]['finalP']= m[19]

	return dataCleanObj


# load dataset Phytoptora
def pload_data_samplefield():
	db = MySQLdb.connect(host="db",   user="root", passwd="<d4+484s3>",  db="dbpnia")
	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# execute SQL query using execute() method.
	cursor.execute("SELECT * from phytoptora")

	# Fetch a single row using fetchone() method.
	adh = cursor.fetchall()

	# disconnect from server
	db.close()


	# set filter set, only load sample dataset which is cleaned 
	data_clean_obj = load_data_clean();

	# main for load data
	data_obj = {}       # data object for store all data
	sample_uniq = {}    # dict for check the sample uniq
	
	print len(adh)

	for m in adh:

		#print len(m)

		# attribute for sample
		sampleID = m[1]
		isolateID = m[2]
		prefix = sampleID[0:2]
		fta = m[3]
		nofta = m[4]
		shost = m[5]  #host
		svariety = m[6]  #variety
		srace = m[19]
		srack = m[42]
		sbox = m[43]
		sgrid = m[44]
		svials = m[45]
		scollector = m[20]
		sdatecollection = m[21]
		sdate = m[41]

		if len(sdate.split("/")) == 3 :
			syear = sdate.split("/")[2]
		else:
			syear = "Unknown"

		sobservation = m[28]

		if sampleID in sample_uniq.keys():
			sys.stderr.write('[ERR]dup sample ID ', sampleID, "\n")
		else:
			sample_uniq[sampleID] = 1

		sequenced = 0
		if sampleID in data_clean_obj:
			sequenced = 1

		# attribute for field
		department = m[7]
		province = m[8]
		district = m[9]
		locality = m[10]
		reference = m[11]
		lat = m[12]
		lng = m[13]
		alt = m[14]
		fid = (m[7].replace(" ", "")+m[8].replace(" ", "")+m[9].replace(" ", "")+m[10].replace(" ", ""))  #m[3]

		#test
		pesticides = m[15]
		matingtype  = m[16]
		rflp  = m[22]
		aflp  = m[23]
		haplotypes  = m[17]
		metalaxyl  = m[18]
		gpiacetate  = m[24]
		gpistarch  = m[25]
		pepacetate  = m[26]
		peppage   = m[27]
		

		pig11 = m[29]
		pi02 = m[30]
		ssr11 = m[31]
		d13 = m[32]
		ssr8 = m[33]
		ssr4 = m[34]
		pi04 = m[35]
		pi70 = m[36]
		ssr6 = m[37]
		pi63 = m[38]
		ssr2 = m[39]
		pi4b = m[40]

		if fid not in data_obj.keys():
			data_obj[fid] = {}
			data_obj[fid]['attr'] = [isolateID,department, province, district, locality, lat, lng, alt, reference]
			data_obj[fid]['samp'] = []
			data_obj[fid]['sampl'] = []
			data_obj[fid]['test'] = []
			data_obj[fid]['test'].append([sampleID, isolateID, fid, matingtype, rflp , aflp , haplotypes , gpiacetate , gpistarch , pepacetate , peppage, metalaxyl, sobservation, pig11, pi02, ssr11, d13, ssr8, ssr4, pi04, pi70, ssr6, pi63, ssr2, pi4b, pesticides,fta,nofta ])
			data_obj[fid]['sampl'].append([sampleID, shost, svariety, srace, srack, sbox, sgrid, svials, scollector, sdatecollection, sequenced])
			data_obj[fid]['samp'].append([sampleID, isolateID, (isolateID), fid, sdate, shost, svariety, srace, srack, sbox, sgrid, svials, scollector, sdatecollection, sdate,sequenced])
		else:
			#data_obj[fid]['samp'] = []
			#data_obj[fid]['sampl'] = []
			data_obj[fid]['test'].append([sampleID, isolateID, fid, matingtype, rflp , aflp , haplotypes , gpiacetate , gpistarch , pepacetate , peppage, metalaxyl, sobservation, pig11, pi02, ssr11, d13, ssr8, ssr4, pi04, pi70, ssr6, pi63, ssr2, pi4b, pesticides,fta,nofta ])
			data_obj[fid]['sampl'].append([sampleID, shost, svariety, srace, srack, sbox, sgrid, svials, scollector, sdatecollection, sdate,  sobservation, sequenced])
			data_obj[fid]['samp'].append([sampleID, isolateID, (isolateID), fid, sdate, shost, svariety, srace, srack, sbox, sgrid, svials, scollector, sdatecollection, sdate,sequenced])
	
	#db.close()

	return data_obj


#Ralstonia:

def load_data_samplefield():
	#datafile = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/data1.txt"

	db = MySQLdb.connect(host="db",   user="root", passwd="<d4+484s3>",  db="dbpnia")
	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# execute SQL query using execute() method.
	cursor.execute("SELECT * from ralstonia")

	# Fetch a single row using fetchone() method.
	adh = cursor.fetchall()

	# disconnect from server
	db.close()


	# set filter set, only load sample dataset which is cleaned 
	data_clean_obj = load_data_clean();

	# main for load data
	data_obj = {}       # data object for store all data
	sample_uniq = {}    # dict for check the sample uniq

	for m in adh:

		# attribute for sample
		sampleID = m[1]
		prefix = sampleID[0:2]
		isolate = m[7]
		sdate = m[2]
		scultivar = m[9]
		shost = m[8]


		if sampleID in sample_uniq.keys():
			sys.stderr.write('[ERR]dup sample ID ', sampleID, "\n")
		else:
			sample_uniq[sampleID] = 1

		sequenced = 0
		if sampleID in data_clean_obj:
			sequenced = 1

		# attribute for field
		department = m[3]
		province = m[4]
		district = m[5]
		locality = m[6]
		lat = m[10]
		lng = m[11]
		alt = m[12]
		fid = (m[3].replace(" ", "")+m[4].replace(" ", "")+m[5].replace(" ", "")+m[6].replace(" ", "")) 
		
		fsize = ''
		fimgs_exist = []
		fimgs = m[0].split("/")
		for fname in fimgs:
			fpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/images/" + prefix + "/" + fname
			if os.path.exists(fpath):
				fimgs_exist.append(fname)

		#test
		pcr_759_760	= m[13]
		biovar = m[14]
		pcr_nmult = m[15]
		phylotype = m[16]
		sequevar = m[17]
		ncbi_acc = m[18]
		

		if fid not in data_obj.keys():
			data_obj[fid] = {}
			data_obj[fid]['attr'] = [department,province, district, locality, lat, lng, alt]
			data_obj[fid]['samp'] = []
			data_obj[fid]['test'] = []
			data_obj[fid]['test'].append([sampleID, fid, pcr_759_760, biovar, pcr_nmult, phylotype, sequevar, ncbi_acc])
			data_obj[fid]['samp'].append([sampleID, fid, isolate, sdate, shost, scultivar, sequenced])
		else:
			data_obj[fid]['test'].append([sampleID, fid, pcr_759_760, biovar, pcr_nmult, phylotype, sequevar, ncbi_acc])
			data_obj[fid]['samp'].append([sampleID, fid, isolate, sdate, shost, scultivar, sequenced])
	
	#db.close()

	return data_obj
	
