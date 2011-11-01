# -*- coding: latin-1 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from gaesessions import get_current_session
import datetime
import entities
import htmlHelper
import webpages
import inputFunctions

class InsertRoot(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        self.response.out.write(htmlHelper.insertRootLink("Afspraak"))
        self.response.out.write(htmlHelper.insertRootLink("Docent"))
        self.response.out.write(htmlHelper.insertRootLink("Vak"))
        self.response.out.write(htmlHelper.insertRootLink("VakPerKlas"))
        self.response.out.write(htmlHelper.insertRootLink("Leerling"))
        self.response.out.write(htmlHelper.insertRootLink("beheerder"))
        self.response.out.write(webpages.footer())

class InsertAfspraak(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        afspraken = entities.Afspraak.all()
        if(afspraken.count() == 0):
            inputFunctions.insertAfspraak()
            self.response.out.write('Afspraken toegevoegd aan de datastore')
        else:
            self.response.out.write(htmlHelper.startTable(header=['leerlingID','DocentID','dag','Tijd','Tafelnummer','beschrijving']))
            for afspraak in afspraken:
                self.response.out.write("<tr>")
                self.response.out.write(htmlHelper.cell(afspraak.leerlingID))
                self.response.out.write(htmlHelper.cell(afspraak.docentID))
                self.response.out.write(htmlHelper.cell(afspraak.dag))
                self.response.out.write(htmlHelper.cell(afspraak.tijd))
                self.response.out.write(htmlHelper.cell(afspraak.tafelnummer))
                self.response.out.write(htmlHelper.cell(afspraak.beschrijving))
                self.response.out.write("</tr>")
            self.response.out.write("</table>")
            self.response.out.write("<form action='/insert/afspraakpost' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete All' /></form")
            self.response.out.write(webpages.footer())

class InsertDocent(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        docenten = entities.Docent.all()
        if(docenten.count() == 0):
            inputFunctions.insertDocent()
            self.response.out.write('Docenten toegevoegd aan de datastore')
        else:
            self.response.out.write(htmlHelper.startTable(header=['docentID','Aanhef','Naam','Postvaknummer','email', 'wachtwoord']))
            for docent in docenten:
                self.response.out.write("<tr>")
                self.response.out.write(htmlHelper.cell(docent.docentID))
                self.response.out.write(htmlHelper.cell(docent.aanhef))
                self.response.out.write(htmlHelper.cell(docent.naam))
                self.response.out.write(htmlHelper.cell(str(docent.postvaknummer)))
                self.response.out.write(htmlHelper.cell(docent.email))
                self.response.out.write(htmlHelper.cell(docent.wachtwoord))
                self.response.out.write("</tr>")
            self.response.out.write("</table>")
            self.response.out.write("<form action='/insert/docentpost' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete All' /></form")
        self.response.out.write(webpages.footer())

class InsertVak(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        vakken = entities.Vak.all()
        if(vakken.count() == 0):
            inputFunctions.insertVak()
            self.response.out.write('Vakken toegevoegd aan de datastore')
        else:
            self.response.out.write(htmlHelper.startTable(header=['VakCode','VakNaam']))
            for vak in vakken:
                self.response.out.write("<tr>")
                self.response.out.write(htmlHelper.cell(vak.vakCode))
                self.response.out.write(htmlHelper.cell(vak.vakNaam))
                self.response.out.write("</tr>")
            self.response.out.write("</table>")
            self.response.out.write("<form action='/insert/vakpost' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete All' /></form")
        self.response.out.write(webpages.footer())

class InsertVakPerKlas(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        vakken = entities.VakPerKlas.all()
        if(vakken.count() == 0):
            inputFunctions.insertVakPerKlas()
            self.response.out.write('Vakken per klas toegevoegd aan de datastore')
        else:
            self.response.out.write(htmlHelper.startTable(header=['Jaargang','Klas','VakCode','docentID']))
            for vak in vakken:
                self.response.out.write("<tr>")
                self.response.out.write(htmlHelper.cell(vak.jaargang))
                self.response.out.write(htmlHelper.cell(vak.klas))
                self.response.out.write(htmlHelper.cell(vak.vakCode))
                self.response.out.write(htmlHelper.cell(vak.docentID))
                self.response.out.write("</tr>")
            self.response.out.write("</table>")
            self.response.out.write("<form action='/insert/vakpost' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete All' /></form")
        self.response.out.write(webpages.footer())

class InsertBeheerder(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        beheerders = entities.Beheerder.all()
        if(beheerders.count() == 0):
            inputFunctions.insertBeheerder()
            self.response.out.write('Beheerders toegevoegd aan de datastore')
        else:
            self.response.out.write(htmlHelper.startTable(header=['Login','beschrijving','wachtwoord','securityLevel']))
            for beheerder in beheerders:
                self.response.out.write("<tr>")
                self.response.out.write(htmlHelper.cell(beheerder.login))
                self.response.out.write(htmlHelper.cell(beheerder.beschrijving))
                self.response.out.write(htmlHelper.cell(beheerder.wachtwoord))
                self.response.out.write(htmlHelper.cell(beheerder.securityLevel))
                self.response.out.write("</tr>")
            self.response.out.write("</table>")
            self.response.out.write("<form action='/insert/beheerderpost' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete All' /></form")
        self.response.out.write(webpages.footer())
        
class InsertLeerling(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        leerlingen = entities.Leerling.all()
        if(leerlingen.count() == 0):
            inputFunctions.insertLeerling()
            self.response.out.write('Leerlingen toegevoegd aan de datastore')
        else:
            tableData = []
            for leerling in leerlingen:
                tableRow = []
                tableRow.append(leerling.leerlingID)
                tableRow.append(leerling.voornaam)
                tableRow.append(leerling.tussenvoegsel)
                tableRow.append(leerling.achternaam)
                tableRow.append(leerling.geslacht)
                tableRow.append(leerling.klas)
                tableRow.append(leerling.aanhefVerzorger)
                tableRow.append(leerling.initialenVerzorger)
                tableRow.append(leerling.voorvoegselsVerzorger)
                tableRow.append(leerling.achternaamVerzorger)
                tableRow.append(leerling.rolVerzorger)
                tableRow.append(leerling.adres)
                tableRow.append(leerling.huisnummer)
                tableRow.append(leerling.woonplaats)
                tableRow.append(leerling.postcode)
                tableRow.append(leerling.mobielnummer)
                tableRow.append(leerling.vastnummer)
                tableRow.append(leerling.email)
                tableData.append(tableRow)
            
            headRow = ["LeerlingID", "Voornaam", "Tussenvoegsel", "Achternaam", "Geslacht", "Klas", "aanhefVerzorger", "initialenVerzorger", "voorvoegselsVerzorger", "achternaamVerzorger", "rolVerzorger", "adres", "huisnummer", "woonplaats", "postcode", "mobielnummer", "vastnummer", "email"]
            self.response.out.write(htmlHelper.table(data=tableData,attributes="border='1'",head=headRow,title="Leerlingen"))
            self.response.out.write("<form action='/insert/leerlingpost' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete All' /></form")
        self.response.out.write(webpages.footer())


class PostAfspraak(webapp.RequestHandler):
    def post(self):
        if(self.request.get('delete') == 'delete'):
            afspraken = db.GqlQuery("SELECT * FROM Afspraak")
            for afspraak in afspraken:
                afspraak.delete()
            session = get_current_session()
            self.response.out.write(webpages.header(session))
            self.response.out.write("<p>Deleted all entries <a href='/insert/afspraak'>terug (insert nieuwe data)</a></p></body></html>")
            self.response.out.write(webpages.footer())

class PostDocent(webapp.RequestHandler):
    def post(self):
        if(self.request.get('delete') == 'delete'):
            docenten = db.GqlQuery("SELECT * FROM Docent")
            for docent in docenten:
                docent.delete()
            session = get_current_session()
            self.response.out.write(webpages.header(session))
            self.response.out.write("<p>Deleted all entries <a href='/insert/docent'>terug (insert nieuwe data)</a></p></body></html>")
            self.response.out.write(webpages.footer())

class PostVak(webapp.RequestHandler):
    def post(self):
        if(self.request.get('delete') == 'delete'):
            vakken = db.GqlQuery("SELECT * FROM Vak")
            for vak in vakken:
                vak.delete()
            session = get_current_session()
            self.response.out.write(webpages.header(session))
            self.response.out.write("<p>Deleted all entries <a href='/insert/vak'>terug (insert nieuwe data)</a></p></body></html>")
            self.response.out.write(webpages.footer())

class PostVakPerKlas(webapp.RequestHandler):
    def post(self):
        if(self.request.get('delete') == 'delete'):
            vakken = db.GqlQuery("SELECT * FROM VakPerKlas")
            for vak in vakken:
                vak.delete()
            session = get_current_session()
            self.response.out.write(webpages.header(session))
            self.response.out.write("<p>Deleted all entries <a href='/insert/vakperklas'>terug (insert nieuwe data)</a></p></body></html>")
            self.response.out.write(webpages.footer())
            
class PostLeerling(webapp.RequestHandler):
    def post(self):
        if(self.request.get('delete') == 'delete'):
            leerlingen = db.GqlQuery("SELECT * FROM Leerling")
            for leerling in leerlingen:
                leerling.delete()
            session = get_current_session()
            self.response.out.write(webpages.header(session))
            self.response.out.write("<p>Deleted all entries <a href='/insert/leerling'>terug (insert nieuwe data)</a></p></body></html>")
            self.response.out.write(webpages.footer())

class PostBeheerder(webapp.RequestHandler):
    def post(self):
        if(self.request.get('delete') == 'delete'):
            beheerders = db.GqlQuery("SELECT * FROM Beheerder")
            for beheerder in beheerders:
                beheerder.delete()
            session = get_current_session()
            self.response.out.write(webpages.header(session))
            self.response.out.write("<p>Deleted all entries <a href='/insert/beheerder'>terug (insert nieuwe data)</a></p></body></html>")
            self.response.out.write(webpages.footer())

def main():
    application = webapp.WSGIApplication([('/insert/afspraak', InsertAfspraak), 
                                          ('/insert/afspraakpost', PostAfspraak),
                                          ('/insert/docent', InsertDocent),
                                          ('/insert/docentpost', PostDocent),
                                          ('/insert/vak', InsertVak),
                                          ('/insert/vakpost', PostVak),
                                          ('/insert/vakperklas', InsertVakPerKlas),
                                          ('/insert/vakperklaspost', PostVakPerKlas),
                                          ('/insert/leerling', InsertLeerling),
                                          ('/insert/leerlingpost', PostLeerling),
                                          ('/insert/beheerder', InsertBeheerder),
                                          ('/insert/beheerderpost', PostBeheerder),
                                          ('/insert', InsertRoot)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
