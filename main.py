import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from gaesessions import get_current_session
import datetime
import webpages


import htmlHelper
import entities

class Login(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""
        <html>
            <head>
                <title>Ouderavondregistratie inlogscherm</title>
                <link rel="stylesheet" href="/css/global.css"/>
            </head>
            <body>
            <div id="div-0">
                <div id="div-head">
                    <h3>Login - ouderavondregistratie</h3>
                </div>
                <div id="div-1">
                    <div id="header">
                        <div id="photo"><img src="../images/DKC.png"></div>
                        <div id="adres"><p>DONALD KNUTH COLLEGE<br />Scholengemeenschap MAVO/HAVO/VWO<br />Pascalstraat 1<br />2811 EL REEUWIJK<br /></div>
                    </div>
        
                    <div id="div-2">
                        <form action="/authenticate" method="post">
                            <table>""")
        session = get_current_session()
        if(session.has_key('loginError')):
            self.response.out.write("""
                                <tr>
                                    <td style="color:red;" colspan="2" align="center">
                                    Geen geldige combinatie!
                                    </td>
                                </tr>""")
            #session.__delitem__('loginError')
            session.terminate()
        else:
            self.response.out.write('<tr><td colspan="2">&nbsp;</td></tr>')       
        self.response.out.write("""
                                <tr>
                                    <td>Gebruikersnaam</td>
                                    <td align="center">
                                        <input type="text" name="id">
                                    </td>
                                </tr>
                                <tr>
                                    <td>Wachtwoord</td>
                                    <td align="center">
                                        <input type="password" name="wachtwoord">
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>
                                        <input type="submit" value="inloggen">
                                    </td>
                                </tr>
                            </table>
                        </form>
                    </div>
                </div>
            </div> 
            </body>
        </html>
        """)

class Logout(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.has_key('id')):
            session.terminate()
            self.redirect('/')
        else:
            self.redirect('/')

class Authenticate(webapp.RequestHandler):
    def post(self):
        wachtwoord=self.request.get("wachtwoord")
        id=self.request.get("id")
        session = get_current_session()
        if(session.has_key('id')):
            session.terminate()
        
        result = db.GqlQuery("SELECT __key__ FROM Leerling where leerlingID = '"+id+"' and wachtwoord = '"+wachtwoord+"'")
        if(result.count() != 0):
            session.__setitem__('id',id)
            session.__setitem__('loginType','leerling')
            session.__setitem__('key',result[0])
            self.redirect('/leerlingafspraak')
            return
        
        result = db.GqlQuery("SELECT __key__ FROM Docent where docentID = '"+id+"' and wachtwoord = '"+wachtwoord+"'")
        if(result.count() != 0):
            session.__setitem__('id',id)
            session.__setitem__('loginType','docent')
            session.__setitem__('key',result[0])
            self.redirect('/docentafspraak')
            return
        
        result = db.GqlQuery("SELECT __key__ FROM Beheerder where login = '"+id+"' and wachtwoord = '"+wachtwoord+"'")
        if(result.count() != 0):
            session.__setitem__('id',id)
            session.__setitem__('loginType','beheerder')
            session.__setitem__('key',result[0])
            self.redirect('/beheerder')
            return
                
        
        session.__setitem__('loginError','error')
        self.redirect('/')

class OuderAvondPlannen(webapp.RequestHandler):
    def get(self):
        self.response.out.write(webpages.header(homeLink="/leerlingafspraak"))
        self.response.out.write(htmlHelper.planningPage())
        self.response.out.write(webpages.footer())

class OuderAvondPlannenPost(webapp.RequestHandler):
    def post(self):
        self.response.out.write(webpages.header())
        docenten = self.request.get("checkedDocenten").split(",")
        datums = self.request.get("datums").split(",")
        splitDatums = []
        for datum in datums:
            splitDatums.append(datum.split("-"))
            
        afspraken = []
        try:
            for docent in docenten:
                for datum in splitDatums:
                    afspraak = entities.Afspraak(leerlingID="0",docentID=docent,dag=datetime.date(int(datum[0]), int(datum[1]), int(datum[2])), tijd=-1,tafelnummer=0,beschrijving='#')
                    afspraken.append(afspraak)
                    #afspraak.put();
                self.response.out.write(docent+" heeft ouderavond(en) op: <br />")
                for datum in datums:
                    self.response.out.write(datum+" <br />")
                self.response.out.write("<br />")
            for afspraak in afspraken:
                afspraak.put()
        except:
            self.response.out.write("Datums verkeerd ingevoerd...")
        self.response.out.write(webpages.footer())
            
class AfspraakPlanningPost(webapp.RequestHandler):
    def post(self):
        key = self.request.get("afzegkey")
        if(len(key) != 0):
            afspraak = entities.Afspraak.get(key)
            afspraak.delete()
            self.redirect('/leerlingafspraak')
            return
        
        klas = self.request.get("klas")
        session = get_current_session()
        leerlingID = session['id']
        vakken = db.GqlQuery("SELECT * FROM VakPerKlas WHERE klas = '"+klas+"'")
        
        #self.response.out.write("<table border='1'><tr><th>leerlingID</th><th>docentID</th><th>dag</th><th>tijd</th><th>beschrijving</th></tr>")
        for vak in vakken:
            afspraakString = self.request.get(vak.docentID+"_afspraak")
            if(len(afspraakString) != 0):
                beschrijving = self.request.get(vak.docentID+"_hidden_beschrijving")
                afspraakData = afspraakString.split("_")
                
                datumStrings = afspraakData[0].split("-")
                
                afspraak = entities.Afspraak(leerlingID = leerlingID,docentID = vak.docentID,dag= datetime.date(int(datumStrings[0]),int(datumStrings[1]), int(datumStrings[2])),tijd= int(afspraakData[1]),tafelnummer=0,beschrijving = beschrijving)
                afspraak.put()
                self.redirect('/leerlingafspraak')

class DocentAfspraak(webapp.RequestHandler):
    def get(self):
        self.response.out.write(webpages.header())
        session = get_current_session()
        if(session.has_key('id') and session.__getitem__('loginType') == "docent"):
            docent = db.GqlQuery("SELECT * FROM Docent where docentID = '"+session['id']+"'")
            docent = docent[0]
            
            self.response.out.write(webpages.DocentPage(docent))
        else:
            self.response.out.write("U heeft niet de juist rechten om deze pagina te bezoeken")
        self.response.out.write(webpages.footer())

class LeerlingAfspraak(webapp.RequestHandler):
    def get(self):
        self.response.out.write(webpages.header(homeLink="/leerlingafspraak"))
        
        session = get_current_session()
        if(session.has_key('id') and session.__getitem__('loginType') == 'leerling'):
            leerling = db.GqlQuery("SELECT * FROM Leerling where leerlingID = '"+session['id']+"'")
            leerling = leerling[0]
            self.response.out.write(htmlHelper.klasAfspraakPage(klas=leerling.klas,leerlingID=leerling.leerlingID))
        else:
            self.response.out.write("U heeft niet de juist rechten om deze pagina te bezoeken")
        self.response.out.write(webpages.footer())

class AccountSettings(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'leerling'):
            self.response.out.write(webpages.header(homeLink="/leerlingafspraak"))
            self.response.out.write("<div class='leerlingAccount'>")
            leerling = db.get(session.__getitem__('key'))
            tableData = []
            tableRow = []
            tableRow.append("Naam")
            tableRow.append(leerling.voornaam+" "+leerling.tussenvoegsel+" "+leerling.achternaam)
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Geslacht")
            tableRow.append(leerling.geslacht)
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Klas")
            tableRow.append(leerling.klas)
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Naam verzorger/voogd")
            tableRow.append(leerling.aanhefVerzorger+" "+leerling.initialenVerzorger+" "+leerling.voorvoegselsVerzorger+" "+leerling.achternaamVerzorger)
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Rol verzorger/voogd")
            tableRow.append(leerling.rolVerzorger)
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Adres")
            tableRow.append(leerling.adres)
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Huisnummer")
            tableRow.append(leerling.huisnummer)
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Woonplaats")
            tableRow.append(leerling.woonplaats)
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Postcode")
            tableRow.append(leerling.postcode)
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Mobielnummer")
            tableRow.append(leerling.mobielnummer)
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Vastnummer")
            tableRow.append(leerling.vastnummer)
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("E-mail")
            tableRow.append(leerling.email)
            tableData.append(tableRow)
            
            self.response.out.write(htmlHelper.table(tableData,attributes="class='accountTable'",title="<h2>Leerling: "+leerling.leerlingID+"</h2>",divAttr='leerlingAccountGegevens'))
            
            tableData = []
            tableRow = []
            self.response.out.write("<form action='/accountwachtwoordpost' method='post'>")
            tableRow.append("Huidig wachtwoord")
            tableRow.append("<input type='password' id='huidig_password' name='huidig_password' />")
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Nieuwe wachtwoord")
            tableRow.append("<input type='password' id='nieuw_password' name='nieuw_password' />")
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Herhaal wachtwoord")
            tableRow.append("<input type='password' id='herhaal_password' name='herhaal_password' />")
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("<input type='submit' value='Ok' />")
            
            tableData.append(tableRow)
            self.response.out.write(htmlHelper.table(tableData,attributes="class='accountTablePassword'",title="<h3>Wachtwoord veranderen</h3>", divAttr='leerlingAccountWachtwoord'))
            self.response.out.write("</form>")
            self.response.out.write("</div>")
        elif(session.__getitem__('loginType') == 'docent'):
            self.response.out.write(webpages.header(homeLink="/docentafspraak"))
            docent = db.get(session.__getitem__('key'))
            
            
            
        elif(session.__getitem__('loginType') == 'beheerder'):
            self.response.out.write(webpages.header(homeLink="/beheerder"))
            beheerder = db.get(session.__getitem__('key'))
            
            
            
        else:
            self.redirect('/')
        self.response.out.write(webpages.footer())
        
class AccountWachtwoordPost(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        if(session.has_key('id')):
            huidigPassword = self.request.get("huidig_password")
            nieuwPassword = self.request.get("nieuw_password")
            herhaalPassword = self.request.get("herhaal_password")
            persoon = db.get(session.__getitem__('key'))
            if(huidigPassword == persoon.wachtwoord):
                if(nieuwPassword == herhaalPassword):
                   persoon.wachtwoord = nieuwPassword
                   persoon.put()
                   self.response.out.write("Wachtwoord veranderd")
                else:
                    self.response.out.write("Nieuwe wachtwoorden waren niet hetzelfde")
            else:
                self.response.out.write("Verkeerde wachtwoord")
        else:
            self.redirect('/')
    
def main():
    application = webapp.WSGIApplication([('/', Login),
                                          ('/logout', Logout),
                                          ('/authenticate', Authenticate),
                                          ('/afspraakplanningpost', AfspraakPlanningPost),
                                          ('/plannen', OuderAvondPlannen),
                                          ('/leerlingafspraak', LeerlingAfspraak),
                                          ('/docentafspraak', DocentAfspraak),
                                          ('/accountsettings', AccountSettings),
                                          ('/accountwachtwoordpost', AccountWachtwoordPost),
                                          ('/plannenpost', OuderAvondPlannenPost)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
