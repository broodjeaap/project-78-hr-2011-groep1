#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import cgi
import datetime
import urllib
import wsgiref.handlers
import htmlHelper

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app



def LoginForm(message='&nbsp;'):
        return """
        <html>
            <head>
                <title>Ouderavondregistratie inlogscherm</title>
                <link rel="stylesheet" href="/css/loginpageStyle.css"/>
            </head>
            <body>
            <div id="div-0">
                <div id="div-head">
                    <h3>Login - ouderavondregistratie</h3>
                </div>
                <div id="div-1">
                    <div id="header">
                        <div id="photo"><img src="../images/DKC.png"></div>
                        <div id="adres"><p>DONALD KNUTH COLLEGE<br />Scholengemeenschap MAVO/HAVO/VWO<br />Pascalstraat 1<br />2811 EL REEUWIJK<br /></div>
                    </div>
        
                    <div id="div-2">
                        <form action="/authenticate" method="post">
                            <table>
                                <tr>
                                    <td style="color:red;" colspan="2" align="center">
                                    """+message+"""
                                    </td>
                                </tr>
                                <tr>
                                    <td>Gebruikersnaam</td>
                                    <td align="center">
                                        <input type="text" name="id">
                                    </td>
                                </tr>
                                <tr>
                                    <td>Wachtwoord</td>
                                    <td align="center">
                                        <input type="password" name="wachtwoord">
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>
                                        <input type="submit" value="inloggen">
                                    </td>
                                </tr>
                            </table>
                        </form>
                    </div>
                </div>
            </div> 
            </body>
        </html>
        """

def DocentPage(docent):
        return """
        <html>
            <head>
                <title>Afspraaksysteem docenten</title>
                 <link rel="stylesheet" href="/css/loginpageStyle.css"/>
            </head>
            <body>
                <div id="backboneWrapper">
                    <div>
                        <h1>Welkom,&nbsp;"""+docent.aanhef+"""&nbsp;"""+docent.naam+"""</h1>
                    </div>
                    <div id="contentWrapper">
                        <div id="tableWrapper">
                            """+htmlHelper.afspraakTable(docent.docentID)+"""
                        </div>
                    <div id="buttons">
                        <a href="http://www.google.nl">
                            <input type="submit" value="print"/>
                        </a>
                        <a href="http://www.google.nl">
                            <input type="submit" value="Uitloggen"/>
                        </a>
                    </div>
                </div>
            </body>
        </html>
        """
def LeerlingPage(student):
    return """
    <html>
        <head>
            <link rel="stylesheet" href="/css/loginpageStyle.css"/>
            <title>Afspraaksysteem leerling</title>
        </head>
        <body>
           <div id="backboneWrapper">
               <div>
                   <h1>Welkom, geachte """+student.rolVerzorger+' van '+student.voornaam+' '+student.tussenvoegsel+' '+student.achternaam+"""</h1>
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
    </html>"""
    
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