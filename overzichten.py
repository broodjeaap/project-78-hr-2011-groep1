from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from gaesessions import get_current_session
import htmlHelper
import entities
import webpages

class AfspraakOverzicht(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            self.response.out.write(webpages.header(session))
            afspraken = entities.Afspraak.all()
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
            self.response.out.write(htmlHelper.table(data=tableData, attributes="class='overzichtTable" ,head=['leerlingID','DocentID','dag','Tijd','Tafelnummer','beschrijving'],title="Afspraken",divAttr='overzichtDiv',evenOdd=True))
            self.response.out.write(webpages.footer())
        else:
            self.redirect('/')
            
class DocentOverzicht(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            self.response.out.write(webpages.header(session))
            docenten = entities.Docent.all()
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
            self.response.out.write(htmlHelper.table(data=tableData, attributes="class='overzichtTable" ,head=['docentID','aanhef','naam','postvaknummer','email','wachtwoord'],title="Docenten",divAttr='overzichtDiv',evenOdd=True))
            self.response.out.write(webpages.footer())
        else:
            self.redirect('/')


class VakOverzicht(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            self.response.out.write(webpages.header(session))
            vakken = entities.Vak.all()
            tableData = []
            for vak in vakken:
                tableRow = []
                tableRow.append(vak.vakCode)
                tableRow.append(vak.vakNaam)
                tableData.append(tableRow)
            self.response.out.write(htmlHelper.table(data=tableData, attributes="class='overzichtTable" ,head=['VakCode','VakNaam'],title="Vakken",divAttr='overzichtDiv',evenOdd=True))
            self.response.out.write(webpages.footer())
        else:
            self.redirect('/')
            
class VakPerKlasOverzicht(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            self.response.out.write(webpages.header(session))
            vakkenPerKlas = entities.VakPerKlas.all()
            tableData = []
            for vakPerKlas in vakkenPerKlas:
                tableRow = []
                tableRow.append(vakPerKlas.jaargang)
                tableRow.append(vakPerKlas.klas)
                tableRow.append(vakPerKlas.vakCode)
                tableRow.append(vakPerKlas.docentID)
                tableData.append(tableRow)
            self.response.out.write(htmlHelper.table(data=tableData, attributes="class='overzichtTable" ,head=['Jaargang','Klas','VakCode','DocentID'],title="Vakken",divAttr='overzichtDiv',evenOdd=True))
            self.response.out.write(webpages.footer())
        else:
            self.redirect('/')

class LeerlingOverzicht(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            self.response.out.write(webpages.header(session))
            leerlingen = entities.Leerling.all()
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
            self.response.out.write(htmlHelper.table(data=tableData, attributes="class='overzichtTable" ,head=['LeerlingID','Wachtwoord','Voornaam','Tussenvoegsel','Achternaam','Geslacht','Klas','AanhefVerzorger','InitialenVerzorger','VoorvoegselsVerzorger','AchternaamVerzorger','RolVerzorger','Adres','Huisnummer','Woonplaats','Postcode','Mobielnummer','Vastnummer','Email'],title="Vakken",divAttr='overzichtDiv',evenOdd=True))
            self.response.out.write(webpages.footer())
        else:
            self.redirect('/')

class BeheerderOverzicht(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            self.response.out.write(webpages.header(session))
            beheerders = entities.Beheerder.all()
            tableData = []
            for beheerder in beheerders:
                tableRow = []
                tableRow.append(beheerder.login)
                tableRow.append(beheerder.beschrijving)
                tableRow.append(beheerder.wachtwoord)
                tableRow.append(beheerder.securityLevel)
                tableData.append(tableRow)
            self.response.out.write(htmlHelper.table(data=tableData, attributes="class='overzichtTable" ,head=['Login','Beschrijving','Wachtwoord','SecurityLevel'],title="Vakken",divAttr='overzichtDiv',evenOdd=True))
            self.response.out.write(webpages.footer())
        else:
            self.redirect('/')

class OverzichtenRoot(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            self.response.out.write(webpages.header(session))
            self.response.out.write(htmlHelper.link('/overzichten/afspraak',"Afspraak"))
            self.response.out.write(htmlHelper.link('/overzichten/docent',"Docent"))
            self.response.out.write(htmlHelper.link('/overzichten/vak',"Vak"))
            self.response.out.write(htmlHelper.link('/overzichten/vakperklas',"Vak per klas"))
            self.response.out.write(htmlHelper.link('/overzichten/leerling',"Leerling"))
            self.response.out.write(htmlHelper.link('/overzichten/beheerder',"Beheerder"))
            self.response.out.write(webpages.footer())
        else:
            self.redirect('/')
    
def main():
    application = webapp.WSGIApplication([('/overzichten/afspraak', AfspraakOverzicht),
                                          ('/overzichten/docent', DocentOverzicht),
                                          ('/overzichten/vak', VakOverzicht),
                                          ('/overzichten/vakperklas', VakPerKlasOverzicht),
                                          ('/overzichten/leerling', LeerlingOverzicht),
                                          ('/overzichten/beheerder', BeheerderOverzicht),
                                          ('/overzichten', OverzichtenRoot)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()