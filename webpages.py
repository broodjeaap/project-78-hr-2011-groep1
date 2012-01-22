from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import mail
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache

import entities
import cgi
import datetime
import urllib
import wsgiref.handlers

def DocentPage(docent):
        return """
            <div id="backboneWrapper">
                <div>
                    <h1>Welkom,&nbsp; %s &nbsp; %s </h1>
                </div>
                <div id="contentWrapper">
                    <div id="tableWrapper">
                        %s
                    </div>
            </div>
        """ %(docent.aanhef, docent.naam, afspraakTableReadOnly(docent.docentID))

def cmsHeader():
    return """
   
           <div id="backboneWrapper">
                <div style="margin-left:231px;">
                   <h1>Content Management System</h1>
                </div>
                
                <div id="CMSnavigation">
                    <ul style="list-style:none;">
                        <li><a style="text-align:left;" class="headerlink" href="/datastore/addstudentpage">Leerling beheer</a></li>
                    </ul>
                 
                </div>
                
                <div id="contentWrapper" style="float:left">"""
    
def cmsFooter():
    return """
                </div>
                <div id="meldingen">
                    <ul id="messages" style="padding-left:20px;">
                    </ul>
                </div>
            </div>"""

                
def header(session,bodyAttributes = ""):
    ret = """
        <html>
                <head>
                    <title>Donald Knuth College</title>
                    <link rel="stylesheet" href="/css/global.css"/>
                    <link rel="stylesheet" type="text/css" href="/css/jquery.datepick.css" media="screen" />
                    <script type='text/javascript' src='/js/jquery-1.7.1.min.js'></SCRIPT>
                    <script type='text/javascript' src='/js/jquery.datepick.js'></script>
                    <script type='text/javascript' src='/js/formulierValidatie.js'></script>
                </head>
                <body %s>
                    <div class='header'>
                        <table id="headerTable">
                            <tr>
                """ %(bodyAttributes)
    if(session.__getitem__('loginType') == 'leerling'):
        ret += "<td><a href='/leerlingafspraak'><div class='headerLink'>Home</div></a></td>"
        ret += "<td><a href='/chat/'><div class='headerLink'>Chat</div></a></td>"
        ret += "<td><a href='/accountsettings'><div class='headerLink'>Account Settings</div></a></td>"
        ret += "<td><a href='/logout'><div class='headerLink'>Uitloggen</div></a></td>"
    elif(session.__getitem__('loginType') == 'docent'):
        ret += "<td><a href='/docnetafspraak'><div class='headerLink'>Home</div></a></td>"
        ret += "<td><a href='/chat/'><div class='headerLink'>Chat</div></a></td>"
        ret += "<td><a href='/accountsettings'><div class='headerLink'>Account Settings</div></a></td>"
        ret += "<td><a href='/logout'><div class='headerLink'>Uitloggen</div></a></td>"
    elif(session.__getitem__('loginType') == 'beheerder'):
        if(session.__getitem__('securityLevel') == 0):
            ret += "<td><a href='/beheerder'><div class='headerLink'>Home</div></a></td>"
            ret += "<td><a href='/chat/'><div class='headerLink'>Chat</div></a></td>"
            ret += "<td><a href='/accountsettings'><div class='headerLink'>Account Settings</div></a></td>"
            ret += "<td><a href='/overzichten'><div class='headerLink'>Overzichten Datastore</div></a></td>"
            ret += "<td><a href='/logout'><div class='headerLink'>Uitloggen</div></a></td>"
            ret += "<td><a href='/stuuremail'><div class='headerLink'>Mail versturen</div></a></td>"
        elif(session.__getitem__('securityLevel') == 1):
            ret += "<td><a href='/beheerder'><div class='headerLink'>Home</div></a></td>"
            ret += "<td><a href='/chat/'><div class='headerLink'>Chat</div></a></td>"
            ret += "<td><a href='/accountsettings'><div class='headerLink'>Account Settings</div></a></td>"
            ret += "<td><a href='/plannen'><div class='headerLink'>Ouder avond plannen</div></a></td>"
            ret += "<td><a href='/logout'><div class='headerLink'>Uitloggen</div></a></td>"
            ret += "<td><a href='/berichtenVersturen'><div class='headerLink'>Berichten versturen</div></a></td>"
        elif(session.__getitem__('securityLevel') == 2):
            ret += "<td><a href='/beheerder'><div class='headerLink'>Home</div></a></td>"
            ret += "<td><a href='/chat/'><div class='headerLink'>Chat</div></a></td>"
            ret += "<td><a href='/accountsettings'><div class='headerLink'>Account Settings</div></a></td>"
            ret += "<td><a href='/plannen'><div class='headerLink'>Ouder avond plannen</div></a></td>"
            ret += "<td><a href='/insert'><div class='headerLink'>Insert Root</div></a></td>"
            ret += "<td><a href='/overzichten'><div class='headerLink'>Overzichten Datastore</div></a></td>"
            ret += "<td><a href='/datastore'><div class='headerLink'>Aanpassen Datastore</div></a></td>"
            ret += "<td><a href='/logout'><div class='headerLink'>Uitloggen</div></a></td>"
    else:
        pass
    ret +="""
                            </tr>
                        </table>
                    </div>"""
    return ret

def footer():
    return "</body></html>"

from google.appengine.ext import db
import datetime

def startTable(header=None, tableStart=True,border=True):
    ret = "";
    if(tableStart):
        if(border):
            ret += "<table border='1'>"
        else:
            ret += "<table>"
    
    if(header != None):
        ret += "<tr>"
        for item in header:
            ret += cell(item)
        ret += "</tr>"
    return ret

def klasAfspraakPage(klas,leerlingID="1234"): #maak voor een klas alle afspraak tabellen aan
    vakken = db.GqlQuery("SELECT * FROM VakPerKlas WHERE klas = '"+klas+"'") # pak alle vakken van een klas
    ret = "<div><script type='text/javascript' src='js/LeerlingAfspraak.js'></SCRIPT>"
    count = 0
    afspraakCount = 0;
    hiddenInputs = []
    for vak in vakken: # voor elk vak in de klas, maak een afspraakTable
        afspraakFunctieReturn = afspraakTable(docentID=vak.docentID,leerlingID=leerlingID,tableCount=count)
        
        if(len(afspraakFunctieReturn) == 2):
            hiddenInputs.append(afspraakFunctieReturn[1])
        ret += "<div class='afspraakDivLeerling'><div class='leerlingTableHeader' onclick=\"afspraakToggle('"+vak.vakCode+"')\">"+getKlasNaam(vak.vakCode)+"</div><div class='toggle_afspraak' id='"+vak.vakCode+"_toggle' >"
        ret += afspraakFunctieReturn[0]
        
        if(ret[-1:] == "1"):
            afspraakCount += 1
            ret = ret[:-1]
        ret += "</div></div>"
        ret += "<input type='hidden' name='klas' value='"+klas+"' />"
        count += 1
    ret += "<form name='afspraken' action='/afspraakplanningpost' method='post' id='leerlingAfspraakForm'>"
    for hiddenInput in hiddenInputs:
        ret += hiddenInput
    ret += "<input type='hidden' id='aantalAfspraken' name='aantalAfspraken' value='"+str(afspraakCount)+"' />"
    ret += "<input type='hidden' name='klas' value='"+klas+"' />"
    ret += "<input type='submit' value='Ok'  /></form></div>"
    return ret

def afspraakTable(docentID,aantalTijden=12,leerlingID="1234",tableCount=0): # maak een afspraakTable
    afspraken = db.GqlQuery("SELECT * FROM Afspraak WHERE docentID = '"+docentID+"'") # pak alle afspraken voor de docent

    oudeAfspraak = False
    for afspraak in afspraken:
        if(afspraak.leerlingID == leerlingID):
            oudeAfspraak = True
            break
    if(oudeAfspraak): # is er al een afspraak geplanned? laat dan geen schema zien, maar de huidige afspraak met een knop om af te zeggen
        afspraakTable = []
        tableRow = []
        oudeAfspraken = db.GqlQuery("SELECT * FROM Afspraak WHERE leerlingID = '"+leerlingID+"' and docentID = '"+docentID+"'") # kijk of deze persoon al een afsrpaak heeft geplanned
        oudeAfspraak = oudeAfspraken[0]
        tableRow.append(oudeAfspraak.leerlingID)
        tableRow.append(oudeAfspraak.docentID)
        tableRow.append(oudeAfspraak.dag)
        tableRow.append(oudeAfspraak.tijd)
        tableRow.append(oudeAfspraak.tafelnummer)
        tableRow.append("<form name='afzeggen_"+docentID+"' action='/afspraakplanningpost' method='post'><input type='hidden' name='afzegkey' value='"+str(oudeAfspraak.key())+"' /><input type='submit' value='Afzeggen' /></form>")
        afspraakTable.append(tableRow)
        ret = table(afspraakTable, attributes="border='1'", head=["LeerlingID","DocentID","Datum","Tijd","Tafelnummer","Afzeggen"])
        ret += "1" #yeah... uuh...
        ret = [ret]
        return ret
    
    if(afspraken.count() == 0):
        return ["<div class='GeenOuderAvondText'>"+docentID+" heeft geen ouderavond ingepland </div>"]
    
    tijden = []
    datums = []
    for afspraak in afspraken: # aanmaken van het 2d afspraken array
        index = inList(afspraak.dag,datums) # zit de datum al in de datums array
        if(index == -1): # nee? voeg em toe + een extra regel van booleans
            datums.append(afspraak.dag)
            tijden.append([False,False,False,False,False,False,False,False,False,False,False,False])\
            
        if(afspraak.tijd >= 0): # zet de afspraak op True in de afspraken array
            tijden[inList(afspraak.dag,datums)][afspraak.tijd] = True
    
    tijden = zip(*tijden) # transponeer de matrix
    
    ret = "<table border='1' class='afspraakTable'><tr><th colspan='100%'>Ouderavond rooster van:&nbsp;"+docentID+"</th></tr>"
    ret += "<input type='hidden' name='"+docentID+"_aantalDagen' id='"+docentID+"_aantalDagen' value='"+str(len(datums))+"' />" #aantal dagen, nodig voor javascript
    ret += "<input type='hidden' name='"+docentID+"_aantalTijden' id='"+docentID+"_aantalTijden' value='"+str(aantalTijden)+"' />" #aantal tijden, nodig voor javascript
    ret += "<input type='hidden' name='"+docentID+"_docentIndex' id='"+docentID+"_docentIndex' value='"+str(tableCount)+"' />"
    
    #ret += "<input type='hidden' name='"+docentID+"_afspraak' id='"+docentID+"_afspraak' value='' />" # belangrijkste data voor post
    ret += "<tr><th>Tijd</th>"
    for datum in datums: #print alle datums uit
        ret += "<th>"+str(datum)+"</th>"
    ret += "</tr>"
    count = 0;
    time = datetime.datetime(2011,1,1,hour=19) #start tijd van de ouderavond
    delta = datetime.timedelta(minutes=15) #tijd die nodig is voor elke afspraak
    afspraaknummer = 0
    for tijdList in tijden: # outer loop voor 2d tijden matrix
        ret += "<tr>"+cell(str(datetime.time(hour=time.hour,minute=time.minute))[:-3])
        dag = 0
        for tijd in tijdList: # inner loop voor 2d tijden matrix
            if(tijd):
                ret += cell(data=" ",attributes="bgcolor=#FF0000 ")
                #ret += "<input type='checkbox' name='afspraak_"+docentID+"' value='afspraak"+str(count)+"' disabled='disabled'/>"
            else:
                #ret += cell("<input type='checkbox' name='checkbox' id='"+docentID+"_"+str(dag)+"_"+str(afspraaknummer)+"' value='afspraak"+str(afspraaknummer)+"' onClick='selectCheckbox(this,"+str(dag)+", "+str(afspraaknummer)+", \""+docentID+"\", \""+str(datums[dag])+"\");'/>", attributes=" ")
                ret += "<td onClick='selectCheckbox(this,"+str(dag)+", "+str(afspraaknummer)+", \""+docentID+"\", \""+str(datums[dag])+"\");' bgcolor=#00FF00> </td>"
            dag += 1
        afspraaknummer += 1
        time += delta # time += 15 minuten
        
    ret += "<tr>"+cell(data="<textarea class='leerlingBeschrijving'  name='"+docentID+"_beschrijving' type='textarea' onChange=\"parseBeschrijving(this,'"+docentID+"')\" >Gespreks punt(en)</textarea>", attributes="colspan='100%' ")+"</tr>"
    ret += "</form></table>"
    ret = [ret, "<input type='hidden' name='"+docentID+"_afspraak' id='"+docentID+"_afspraak' value='' /> <input type='hidden' name='"+docentID+"_hidden_beschrijving' id='"+docentID+"_hidden_beschrijving' />"]
    return ret

def afspraakTableReadOnly(docentID="BAARR"):
    afspraken = db.GqlQuery("SELECT * FROM Afspraak WHERE docentID = '"+docentID+"'")
    if(afspraken.count() == 0):
        return "<h3>"+docentID+" heeft geen ouderavond ingepland </h3>"
    tijden = []
    datums = []
    echteAfspraken = []
    for afspraak in afspraken: # aanmaken van het 2d afspraken array
        index = inList(afspraak.dag,datums) # zit de datum al in de datums array
        if(index == -1): # nee? voeg em toe + een extra regel van booleans
            datums.append(afspraak.dag)
            tijden.append([False,False,False,False,False,False,False,False,False,False,False,False])\
            
        if(afspraak.tijd >= 0): # zet de afspraak op True in de afspraken array
            tijden[inList(afspraak.dag,datums)][afspraak.tijd] = True
            echteAfspraken.append(afspraak)
    
    tijden = zip(*tijden) # transponeer de matrix
    ret = "<script type='text/javascript' src='js/DocentAfspraak.js'></script><script type='text/javascript' src='js/jquery-1.6.4.js'></SCRIPT><div class='afspraakDivDocent'><table border='1' class='afspraakTable'><tr><th colspan='100%'>Ouderavond rooster van:&nbsp;"+docentID+"</th></tr>"
    ret += "<tr><th>Tijd</th>"
    for datum in datums: #print alle datums uit
        ret += "<th>"+str(datum)+"</th>"
    ret += "</tr>"
    count = 0;
    time = datetime.datetime(2011,1,1,hour=19) #start tijd van de ouderavond
    delta = datetime.timedelta(minutes=15) #tijd die nodig is voor elke afspraak
    afspraakCounter = 0
    for tijdList in tijden: # outer loop voor 2d tijden matrix
        ret += "<tr>"+cell(str(datetime.time(hour=time.hour,minute=time.minute))[:-3])
        dag = 0
        for tijd in tijdList: # inner loop voor 2d tijden matrix
            if(tijd):
                functie = "\"showAfspraak('"+echteAfspraken[afspraakCounter].leerlingID+"','"+str(echteAfspraken[afspraakCounter].dag)+"','"+str(echteAfspraken[afspraakCounter].tijd)+"','"+str(echteAfspraken[afspraakCounter].tafelnummer)+"','"+echteAfspraken[afspraakCounter].beschrijving+"')\""
                #ret += functie
                ret += cell(data=" ",attributes="bgcolor=#FF0000 onMouseOver="+functie)
                afspraakCounter += 1
            else:
                ret += cell(data=" ",attributes="bgcolor=#00FF00")
                dag += 1
                #showAfspraak(leerlingID,dag,tijd,tafelnummer,beschrijving)
        time += delta # time += 15 minuten
        
    ret += "</form></table>"
    ret += "<table class='afspraakTable' style='width:425px;'>"
    ret += "<tr><td><b>LeerlingID</b></td><td id='leerlingID'></td></tr>"
    ret += "<tr><td><b>Dag</b></td><td id='dag'></td></tr>"
    ret += "<tr><td><b>Tijd</b></td><td id='tijd'></td></tr>"
    ret += "<tr><td><b>Tafelnummer</b></td><td id='tafelnummer'></td></tr>"
    ret += "<tr><td><b>Beschrijving</b></td><td id='beschrijving'></td></tr>"
    ret += "</table></div>"
    return ret
    
def inList(item, list): #checkt of 'item' in de 'list' zit, zo ja, return de index van het item, nee return -1
    count = 0
    for i in range(len(list)):
        if(item == list[i]):
            return count
        count += 1
    return -1

def planningPage():
    docentTable = []
    tableRow = []
    ret = "<script type='text/javascript' src='js/OuderAvondPlannen.js'></SCRIPT><form name='plannen' action='/plannenpost' method='post'>"
    ret += "<input type='hidden' name='checkedDocenten' id='checkedDocenten' value='' />"
    tableRow.append("""<input type='text' name='datums' id='datepicker' />
                <script type="text/javascript">
                    $('#datepicker').datepick({
                    multiSelect: 999,
                    dateFormat: 'yyyy-mm-dd',
                    showTrigger: '#calImg', 
                    monthsToShow: 3, 
                    monthsToStep: 3, 
                    prevText: 'Prev months', 
                    nextText: 'Next months'});
                </script>""")
    tableRow.append("<input type='submit' value='Ok'>")
    docentTable.append(tableRow)
    
    tableRow = []
    tableRow.append("<h3>Select All</h3>")
    tableRow.append("<input type='checkbox' name='select_all' id='select_all' value='select_all' />")
    docentTable.append(tableRow)
    
    docenten = db.GqlQuery("SELECT * FROM Docent")
    for docent in docenten:
        tableRow = []
        tableRow.append(docent.naam)
        tableRow.append("<input type='checkbox' name='docent_planning_checkbox' id='"+docent.docentID+"_planning_checkbox' docentCheckBox='true' value='"+docent.docentID+"' />")
        docentTable.append(tableRow)
    
    ret += table(docentTable,attributes="border='1'",title="Ouder avond plannen")
    ret += "</form>"
    return ret

def insertRootLink(entiteitNaam):
    return "<a href = '/insert/"+entiteitNaam.lower()+"'>"+entiteitNaam+" insert</a><form action='/insert/"+entiteitNaam.lower()+"post' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete all from "+entiteitNaam+"' /></form><br />"

def table(data, attributes="",head=None, headAttributes="",title=None,divAttr='',evenOdd=False):
    ret = "<div class="+divAttr+"><table "+attributes+" >"
    if(title != None):
        ret += "<tr><td colspan='100%'>"+str(title)+"</td></tr>"
    if(head != None):
        ret += "<tr "+headAttributes+">"
        for item in head:
            ret += "<th>"+str(item)+"</th>"
        ret += "</tr>"
    if(evenOdd):
        even = False
        for tableRow in data:
            if(even):
                ret += row(tableRow,attributes="class='odd'")
                even = False
            else:
                ret += row(tableRow,attributes="class='even'")
                even = True
    else:
        for tableRow in data:
            ret += row(tableRow)
        
    ret += "</table></div>"
    return ret

def row(values,attributes=""):
    ret = "<tr "+attributes+" >"
    for value in values:
        ret += cell(value)
    ret += "</tr>"
    return ret

def cell(data,attributes=""):
    ret = ""
    try:
      ret = "<td "+attributes+" >"+str(data)+"</td>"
    except: 
      ret = "<td "+attributes+" >"+str(data.encode('utf-8'))+"</td>"
    return ret

def link(href,text):
    return "<a href='"+href+"' >"+text+"</a>"

def chatBox(id,room="global"):
    ret = """ <script type='text/javascript' src='/js/Chat.js'></script>
                                        <div class='chatDiv' id='chatDiv'>
                                            <div class='chatHeader' id='chatHeader'>
                                                Chatting in %s
                                            </div>
                                            <div class='userSpace' id='userSpace'>

                                            </div>
                                            <div class='chatSpace' id='chatSpace'>
                                                
                                            </div>
                                            <div class='chatControls' id='chatControls'>
                                                <table width='450px'>
                                                    <tr>
                                                        <td>
                                                            <input type='hidden' name='id' id='id' value='%s' />
                                                            <input type='hidden' name='room' id='room' value='%s' />
                                                        </td>
                                                        <td>
                                                            <input type='text' size='60' id='chatTextBox' />
                                                        </td> 
                                                        <td>
                                                            <img src="/images/chatSend.png" alt="send" onclick='send();'/>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </div>
                                        </div> 
                                        """ %(room,id,room)
    return ret

def getKlasNaam(vakCode):
    klassen = memcache.get("klassen")
    if(klassen == None):
        klassen = []
        datastoreVak = entities.Vak.all()
        for vak in datastoreVak:
            klassen.append(vak)
    for klas in klassen:
        if(klas.vakCode == vakCode):
            return klas.vakNaam
    return "Null"

def addStudent(leerlingID, leerlingIDS=[], klassen=[]):
    cmsPage = """
    
       <div id="tableFormWrapper" style="width:882; margin:50px auto;">
        <div style=" float:left; border:1px solid black; width:214px; height:440px; padding:5px;">
            Voor het
            <ul style="margin:3px;">
                <li>Weergeven</li>
                <li>aanpassen</li>
                <li> of verwijderen</li>
            </ul>
            van een leerling, selecteer een ID
            <form method="get" action="/datastore/addstudentpage">        
                <select  name='id' onChange="submitForm(this.form)" style="margin:5px 80px;">
                    <option  value=""></option>"""
    for id in leerlingIDS:
        cmsPage += "<option value=" + id +">" + id +"</option>"
            
    cmsPage += """"</select></form>
         </div>
        
        
            <form action="/datastore/leerlingpost" method="post">
                <div style="float:left; border:1px solid black; margin-left:25px; width:300px; height:450px;">
            <table>
            <tr>
                <th colspan="2" style="text-align:left;">Gegevens ouder /verzorger</th>
            </tr>
            <tr>
                <td colspan="2">&nbsp;</td>
            </tr>
            <tr>
                <td></td>
                <td>
                    dhr.    <input type="radio" name="aanhefVerzorger" value="dhr."/>
                    mw.        <input type="radio" name="aanhefVerzorger" value="mw."/>
                </td>
            </tr>
            <tr>
                <td>initialen</td>
                <td>
                    <input type="text" name="initialenVerzorger"/>
                </td>
            </tr>
            <tr>
                <td>tussenvoegsel</td>
                <td>
                    <input type="text" name="tussenvoegselVerzorger"/>
                </td>
            </tr>
            <tr>
                <td>achternaam</td>
                <td>
                    <input type="text" name="achternaamVerzorger" />
                </td>
            </tr>
            <tr>
                <td>rol</td>
                <td>
                    <select name="rolVerzorger">
                        <option></option>
                        <option value="ouder">ouder</option>
                        <option value="voogd">voogd</option>
                    </select>
            </tr>
            <tr>
                <td colspan="2">&nbsp;</td>
            </tr>
             <tr>
                <th colspan="2" style="text-align:left;">Contact gegevens</th>
            </tr>
            <tr>
                <td colspan="2">&nbsp;</td>
            </tr>
            <tr>
                <td>adres</td>
                <td>
                    <input type="text" style="margin-right:4px;" size="13" name="adres">
                    <input type="text" size="2" name="huisnummer" style="">
                </td>
            </tr>
            <tr>
                <td>postcode</td>
                <td>
                    <input type="text" name="postcode"/>
                </td>
            </tr>
            <tr>
                <td>woonplaats</td>
                <td>
                    <input type="text" name="woonplaats" />
                </td>
            </tr>
            <tr>
                <td>e-mailadres</td>
                <td>
                    <input type="text" name="email" />
                </td>
            </tr>
            <tr>
                <td>telefoon vast</td>
                <td>
                    <input type="text" name="telefoon_vast" />
                </td>
            </tr>
            <tr>
                <td>mobiel</td>
                <td>
                    <input type="text" name="mobiel" />
                </td>
            </tr>
            </table>
            </div>
            <div style="float:left; margin-bottom:5px; margin-left:25px; border:1px solid black; width:300px; height:450px">
            <table>
              <tr>
                <th colspan="2" style="text-align:left;">Gegevens leerling</th>
            </tr>
            <tr>
                <td colspan="2">&nbsp;</td>
            </tr>
            <tr>
                <td>geslacht</td>
                <td>
                    man        <input type="radio" name="geslacht" value="man"/>
                    vrouw    <input type="radio" name="geslacht" value="vrouw"/>
                </td>
            </tr>
            <tr>
                <td>voornaam</td> 
                <td><input type="text" name="voornaam"/></td>
            </tr>
            <tr>
                <td>tussenvoegsel</td> 
                <td><input type="text" name="tussenvoegsel" /></td>
            </tr>
            <tr>
                <td>achternaam</td> 
                <td><input type="text" name="achternaam" /></td>
            </tr>
             <tr>
                <td>klas</td> 
                <td>
                    <select name="klas">
                        <option></option>"""
    for klas in klassen:
        cmsPage += "<option>" + klas +"</option>"
    
                    
    cmsPage += """"</select></td>
            </tr>
            <tr>
                <td colspan="2">&nbsp;</td>
            </tr>
             <tr>
                <th colspan="2" style="text-align:left;">Account gegevens</th>
            </tr>
            <tr>
                <td colspan="2">&nbsp;</td>
            </tr>
            <tr>
                <td>leerlingID</td> 
                <td><input type="text" value="%s" disabled="disabled" /><input type="hidden" name="leerlingID" value="%s"/></td>
            </tr>
            <tr>
                <td>wachtwoord</td> 
                <td><input type="password" name="wachtwoord" /></td>
            </tr>
            <tr>
                <td>wachtwoord 2x</td> 
                <td><input type="password" name="password" /></td>
            </tr>
             </table>
             
            </div>
            <div style="text-align:right; clear:both; height:25px; width:882px;">
                <input type="button" value="Toevoegen" onClick="formulierCheck(this.form)"/>
            </div>
        </form>
    </div>"""%(leerlingID, leerlingID)
    return cmsPage

def modifyStudent(leerling, leerlingIDS=[],klassen=[]):
    cmsPage = """
    
     <div id="tableFormWrapper" style="width:882; margin:50px auto;">
        <div style=" float:left; border:1px solid black; width:214px; height:440px; padding:5px;">
            Voor het
            <ul style="margin:3px;">
                <li>Weergeven</li>
                <li>aanpassen</li>
                <li> of verwijderen</li>
            </ul>
            van een leerling, selecteer een ID
        <form method="get" action="/datastore/addstudentpage">                 
                <select  name='id' onChange="submitForm(this.form)" style="margin:5px 80px;">
                    <option  value=""></option>"""
    for id in leerlingIDS:
        if(leerling.leerlingID == id):
            cmsPage += "<option selected='true' value=" + id +">" + id +"</option>"
        else: cmsPage += "<option value=" + id +">" + id +"</option>"
    
                    
    cmsPage += """"</select>
    </form>
         </div>
        
            <form id='formAction' method="post">
                <div style="float:left; border:1px solid black; margin-left:25px; width:300px; height:450px;">
            <table>
            <tr>
                <th colspan="2" style="text-align:left;">Gegevens ouder /verzorger</th>
            </tr>
            <tr>
                <td colspan="2">&nbsp;</td>
            </tr>
            <tr>
                <td></td>"""
    if(leerling.aanhefVerzorger == 'dhr.'):
        cmsPage += """ 
                <td>
                    dhr.    <input checked="true" type="radio" name="aanhefVerzorger" value="dhr."/>
                    mw.        <input type="radio" name="aanhefVerzorger" value="mw."/>
                </td>"""
    else: 
        
        cmsPage += """ 
                <td>
                    dhr.    <input type="radio" name="aanhefVerzorger" value="dhr."/>
                    mw.        <input checked="true"  type="radio" name="aanhefVerzorger" value="mw."/>
                </td>"""
                
    cmsPage += """      
            </tr>
            <tr>
                <td>initialen</td>
                <td>
                    <input type="text" name="initialenVerzorger" value="%s"/>
                </td>
            </tr>
            <tr>
                <td>tussenvoegsel</td>
                <td>
                    <input type="text" name="tussenvoegselVerzorger value="%s""/>
                </td>
            </tr>
            <tr>
                <td>achternaam</td>
                <td>
                    <input type="text" name="achternaamVerzorger" value="%s"/>
                </td>
            </tr>
            <tr>
                <td>rol</td>
                <td>
                    <select name="rolVerzorger">
                        <option></option>"""%(leerling.initialenVerzorger, leerling.voorvoegselsVerzorger, leerling.achternaamVerzorger)
    if(leerling.rolVerzorger == 'ouder'):
         cmsPage += """<option selected='true' value='ouder'>ouder</option>
                       <option value='voogd'>voogd</option>"""
         
    else:
         cmsPage += """<option value='ouder'>ouder</option>"
                        <option selected='true' value='voogd'>voogd</option>"""
                    
                    
    cmsPage += """
         </select>
            </tr>
            <tr>
                <td colspan="2">&nbsp;</td>
            </tr>
            <tr>
                <th colspan="2" style="text-align:left;">Contact gegevens</th>
            </tr>
            <tr>
                <td colspan="2">&nbsp;</td>
            </tr>
            <tr>
                <td>adres</td>
                <td>
                    <input type="text" style="margin-right:4px;" size="13" name="adres" value="%s">
                    <input type="text" size="2" name="huisnummer" value="%s">
                </td>
            </tr>
            <tr>
                <td>postcode</td>
                <td>
                    <input type="text" name="postcode" value='%s'/>
                </td>
            </tr>
            <tr>
                <td>woonplaats</td>
                <td>
                    <input type="text" name="woonplaats" value='%s' />
                </td>
            </tr>
            <tr>
                <td>e-mailadres</td>
                <td>
                    <input type="text" name="email" value='%s' />
                </td>
            </tr>
            <tr>
                <td>telefoon vast</td>
                <td>
                    <input type="text" name="telefoon_vast" value='%s' />
                </td>
            </tr>
            <tr>
                <td>mobiel</td>
                <td>
                    <input type="text" name="mobiel" value="%s" />
                </td>
            </tr>
            </table>
            </div>
            <div style="float:left; margin-bottom:5px; margin-left:25px; border:1px solid black; width:300px; height:450px">
            <table>
              <tr>
                <th colspan="2" style="text-align:left;">Gegevens leerling</th>
            </tr>
            <tr>
                <td colspan="2">&nbsp;</td>
            </tr>
            <tr>
                <td>geslacht</td>"""%(leerling.adres, leerling.huisnummer, leerling.postcode, leerling.woonplaats, leerling.email, leerling.vastnummer, leerling.mobielnummer )
                
    if(leerling.geslacht == "M"):
        cmsPage += """ 
                  <td>
                    man       <input checked='true' type="radio" name="geslacht" value="M"/>
                    vrouw    <input type="radio" name="geslacht" value="V"/>
                </td>"""
    else: 
        
        cmsPage += """ 
                <td>
                    man       <input  type="radio" name="geslacht" value="M"/>
                    vrouw    <input checked='true' type="radio" name="geslacht" value="V"/>
                </td>"""
                
                
                
              
    cmsPage += """</tr>
            <tr>
                <td>voornaam</td> 
                <td><input type="text" name="voornaam" value="%s"/></td>
            </tr>
            <tr>
                <td>tussenvoegsel</td> 
                <td><input type="text" name="tussenvoegsel" value="%s" /></td>
            </tr>
            <tr>
                <td>achternaam</td> 
                <td><input type="text" name="achternaam" value="%s" /></td>
            </tr>
             <tr>
                <td>klas</td> 
                <td>
                    <select name="klas">
                        <option></option>"""%(leerling.voornaam, leerling.tussenvoegsel, leerling.achternaam)
    for klas in klassen:
        if(klas == leerling.klas):
            cmsPage += "<option selected='true'>" + klas +"</option>"
        else:
            cmsPage += "<option>" + klas +"</option>"
    
                    
    cmsPage += """"</select></td>
            </tr>
            <tr>
                <td colspan="2">&nbsp;</td>
            </tr>
             <tr>
                <th colspan="2" style="text-align:left;">Account gegevens</th>
            </tr>
            <tr>
                <td colspan="2">&nbsp;</td>
            </tr>
            <tr>
                <td>leerlingID</td> 
                <td><input type="text" value="%s" disabled="disabled" /><input type="hidden" name="leerlingID" value="%s"/></td>
            </tr>
            <tr>
                <td>wachtwoord</td> 
                <td><input type="password" name="wachtwoord" value="%s" /></td>
            </tr>
            <tr>
                <td>wachtwoord 2x</td> 
                <td><input type="password" name="password" value="%s"/></td>
            </tr>
             </table>
             
            </div>
            <div style="text-align:right; clear:both; height:25px; width:882px;">
                <input type="button" value="Verwijderen" onClick="deleteForm(this.form)"/>
                <input type="button" value="aanpassen" onClick="updateForm(this.form)"/>
            </div>
        </form>
    </div>"""%(leerling.leerlingID, leerling.leerlingID, leerling.wachtwoord, leerling.wachtwoord)
    return cmsPage












