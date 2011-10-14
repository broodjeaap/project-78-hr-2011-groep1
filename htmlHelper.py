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

def klasAfspraakPage(klas,leerlingID="1234"):
    vakken = db.GqlQuery("SELECT * FROM VakPerKlas WHERE klas = '"+klas+"'")
    ret = "<div><form name='afspraken' action='/afspraakplanningpost' method='post'>"
    for vak in vakken:
        ret += afspraakTable(vak.docentID,leerlingID)
    ret += "<input type='hidden' name='klas' value='"+klas+"' />"
    ret += "<input type='submit' value='Ok' /></form></div>"
    return ret

def afspraakTable(docentID,aantalTijden=12,leerlingID="1234"):
    afspraken = db.GqlQuery("SELECT * FROM Afspraak WHERE docentID = '"+docentID+"'")
    
    oudeAfspraken = db.GqlQuery("SELECT * FROM Afspraak WHERE leerlingID = '"+leerlingID+"' and docentID = '"+docentID+"'")
    oudeAfspraak = None
    for tmp in oudeAfspraken:
        oudeAfspraak = tmp
    
    if(oudeAfspraak != None):
        ret = "<table border='1'><tr><th colspan='100%'>"+docentID+"</th></tr>"
        ret += "<tr><th>LeerlingID</th><th>DocentID</th><th>Datum</th><th>Tijd</th><th>Tafelnummer</th><th>Afzeggen</th></tr>"
        ret += "<tr>"+cell(oudeAfspraak.leerlingID)+cell(oudeAfspraak.docentID)+cell(oudeAfspraak.dag)+cell(oudeAfspraak.tijd)+cell(oudeAfspraak.tafelnummer)+cell("<form name='afzeggen_"+docentID+"' action='/afspraakplanningpost' method='post'><input type='hidden' name='afzegkey' value='"+str(oudeAfspraak.key())+"' /><input type='submit' value='Afzeggen' /></form>")+"</tr>"
        ret += "</table>"
        return ret
    
    tijden = []
    datums = []
    for afspraak in afspraken:
        index = inList(afspraak.dag,datums)
        if(index == -1):
            datums.append(afspraak.dag)
            tijden.append([False,False,False,False,False,False,False,False,False,False,False,False])\
            
        if(afspraak.tijd >= 0): 
            tijden[inList(afspraak.dag,datums)][afspraak.tijd] = True
    
    tijden = zip(*tijden)
    
    ret = "<table border='1'><tr><th colspan='100%'>"+docentID+"</th></tr>"
    ret += "<input type='hidden' name='"+docentID+"_aantalDagen' id='"+docentID+"_aantalDagen' value='"+str(len(datums))+"' />"
    ret += "<input type='hidden' name='"+docentID+"_aantalTijden' id='"+docentID+"_aantalTijden' value='"+str(aantalTijden)+"' />"
    ret += "<input type='text' name='"+docentID+"_afspraak' id='"+docentID+"_afspraak' value='' />"
    ret += "<tr><th>Tijd</th>"
    for datum in datums:
        ret += "<th>"+str(datum)+"</th>"
    ret += "</tr>"
    count = 0;
    time = datetime.datetime(2011,1,1,hour=19)
    delta = datetime.timedelta(minutes=15)
    afspraaknummer = 0
    for tijdList in tijden:
        ret += "<tr>"+cell(str(datetime.time(hour=time.hour,minute=time.minute))[:-3])
        dag = 0
        for tijd in tijdList:
            if(tijd):
                ret += cell(data=" ",attributes="bgcolor=#FF0000 ")
                #ret += "<input type='checkbox' name='afspraak_"+docentID+"' value='afspraak"+str(count)+"' disabled='disabled'/>"
            else:
                ret += cell("<input type='checkbox' name='checkbox' id='"+docentID+"_"+str(dag)+"_"+str(afspraaknummer)+"' value='afspraak"+str(afspraaknummer)+"' onClick='selectCheckbox(this,"+str(dag)+", "+str(afspraaknummer)+", \""+docentID+"\", \""+str(datums[dag])+"\");'/>", attributes="bgcolor=#00FF00 ")
                dag += 1
        afspraaknummer += 1
        time += delta
        
    ret += "<tr>"+cell(data="<input style='width:100%' name='"+docentID+"_beschrijving' type='text' value='Gespreks punt(en)' />", attributes="colspan='100% ")+"</tr>"
    ret += "</form></table>"
    return ret

def inList(item, list):
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
    