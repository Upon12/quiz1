import os
import re
import shutil
import csv
import sys
import pyodbc
from io import BytesIO
# from turtle import title, width
from flask import Flask,render_template, url_for, flash, redirect, request
# from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileRequired, FileAllowed
# from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_bootstrap import Bootstrap
# from wtforms import StringField, IntegerField, SubmitField, SelectField
# from wtforms.validators import DataRequired
from PIL import Image

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'wzg'

# ROUTES!
@app.route('/')
def part10():
	cnxn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:wzgserver.database.windows.net,1433;Database=wzgdb;Uid=wzg;Pwd={zg123456!};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
	cursor = cnxn.cursor()
	cursor.execute("select count(*) as quakes from nquakes")
	quake = cursor.fetchone() #row[0],
	cursor.execute("SELECT * from nquakes where mag = (SELECT MAX(mag) from nquakes)")
	large = cursor.fetchone() #row[0],
	cursor.execute("SELECT * from nquakes where mag = (SELECT min(mag) from nquakes)")
	small = cursor.fetchone() #row[0],
	q=''+str(quake[0])
	l=''+str(large[7])+'          '+str(large[6])
	s=''+str(small[7])+'          '+str(small[6])

	return render_template('part10.html',quakes=q,largest=l,smallest=s,part10_active="active",title="Part 10")

@app.route('/part11')
def part11():
	if request.method=='GET':
		return render_template('part11.html',part11_active = "active",title="Part 11")
	if request.method=='POST':
		low = request.form["low"]
		high = request.form["high"]
		n = request.form["n"]
		cnxn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:wzgserver.database.windows.net,1433;Database=wzgdb;Uid=wzg;Pwd={zg123456!};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
		cursor = cnxn.cursor()
		dat=[]
		for i in range(n):
			high=low+(high-low)/i
			cursor.execute("select count(*) as quakes from nquakes where mag >=? and mag <?",low,high)
			r = cursor.fetchone()
			cursor.execute("select * as quakes from nquakes where mag=(select max(mag) from  nquakes where mag >=? and mag <? ) ",low,high)
			row = cursor.fetchone()
			d={
				'patten':i+1,
				'quakes':r[0],
				'time':row[0],
				'location':row[7]
			}
			dat.append(d)
		
	return render_template('part11.html',data=dat,part11_active = "active",title="Part 11")

@app.route('/part12',methods=['GET','POST'])
def part12():
	if request.method=='GET':
		return render_template('part12.html',part12_active = "active",title="Part 12")
	if request.method=='POST':
		name = request.form["name"]
		cnxn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:wzgserver.database.windows.net,1433;Database=wzgdb;Uid=wzg;Pwd={zg123456!};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
		cursor = cnxn.cursor()
		cursor.execute("select Name,Keywords,Picture from quiz0data where Name=?",name)
		row = cursor.fetchone()
		if row is not None:
			return render_template('part12.html',part12_active = "active",data = {
				'name':row[0],
				'keywords':row[1],
				'picture':row[2]
			})
		else:
			return render_template('part12.html',part12_active = "active",information="no information or picture available",title="Part 12")

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
	return render_template('404.html',title='404')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
	return render_template('500.html',title='500')


if __name__ == '__main__':
	app.run()