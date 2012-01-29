# -*- coding: latin-1 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from gaesessions import get_current_session
import datetime
import entities
import webpages
import webpages
import inputFunctions

class InsertRoot(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                self.response.out.write(webpages.header(session))
                self.response.out.write(webpages.insertRootLink("Afspraak"))
                self.response.out.write(webpages.insertRootLink("Docent"))
                self.response.out.write(webpages.insertRootLink("Vak"))
                self.response.out.write(webpages.insertRootLink("VakPerKlas"))
                self.response.out.write(webpages.insertRootLink("Leerling"))
                self.response.out.write(webpages.insertRootLink("beheerder"))
                self.response.out.write(webpages.footer())
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')
            
class InsertAfspraak(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                self.response.out.write(webpages.header(session))
                afspraken = entities.Afspraak.all()
                if(afspraken.count() == 0):
                    inputFunctions.insertAfspraak()
                    self.response.out.write('Afspraken toegevoegd aan de datastore')
                else:
                    tableData = []
                    for afspraak in afspraken:
                        tableRow = []
                        tableRow.append(afspraak.leerlingID)
                        tableRow.append(afspraak.docentID)
                        tableRow.append(afspraak.dag)
                        tableRow.append(afspraak.tijd)
                        tableRow.append(afspraak.tafelnummer)
                        tableRow.append(afspraak.beschrijving)
                        tableData.append(tableRow)
                    self.response.out.write(webpages.table(data=tableData, attributes="class='overzichtTable" ,head=['leerlingID','DocentID','dag','Tijd','Tafelnummer','beschrijving'],title="Afspraken",divAttr='overzichtDiv',evenOdd=True))
                    self.response.out.write("<form action='/insert/afspraakpost' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete All' /></form")
                    self.response.out.write(webpages.footer())
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')

class InsertDocent(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                self.response.out.write(webpages.header(session))
                docenten = entities.Docent.all()
                if(docenten.count() == 0):
                    inputFunctions.insertDocent()
                    self.response.out.write('Docenten toegevoegd aan de datastore')
                else:
                    tableData = []
                    for docent in docenten:
                        tableRow = []
                        tableRow.append(docent.docentID)
                        tableRow.append(docent.aanhef)
                        tableRow.append(docent.naam)
                        tableRow.append(docent.postvaknummer)
                        tableRow.append(docent.email)
                        tableRow.append(docent.wachtwoord)
                        tableData.append(tableRow)
                    self.response.out.write(webpages.table(data=tableData, attributes="class='overzichtTable" ,head=['docentID','aanhef','naam','postvaknummer','email','wachtwoord'],title="Docenten",divAttr='overzichtDiv',evenOdd=True))
                    self.response.out.write("<form action='/insert/docentpost' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete All' /></form")
                self.response.out.write(webpages.footer())
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')

class InsertVak(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                self.response.out.write(webpages.header(session))
                vakken = entities.Vak.all()
                if(vakken.count() == 0):
                    inputFunctions.insertVak()
                    self.response.out.write('Vakken toegevoegd aan de datastore')
                else:
                    tableData = []
                    for vak in vakken:
                        tableRow = []
                        tableRow.append(vak.vakCode)
                        tableRow.append(vak.vakNaam)
                        tableData.append(tableRow)
                    self.response.out.write(webpages.table(data=tableData, attributes="class='overzichtTable" ,head=['VakCode','VakNaam'],title="Vakken",divAttr='overzichtDiv',evenOdd=True))
                    self.response.out.write("<form action='/insert/vakpost' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete All' /></form")
                self.response.out.write(webpages.footer())
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')


class InsertVakPerKlas(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                self.response.out.write(webpages.header(session))
                vakken = entities.VakPerKlas.all()
                if(vakken.count() == 0):
                    inputFunctions.insertVakPerKlas()
                    self.response.out.write('Vakken per klas toegevoegd aan de datastore')
                else:
                    tableData = []
                    for vakPerKlas in vakken:
                        tableRow = []
                        tableRow.append(vakPerKlas.jaargang)
                        tableRow.append(vakPerKlas.klas)
                        tableRow.append(vakPerKlas.vakCode)
                        tableRow.append(vakPerKlas.docentID)
                        tableData.append(tableRow)
                    self.response.out.write(webpages.table(data=tableData, attributes="class='overzichtTable" ,head=['Jaargang','Klas','VakCode','DocentID'],title="Vakken",divAttr='overzichtDiv',evenOdd=True))
                    self.response.out.write("<form action='/insert/vakpost' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete All' /></form")
                self.response.out.write(webpages.footer())
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')


class InsertBeheerder(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                self.response.out.write(webpages.header(session))
                beheerders = entities.Beheerder.all()
                if(beheerders.count() == 0):
                    inputFunctions.insertBeheerder()
                    self.response.out.write('Beheerders toegevoegd aan de datastore')
                else:
                    tableData = []
                    for beheerder in beheerders:
                        tableRow = []
                        tableRow.append(beheerder.login)
                        tableRow.append(beheerder.beschrijving)
                        tableRow.append(beheerder.wachtwoord)
                        tableRow.append(beheerder.securityLevel)
                        tableData.append(tableRow)
                    self.response.out.write(webpages.table(data=tableData, attributes="class='overzichtTable" ,head=['Login','Beschrijving','Wachtwoord','SecurityLevel'],title="Vakken",divAttr='overzichtDiv',evenOdd=True))
                    self.response.out.write("<form action='/insert/beheerderpost' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete All' /></form")
                self.response.out.write(webpages.footer())
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')

class InsertLeerling(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
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
                        tableRow.append(leerling.wachtwoord)
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
                    self.response.out.write(webpages.table(data=tableData, attributes="class='overzichtTable" ,head=['LeerlingID','Wachtwoord','Voornaam','Tussenvoegsel','Achternaam','Geslacht','Klas','AanhefVerzorger','InitialenVerzorger','VoorvoegselsVerzorger','AchternaamVerzorger','RolVerzorger','Adres','Huisnummer','Woonplaats','Postcode','Mobielnummer','Vastnummer','Email'],title="Vakken",divAttr='overzichtDiv',evenOdd=True))
                    self.response.out.write("<form action='/insert/leerlingpost' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete All' /></form")
                self.response.out.write(webpages.footer())
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')

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
            klassen = db.GqlQuery("SELECT * FROM Klas")
            for klas in klassen:
                klas.delete()
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
