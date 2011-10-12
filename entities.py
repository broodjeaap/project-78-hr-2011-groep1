from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db

class Afspraak(db.Model):
  leerlingID = db.StringProperty()
  klas = db.StringProperty()
  docent = db.StringProperty()
  tijd = db.IntegerProperty()
  dag = db.DateProperty()
  
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