from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
import datetime
import entities
import htmlHelper

class InsertAfspraak(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        afspraken = db.GqlQuery("SELECT * FROM Afspraak")
        if(afspraken.count() == 0):
            afspraak = entities.Afspraak(leerlingID="1234",klas = 'h3',docent='ABC',tijd=1,dag=datetime.date(2011, 10, 11))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="4523",klas = 'h3',docent='ABC',tijd=4,dag=datetime.date(2011, 10, 11))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="5432",klas = 'h3',docent='ABC',tijd=8,dag=datetime.date(2011, 10, 11))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="3432",klas = 'h3',docent='ABC',tijd=11,dag=datetime.date(2011, 10, 11))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="4532",klas = 'h3',docent='ABC',tijd=11,dag=datetime.date(2011, 10, 12))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="2321",klas = 'h3',docent='ABC',tijd=4,dag=datetime.date(2011, 10, 12))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="3423",klas = 'h3',docent='ABC',tijd=1,dag=datetime.date(2011, 10, 12))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="4321",klas = 'h3',docent='ABC',tijd=1,dag=datetime.date(2011, 10, 13))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="2321",klas = 'h3',docent='ABC',tijd=2,dag=datetime.date(2011, 10, 13))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="2432",klas = 'h3',docent='ABC',tijd=6,dag=datetime.date(2011, 10, 13))
            afspraak.put();
            
            
            afspraak = entities.Afspraak(leerlingID="1234",klas = 'h3',docent='DEF',tijd=0,dag=datetime.date(2011, 10, 11))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="2432",klas = 'h3',docent='DEF',tijd=1,dag=datetime.date(2011, 10, 11))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="2321",klas = 'h3',docent='DEF',tijd=2,dag=datetime.date(2011, 10, 11))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="4321",klas = 'h3',docent='DEF',tijd=3,dag=datetime.date(2011, 10, 11))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="3423",klas = 'h3',docent='DEF',tijd=6,dag=datetime.date(2011, 10, 11))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="4346",klas = 'h3',docent='DEF',tijd=8,dag=datetime.date(2011, 10, 11))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="4532",klas = 'h3',docent='DEF',tijd=8,dag=datetime.date(2011, 10, 12))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="3421",klas = 'h3',docent='DEF',tijd=-1,dag=datetime.date(2011, 10, 13))
            afspraak.put();
            afspraak = entities.Afspraak(leerlingID="6754",klas = 'h3',docent='DEF',tijd=-1,dag=datetime.date(2011, 10, 14))
            afspraak.put();
            
            self.response.out.write('Afspraken toegevoegd aan de datastore')
        else:
            startTime = datetime.time(19,0,0)
            self.response.out.write(htmlHelper.startTable(header=['leerlingID','Klas','Docent','Tijd','Dag']))
            for afspraak in afspraken:
                self.response.out.write("<tr>")
                self.response.out.write("<td>"+str(afspraak.leerlingID)+"</td>")
                self.response.out.write("<td>"+afspraak.klas+"</td>")
                self.response.out.write("<td>"+afspraak.docent+"</td>")
                self.response.out.write("<td>"+str(afspraak.tijd)+"</td>")
                self.response.out.write("<td>"+str(afspraak.dag)+"</td>")
                self.response.out.write("</tr>")
            self.response.out.write("</table>")
            self.response.out.write("<form action='/insert/afspraakpost' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete All' /></form")
                
class PostAfspraak(webapp.RequestHandler):
    def post(self):
        if(self.request.get('delete') == 'delete'):
            afspraken = db.GqlQuery("SELECT * FROM Afspraak")
            for afspraak in afspraken:
                afspraak.delete()
            self.response.out.write("<html><body><p>Deleted all entries</p></body></html>")
            self.redirect("/insert/afspraak")

        
class InsertDocent(webapp.RequestHandler):
    def get(self):
        self.response.out.write("docent")

def main():
    application = webapp.WSGIApplication([('/insert/afspraak', InsertAfspraak), 
                                          ('/insert/afspraakpost', PostAfspraak),
                                          ('/insert/docent', InsertDocent)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
