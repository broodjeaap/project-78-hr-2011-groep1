from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app

import cgi
import datetime
import urllib
import wsgiref.handlers
import htmlHelper

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
        """ %(docent.aanhef, docent.naam, htmlHelper.afspraakTableReadOnly(docent.docentID))
def LeerlingPage(student):
    return """
    <html>
        <head>
            <link rel="stylesheet" href="/css/global.css"/>
            <title>Afspraaksysteem leerling</title>
        </head>
        <body>
           <div id="backboneWrapper">
               <div>
                   <h1>Welkom, geachte %s van %s %s %s</h1>
                </div>
                <div id="contentWrapper">
                    <div id=tableWrapper/>
                    <div id="buttons">
                        <a style="text-decoration:none; href="http://www.google.nl">
                            <input type="submit" value="print"/>
                        </a>
                        <a style="text-decoration:none;" href="http://www.google.nl">
                            <input type="submit" value="Uitloggen"/>
                        </a>
                    </div>
            </div>
        </body>
    </html>""" %(student.rolVerzorger,student.voornaam,student.voornaam,student.tussenvoegsel,student.achternaam)
    
def header(session,bodyAttributes = ""):
    ret = """<html>
                <head>
                    <title>Donald Knuth College</title>
                    <link rel="stylesheet" href="/css/global.css"/>
                    <link rel="stylesheet" type="text/css" href="css/jquery.datepick.css" media="screen" />
                    <script type='text/javascript' src='js/jquery-1.6.4.js'></SCRIPT>
                    <script type='text/javascript' src='js/jquery.datepick.js'></script>
                </head>
                <body %s>
                    <div class='header'>
                        <table id="headerTable">
                            <tr>
                """ %(bodyAttributes)
    if(session.__getitem__('loginType') == 'leerling'):
        ret += "<td><a href='/leerlingafspraak'><div class='headerLink'>Home</div></a></td>"
        ret += "<td><a href='/accountsettings'><div class='headerLink'>Account Settings</div></a></td>"
        ret += "<td><a href='/logout'><div class='headerLink'>Uitloggen</div></a></td>"
    elif(session.__getitem__('loginType') == 'docent'):
        ret += "<td><a href='/docnetafspraak'><div class='headerLink'>Home</div></a></td>"
        ret += "<td><a href='/accountsettings'><div class='headerLink'>Account Settings</div></a></td>"
        ret += "<td><a href='/logout'><div class='headerLink'>Uitloggen</div></a></td>"
    elif(session.__getitem__('loginType') == 'beheerder'):
        if(session.__getitem__('securityLevel') == 0):
            ret += "<td><a href='/beheerder'><div class='headerLink'>Home</div></a></td>"
            ret += "<td><a href='/accountsettings'><div class='headerLink'>Account Settings</div></a></td>"
            ret += "<td><a href='/overzichten'><div class='headerLink'>Overzichten Datastore</div></a></td>"
            ret += "<td><a href='/logout'><div class='headerLink'>Uitloggen</div></a></td>"
        elif(session.__getitem__('securityLevel') == 1):
            ret += "<td><a href='/beheerder'><div class='headerLink'>Home</div></a></td>"
            ret += "<td><a href='/accountsettings'><div class='headerLink'>Account Settings</div></a></td>"
            ret += "<td><a href='/plannen'><div class='headerLink'>Ouder avond plannen</div></a></td>"
            ret += "<td><a href='/logout'><div class='headerLink'>Uitloggen</div></a></td>"
        elif(session.__getitem__('securityLevel') == 2):
            ret += "<td><a href='/beheerder'><div class='headerLink'>Home</div></a></td>"
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