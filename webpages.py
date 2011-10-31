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
    
def header(bodyAttributes = "",title="",homeLink="/"):
    return """<html>
                <head>
                    <title>%s</title>
                    <link rel="stylesheet" href="/css/global.css"/>
                </head>
                <body %s>
                    <link rel="stylesheet" type="text/css" href="css/jquery.datepick.css" media="screen" />
                    <script type='text/javascript' src='js/jquery-1.6.4.js'></SCRIPT>
                    <script type='text/javascript' src='js/jquery.datepick.js'></script>
                    <div class='header'>
                        <table id="headerTable" width='500'>
                            <tr>
                                <td><a href='%s'><div class='headerLink'>Home</div></a></td>
                                <td><a href='/insert'><div class='headerLink'>Insert root</div></a></td>
                                <td><a href='/plannen'><div class='headerLink'>Ouder avond plannen</div></a></td>
                                <td><a href='/accountsettings'><div class='headerLink'>Account Settings</div></a></td>
                                <td><a href='/logout'><div class='headerLink'>Logout</div></a></td>
                            </tr>
                        </table>
                    </div>""" %(str(title),bodyAttributes,homeLink)
                    

def footer():
    return "</body></html>"