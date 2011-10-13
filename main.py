from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
import datetime


import htmlHelper
import entities

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(htmlHelper.header())
        self.response.out.write(htmlHelper.klasAfspraakPage('h3'))
        self.response.out.write(htmlHelper.footer())
        
class AfspraakPlanningPost(webapp.RequestHandler):
    def post(self):
        key = self.request.get("afzegkey")
        if(len(key) != 0):
            afspraak = entities.Afspraak.get(key)
            afspraak.delete()
            self.redirect('/')
            return
            
        """
        entities.Afspraak(leerlingID="0",
                            docentID='BAARR',
                            dag=datetime.date(2011, 10, 11), 
                            tijd=-1,
                            tafelnummer=0,
                            beschrijving='test')
        """
        klas = self.request.get("klas")
        leerlingID = "1234"
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
                """
                self.response.out.write("<tr>")
                self.response.out.write("<td>"+afspraak.leerlingID+"</td>")
                self.response.out.write("<td>"+afspraak.docentID+"</td>")
                self.response.out.write("<td>"+str(afspraak.dag)+"</td>")
                self.response.out.write("<td>"+str(afspraak.tijd)+"</td>")
                self.response.out.write("<td>"+afspraak.beschrijving+"</td>")
                self.response.out.write("</tr>")
        self.response.out.write("</table>")"""
    
def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/afspraakplanningpost', AfspraakPlanningPost)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
