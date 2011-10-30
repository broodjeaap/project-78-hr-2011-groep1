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
            session.__delitem__('loginError')
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
        if(db.GqlQuery("SELECT __key__ FROM Leerling where leerlingID = '"+id+"' and wachtwoord = '"+wachtwoord+"'").count() != 0):
            session.__setitem__('id',id)
            session.__setitem__('loginType','leerling')
            self.redirect('/leerlingafspraak')
        elif(db.GqlQuery("SELECT __key__ FROM Docent where docentID = '"+id+"' and wachtwoord = '"+wachtwoord+"'").count() != 0):
            session.__setitem__('id',id)
            session.__setitem__('loginType','docent')
            self.redirect('/docentafspraak')
        elif(db.GqlQuery("SELECT __key__ FROM Beheerder where login = '"+id+"' and wachtwoord = '"+wachtwoord+"'").count() != 0):
            session.__setitem__('id',id)
            session.__setitem__('loginType','beheerder')
            self.redirect('/beheerder')
        else:
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
        
def main():
    application = webapp.WSGIApplication([('/', Login),
                                          ('/logout', Logout),
                                          ('/authenticate', Authenticate),
                                          ('/afspraakplanningpost', AfspraakPlanningPost),
                                          ('/plannen', OuderAvondPlannen),
                                          ('/leerlingafspraak', LeerlingAfspraak),
                                          ('/docentafspraak', DocentAfspraak),
                                          ('/plannenpost', OuderAvondPlannenPost)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
