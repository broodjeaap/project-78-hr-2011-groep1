from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from gaesessions import get_current_session
import webpages
import entities
import webpages
import datetime

class AfspraakDatastore(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                self.response.out.write(webpages.header(session))
                afspraken = entities.Afspraak.all()
                tableData = []
                for afspraak in afspraken:
                    tableRow = []
                    tableRow.append("<form action='/datastore/afspraakpost' method='post'>")
                    tableRow.append("<input type='text' name='leeringID' value='"+afspraak.leerlingID+"' />")
                    tableRow.append("<input type='text' name='docentID' value='"+afspraak.docentID+"' />")
                    tableRow.append("<input type='text' name='dag' value='"+str(afspraak.dag)+"' />")
                    tableRow.append("<input type='text' name='tijd' value='"+str(afspraak.tijd)+"' />")
                    tableRow.append("<input type='text' name='tafelnummer' value='"+str(afspraak.tafelnummer)+"' />")
                    tableRow.append("<input type='text' name='beschrijving' value='"+str(afspraak.beschrijving)+"' />")
                    tableRow.append("<input type='hidden' name='key' value='"+str(afspraak.key())+"'><input type='submit' value='Aanpassen' /></form>")
                    tableRow.append("<form action='/datastore/afspraakpost' method='post'><input type='hidden' name='key' value='"+str(afspraak.key())+"'><input type='hidden' name='delete' value='delete' />")
                    tableRow.append("<input type='submit' value='Verwijderen' /></form>")
                    tableData.append(tableRow)
                self.response.out.write(webpages.table(data=tableData, attributes="class='overzichtTable" ,head=['','leerlingID','DocentID','dag','Tijd','Tafelnummer','beschrijving'],title="Afspraken",divAttr='dataStoreDiv',evenOdd=True))
                self.response.out.write(webpages.footer())
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')
            
class AfspraakDatastorePost(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                key = self.request.get("key")
                afspraak = db.get(key)
                if(self.request.get("delete") == 'delete'):
                    afspraak.delete()
                    self.redirect('/datastore/afspraak')
                    return
                
                afspraak.leerlingID = self.request.get("leerlingID")
                afspraak.docentID = self.request.get("docentID")
                dag = self.request.get("dag").split("-")
                afspraak.dag = datetime.date(int(dag[0]),int(dag[1]), int(dag[2]))
                afspraak.tijd = int(self.request.get("tijd"))
                afspraak.tafelnummer = int(self.request.get("tafelnummer"))
                afspraak.beschrijving = self.request.get("beschrijving")
                afspraak.put()
                self.redirect('/datastore/afspraak')
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')

class DocentDatastore(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                self.response.out.write(webpages.header(session))
                docenten = entities.Docent.all()
                tableData = []
                for docent in docenten:
                    tableRow = []
                    tableRow.append("<form action='/datastore/docentpost' method='post'>")
                    tableRow.append("<input type='text' name='docentID' value='"+docent.docentID+"' />")
                    tableRow.append("<input type='text' name='aanhef' value='"+docent.aanhef+"' />")
                    tableRow.append("<input type='text' name='naam' value='"+docent.naam+"' />")
                    tableRow.append("<input type='text' name='postvaknummer' value='"+str(docent.postvaknummer)+"' />")
                    tableRow.append("<input type='text' name='email' value='"+docent.email+"' />")
                    tableRow.append("<input type='text' name='wachtwoord' value='"+docent.wachtwoord+"' />")
                    tableRow.append("<input type='hidden' name='key' value='"+str(docent.key())+"'><input type='submit' value='Aanpassen' /></form>")
                    tableRow.append("<form action='/datastore/docentpost' method='post'><input type='hidden' name='key' value='"+str(docent.key())+"'><input type='hidden' name='delete' value='delete' />")
                    tableRow.append("<input type='submit' value='Verwijderen' /></form>")
                    tableData.append(tableRow)
                self.response.out.write(webpages.table(data=tableData, attributes="class='overzichtTable" ,head=['','docentID','aanhef','naam','postvaknummer','email','wachtwoord'],title="Docenten",divAttr='dataStoreDiv',evenOdd=True))
                self.response.out.write(webpages.footer())
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')
            
class DocentDatastorePost(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                key = self.request.get("key")
                docent = db.get(key)
                if(self.request.get("delete") == 'delete'):
                    docent.delete()
                    self.redirect('/datastore/docent')
                    return
                
                docent.docentID = self.request.get("docentID")
                docent.aanhef = self.request.get("aanhef")
                docent.naam = self.request.get("naam")
                docent.postvaknummer = int(self.request.get("postvaknummer"))
                docent.email = self.request.get("email")
                docent.wachtwoord = self.request.get("wachtwoord")
                docent.put()
                self.redirect('/datastore/docent')
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')






class VakDatastore(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                self.response.out.write(webpages.header(session))
                vakken = entities.Vak.all()
                tableData = []
                for vak in vakken:
                    tableRow = []
                    tableRow.append("<form action='/datastore/vakpost' method='post'>")
                    tableRow.append("<input type='text' name='vakCode' value='"+vak.vakCode+"' />")
                    tableRow.append("<input type='text' name='vakNaam' value='"+vak.vakNaam+"' />")
                    tableRow.append("<input type='hidden' name='key' value='"+str(vak.key())+"'><input type='submit' value='Aanpassen' /></form>")
                    tableRow.append("<form action='/datastore/vakpost' method='post'><input type='hidden' name='key' value='"+str(vak.key())+"'><input type='hidden' name='delete' value='delete' />")
                    tableRow.append("<input type='submit' value='Verwijderen' /></form>")
                    tableData.append(tableRow)
                self.response.out.write(webpages.table(data=tableData, attributes="class='overzichtTable" ,head=['','vakCode','vakNaam'],title="Vakken",divAttr='dataStoreDiv',evenOdd=True))
                self.response.out.write(webpages.footer())
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')

class VakPerKlasDatastore(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                self.response.out.write(webpages.header(session))
                vakkenPerKlas = entities.VakPerKlas.all()
                tableData = []
                for vakPerKlas in vakkenPerKlas:
                    tableRow = []
                    tableRow.append("<form action='/datastore/vakperklaspost' method='post'>")
                    tableRow.append("<input type='text' name='jaargang' value='"+vakPerKlas.jaargang+"' />")
                    tableRow.append("<input type='text' name='klas' value='"+vakPerKlas.klas+"' />")
                    tableRow.append("<input type='text' name='vakCode' value='"+vakPerKlas.vakCode+"' />")
                    tableRow.append("<input type='text' name='docentID' value='"+vakPerKlas.docentID+"' />")
                    tableRow.append("<input type='hidden' name='key' value='"+str(vakPerKlas.key())+"'><input type='submit' value='Aanpassen' /></form>")
                    tableRow.append("<form action='/datastore/vakperklaspost' method='post'><input type='hidden' name='key' value='"+str(vakPerKlas.key())+"'><input type='hidden' name='delete' value='delete' />")
                    tableRow.append("<input type='submit' value='Verwijderen' /></form>")
                    tableData.append(tableRow)
                self.response.out.write(webpages.table(data=tableData, attributes="class='overzichtTable" ,head=['','vakCode','vakNaam'],title="Vakken per klas",divAttr='dataStoreDiv',evenOdd=True))
                self.response.out.write(webpages.footer())
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')
            
class VakPerKlasDatastorePost(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                key = self.request.get("key")
                vakPerKlas = db.get(key)
                if(self.request.get("delete") == 'delete'):
                    vakPerKlas.delete()
                    self.redirect('/datastore/vakperklas')
                    return
                
                vakPerKlas.jaargang = self.request.get("jaargang")
                vakPerKlas.klas = self.request.get("klas")
                vakPerKlas.vakCode = self.request.get("vakCode")
                vakPerKlas.docentID = self.request.get("docentID")
                vakPerKlas.put()
                self.redirect('/datastore/vakperklas')
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')




class LeerlingDatastore(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                self.response.out.write(webpages.header(session))
                leerlingen = entities.Leerling.all()
                tableData = []
                for leerling in leerlingen:
                    tableRow = []
                    tableRow.append("<form action='/datastore/leerlingpost' method='post'>")
                    tableRow.append("<input type='text' name='leerlingID' value='"+leerling.leerlingID+"' />")
                    tableRow.append("<input type='text' name='wachtwoord' value='"+leerling.wachtwoord+"' />")
                    tableRow.append("<input type='text' name='voornaam' value='"+leerling.voornaam+"' />")
                    tableRow.append("<input type='text' name='tussenvoegsel' value='"+leerling.tussenvoegsel+"' />")
                    tableRow.append("<input type='text' name='achternaam' value='"+leerling.achternaam+"' />")
                    tableRow.append("<input type='text' name='geslacht' value='"+leerling.geslacht+"' />")
                    tableRow.append("<input type='text' name='klas' value='"+leerling.klas+"' />")
                    tableRow.append("<input type='text' name='aanhefVerzorger' value='"+leerling.aanhefVerzorger+"' />")
                    tableRow.append("<input type='text' name='initialenVerzorger' value='"+leerling.initialenVerzorger+"' />")
                    tableRow.append("<input type='text' name='voorvoegselsVerzorger' value='"+leerling.voorvoegselsVerzorger+"' />")
                    tableRow.append("<input type='text' name='achternaamVerzorger' value='"+leerling.achternaamVerzorger+"' />")
                    tableRow.append("<input type='text' name='rolVerzorger' value='"+leerling.rolVerzorger+"' />")
                    tableRow.append("<input type='text' name='adres' value='"+leerling.adres+"' />")
                    tableRow.append("<input type='text' name='huisnummer' value='"+leerling.huisnummer+"' />")
                    tableRow.append("<input type='text' name='woonplaats' value='"+leerling.woonplaats+"' />")
                    tableRow.append("<input type='text' name='postcode' value='"+leerling.postcode+"' />")
                    tableRow.append("<input type='text' name='mobielnummer' value='"+leerling.mobielnummer+"' />")
                    tableRow.append("<input type='text' name='vastnummer' value='"+leerling.vastnummer+"' />")
                    tableRow.append("<input type='text' name='email' value='"+leerling.email+"' />")
                    tableRow.append("<input type='hidden' name='key' value='"+str(leerling.key())+"'><input type='submit' value='Aanpassen' /></form>")
                    tableRow.append("<form action='/datastore/leerlingpost' method='post'><input type='hidden' name='key' value='"+str(leerling.key())+"'><input type='hidden' name='delete' value='delete' />")
                    tableRow.append("<input type='submit' value='Verwijderen' /></form>")
                    tableData.append(tableRow)
                self.response.out.write(webpages.table(data=tableData, attributes="class='overzichtTable" ,head=['','leerlingID','wachtwoord','voornaam','tussenvoegsel','achternaam','geslacht','klas','aanhefVerzorger','initialenVerzorger','voorvoegselsVerzorger','achternaamVerzorger','rolVerzorger','adres','huisnummer','woonplaats','postcode','mobielnummer','vastnummer','email'],title="Leerlingen",divAttr='dataStoreDiv',evenOdd=True))
                self.response.out.write(webpages.footer())
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')



def klassenLijst():

    result = db.GqlQuery("SELECT * FROM VakPerKlas")
    klassen = []
    unique = []
    
    if result.count()>0:
        for VakPerKlas in result:
            klassen.append(VakPerKlas.klas)   
        
        klassen.sort()
        unique.append(klassen[0])
        
        klassenIndex = 1
        uniqueIndex = 0
        
        while klassenIndex < len(klassen):
            if(unique[uniqueIndex] == klassen[klassenIndex]):
                klassenIndex +=1
            else:
                unique.append(klassen[klassenIndex])
                klassenIndex +=1
                uniqueIndex  +=1

    return unique

def leerlingIDS():

    result = db.GqlQuery("SELECT * FROM Leerling")
    ids = []    
    
    for leerling in result:
        ids.append(leerling.leerlingID)   
    
    ids.sort()
    
    return ids

def newLeerlingID(increment=False):
    
    counter = entities.idCounter.get_by_key_name("idcounter")
    
    if increment:
        if not counter:
            counter = entities.idCounter(key_name="idcounter")
            counter.count +=1
            counter.put()
            return
        else:
            counter.count +=1
            counter.put()     
    else:
        if not counter:
            counter = entities.idCounter(key_name="idcounter")
            counter.count +=1
            
        else:
            counter.count +=1
        
    return counter.count

class DeleteStudent(webapp.RequestHandler):
    def post(self):
         result = db.GqlQuery("SELECT * FROM Leerling WHERE leerlingID = '%s'"%(self.request.get('leerlingID')))
         leerling = result[0]
         leerling.delete()
         self.redirect('/datastore/addstudentpage')

class DeleteVak(webapp.RequestHandler):
    def post(self):
         result = db.GqlQuery("SELECT * FROM Vak WHERE vakCode = '%s'"%(self.request.get('vakcode')))
         vak = result[0]
         vak.delete()
         self.redirect('/datastore/addvakpage')

class DeleteBeheerder(webapp.RequestHandler):
    def post(self):
         result = db.GqlQuery("SELECT * FROM Beheerder WHERE login = '%s'"%(self.request.get('gebruikersnaam')))
         beheerder = result[0]
         beheerder.delete()
         self.redirect('/datastore/addbeheerderpage')

class addStudentPage(webapp.RequestHandler):
    def get(self):
        id = self.request.get('id')
        leerling = None
        
        
        result = db.GqlQuery("SELECT * FROM Leerling WHERE leerlingID = '%s'"%(id))
        if result.count()>0:
            leerling = result[0]

        self.response.out.write(webpages.header(get_current_session()))
        self.response.out.write(webpages.cmsHeader())
        if not leerling:
            self.response.out.write(webpages.addStudent(newLeerlingID(), leerlingIDS(), klassenLijst()))
        else:
            self.response.out.write(webpages.modifyStudent(leerling, leerlingIDS(), klassenLijst()))
        self.response.out.write(webpages.cmsFooter())
        self.response.out.write(webpages.footer())

def docentIDS():
    result = db.GqlQuery("SELECT * FROM Docent")
    ids = []    
    
    for docent in result:
        ids.append(docent.docentID)   
    
    ids.sort()
    
    return ids


class addDocentPage(webapp.RequestHandler):
    def get(self):
        
        self.response.out.write(webpages.header(get_current_session()))
        self.response.out.write(webpages.cmsHeader())

        id = self.request.get('id')
        docent = None

        result = db.GqlQuery("SELECT * FROM Docent WHERE docentID = '%s'"%(id))
        if result.count()>0:
            docent = result[0]

        if not docent:
            self.response.out.write(webpages.addDocent(docentIDS()))
        else:
            self.response.out.write(webpages.modifyDocent(docent, docentIDS()))
        self.response.out.write(webpages.cmsFooter())
        self.response.out.write(webpages.footer())


class AddStudent(webapp.RequestHandler):
    def post(self):
        
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                leerling = None
                if str(newLeerlingID()) == self.request.get('leerlingID'):
                    leerling = entities.Leerling()
                    newLeerlingID(True)
                else:
                     result = db.GqlQuery("SELECT * FROM Leerling WHERE leerlingID = '%s'"%(self.request.get('leerlingID')))
                     leerling = result[0]
                
                leerling.aanhefVerzorger = self.request.get("aanhefVerzorger")
                leerling.initialenVerzorger = self.request.get("initialenVerzorger")
                leerling.voorvoegselsVerzorger = self.request.get("voorvoegselsVerzorger")
                leerling.achternaamVerzorger = self.request.get("achternaamVerzorger")
                leerling.rolVerzorger = self.request.get("rolVerzorger")
                
                leerling.adres = self.request.get("adres")
                leerling.huisnummer = self.request.get("huisnummer")
                leerling.postcode = self.request.get("postcode")
                leerling.woonplaats = self.request.get("woonplaats")
                leerling.email = self.request.get("email")
                leerling.vastnummer = self.request.get("telefoon_vast")
                leerling.mobielnummer = self.request.get("mobiel")
                    
                leerling.geslacht = self.request.get("geslacht")
                leerling.voornaam = self.request.get("voornaam")
                leerling.tussenvoegsel = self.request.get("tussenvoegsel")
                leerling.achternaam = self.request.get("achternaam")
                leerling.klas = self.request.get("klas")                                  
                
                
                
                leerling.leerlingID = self.request.get("leerlingID")
                leerling.wachtwoord = self.request.get("wachtwoord")
                
                leerling.put()

                self.redirect('/datastore/addstudentpage')

class AddDocent(webapp.RequestHandler):
    def post(self):
        
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                
                docent = None
                result = db.GqlQuery("SELECT * FROM Docent WHERE docentID = '%s'"%(self.request.get('docentID')))
                
                if result.count()>0:
                    docent = result[0]
                else:
                    docent = entities.Docent()
                
                achterTitels = ['Ad', 'BA', 'BSc', 'LLB', 'MA', 'MSc', 'LLM', 'MPhil', 'RA']
                achterTitel = ''
                for x in achterTitels:
                     achterTitel += self.request.get(x)
                
                aanhefTitels = ['drs.', 'mr.', 'ir.', 'dr.']
                aanhefTitel = ''
                for x in aanhefTitels:
                     aanhefTitel += self.request.get(x)
                                
                
                docent.docentID = self.request.get('docentID')
                docent.aanhef = self.request.get('aanhef')+aanhefTitel
                docent.naam = self.request.get('naam') + achterTitel
                docent.email = self.request.get('email')
                docent.postvaknummer = int(self.request.get('postvaknummer'))
                docent.wachtwoord = self.request.get('wachtwoord')

                docent.put()

                self.redirect('/datastore/adddocentpage')
                
class AddBeheerder(webapp.RequestHandler):
    def post(self):
        
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                
                beheerder = None
                result = db.GqlQuery("SELECT * FROM Beheerder WHERE login = '%s'"%(self.request.get('login')))
                
                if result.count()>0:
                    beheerder = result[0]
                else:
                    beheerder = entities.Beheerder()
                
                beheerder.login = self.request.get('gebruikersnaam')
                beheerder.wachtwoord = self.request.get('wachtwoord')
                beheerder.securityLevel = int(self.request.get('securitylevel'))
                beheerder.beschrijving = self.request.get('beschrijving')

                beheerder.put()
                
                self.redirect('/datastore/addbeheerderpage')

def beheerderIDS():
    result = db.GqlQuery("SELECT * FROM Beheerder")
    ids = []    
    
    for beheerder in result:
        ids.append(beheerder.login)   
    
    ids.sort()
    
    return ids

class addBeheerderPage(webapp.RequestHandler):
    def get(self):
        
        self.response.out.write(webpages.header(get_current_session()))
        self.response.out.write(webpages.cmsHeader())

        id = self.request.get('id')
        beheerder = None

        result = db.GqlQuery("SELECT * FROM Beheerder WHERE login = '%s'"%(id))
        if result.count()>0:
            beheerder = result[0]

        if not beheerder:
            self.response.out.write(webpages.addBeheerderPage(beheerderIDS()))
        else:
            self.response.out.write(webpages.modifyBeheerder(beheerder, beheerderIDS()))
        self.response.out.write(webpages.cmsFooter())
        self.response.out.write(webpages.footer())

def vakken():
    result = db.GqlQuery("SELECT * FROM Vak")
    vakCodes = []    
    
    for vak in result:
        vakCodes.append(vak)   
        
    return vakCodes

class addVakPage(webapp.RequestHandler):
    def get(self):
        
        self.response.out.write(webpages.header(get_current_session()))
        self.response.out.write(webpages.cmsHeader())

        vakCode = self.request.get('id')
        vak = None

        result = db.GqlQuery("SELECT * FROM Vak WHERE vakCode = '%s'"%(vakCode))
        if result.count()>0:
            vak = result[0]

        if not vak:
            self.response.out.write(webpages.addVakPage(vakken()))
        else:
            self.response.out.write(webpages.modifyVak(vak, vakken()))
        self.response.out.write(webpages.cmsFooter())
        self.response.out.write(webpages.footer())

class AddVak(webapp.RequestHandler):
    def post(self):
        
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                
                vak = None
                result = db.GqlQuery("SELECT * FROM Vak WHERE vakCode = '%s'"%(self.request.get('vakcodereal')))
                
                if result.count()>0:
                    vak = result[0]
                else:
                    vak = entities.Vak()
                
                vak.vakCode = self.request.get('vakcode')
                vak.vakNaam = self.request.get('vaknaam')
                
                vak.put()
                
                self.redirect('/datastore/addvakpage')

class addKlasPage(webapp.RequestHandler):
    def get(self):
        
        self.response.out.write(webpages.header(get_current_session()))
        self.response.out.write(webpages.cmsHeader())

        klasCode = self.request.get('klasCode')
        klas = None

        result = db.GqlQuery("SELECT * FROM VakPerKlas WHERE klas = '%s'"%(klasCode))

        if result.count()>0:
            klas = result[0]

        if not klas:
            self.response.out.write(webpages.addKlasPage(klassenLijst(), docentIDS(), vakken()))
        else:
            sendResult = []
            sendResult.extend(result) 
            self.response.out.write(webpages.modifyKlas(klassenLijst(), docentIDS(), vakken(), sendResult))
        self.response.out.write(webpages.cmsFooter())
        self.response.out.write(webpages.footer())

class AddKlas(webapp.RequestHandler):
    def post(self):
        
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                
                 vakPerKlas = db.GqlQuery("SELECT * FROM VakPerKlas WHERE klas = '%s'"%(self.request.get('klas')))
                 vakjes = vakken()
                 
                 filter = []
                 filter.extend(vakPerKlas)
                 
                 x = 0
                 for  vak in vakjes:
                     value = self.request.get(str(x))

                     if value:
                         isNotfound = True
                         
                         for vak in filter:
                            
                            if vak.vakCode == value:
                                filter.remove(vak)
                                isNotfound = False
                                break
                         
                         if isNotfound == True:
                             vakAdd = entities.VakPerKlas()
                             vakAdd.jaargang = self.request.get('jaargang')
                             vakAdd.klas = self.request.get('klas')
                             vakAdd.docentID = self.request.get('docent'+str(x))
                             vakAdd.vakCode = value
                             vakAdd.put()
                     x +=1

                 for vak in filter:
                     vak.delete()

class BeheerderDatastore(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                self.response.out.write(webpages.header(session))
                beheerders = entities.Beheerder.all()
                tableData = []
                for beheerder in beheerders:
                    tableRow = []
                    tableRow.append("<form action='/datastore/beheerderpost' method='post'>")
                    tableRow.append("<input type='text' name='login' value='"+beheerder.login+"' />")
                    tableRow.append("<input type='text' name='beschrijving' value='"+beheerder.beschrijving+"' />")
                    tableRow.append("<input type='text' name='wachtwoord' value='"+beheerder.wachtwoord+"' />")
                    tableRow.append("<input type='text' name='securityLevel' value='"+str(beheerder.securityLevel)+"' />")
                    tableRow.append("<input type='hidden' name='key' value='"+str(beheerder.key())+"'><input type='submit' value='Aanpassen' /></form>")
                    tableRow.append("<form action='/datastore/beheerderpost' method='post'><input type='hidden' name='key' value='"+str(beheerder.key())+"'><input type='hidden' name='delete' value='delete' />")
                    tableRow.append("<input type='submit' value='Verwijderen' /></form>")
                    tableData.append(tableRow)
                self.response.out.write(webpages.table(data=tableData, attributes="class='overzichtTable" ,head=['','login','beschrijving','wachtwoord','securityLevel'],title="Beheerders",divAttr='dataStoreDiv',evenOdd=True))
                self.response.out.write(webpages.footer())
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')
            
class BeheerderDatastorePost(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            if(session.__getitem__('securityLevel') == 2):
                key = self.request.get("key")
                beheerder = db.get(key)
                if(self.request.get("delete") == 'delete'):
                    beheerder.delete()
                    self.redirect('/datastore/beheerder')
                    return
                
                beheerder.login = self.request.get("login")
                beheerder.beschrijving = self.request.get("beschrijving")
                beheerder.wachtwoord = self.request.get("wachtwoord")
                beheerder.securityLevel = int(self.request.get("securityLevel"))
                beheerder.put()
                self.redirect('/datastore/beheerder')
            else:
                self.redirect('/beheerder')
        else:
            self.redirect('/')



class DatastoreRoot(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session.__getitem__('loginType') == 'beheerder'):
            self.response.out.write(webpages.header(session))
            self.response.out.write(webpages.link('/datastore/afspraak',"Afspraak"))
            self.response.out.write(webpages.link('/datastore/docent',"Docent"))
            self.response.out.write(webpages.link('/datastore/vak',"Vak"))
            self.response.out.write(webpages.link('/datastore/vakperklas',"Vak per klas"))
            self.response.out.write(webpages.link('/datastore/leerling',"Leerling"))
            self.response.out.write(webpages.link('/datastore/beheerder',"Beheerder"))
            self.response.out.write(webpages.footer())
        else:
            self.redirect('/')
            
def main():
    application = webapp.WSGIApplication([('/datastore/afspraak', AfspraakDatastore),
                                          ('/datastore/afspraakpost', AfspraakDatastorePost),
                                          ('/datastore/docent', DocentDatastore),
                                          ('/datastore/docentpost', AddDocent),
                                          ('/datastore/vak', VakDatastore),
                                          ('/datastore/vakperklas', VakPerKlasDatastore),
                                          ('/datastore/vakperklaspost', VakPerKlasDatastorePost),
                                          ('/datastore/leerling', LeerlingDatastore),
                                          ('/datastore/leerlingpost', AddStudent),
                                          ('/datastore/beheerderpost', AddBeheerder),
                                          ('/datastore/deletebeheerder', DeleteBeheerder),
                                          ('/datastore/beheerder', BeheerderDatastore),
                                          ('/datastore/addstudentpage', addStudentPage),
                                          ('/datastore/modifystudentpage', addStudentPage),
                                          ('/datastore/adddocentpage', addDocentPage),
                                          ('/datastore/deletestudent', DeleteStudent),
                                          ('/datastore/updatestudent', AddStudent),
                                          ('/datastore/updatedocent', AddDocent),
                                          ('/datastore/addbeheerderpage', addBeheerderPage),
                                          ('/datastore/addvakpage', addVakPage),
                                          ('/datastore/vakpost', AddVak),
                                          ('/datastore/deletevak', DeleteVak),
                                          ('/datastore', DatastoreRoot),
                                          ('/datastore/addklaspage', addKlasPage),
                                          ('/datastore/klaspost', AddKlas)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()