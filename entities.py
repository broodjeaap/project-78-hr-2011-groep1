from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db

class Afspraak(db.Model):
    leerlingID = db.StringProperty()
    docentID = db.StringProperty()
    dag = db.DateProperty()
    tijd = db.IntegerProperty()
    tafelnummer = db.IntegerProperty()
    beschrijving = db.TextProperty()
  
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
    
class Leerling(db.Model):
    leerlingID = db.StringProperty()
    wachtwoord = db.StringProperty()
    voornaam = db.StringProperty()
    tussenvoegsel = db.StringProperty()
    achternaam = db.StringProperty()
    geslacht = db.StringProperty()
    klas = db.StringProperty()
    aanhefVerzorger = db.StringProperty()
    initialenVerzorger = db.StringProperty()
    voorvoegselsVerzorger = db.StringProperty()
    achternaamVerzorger = db.StringProperty()
    rolVerzorger = db.StringProperty()
    adres = db.StringProperty()
    huisnummer = db.StringProperty()
    woonplaats = db.StringProperty()
    postcode = db.StringProperty()
    mobielnummer = db.StringProperty()
    vastnummer = db.StringProperty()
    email = db.StringProperty()
    lokatie = db.GeoPtProperty()
    
class Beheerder(db.Model):
    login = db.StringProperty()
    beschrijving = db.StringProperty()
    wachtwoord = db.StringProperty()
    securityLevel = db.IntegerProperty()
    
class ChatMessage(db.Model):
    poster = db.StringProperty()
    room = db.StringProperty()
    time = db.TimeProperty(auto_now=True)
    message = db.StringProperty()
    
class idCounter(db.Model):
    count = db.IntegerProperty(required=True, default=3321)
