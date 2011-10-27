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
    count = 0
    afspraakCount = 0;
    for vak in vakken: # voor elk vak in de klas, maak een afspraakTable
        ret += afspraakTable(docentID=vak.docentID,leerlingID=leerlingID,tableCount=count)
        if(ret[-1:] == "1"):
            afspraakCount += 1
            ret = ret[:-1]
        ret += "<input type='hidden' name='klas' value='"+klas+"' />"
        count += 1
    
    ret += "<input type='hidden' id='aantalAfspraken' name='aantalAfspraken' value='"+str(afspraakCount)+"' />"
    ret += "<input type='hidden' name='klas' value='"+klas+"' />"
    ret += "<input type='submit' value='Ok' /></form></div>"
    return ret

def afspraakTable(docentID,aantalTijden=12,leerlingID="1234",tableCount=0): # maak een afspraakTable
    afspraken = db.GqlQuery("SELECT * FROM Afspraak WHERE docentID = '"+docentID+"'") # pak alle afspraken voor de docent
    
    
    oudeAfspraak = False
    for afspraak in afspraken:
        if(afspraak.leerlingID == leerlingID):
            oudeAfspraak = True
            break
    
    """
    
    afspraakTest = None
    ret = "blaat"
    for tmp in oudeAfspraken:
        afspraakTest = tmp
        ret += "blaat"
    ret += "blaat"
    """
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
        return ret
    
    if(afspraken.count() == 0):
        return "<h3>"+docentID+" heeft geen ouderavond ingepland </h3>"
    
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
    ret += "<input type='hidden' name='"+docentID+"_docentIndex' id='"+docentID+"_docentIndex' value='"+str(tableCount)+"' />"
    
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
                #ret += cell("<input type='checkbox' name='checkbox' id='"+docentID+"_"+str(dag)+"_"+str(afspraaknummer)+"' value='afspraak"+str(afspraaknummer)+"' onClick='selectCheckbox(this,"+str(dag)+", "+str(afspraaknummer)+", \""+docentID+"\", \""+str(datums[dag])+"\");'/>", attributes=" ")
                ret += "<td onClick='selectCheckbox(this,"+str(dag)+", "+str(afspraaknummer)+", \""+docentID+"\", \""+str(datums[dag])+"\");' bgcolor=#00FF00> </td>"
                dag += 1
        afspraaknummer += 1
        time += delta # time += 15 minuten
        
    ret += "<tr>"+cell(data="<input style='width:100%'  name='"+docentID+"_beschrijving' type='text' value='Gespreks punt(en)' />", attributes="colspan='100%' ")+"</tr>"
    ret += "</form></table>"
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
    ret = "<form name='plannen' action='/plannenpost' method='post'>"
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
    
def header(bodyAttributes = ""):
    return """<html>
                <body %s>
                    <link rel="stylesheet" type="text/css" href="css/jquery.datepick.css" media="screen" />
                    <script type='text/javascript' src='js/jquery-1.6.4.js'></SCRIPT>
                    <script type='text/javascript' src='js/jquery.datepick.js'></script>
                    <script type='text/javascript' src='js/Afspraak.js'></SCRIPT>
                    <table width='500'>
                        <tr>
                            <td><a href='/'>Home</a></td>
                            <td><a href='/insert'>Insert root</a></td>
                            <td><a href='/plannen'>Ouder avond plannen</a></td>
                        </tr>
                    </table>""" %(bodyAttributes)

def footer():
    return "</body></html>"

def table(data, attributes="",head=None, headAttributes="",title=None):
    ret = "<table "+attributes+" >"
    if(title != None):
        ret += "<tr><td colspan='100%'>"+str(title)+"</td></tr>"
    if(head != None):
        ret += "<tr "+headAttributes+">"
        for item in head:
            ret += "<th>"+str(item)+"</th>"
        ret += "</tr>"
    for tableRow in data:
        ret += row(tableRow)
    ret += "</table>"
    return ret

def row(values,attributes=""):
    ret = "<tr "+attributes+" >"
    for value in values:
        ret += cell(value)
    ret += "</tr>"
    return ret

def cell(data,attributes=""):
    return "<td "+attributes+" >"+str(data.encode('utf-8'))+"</td>"
    