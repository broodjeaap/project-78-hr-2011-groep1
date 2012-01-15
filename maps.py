# -*- coding: latin-1 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import memcache
from geopy import geocoders
from geopy import distance
from gaesessions import get_current_session
from math import *
import datetime
import entities
import webpages
import inputFunctions

MAX = 2147483647

class MapRoot(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        #self.response.out.write("<a href='/map/fill' >fill</a>")
        self.response.out.write(webpages.footer())

class MapFill(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        g = geocoders.Google()
        leerlingen = entities.Leerling.all()
        failedLeerlingen = []
        for leerling in leerlingen:
            if not leerling.lokatie:
                try:
                    place, (lat, lng) = g.geocode(leerling.adres+" "+leerling.huisnummer+" "+leerling.woonplaats+" netherlands")
                    leerling.lokatie = db.GeoPt(lat,lng)
                    leerling.put()
                except:
                    failedLeerlingen.append(leerling)
        for leerling in failedLeerlingen:
            leerling.lokatie = db.GeoPt(52.0465345,4.7203522)
            leerling.put()
        self.response.out.write(str(len(failedLeerlingen))+" leerlingen zijn niet succesvol gegeocode en hebben 52.0465345,4.7203522 als lokatie gekregen")    
        self.response.out.write(webpages.footer())

class Afstanden(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        distances = [1,2,5,7,10,15]
        counts = [0,0,0,0,0,0]
        g = geocoders.Google()
        place, (lat, lng) = g.geocode("Kanaalstraat 31, 2801 SH Gouda")
        school = db.GeoPt(lat,lng)
        leerlingen = entities.Leerling.all().fetch(MAX)
        for leerling in leerlingen:
            if leerling.lokatie:
                distanceTo = haversine(school,leerling.lokatie)
                for i in range(len(distances)):
                    if distanceTo < distances[i]:
                        counts[i] += 1
                        break
        self.response.out.write("""<iframe id='afstandMap' frameborder=0 marginwidth=0 marginheight=0 border=0 style="border:0;margin:0;width:500px;height:375px;" src="http://www.google.com/uds/modules/elements/mapselement/iframe.html?maptype=roadmap&latlng=52.015043%2C4.695895&mlatlng=52.015043%2C4.695895&maddress1=Kanaalstraat%2031&maddress2=2801%20Gouda%2C%20The%20Netherlands&mtitle=School&element=true" scrolling="no" allowtransparency="true"></iframe>""")
        #self.response.out.write("<a href='#' onclick='test()'>test</a>")
                        
        self.response.out.write("<h1>Afstanden van leerlingen tot de school</h1><br /><table border='1'>")
        for i in range(len(counts)):
            self.response.out.write("<tr><td> < "+str(distances[i])+"km</td><td>"+str(counts[i])+"</td></tr> <br />")
        self.response.out.write("</table>")
        self.response.out.write(webpages.footer())

class KortsteRoute(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        leerlingen = entities.Leerling.all().fetch(MAX)
        matrix = {}
        matrixRegel = {}
        length = len(leerlingen)
        for a in range(length):
            for b in range(length):
                matrixRegel[leerlingen[b].leerlingID] = haversine(leerlingen[a].lokatie,leerlingen[b].lokatie)
            matrix[leerlingen[a].leerlingID] = matrixRegel
            matrixRegel = {}
        
        """
        debugging...
        self.response.out.write("<h1>~Snelste routen tussen leerlingen</h1><br /><table border='1'><tr><td> </td>")
        self.response.out.write("</tr>")
        for key,dict in matrix.iteritems():
            self.response.out.write("<tr><td>"+key+"</td>")
            for key2,dictLine in dict.iteritems():
                self.response.out.write("<td>"+str(dictLine)+"</td>")
                
            self.response.out.write("</tr>")
        self.response.out.write("</table>")
        """
        leerlingenDic = {}
        for leerling in leerlingen:
            leerlingenDic[leerling.leerlingID] = leerling
        output = []
        visited = []
        current = leerlingen[0]
        
        tmp = []
        count = 0
        for leerling in leerlingen:
            if leerling.lokatie in tmp:
                count += 1
            else:
                tmp.append(leerling.lokatie)
                
        self.response.out.write(str(count)+": "+str(len(tmp)))
        
        
        
        
        output.append(current)
        visited.append(current.leerlingID)
        while len(output) < len(leerlingen):
            lowest = MAX
            lowestID = current.leerlingID
            for key,afstand in matrix[current.leerlingID].iteritems():
                if afstand < lowest and key not in visited:
                    if afstand != 0:
                        lowest = afstand
                        lowestID = key
                    else:
                        visited.append(key)
            current = leerlingenDic[lowestID]
            visited.append(leerling.leerlingID)
            output.append(current)
            
        for leerling in output:
            self.response.out.write(leerling.leerlingID+"<br />")
        """
        self.response.out.write("<h1>~Snelste routen tussen leerlingen</h1><br /><table border='1'>")
        for i in range(len(counts)):
            self.response.out.write("<tr><td> < "+str(distances[i])+"km</td><td>"+str(counts[i])+"</td></tr> <br />")
        self.response.out.write("</table>")
        """
        self.response.out.write(webpages.footer())

def haversine(point1,point2):
    lon1, lat1, lon2, lat2 = map(radians, [point1.lon, point1.lat, point2.lon, point2.lat])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def main():
    application = webapp.WSGIApplication([('/map/', MapRoot),
                                          ('/map/fill', MapFill),
                                          ('/map/afstanden', Afstanden),
                                          ('/map/kortsteroute', KortsteRoute)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
