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
    ret = "<div><form name='afspraken' action='/afspraakplanningpost' method='post'>"
    for vak in vakken: # voor elk vak in de klas, maak een afspraakTable
        ret += afspraakTable(vak.docentID,leerlingID)
    ret += "<input type='hidden' name='klas' value='"+klas+"' />"
    ret += "<input type='submit' value='Ok' /></form></div>"
    return ret

def afspraakTable(docentID,aantalTijden=12,leerlingID="1234"): # maak een afspraakTable
    afspraken = db.GqlQuery("SELECT * FROM Afspraak WHERE docentID = '"+docentID+"'") # pak alle afspraken voor de docent
    
    oudeAfspraken = db.GqlQuery("SELECT * FROM Afspraak WHERE leerlingID = '"+leerlingID+"' and docentID = '"+docentID+"'") # kijk of deze persoon al een afsrpaak heeft geplanned
    oudeAfspraak = None
    for tmp in oudeAfspraken:
        oudeAfspraak = tmp
    
    if(oudeAfspraak != None): # is er al een afspraak geplanned? laat dan geen schema zien, maar de huidige afspraak met een knop om af te zeggen
        ret = "<table border='1'><tr><th colspan='100%'>"+docentID+"</th></tr>"
        ret += "<tr><th>LeerlingID</th><th>DocentID</th><th>Datum</th><th>Tijd</th><th>Tafelnummer</th><th>Afzeggen</th></tr>"
        ret += "<tr>"+cell(oudeAfspraak.leerlingID)+cell(oudeAfspraak.docentID)+cell(oudeAfspraak.dag)+cell(oudeAfspraak.tijd)+cell(oudeAfspraak.tafelnummer)+cell("<form name='afzeggen_"+docentID+"' action='/afspraakplanningpost' method='post'><input type='hidden' name='afzegkey' value='"+str(oudeAfspraak.key())+"' /><input type='submit' value='Afzeggen' /></form>")+"</tr>"
        ret += "</table>"
        return ret
    
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
    
    ret = "<table border='1'><tr><th colspan='100%'>"+docentID+"</th></tr>"
    ret += "<input type='hidden' name='"+docentID+"_aantalDagen' id='"+docentID+"_aantalDagen' value='"+str(len(datums))+"' />" #aantal dagen, nodig voor javascript
    ret += "<input type='hidden' name='"+docentID+"_aantalTijden' id='"+docentID+"_aantalTijden' value='"+str(aantalTijden)+"' />" #aantal tijden, nodig voor javascript
    ret += "<input type='hidden' name='"+docentID+"_afspraak' id='"+docentID+"_afspraak' value='' />" # belangrijkste data voor post
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
                ret += cell("<input type='checkbox' name='checkbox' id='"+docentID+"_"+str(dag)+"_"+str(afspraaknummer)+"' value='afspraak"+str(afspraaknummer)+"' onClick='selectCheckbox(this,"+str(dag)+", "+str(afspraaknummer)+", \""+docentID+"\", \""+str(datums[dag])+"\");'/>", attributes="bgcolor=#00FF00 ")
                dag += 1
        afspraaknummer += 1
        time += delta # time += 15 minuten
        
    ret += "<tr>"+cell(data="<input style='width:100%' name='"+docentID+"_beschrijving' type='text' value='Gespreks punt(en)' />", attributes="colspan='100% ")+"</tr>"
    ret += "</form></table>"
    return ret

def inList(item, list): #checkt of 'item' in de 'list' zit, zo ja, return de index van het item, nee return -1
    count = 0
    for i in range(len(list)):
        if(item == list[i]):
            return count
        count += 1
    return -1

def insertRootLink(entiteitNaam):
    return "<a href = '/insert/"+entiteitNaam.lower()+"'>"+entiteitNaam+" insert</a><form action='/insert/"+entiteitNaam.lower()+"post' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete all from "+entiteitNaam+"' /></form><br />"
    
def header():
    return """<html>
                <body>
                    <SCRIPT LANGUAGE='JavaScript' SRC='/js/Afspraak.js'></SCRIPT>
                    <table width='500'>
                        <tr>
                            <td><a href='/'>Home</a></td>
                            <td><a href='/insert'>Insert root</a></td>
                        </tr>
                    </table>"""

def footer():
    return "</body></html>"

def cell(data,attributes=""):
    return "<td "+attributes+">"+str(data)+"</td>"
    