from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
import datetime


import htmlHelper
import entities

class Authenticate(webapp.RequestHandler):
    def post(self):
        inlogcode=self.request.get("inlogcode")
        emailadres=self.request.get("emailadres")   
        
        
        users = db.GqlQuery("SELECT __key__ FROM Docent WHERE email='"+emailadres+"' AND wachtwoord='"+inlogcode+"'")
        
        for user in users:
            userObject = db.get(user)
            self.response.out.write('<html><head><title>Afspraaksysteem docenten</title></head><body style="background-color:#FCF2E6;">')
            self.response.out.write('<div id="contentWrapper" style="postion:relative; width:1030px; margin-left:auto; margin-right:auto; margin-top:80px;">')
            self.response.out.write('<div><h1 style="margin-bottom:0px;">Welkom '+userObject.aanhef+'&nbsp;'+userObject.naam+'</h1></div>')
            self.response.out.write('<div style="position:relative; width:1024px; min-height:400px; background-color:#FFE4C4; border: 3px coral solid;">')
            self.response.out.write('<div style=" background-color:#FFFFFF;width:360px; margin-left:auto; margin-right:auto; margin-top:15px;">'+htmlHelper.afspraakTable(userObject.docentID)+'</div>')# fungeert als tablewrapper voor het uitlijnen van de tabel precies in het midden.
            self.response.out.write('<div style=" margin-bottom:10px; position:relative; left: 880px;"><a style="text-decoration:none; href="http://www.google.nl"><input type="submit" value="print"/></a>&nbsp;&nbsp;<a style="text-decoration:none;" href="http://www.google.nl"><input type="submit" value="Uitloggen"/></a></div>')
            self.response.out.write("</div>")
            self.response.out.write('</body></html>')
            
            
        
        #'
        #self.response.out.write(htmlHelper.header(bodyAttributes ="onload='afspraakInit()'" ))
        #self.response.out.write(htmlHelper.klasAfspraakPage('h3',leerlingID="1234"))
        #self.response.out.write(htmlHelper.footer())

class OuderAvondPlannen(webapp.RequestHandler):
    def get(self):
        self.response.out.write(htmlHelper.header())
        self.response.out.write(htmlHelper.planningPage())
        self.response.out.write(htmlHelper.footer())

class OuderAvondPlannenPost(webapp.RequestHandler):
    def post(self):
        self.response.out.write(htmlHelper.header())
        docenten = self.request.get("checkedDocenten").split(",")
        datums = self.request.get("datums").split(",")
        splitDatums = []
        for datum in datums:
            splitDatums.append(datum.split("-"))
            
        for docent in docenten:
            for datum in splitDatums:
                afspraak = entities.Afspraak(leerlingID="0",docentID=docent,dag=datetime.date(int(datum[0]), int(datum[1]), int(datum[2])), tijd=-1,tafelnummer=0,beschrijving='#')
                afspraak.put();
            self.response.out.write(docent+" heeft ouderavond(en) op: <br />")
            for datum in datums:
                self.response.out.write(datum+" <br />")
            self.response.out.write("<br />")
        self.response.out.write(htmlHelper.footer())
            
class AfspraakPlanningPost(webapp.RequestHandler):
    def post(self):
        key = self.request.get("afzegkey")
        if(len(key) != 0):
            afspraak = entities.Afspraak.get(key)
            afspraak.delete()
            self.redirect('/')
            return
        klas = self.request.get("klas")
        leerlingID = "4321"
        vakken = db.GqlQuery("SELECT * FROM VakPerKlas WHERE klas = '"+klas+"'")
        
        #self.response.out.write("<table border='1'><tr><th>leerlingID</th><th>docentID</th><th>dag</th><th>tijd</th><th>beschrijving</th></tr>")
        for vak in vakken:
            afspraakString = self.request.get(vak.docentID+"_afspraak")
            if(len(afspraakString) != 0):
                beschrijving = self.request.get(vak.docentID+"_beschrijving")
                afspraakData = afspraakString.split("_")
                
                datumStrings = afspraakData[0].split("-")
                
                afspraak = entities.Afspraak(leerlingID = leerlingID,docentID = vak.docentID,dag= datetime.date(int(datumStrings[0]),int(datumStrings[1]), int(datumStrings[2])),tijd= int(afspraakData[1]),tafelnummer=0,beschrijving = beschrijving)
                afspraak.put()
                self.redirect('/')
    
def main():
    application = webapp.WSGIApplication([('/authenticate', Authenticate),
                                          ('/afspraakplanningpost', AfspraakPlanningPost),
                                          ('/plannen', OuderAvondPlannen),
                                          ('/plannenpost', OuderAvondPlannenPost)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
