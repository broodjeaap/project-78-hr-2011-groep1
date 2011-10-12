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
            ret += "<th>"+str(item)+"</th>"
        ret += "</tr>"
    return ret

def afspraakTable(docentNaam):
    afspraken = db.GqlQuery("SELECT * FROM Afspraak WHERE docent = '"+docentNaam+"'")
    tijden = []
    datums = []
    for afspraak in afspraken:
        index = inList(afspraak.dag,datums)
        if(index == -1):
            datums.append(afspraak.dag)
            tijden.append([False,False,False,False,False,False,False,False,False,False,False,False])\
            
        if(afspraak.tijd != -1): 
            tijden[inList(afspraak.dag,datums)][afspraak.tijd] = True
    
    tijden = zip(*tijden)
    
    ret = "<form action='/' name='"+docentNaam+"'><table border='0'><tr><th colspan='100%'>"+docentNaam+"</th></tr>"
    ret += "<tr><th>Tijd</th>"
    for datum in datums:
        ret += "<th>"+str(datum)+"</th>"
    count = 0;
    time = datetime.datetime(2011,1,1,hour=19)
    delta = datetime.timedelta(minutes=15)
    for tijdList in tijden:
        ret += "<tr><td>"+str(datetime.time(hour=time.hour,minute=time.minute))[:-3]+"</td>"
        for tijd in tijdList:
            
            if(tijd):
                ret += "<td bgcolor=#FF0000>"
                #ret += "<input type='checkbox' name='afspraak_"+docentNaam+"' value='afspraak"+str(count)+"' disabled='disabled'/>"
                ret += "</td>"
            else:
                ret += "<td bgcolor=#00FF00>"
                ret += "<input type='checkbox' name='"+docentNaam+str(count)+"' id='"+docentNaam+str(count)+"' value='afspraak"+str(count)+"' onClick='selectCheckbox(this,"+str(count)+", \""+docentNaam+"\");'/>"
                ret += "</td>"
            count += 1
        time += delta
        
    ret += "<tr ><td colspan='100%'><input type='submit' value='Ok' /></td></tr>"
    ret += "</form></table>"
    return ret

def inList(item, list):
    count = 0
    for i in range(len(list)):
        if(item == list[i]):
            return count
        count += 1
    return -1

def insertLink(entiteitNaam):
    entiteitNaam = entiteitNaam.lower()
    return "<a href = '/insert/"+entiteitNaam+"'>"+entiteitNaam.capitalize()+" insert</a><form action='/insert/"+entiteitNaam+"post' method='post'><input type='hidden' name='delete' value='delete' /><input type='submit' value='Delete all from "+entiteitNaam.capitalize()+"' /></form><br />"
    
    
    