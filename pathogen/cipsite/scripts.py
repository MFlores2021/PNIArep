import xlrd
import MySQLdb
import os
from django.db import connection
from django.db import IntegrityError

def upload_sql_xlsx(xlsx_file,dbase,uoption):

	if xlsx_file == '':
		return redirect("upload.html")

	if dbase == '':
		return redirect("upload.html")

	if uoption == '':
		return redirect("upload.html")

	f = os.path.exists(xlsx_file)

	if f and allowed_file(xlsx_file):
		# Open the workbook and define the worksheet
		book = xlrd.open_workbook(xlsx_file)
		sheet = book.sheet_by_index(1)


		# Create the INSERT INTO sql query
		if uoption == "upload":
			query = "INSERT INTO " + dbase + " (id, per_code , isolate_code , fta_alive , temporary_code , CIPnumber , datecollection , host , department, province , district , locality , field , latitude , longitude , altitude, matingtype , haplotypes , metalaxyl , race , genotypic_method , clonal_lineage , date_intro , rack , box , grid , vials , biovar , phylotype , sequevar , ncbi_accession , cultivo_age , phenological_state , field_size , pict_field , pict_plant , pict_leaves , intercultivar , cultivar , seed_origin , man_system , pesticides , virus_detected , new_virus , novel_virus , symptoms) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

		elif uoption == "update":
   			query = "UPDATE " + dbase + " SET per_code=%s , isolate_code=%s , fta_alive=%s , temporary_code=%s , datecollection=%s, host=%s , department=%s, province=%s , district=%s , locality=%s , field=%s , latitude=%s , longitude=%s, altitude=%s, matingtype=%s , haplotypes=%s , metalaxyl=%s, race=%s , genotypic_method=%s , clonal_lineage=%s , date_intro=%s , rack=%s , box=%s , grid=%s , vials=%s , biovar=%s , phylotype=%s , sequevar=%s , ncbi_accession=%s , cultivo_age=%s , phenological_state=%s , field_size=%s , pict_field=%s , pict_plant=%s , pict_leaves=%s , intercultivar=%s , cultivar=%s , seed_origin=%s , man_system=%s , pesticides=%s , virus_detected=%s , new_virus=%s , novel_virus=%s , symptoms=%s  WHERE CIPnumber=%s"

   		elif uoption == "delete":
   			query = "DELETE FROM " + dbase + " WHERE CIPnumber = %s"

   		else:
   			print("error")


		with connection.cursor() as cursor:

			# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
			for r in range(1, sheet.nrows):

				id = sheet.cell(r,0).value
				per_code  = sheet.cell(r,1).value
				isolate_code  = sheet.cell(r,2).value
				fta_alive  = sheet.cell(r,3).value
				temporary_code  = sheet.cell(r,4).value
				CIPnumber  = sheet.cell(r,5).value
				datecollection  = sheet.cell(r,6).value
				host  = sheet.cell(r,7).value
				department = sheet.cell(r,8).value
				province  = sheet.cell(r,9).value
				district  = sheet.cell(r,10).value
				locality  = sheet.cell(r,11).value
				field  = sheet.cell(r,12).value
				latitude  = sheet.cell(r,13).value
				longitude  = sheet.cell(r,14).value
				altitude       = sheet.cell(r,15).value
				matingtype  = sheet.cell(r,16).value
				haplotypes  = sheet.cell(r,17).value
				metalaxyl  = sheet.cell(r,18).value
				race  		= sheet.cell(r,19).value
				genotypic_method  = sheet.cell(r,20).value
				clonal_lineage  = sheet.cell(r,21).value
				date_intro  = sheet.cell(r,22).value
				rack  		= sheet.cell(r,23).value
				box  		= sheet.cell(r,24).value
				grid  		= sheet.cell(r,25).value
				vials  	= sheet.cell(r,26).value
				biovar 	 = sheet.cell(r,27).value
				phylotype  = sheet.cell(r,28).value
				sequevar  = sheet.cell(r,29).value
				ncbi_accession  = sheet.cell(r,30).value
				cultivo_age  = sheet.cell(r,31).value
				phenological_state  = sheet.cell(r,32).value
				field_size  = sheet.cell(r,33).value
				pict_field  = sheet.cell(r,34).value
				pict_plant  = sheet.cell(r,35).value
				pict_leaves  = sheet.cell(r,36).value
				intercultivar  = sheet.cell(r,37).value
				cultivar  = sheet.cell(r,38).value
				seed_origin  = sheet.cell(r,39).value
				man_system  = sheet.cell(r,40).value
				pesticides  = sheet.cell(r,41).value
				virus_detected  = sheet.cell(r,42).value
				new_virus  = sheet.cell(r,43).value
				novel_virus  = sheet.cell(r,44).value
				symptoms = sheet.cell(r,45).value

				try:

					if uoption == "upload":
						# Assign values from each row
						values = (id, per_code , isolate_code , fta_alive , temporary_code , CIPnumber , datecollection, host , department, province , district , locality , field , latitude , longitude, altitude, matingtype , haplotypes , metalaxyl , race , genotypic_method , clonal_lineage , date_intro , rack , box , grid , vials , biovar , phylotype , sequevar , ncbi_accession , cultivo_age , phenological_state , field_size , pict_field , pict_plant , pict_leaves , intercultivar , cultivar , seed_origin , man_system , pesticides , virus_detected , new_virus , novel_virus , symptoms)
						# Execute sql Query
						cursor.execute(query, values)
					
					elif uoption == "update":

						values = (per_code , isolate_code , fta_alive , temporary_code , datecollection, host , department, province , district , locality , field , latitude , longitude, altitude, matingtype , haplotypes , metalaxyl , race , genotypic_method , clonal_lineage , date_intro , rack , box , grid , vials , biovar , phylotype , sequevar , ncbi_accession , cultivo_age , phenological_state , field_size , pict_field , pict_plant , pict_leaves , intercultivar , cultivar , seed_origin , man_system , pesticides , virus_detected , new_virus , novel_virus , symptoms, CIPnumber)
						# Execute sql Query
						cursor.execute(query, values)

					elif uoption == "delete":
						# Execute sql Query
						cursor.execute(query, (CIPnumber,))

					else:
						print("Error")

					result = "Operation successfully completed !"

				except (IntegrityError) as error:
					result = error.__cause__

				# Close the cursor
			cursor.close()

		# 		columns = str(sheet.ncols)
		# 		rows = str(sheet.nrows)
		# 		result = rows + " rows were imported to the database!"	

	else:
		result = "Soomething went wrong check your XLSX file "


	return result

#upload_sql_xlsx("towebsitedec2017.xlsx")

ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
