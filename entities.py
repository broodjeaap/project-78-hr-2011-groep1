from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db

class Afspraak(db.Model):
  leerlingID = db.StringProperty()
  klas = db.StringProperty()
  docent = db.StringProperty()
  tijd = db.IntegerProperty()
  dag = db.DateProperty()
  
  