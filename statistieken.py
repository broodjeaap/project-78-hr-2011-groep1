import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from gaesessions import get_current_session
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import memcache
import datetime
import webpages
class Statistiek(webapp.RequestHandler):
    def get(self):
	    
		session = get_current_session()
		self.response.out.write(webpages.header(session))
		self.response.out.write("<script type='text/javascript' src='https://www.google.com/jsapi'></script> <script type='text/javascript'>")
		self.response.out.write("google.load('visualization', '1', {packages:['corechart']});")
		self.response.out.write("google.setOnLoadCallback(drawChart); function drawChart() {")
		self.response.out.write("var data = new google.visualization.DataTable();")
		self.response.out.write("data.addColumn('string', 'Geslacht');")
		self.response.out.write("data.addColumn('number', 'Aantal');")
		self.response.out.write("data.addRows([")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE woonplaats='Gouda'")
		woonplaats = str(result.count())
		self.response.out.write("['Gouda', "+woonplaats+"],")  
		result = db.GqlQuery("SELECT * FROM Leerling WHERE woonplaats='Reeuwijk'")
		woonplaats = str(result.count())
		self.response.out.write("['Reeuwijk', "+woonplaats+"],")  
		result = db.GqlQuery("SELECT * FROM Leerling WHERE woonplaats='Stolwijk'")
		woonplaats = str(result.count())
		self.response.out.write("['Stolwijk', "+woonplaats+"]")  
		self.response.out.write("]);")
		self.response.out.write("var options = {")
		self.response.out.write("width: 450, height: 300,")
		self.response.out.write("title: 'Woonplaats leerlingen',")
		self.response.out.write("backgroundColor: { fill:'transparent' }")
		self.response.out.write("};")
		self.response.out.write("var chart = new google.visualization.PieChart(document.getElementById('woonplaats'));")
		self.response.out.write("chart.draw(data, options); } </script>")
		
		self.response.out.write("<script type='text/javascript' src='https://www.google.com/jsapi'></script> <script type='text/javascript'>")
		self.response.out.write("google.load('visualization', '1', {packages:['corechart']});")
		self.response.out.write("google.setOnLoadCallback(drawChart); function drawChart() {")
		self.response.out.write("var data = new google.visualization.DataTable();")
		self.response.out.write("data.addColumn('string', 'Geslacht');")
		self.response.out.write("data.addColumn('number', 'Aantal');")
		self.response.out.write("data.addRows([")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE geslacht='M'")
		aantalM = str(result.count())
		self.response.out.write("['Jongens', "+aantalM+"],")  
		result = db.GqlQuery("SELECT * FROM Leerling WHERE geslacht='V'")
		aantalV = str(result.count())
		self.response.out.write("['Meisjes', "+aantalV+"]")
		self.response.out.write("]);")
		self.response.out.write("var options = {")
		self.response.out.write("width: 450, height: 300,")
		self.response.out.write("title: 'Percentage geslacht J/M',")
		self.response.out.write("backgroundColor: { fill:'transparent' }")
		self.response.out.write("};")
		self.response.out.write("var chart = new google.visualization.PieChart(document.getElementById('geslachtJM'));")
		self.response.out.write("chart.draw(data, options); } </script>")
		
		self.response.out.write("<script type='text/javascript' src='https://www.google.com/jsapi'></script> <script type='text/javascript'>")
		self.response.out.write("google.load('visualization', '1', {packages:['corechart']});")
		self.response.out.write("google.setOnLoadCallback(drawChart); function drawChart() {")
		self.response.out.write("var data = new google.visualization.DataTable();")
		self.response.out.write("data.addColumn('string', 'Klas');")
		self.response.out.write("data.addColumn('number', 'Aantal Leerlingen');")
		self.response.out.write("data.addRows([")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1M1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['1M1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1M2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['1M2', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1M3'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['1M3', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2M1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['2M1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2M2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['2M2', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2M3'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['2M3', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2M4'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['2M4', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3M1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['3M1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3M2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['3M2', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3M3'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['3M3', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4M1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['4M1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4M2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['4M2', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4M3'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['4M3', "+aantalLeerlingen+"]")
		self.response.out.write("]);")
		self.response.out.write("var options = {")
		self.response.out.write("width: 800, height: 300, hAxis: {title: 'Klas', titleTextStyle: {color: 'red'}},")
		self.response.out.write("title: 'Aantal leerlingen per MAVO klas',")
		self.response.out.write("backgroundColor: { fill:'transparent' }")
		self.response.out.write("};")
		self.response.out.write("var chart = new google.visualization.ColumnChart(document.getElementById('aantalLeerlingenPerKlasMAVO'));")
		self.response.out.write("chart.draw(data, options); } </script>")
		
		self.response.out.write("<script type='text/javascript' src='https://www.google.com/jsapi'></script> <script type='text/javascript'>")
		self.response.out.write("google.load('visualization', '1', {packages:['corechart']});")
		self.response.out.write("google.setOnLoadCallback(drawChart); function drawChart() {")
		self.response.out.write("var data = new google.visualization.DataTable();")
		self.response.out.write("data.addColumn('string', 'Klas');")
		self.response.out.write("data.addColumn('number', 'Aantal Leerlingen');")
		self.response.out.write("data.addRows([")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1H1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['1H1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1H2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['1H2', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2H1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['2H1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2H2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['2H2', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2H3'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['2H3', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3H1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['3H1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3H2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['3H2', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3H3'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['3H3', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4H1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['4H1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4H2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['4H2', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='5H1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['5H1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='5H2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['5H2', "+aantalLeerlingen+"]")
		self.response.out.write("]);")
		self.response.out.write("var options = {")
		self.response.out.write("width: 800, height: 300, hAxis: {title: 'Klas', titleTextStyle: {color: 'red'}},")
		self.response.out.write("title: 'Aantal leerlingen per HAVO klas',")
		self.response.out.write("backgroundColor: { fill:'transparent' }")
		self.response.out.write("};")
		self.response.out.write("var chart = new google.visualization.ColumnChart(document.getElementById('aantalLeerlingenPerKlasHAVO'));")
		self.response.out.write("chart.draw(data, options); } </script>")
		
		self.response.out.write("<script type='text/javascript' src='https://www.google.com/jsapi'></script> <script type='text/javascript'>")
		self.response.out.write("google.load('visualization', '1', {packages:['corechart']});")
		self.response.out.write("google.setOnLoadCallback(drawChart); function drawChart() {")
		self.response.out.write("var data = new google.visualization.DataTable();")
		self.response.out.write("data.addColumn('string', 'Klas');")
		self.response.out.write("data.addColumn('number', 'Aantal Leerlingen');")
		self.response.out.write("data.addRows([")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1V1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['1V1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1V2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['1V2', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2V1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['2V1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2V2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['2V2', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2V2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['2V3', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3V1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['3V1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3V2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['3V2', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4V1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['4V1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4V2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['4V2', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='5V1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['5V1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='5V2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['5V2', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='6V1'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['6V1', "+aantalLeerlingen+"],")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='6V2'")
		aantalLeerlingen = str(result.count())
		self.response.out.write("['6V2', "+aantalLeerlingen+"]")
		self.response.out.write("]);")
		self.response.out.write("var options = {")
		self.response.out.write("width: 800, height: 300, hAxis: {title: 'Klas', titleTextStyle: {color: 'red'}},")
		self.response.out.write("title: 'Aantal leerlingen per jaargang',")
		self.response.out.write("backgroundColor: { fill:'transparent' }")
		self.response.out.write("};")
		self.response.out.write("var chart = new google.visualization.ColumnChart(document.getElementById('aantalLeerlingenPerKlasVWO'));")
		self.response.out.write("chart.draw(data, options); } </script>")
		
		self.response.out.write("<script type='text/javascript' src='https://www.google.com/jsapi'></script> <script type='text/javascript'>")
		self.response.out.write("google.load('visualization', '1', {packages:['corechart']});")
		self.response.out.write("google.setOnLoadCallback(drawChart); function drawChart() {")
		self.response.out.write("var data = new google.visualization.DataTable();")
		self.response.out.write("data.addColumn('string', 'Klas');")
		self.response.out.write("data.addColumn('number', 'Aantal Leerlingen');")
		self.response.out.write("data.addRows([")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1B1'")
		aantalLeerlingen = result.count()
		tempCount = aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1B2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1B3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1V1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1V2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1H1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1H2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1M1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1M2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1M3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		strTempCount = str(tempCount)
		self.response.out.write("['Jaar 1', "+strTempCount+"],")
		tempCount = '0'
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2V1'")
		aantalLeerlingen = result.count()
		tempCount = aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2V2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2V3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2H1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2H2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2H3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2M1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2M2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2M3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2M4'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		strTempCount = str(tempCount)
		self.response.out.write("['Jaar 2', "+strTempCount+"],")
		tempCount = '0'
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3V1'")
		aantalLeerlingen = result.count()
		tempCount = aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3V2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3H1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3H2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3H3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3M1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3M2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3M3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		strTempCount = str(tempCount)
		self.response.out.write("['Jaar 3', "+strTempCount+"],")
		tempCount = '0'
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4V1'")
		aantalLeerlingen = result.count()
		tempCount = aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4V2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4H1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4H2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4M1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4M2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4M3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		strTempCount = str(tempCount)
		self.response.out.write("['Jaar 4', "+strTempCount+"],")
		tempCount = '0'
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='5V1'")
		aantalLeerlingen = result.count()
		tempCount = aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='5V2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='5H1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='5H2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		strTempCount = str(tempCount)
		self.response.out.write("['Jaar 5', "+strTempCount+"],")
		tempCount = '0'
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='6V1'")
		aantalLeerlingen = result.count()
		tempCount = aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='6V2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		strTempCount = str(tempCount)
		self.response.out.write("['Jaar 6', "+strTempCount+"],")
		tempCount = '0'
		self.response.out.write("]);")
		self.response.out.write("var options = {")
		self.response.out.write("width: 800, height: 300, hAxis: {title: 'Klas', titleTextStyle: {color: 'red'}},")
		self.response.out.write("title: 'Aantal leerlingen per VWO klas',")
		self.response.out.write("backgroundColor: { fill:'transparent' }")
		self.response.out.write("};")
		self.response.out.write("var chart = new google.visualization.ColumnChart(document.getElementById('aantalLeerlingenPerJaar'));")
		self.response.out.write("chart.draw(data, options); } </script>")
		
		self.response.out.write("<script type='text/javascript' src='https://www.google.com/jsapi'></script> <script type='text/javascript'>")
		self.response.out.write("google.load('visualization', '1', {packages:['corechart']});")
		self.response.out.write("google.setOnLoadCallback(drawChart); function drawChart() {")
		self.response.out.write("var data = new google.visualization.DataTable();")
		self.response.out.write("data.addColumn('string', 'Geslacht');")
		self.response.out.write("data.addColumn('number', 'Aantal');")
		self.response.out.write("data.addRows([")
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1M1'")
		aantalLeerlingen = result.count()
		tempCount = aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1M2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1M3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2M1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2M2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2M3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2M4'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3M1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3M2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3M3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4M1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4M2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4M3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		strTempCount = str(tempCount)
		self.response.out.write("['MAVO', "+strTempCount+"],")
		tempCount='0'
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1H1'")
		aantalLeerlingen = result.count()
		tempCount = aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1H2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2H1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2H3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3H1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3H2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3H3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4H1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4H2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='5H1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='5H2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		strTempCount = str(tempCount)
		self.response.out.write("['HAVO', "+strTempCount+"],")
		tempCount='0'
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1V1'")
		aantalLeerlingen = result.count()
		tempCount = aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='1V2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2V1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2V2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='2V3'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3V1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='3V2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4V1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='4V2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='5V1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='5V2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='6V1'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		result = db.GqlQuery("SELECT * FROM Leerling WHERE klas='6V2'")
		aantalLeerlingen = result.count()
		tempCount = tempCount+aantalLeerlingen
		strTempCount = str(tempCount)
		self.response.out.write("['VWO', "+strTempCount+"],")
		self.response.out.write("]);")
		self.response.out.write("var options = {")
		self.response.out.write("width: 450, height: 300,")
		self.response.out.write("title: 'Percentage leerlingen per niveau',")
		self.response.out.write("backgroundColor: { fill:'transparent' }")
		self.response.out.write("};")
		self.response.out.write("var chart = new google.visualization.PieChart(document.getElementById('percentageLeerlingenPerNiveau'));")
		self.response.out.write("chart.draw(data, options); } </script>")
		
		self.response.out.write("<body>")
		self.response.out.write("<div id='woonplaats'></div>")
		self.response.out.write("<div id='geslachtJM'></div>")
		self.response.out.write("<div id='aantalLeerlingenPerJaar'></div>")
		self.response.out.write("<div id='aantalLeerlingenPerNiveau'></div>")
		self.response.out.write("<div id='aantalLeerlingenPerKlasMAVO'></div>")
		self.response.out.write("<div id='aantalLeerlingenPerKlasHAVO'></div>")
		self.response.out.write("<div id='aantalLeerlingenPerKlasVWO'></div>")
		self.response.out.write("<div id='percentageLeerlingenPerNiveau'></div>")
		self.response.out.write("</body>")
		self.response.out.write(webpages.footer())
        
def main():
    application = webapp.WSGIApplication([('/statistieken', Statistiek)],
                                            debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()