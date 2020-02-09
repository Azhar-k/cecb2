import pymysql
import json

#test.hello()



def addForm():
	connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='cecb',
	)
	name = input("Enter name of form: ")
	path = input("Enter path : ")

	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO forms (`name`, `path`) VALUES (%s, %s)"
			try:
				cursor.execute(sql, (name, path))
				print("Form added successfully")
			except:
				print("Oops! Something wrong")

		connection.commit()
	finally:
		connection.close()
def getPlacementRecord(year):
	connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='cecb',
	)
	rec=''
	try:
		with connection.cursor() as cursor:
			sql = "SELECT id,company_name,count FROM placement_statistics where year="+year
			try:
				cursor.execute(sql)
				result = cursor.fetchall()
				#print("Id\t\t name")
				#print("----------------------")
				for row in result:
					temprec={}
					temprec['company']=row[1]
					temprec['number']=str(row[2])
					rec=rec+str(temprec)+','					
					#print(str(row[0]) + "\t\t" + row[1] + "\t\t\t\t\t" + str(row[2]))
			except Exception as e:
				#print("Oops! Something wrong")
				print(e)
		connection.commit()
	finally:
		connection.close()
	recStr=str(rec)
	recStr=recStr.replace("\'", "\"")
	recStr=recStr[0:len(recStr)-1]	
	return recStr
def getYears():
	connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='cecb',
	)
	years=[]
	try:
		with connection.cursor() as cursor:
			sql = "SELECT distinct year FROM placement_statistics "
			try:
				cursor.execute(sql)
				result = cursor.fetchall()
				#print("Id\t\t name")
				#print("----------------------")
				for row in result:
					years.append(str(row[0]))					
					#print(str(row[0]))
			except Exception as e:
				#print("Oops! Something wrong")
				print(e)
		connection.commit()
	finally:
		connection.close()
	#print(years)	
	return years
#addForm()
#getPlacementRecord()
#getYears()