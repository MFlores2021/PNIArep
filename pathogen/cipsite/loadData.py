#!/usr/bin/python
# -*- coding: utf-8 -*-

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

def p_summary():
	db = MySQLdb.connect(host="db",   user="root", passwd="<d4+484s3>",  db="dbpnia", charset='utf8mb4')
	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# execute SQL query using execute() method.
	cursor.execute("SELECT department,COUNT(*) FROM `phytoptora` GROUP BY department")
	#cursor.execute("SELECT * from phytoptora")
	adh = cursor.fetchall()

	# disconnect from server
	db.close()

	data_obj = {}

	for m in adh:
		sid = m[0] #.upper()
		value = m[1]
		data_obj[sid] = {}
		data_obj[sid] = value

	return data_obj

#phytoptora

def pload_data_samplefield():
	db = MySQLdb.connect(host="db",   user="root", passwd="<d4+484s3>",  db="dbpnia", charset='utf8mb4')
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
	
	for m in adh:

		# attribute for sample
		sampleID = m[5]
		isolateID = m[2]
		prefix = sampleID[0:2]
		fta = m[3]
		nofta = m[4]
		shost = m[7]  #host
		svariety = m[6]  #variety
		srace = m[19]
		srack = m[42]
		sbox = m[43]
		sgrid = m[44]
		svials = m[45]
		scollector = m[20]
		sdatecollection = m[21]
		sdate = m[6]

		# if len(sdate.split("/")) == 3 :
		# 	syear = sdate.split("/")[2]
		# else:
		# 	syear = "Unknown"
		syear = sdate
		sobservation = m[28]

		# if sampleID in sample_uniq.keys():
		# 	sys.stderr.write('[ERR]dup sample ID ', sampleID, "\n")
		# else:
		sample_uniq[sampleID] = 1

		sequenced = 0
		if sampleID in data_clean_obj:
			sequenced = 1
		
		# attribute for field
		# department =  to_unicode_or_bust(m[7])
		department = m[8]
		province = m[9]
		district = m[10]
		latitude = m[13]
		longitude = m[14]
		altitude      = m[15]

		locality = m[6]
		fid = (m[8].replace(" ", "")+m[9].replace(" ", "")+m[10].replace(" ", "")) 
		#fid = (m[7].replace(" ", "")+m[8].replace(" ", "")+m[9].replace(" ", "")+m[10].replace(" ", ""))  #m[3]

		#test
		pesticides = m[15]
		matingtype  = m[16]
		rflp  = m[22]
		aflp  = m[23]
		haplotypes  = m[17]
		metalaxyl  = m[18]
		genotypic  = m[20]
		clonal  = m[21]
		pepacetate  = m[26]
		peppage   = m[27]
		

		if fid not in data_obj.keys():
			data_obj[fid] = {}
			data_obj[fid]['attr'] = [isolateID,department, province, district, locality, latitude, longitude, altitude]
			data_obj[fid]['samp'] = []
			data_obj[fid]['sampl'] = []
			data_obj[fid]['test'] = []
			data_obj[fid]['test'].append([sampleID, isolateID, fid, matingtype, sdate, shost,  haplotypes, srace  , genotypic , clonal ,  peppage, metalaxyl, sobservation ])
			data_obj[fid]['sampl'].append([sampleID, shost, sdate, srace, genotypic , clonal ])
			data_obj[fid]['samp'].append([sampleID, isolateID, (isolateID), fid, sdate, shost, svariety, srace, srack, sbox, sgrid, svials, scollector, sdatecollection, sdate,sequenced])
		else:
			#data_obj[fid]['samp'] = []
			#data_obj[fid]['sampl'] = []
			data_obj[fid]['test'].append([sampleID, isolateID, fid, matingtype, sdate, shost,  haplotypes, srace  , genotypic , clonal ,  peppage, metalaxyl, sobservation ])
			data_obj[fid]['sampl'].append([sampleID, shost, sdate, srace, genotypic , clonal  ])
			data_obj[fid]['samp'].append([sampleID, isolateID, (isolateID), fid, sdate, shost, svariety, srace, srack, sbox, sgrid, svials, scollector, sdatecollection, sdate,sequenced])
	
	#db.close()

	return data_obj


#Ralstonia:

def load_data_samplefield():
	#datafile = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/data1.txt"

	db = MySQLdb.connect(host="db",   user="root", passwd="<d4+484s3>",  db="dbpnia", charset='utf8mb4')
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
		sampleID = m[5]
		# prefix 	= sampleID[0:2]
		sdate = m[6]
		shost = m[7]

		# if sampleID in sample_uniq.keys():
		# 	sys.stderr.write('[ERR]dup sample ID ', sampleID, "\n")
		# else:
		sample_uniq[sampleID] = 1

		sequenced = 0
		if sampleID in data_clean_obj:
			sequenced = 1

		# attribute for field
		department = m[8]
		province = m[9]
		district = m[10]
		latitude = m[13]
		longitude = m[14]
		altitude      = m[15]
		locality = m[6]
		fid = (m[8].replace(" ", "")+m[9].replace(" ", "")+m[10].replace(" ", "")) 
		
		fsize = ''
		# fimgs_exist = []
		# fimgs = m[0].split("/")
		# for fname in fimgs:
		# 	fpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/images/" + prefix + "/" + fname
		# 	if os.path.exists(fpath):
		# 		fimgs_exist.append(fname)

		#test
		biovar = m[27]
		phylotype = m[28]
		sequevar = m[29]
		ncbi_acc = m[30]
		

		if fid not in data_obj.keys():
			data_obj[fid] = {}
			data_obj[fid]['attr'] = [department,province, district, locality, latitude, longitude, altitude]
			data_obj[fid]['samp'] = []
			data_obj[fid]['test'] = []
			data_obj[fid]['test'].append([sampleID, fid, biovar, phylotype, sequevar, ncbi_acc, sdate, shost, sequenced])
			data_obj[fid]['samp'].append([sampleID, fid, sdate, shost, sequenced])
		else:
			data_obj[fid]['test'].append([sampleID, fid, biovar, phylotype, sequevar, ncbi_acc, sdate, shost, sequenced])
			data_obj[fid]['samp'].append([sampleID, fid, sdate, shost, sequenced])
	
	#db.close()

	return data_obj
	

#Virome:

def vload_data_samplefield():
	db = MySQLdb.connect(host="db",   user="root", passwd="<d4+484s3>",  db="dbpnia", charset='utf8mb4')
	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# execute SQL query using execute() method.
	cursor.execute("SELECT * from virome")

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
		sampleID = m[5]
		isolateID = m[2]
		prefix = sampleID[0:2]
		shost = m[7]  #host
		svariety = m[6]  #variety
		scollector = m[20]
		sdatecollection = m[21]
		sdate = m[6]
		field = m[12]
		# if len(sdate.split("/")) == 3 :
		# 	syear = sdate.split("/")[2]
		# else:
		# 	syear = "Unknown"
		syear = sdate
		sobservation = m[28]

		# if sampleID in sample_uniq.keys():
		# 	sys.stderr.write('[ERR]dup sample ID ', sampleID, "\n")
		# else:
		sample_uniq[sampleID] = 1

		sequenced = 0
		if sampleID in data_clean_obj:
			sequenced = 1
		
		# attribute for field
		# department =  to_unicode_or_bust(m[7])
		department = m[8]
		province = m[9]
		district = m[10]
		latitude = m[13]
		longitude = m[14]
		altitude      = m[15]

		locality = m[11]
		fid = (m[8].replace(" ", "")+m[9].replace(" ", "")+m[10].replace(" ", "")) 

		#test
		cultivarage= m[31]
		phenologic= m[32]
		fieldsize= m[33]
		fieldpict= m[34]
		plantpict= m[35]
		leavepict= m[36]
		intercultivar= m[37]
		cultivar= m[38]
		seedorigin= m[39]
		management= m[40]
		pesticides= m[41]
		commonvirus= m[42]
		newvirus= m[43]
		novelvirus= m[44]
		symptoms= m[45]

		if fid not in data_obj.keys():
			data_obj[fid] = {}
			data_obj[fid]['attr'] = [isolateID,department, province, district, locality, latitude, longitude, altitude]
			data_obj[fid]['samp'] = []
			data_obj[fid]['sampl'] = []
			data_obj[fid]['test'] = []
			data_obj[fid]['test'].append([sampleID,  fid,  sdate, shost, cultivar, cultivarage, phenologic, intercultivar, field, fieldsize, fieldpict, plantpict, leavepict, seedorigin, management, pesticides, commonvirus, newvirus, novelvirus, symptoms ])
			data_obj[fid]['sampl'].append([sampleID, sdate,shost,cultivar,  sequenced  ])
			data_obj[fid]['samp'].append([sampleID, isolateID, (isolateID), fid, sdate, shost, svariety, sequenced])
		else:
			#data_obj[fid]['samp'] = []
			#data_obj[fid]['sampl'] = []
			data_obj[fid]['test'].append([sampleID,  fid,  sdate, shost, cultivar, cultivarage, phenologic, intercultivar, field, fieldsize, fieldpict, plantpict, leavepict, seedorigin, management, pesticides, commonvirus, newvirus, novelvirus, symptoms ])
			data_obj[fid]['sampl'].append([sampleID, sdate, shost,cultivar, sequenced  ])
			data_obj[fid]['samp'].append([sampleID, isolateID, (isolateID), fid, sdate, shost, svariety, sequenced])
	
	#db.close()

	return data_obj



#map


def load_map():
	#datafile = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/../../static/data1.txt"

	db = MySQLdb.connect(host="db",   user="root", passwd="<d4+484s3>",  db="dbpnia", charset='utf8mb4')
	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	cursor1 = db.cursor()
	cursorp = db.cursor()

	# execute SQL query using execute() method.
	cursor.execute("SELECT CIPnumber,latitude, longitude, province from ralstonia")
	cursorp.execute("SELECT CIPnumber,latitude, longitude, province from phytoptora")
	# cursor1.execute("SELECT department,COUNT(*) FROM `ralstonia` GROUP BY department")
	# SELECT CIPnumber,latitude, longitude, province from `ralstonia` union SELECT CIPnumber,latitude, longitude, province FROM `phytoptora` 
	# SELECT department,COUNT(*) FROM `phytoptora` GROUP BY department union SELECT department,COUNT(*) FROM `ralstonia` GROUP BY department
	cursor1.execute("SELECT department,COUNT(*),'phytoptora' FROM `phytoptora` GROUP BY department union SELECT department,COUNT(*),'ralstonia' FROM `ralstonia` GROUP BY department")
	# Fetch a single row using fetchone() method.
	adh = cursor.fetchall()
	adh1 = cursor1.fetchall()
	adhp = cursorp.fetchall()
	# disconnect from server
	db.close()

	# set filter set, only load sample dataset which is cleaned 
	data_clean_obj = load_data_clean();

	# main for load data
	data_obj = {}       # data object for store all data
	sample_uniq = {}    # dict for check the sample uniq

	data_obj["ral"] = {}

	for m in adh:

		province = m[3]
		latitude = m[1]
		longitude = m[2]
		CIPnumber = m[0]
		# if fid not in data_obj.keys():

		data_obj["ral"] [CIPnumber] = {}
		data_obj["ral"] [CIPnumber]['attr'] = [latitude, longitude, province]
		# else:
		# 	data_obj[fid]['test'].append([sampleID, fid, biovar, phylotype, sequevar, ncbi_acc])
		# 	data_obj[fid]['samp'].append([sampleID, fid, sdate, shost, sequenced])

	data_obj["phy"] = {}
	for m in adhp:

		province = m[3]
		latitude = m[1]
		longitude = m[2]
		CIPnumber = m[0]
		# if fid not in data_obj.keys():

		data_obj["phy"] [CIPnumber] = {}
		data_obj["phy"] [CIPnumber]['attr'] = [latitude, longitude, province]


	data_obj["sum"] = {}
	data_obj["sum"]["ralstonia"] = {}
	data_obj["sum"]["phytoptora"] = {}

	for m in adh1:
		sid = m[0] #.upper()
		value = m[1]
		pat = m[2]
		data_obj["sum"][pat][sid] = {}
		data_obj["sum"][pat][sid] = value



	return data_obj
	
