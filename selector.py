import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from gaesessions import get_current_session
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import memcache
import datetime
import webpages
import entities


import wsgiref.handlers
import sys
from reportlab.pdfgen import canvas

MAX = 2147483647

"""
De selector Module zorgt voor een makkelijke/overzichtelijke manier om leerlingen
te selecteren, individueel of op basis van hele klassen.
"""

class Main(webapp.RequestHandler):
    """
    Main pagina van de selector module, hier zijn drie kollommen te zien
    een klassen kolom, een leerlingen kolom en een geselecteerde kolom
    """
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        if session.has_key("selectionReferer"):
            self.response.out.write("<h1><a href="+session["selectionReferer"]+">Continue with current selection</a></h1>")
        self.response.out.write("<a href='#' onclick='clearselection()' ><h3>Selectie verwijderen</h3></a>");
        self.response.out.write("<script type='text/javascript' src='/js/selector.js'></SCRIPT>");
        self.response.out.write("<div class='selectorDiv'>")
        self.response.out.write("<div class='leerlingSelectorDiv'>");
        self.response.out.write("<h3>Individuele leerlingen toevoegen</h3>");
        self.response.out.write("Zoek op id: <input type='text' id='leerlingIDText' onkeyup='textboxchange(this.value,\"leerling\");' />");
        self.response.out.write("<div class='leerlingenOutputDiv' id='leerlingenOutputDiv'>");
        self.response.out.write("</div>")
        self.response.out.write("</div>")
        self.response.out.write("<div class='klasSelectorDiv'>");
        self.response.out.write("<h3>Klassen toevoegen</h3>");
        self.response.out.write("Zoek op id: <input type='text' id='klasIDText' onkeyup='textboxchange(this.value,\"klas\");' />");
        self.response.out.write("<div class='klassenOutputDiv' id='klassenOutputDiv'>");
        self.response.out.write("</div>")
        self.response.out.write("</div>")
        self.response.out.write("<div class='selectedSelectorDiv'>");
        self.response.out.write("<h3>Huidige Selectie</h3>");
        self.response.out.write("<div class='selectedOutputDiv' id='selectedOutputDiv'>");
        self.response.out.write("</div>")
        self.response.out.write("</div>")
        self.response.out.write("</div>")
        self.response.out.write(webpages.footer())

class LeerlingGet(webapp.RequestHandler):
    """
    AJAX pagina die op basis van 'q' leerlingen returned (deze worden weergegeven
    in de leerlingen kolom) 
    """
    def get(self):
        session = get_current_session()
        q = self.request.get('q')
        list = getList()
        leerlingen = getLeerlingen();
        result = []
        for leerling in leerlingen:
            if(leerling.leerlingID.find(q) != -1):
                result.append(leerling)
        self.response.out.write("<table border='1'>")
        for leerling in result:
            image = "redcross.png"
            onclick ="addleerling(\""+leerling.leerlingID+"\")"
            for l in list:
                if l.leerlingID == leerling.leerlingID:
                    image = "greencheck.png"
                    onclick ="removeleerling(\""+leerling.leerlingID+"\")"
                    break
            self.response.out.write("<tr id='"+leerling.leerlingID+"row' onclick='"+onclick+"'>      <td><img id='"+leerling.leerlingID+"image' src='/images/"+image+"' width='20' height='20' /></td>          <td>"+leerling.leerlingID+"</td><td>"+leerling.voornaam+" "+leerling.tussenvoegsel+" "+leerling.achternaam+"</td><td>"+leerling.klas+"</tr>")
        self.response.out.write("</table>")
        
class LeerlingAdd(webapp.RequestHandler):
    """
    AJAX pagina voor het toevoegen van een leerling aan de huidige selectie.
    """
    def post(self):
        list = getList()
        id = self.request.get('id')
        leerling = getLeerling(id)
        check = True
        for l in list:
            if l.leerlingID == id:
                check = False
                break
        if check:
            list.append(leerling)
        setList(list)
        
class LeerlingRemove(webapp.RequestHandler):
    """
    AJAX pagina voor het verwijderen van een leerlingen uit de huidige selectie
    """
    def post(self):
        list = getList()
        id = self.request.get('id')
        leerling = getLeerling(id)
        for a, l in enumerate(list):
            if l.leerlingID == leerling.leerlingID:
                del list[a]
                break
        setList(list)

class KlassenGet(webapp.RequestHandler):
    """
    AJAX pagina die de klassen weergeeft die voldoen aan de query 'q'
    Deze pagina is erg langzaam en wachttijden kunnen tot wel 10 seconden duren
    Dit komt vooral door de bruteforce methode van het checken of een hele klas
    geselecteerd is. (zie 'isKlasFilled()')
    """
    def get(self):
        session = get_current_session()
        q = self.request.get('q')
        list = []
        klassen = getKlassen()
        result = []
        for k,v in klassen.iteritems():
            if k.find(q) != -1:
                result.append(k)
        self.response.out.write("<table border='1'>")
        for klas in result:
            image = "redcross.png"
            onclick ="addklas(\""+klas+"\")"
            if isKlasFilled(klas):
                image = "greencheck.png"
                onclick ="removeklas(\""+klas+"\")"
            self.response.out.write("<tr id='"+klas+"row' onclick='"+onclick+"'>      <td><img id='"+klas+"image' src='/images/"+image+"' width='20' height='20' /></td>          <td>"+klas+"</td></tr>")
        self.response.out.write("</table>")
        
def isKlasFilled(id):
    """
    Deze functie kijkt of een klas ('id') gevuld is en dus als geselecteerd weergegeven
    kan worden.
    Dit wordt op het moment gedaan door bruteforce alles na te kijken en is dus erg langzaam.
    """
    klas = getKlas(id)
    check = {}
    for leerling in klas:
        check[leerling.leerlingID] = False
    list = getList()
    for leerling in list:
        if leerling.leerlingID in check.keys():
            check[leerling.leerlingID] = True
    for key in check.keys():
        if not check[key]:
            return False
        
    return True
        
class KlasAdd(webapp.RequestHandler):
    """
    AJAX pagina om een hele klas toe te voegen aan de huidige selectie.
    """
    def post(self):
        list = getList()
        klas = getKlas(self.request.get('id'))
        for leerling in klas:
            check = True
            for l in list:
                if l.leerlingID == leerling.leerlingID:
                    check = False
                    break
            if check:
                list.append(leerling)
        setList(list)
            
    
class KlasRemove(webapp.RequestHandler):
    """
    AJAX pagina om een hele klas te verwijderen uit de huidige selectie.
    """
    def post(self):
        list = getList()
        klas = getKlas(self.request.get('id'))
        for leerling in klas:
            for a, l in enumerate(list):
                if l.leerlingID == leerling.leerlingID:
                    del list[a]
                    break
        setList(list)

class Selection(webapp.RequestHandler):
    """
    AJAX voor het overzicht van de huidige selectie
    """
    def get(self):
        list = getList()
        self.response.out.write("<table border='1'>")
        for leerling in list:
            self.response.out.write("<tr id='"+leerling.leerlingID+"row' onclick='removeleerling(\""+leerling.leerlingID+"\")'>      <td><img id='"+leerling.leerlingID+"image' src='/images/greencheck.png' width='20' height='20' /></td>          <td>"+leerling.leerlingID+"</td><td>"+leerling.voornaam+" "+leerling.tussenvoegsel+" "+leerling.achternaam+"</td><td>"+leerling.klas+"</tr>")
        self.response.out.write("</table>")
        
class Clear(webapp.RequestHandler):
    """
    AJAX pagina om de hele selectie te verwijderen
    """
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        session.__delitem__("selectorList")
        self.response.out.write("Selectie verwijderd, <a href='/selector'>terug</a>")
        self.response.out.write(webpages.footer())


"""
Functie die leerlingen ophaalt en cached in memcache.
"""
def getLeerlingen():
    leerlingen = memcache.get("leerlingen1")
    if leerlingen:
        leerlingen += memcache.get("leerlingen2")
    if not leerlingen:
        leerlingen = db.GqlQuery("SELECT * FROM Leerling")
        leerlingen = leerlingen.fetch(MAX)
        memcache.set("leerlingen1",leerlingen[:(len(leerlingen) / 2)])
        memcache.set("leerlingen2",leerlingen[((len(leerlingen) /2)+1):])
    return leerlingen

"""
Functie die 1 leerling ophaalt en cached in memcache.
"""
def getLeerling(id):
    leerling = memcache.get(id)
    if not leerling:
        leerlingen = getLeerlingen()
        for l in leerlingen:
            if l.leerlingID == id:
                leerling = l
                break
        memcache.set(id,leerling)
    return leerling

"""
Functie die klassen ophaalt en cached in memcache.
"""
def getKlassen():
    klassen = db.GqlQuery("SELECT * FROM Klas")
    dic = {}
    for klas in klassen:
        dic[klas.klas] = []
    leerlingen = getLeerlingen()
    for leerling in leerlingen:
        list = dic[leerling.klas.encode('utf-8')]
        list.append(leerling)
    klassen = dic
    return klassen

"""
Functie 1 klas ophaalt en cached in memcache.
"""
def getKlas(id):
    klassen = getKlassen()
    klas = klassen[id]
    return klas

"""
Functie die de huidige selectie ophaalt.
"""
def getList():
    session = get_current_session()
    if session.__contains__("selectorList"):
        list = session["selectorList"]
    else:
        list = []
        session["selectorList"] = list
    return list
"""
Functie die de huidige selectie opslaat.
"""
def setList(list):
    session = get_current_session()
    session["selectorList"] = list

def main():
    application = webapp.WSGIApplication([('/selector', Main),
                                          ('/selector/selection', Selection),
                                          ('/selector/leerlingget', LeerlingGet),
                                          ('/selector/leerlingadd', LeerlingAdd),
                                          ('/selector/leerlingremove', LeerlingRemove),
                                          ('/selector/klassenget', KlassenGet),
                                          ('/selector/klasadd', KlasAdd),
                                          ('/selector/klasremove', KlasRemove),
                                          ('/selector/clear', Clear)],
                                            debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
