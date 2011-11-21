import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from gaesessions import get_current_session
from google.appengine.ext import db
from google.appengine.api import mail
import datetime
import webpages
import entities

import wsgiref.handlers
import sys
from reportlab.pdfgen import canvas

class Login(webapp.RequestHandler):
    def get(self):
        beheerder = entities.Beheerder(login='admin', beschrijving='Ingebouwde admin account', wachtwoord='admin', securityLevel=2)
        beheerder.put()
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
            session.__setitem__('securityLevel',db.get(result[0]).securityLevel)
            self.redirect('/beheerder')
            return
                
        
        session.__setitem__('loginError','error')
        self.redirect('/')

class OuderAvondPlannen(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        self.response.out.write(webpages.planningPage())
        self.response.out.write(webpages.footer())

class OuderAvondPlannenPost(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
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
                beschrijving = self.request.get(vak.docentID+"_hidden_beschrijving").replace('\n',", ")
                afspraakData = afspraakString.split("_")
                
                datumStrings = afspraakData[0].split("-")
                
                afspraak = entities.Afspraak(leerlingID = leerlingID,docentID = vak.docentID,dag= datetime.date(int(datumStrings[0]),int(datumStrings[1]), int(datumStrings[2])),tijd= int(afspraakData[1]),tafelnummer=0,beschrijving = beschrijving)
                afspraak.put()
                self.redirect('/leerlingafspraak')

class DocentAfspraak(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        if(session.has_key('id') and session.__getitem__('loginType') == "docent"):
            docent = db.GqlQuery("SELECT * FROM Docent where docentID = '"+session['id']+"'")
            docent = docent[0]
            
            self.response.out.write(webpages.DocentPage(docent))
        else:
            self.redirect('/')
        self.response.out.write(webpages.footer())

class LeerlingAfspraak(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        if(session.has_key('id') and session.__getitem__('loginType') == 'leerling'):
            leerling = db.GqlQuery("SELECT * FROM Leerling where leerlingID = '"+session['id']+"'")
            leerling = leerling[0]
            self.response.out.write(webpages.klasAfspraakPage(klas=leerling.klas,leerlingID=leerling.leerlingID))
        else:
            self.redirect('/')
        self.response.out.write(webpages.footer())

class Beheerder(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        header=webpages.header(session)
        session.__setitem__('header', header)
        self.response.out.write(header)
        self.response.out.write('Beheer pagina')
        self.response.out.write(webpages.footer())
class AccountSettings(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'leerling'):
            self.response.out.write(webpages.header(session))
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
            
            self.response.out.write(webpages.table(tableData,attributes="class='accountTable'",title="<h2>Leerling: "+leerling.leerlingID+"</h2>",divAttr='leerlingAccountGegevens'))
            
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
            self.response.out.write(webpages.table(tableData,attributes="class='accountTablePassword'",title="<h3>Wachtwoord veranderen</h3>", divAttr='leerlingAccountWachtwoord'))
            self.response.out.write("</form>")
            self.response.out.write("</div>")
        elif(session.__getitem__('loginType') == 'docent'):
            self.response.out.write(webpages.header(session))
            self.response.out.write("<div class='docentAccount'>")
            docent = db.get(session.__getitem__('key'))
            
            tableData = []
            tableRow = []
            tableRow.append("Naam")
            tableRow.append(docent.aanhef+" "+docent.naam)
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Postvaknummer")
            tableRow.append(str(docent.postvaknummer))
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("Email")
            tableRow.append(docent.email)
            tableData.append(tableRow)
            
            self.response.out.write(webpages.table(tableData,attributes="class='accountTable'",title="<h2>Docent: "+docent.docentID+"</h2>",divAttr='docentAccountGegevens'))
            
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
            self.response.out.write(webpages.table(tableData,attributes="class='accountTablePassword'",title="<h3>Wachtwoord veranderen</h3>", divAttr='leerlingAccountWachtwoord'))
            self.response.out.write("</form>")
            self.response.out.write("</div>")
            
        elif(session.__getitem__('loginType') == 'beheerder'):
            self.response.out.write(session.__getitem__('header'))
            self.response.out.write("<div class='beheerAccount'>")
            beheerder = db.get(session.__getitem__('key'))
            tableData = []
            tableRow = []
            tableRow.append("Beschrijving")
            tableRow.append(beheerder.beschrijving)
            tableData.append(tableRow)
            tableRow = []
            tableRow.append("SecurityLevel")
            if(beheerder.securityLevel == 0):
                tableRow.append("Read-only access")
            elif(beheerder.securityLevel == 1):
                tableRow.append("Secretariaat")
            elif(beheerder.securityLevel == 2):
                tableRow.append("Admin")
            else:
                tableRow.append("Error")
            tableData.append(tableRow)
            tableRow = []
            self.response.out.write(webpages.table(tableData,attributes="class='accountTable'",title="<h2>Beheerder: "+beheerder.login+"</h2>",divAttr='docentAccountGegevens'))
            
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
            self.response.out.write(webpages.table(tableData,attributes="class='accountTablePassword'",title="<h3>Wachtwoord veranderen</h3>", divAttr='leerlingAccountWachtwoord'))
            self.response.out.write("</form>")
            self.response.out.write("</div>")
        else:
            self.redirect('/')
        self.response.out.write(webpages.footer())
        
class AccountWachtwoordPost(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        if(session.has_key('id')):
            huidigPassword = self.request.get("huidig_password")
            nieuwPassword = self.request.get("nieuw_password")
            herhaalPassword = self.request.get("herhaal_password")
            persoon = db.get(session.__getitem__('key'))
            if(huidigPassword == persoon.wachtwoord):
                if(nieuwPassword == herhaalPassword):
                   persoon.wachtwoord = nieuwPassword
                   persoon.put()
                   self.response.out.write("<div class='wachtwoordPost'>Wachtwoord veranderd <br /><a href='/accountsettings'>Terug</a></div>")
                else:
                    self.response.out.write("<div class='wachtwoordPost'>Nieuwe wachtwoorden waren niet hetzelfde <br /><a href='/accountsettings'>Terug</a></div>")
            else:
                self.response.out.write("<div class='wachtwoordPost'>Verkeerde wachtwoord <br /><a href='/accountsettings'>Terug</a></div>")
        else:
            self.redirect('/')
        self.response.out.write(webpages.footer())
        
class Chat(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        if(session.has_key('id')):
            self.response.out.write(webpages.chatBox(session['id'],"global"))
        self.response.out.write(webpages.footer())
    
class AjaxChatHandler(webapp.RequestHandler):
    def get(self):
        if(self.request.get('type') == 'get'):
            messages = db.GqlQuery("SELECT * FROM ChatMessage where room = '"+self.request.get('room')+"'")
            ret = "";
            for message in messages:
                ret += str(message.time)[:-7]+"-"+message.poster+": "+message.message.replace("_"," ")+"<br />"
            self.response.out.write(ret)
        elif (self.request.get('type') == 'post'):
            message = entities.ChatMessage(poster=self.request.get('id'),room=self.request.get('room'),time=datetime.datetime.now().time(),message=self.request.get('message'))
            message.put();


class pdfWriter(webapp.RequestHandler):

    def get(self):
        result = db.GqlQuery("SELECT __key__ FROM Leerling where email = ''")                                
        self.response.headers['Content-Type'] = 'application.pdf'
       
        p = canvas.Canvas(self.response.out)
        for leerling in result:
            Ouder = db.get(leerling)
            p.drawString(100, 750, "Geachte meneer/mevrouw " + "%s" % Ouder.achternaam + ",")
            p.drawString(100, 690, "Op 10 december 2011 is er weer de mogelijkheid om met de docenten")                            
            p.drawString(100, 665, "van " + "%s" % Ouder.voornaam + " te praten.")
            p.drawString(100, 615, "De avonden worden gehouden van 19:00 tot 22:00 uur.")
            p.drawString(100, 565, "Wij verzoeken u om telefonisch contact op te nemen om een afspraak te maken.")
            p.drawString(100, 540, "Wij zijn bereikbaar van 8:30 tot 17:00 uur op 070-1234567.")
            p.drawString(100, 490, "Wij hopen u spoedig te mogen verwelkomen op de ouderavond.")
            p.drawString(100, 430, "Met vriendelijke groeten,")
            p.drawString(100, 405, "Bob Bemer MSc, directeur DKC")
            p.showPage()   
            p.save()

class StuurEmail(webapp.RequestHandler):      
    
    def get(self):                
        
        result = db.GqlQuery("SELECT * FROM Leerling WHERE email = 'jordyhert@gmail.com'")   
        for leerling in result:
            message = mail.EmailMessage(sender="Donald Knuth College <jordyhert@gmail.com>", subject="Uitnodiging ouderavond")
            message.to = leerling.aanhefVerzorger+"<jordyhert@gmail.com>"
            message.body = """
            Geachte meneer/mevrouw """ + leerling.aanhefVerzorger + """ """ + leerling.achternaamVerzorger + """

            Op 10 december 2011 is er weer de mogelijkheid om met de docenten van """ + leerling.voornaam + """ te praten. 
            
            De avond vindt plaats tussen 19:00 en 22:00 uur.

            Door de onderstaande pagina te openen kunt u zich inschrijven voor de ouderavond.

            http://hrpro78.appspot.com

            U kunt inloggen met de volgende gegevens:
            
            Gebruikersnaam: """ + leerling.achternaamVerzorger + """
            Wachtwoord: """ + leerling.wachtwoord + """

            Wij hopen u spoedig te mogen verwelkomen op de ouderavond.

            Met vriendelijke groeten,

            Bob Bemer MSc, directeur DKC
            """            
            message.send()
    
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
                                          ('/beheerder',Beheerder),
                                          ('/chat',Chat),
                                          ('/chatajaxhandler',AjaxChatHandler),
                                          ('/plannenpost', OuderAvondPlannenPost),
                                          ('/plannenpost', OuderAvondPlannenPost),
                                          ('/berichtenVersturen', pdfWriter),
                                          ('/stuuremail', StuurEmail)],
                                            debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
