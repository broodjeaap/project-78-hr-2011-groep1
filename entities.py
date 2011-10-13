from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db

class Afspraak(db.Model):
  leerlingID = db.StringProperty()
  docentID = db.StringProperty()
  dag = db.DateProperty()
  tijd = db.IntegerProperty()
  tafelnummer = db.IntegerProperty()
  beschrijving = db.StringProperty()
  
  
  
class Docent(db.Model):
    docentID = db.StringProperty()
    aanhef = db.StringProperty()
    naam = db.StringProperty()
    postvaknummer = db.IntegerProperty()
    email= db.StringProperty()
    wachtwoord = db.StringProperty()
    
class Vak(db.Model):
    vakCode = db.StringProperty()
    vakNaam = db.StringProperty()
    
class VakPerKlas(db.Model):
    jaargang = db.StringProperty()
    klas = db.StringProperty()
    vakCode = db.StringProperty()
    docentID = db.StringProperty()
    