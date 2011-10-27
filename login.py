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

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app


class LoginForm(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""
       <html>
    <head>
    <title>Ouderavondregistratie inlogscherm</title>
    <style type="text/css">
    body
    {
     background-color:#FCF2E6;
    }
    #div-1 {
    position:absolute;
    margin-right:-250px;
    margin-top:-150px;
    top:50%;
    right:50%;
    width:500px;
    height:250px;
    border:5px;
    border: 3px coral solid;
    background-color:#FFE4C4;
    }
    #div-2 {
    position:absolute;
    top:50%;
    right:50%;
    width:125px;
    height:100px;
    margin-right:-63px;
    }
    #test {
    
    }
    p
    {
    font-size:12px;
    text-align:right;
    }
    #test2
    {
    position:absolute;
    width:250px;
    margin-right:0px;
    margin-top:25px;
    }
    h5
    {
    margin-bottom:0px;
    }
    #adres
    {
    float:right;
    margin-right:25px;
    margin-top:25px;
    }
    #photo
    {
    margin-left:25px;
    margin-top:25px;
    float:left;
    }

    </style>
    </head>
    <body>
    <div id="div-1">
        <div id="header">
            <div id="photo"><img src="../images/DKC.png"></div>
            <div id="adres"><p>DONALD KNUTH COLLEGE<br />Scholengemeenschap MAVO/HAVO/VWO<br />Pascalstraat 1<br />2811 EL REEUWIJK<br /></div>
        </div>
        
        <div id="div-2">

        <form action="/authenticate" method="post" name="test">
        <table>
        <tr><td align="center"><h5><i>Ouderavondregistratie</i></h5></td></tr>
        <tr><td align="center"><input type="text" name="emailadres" value="emailadres"></td></tr>
        <tr><td align="center"><input type="password" name=inlogcode value="inlogcode"></td></tr>
        <tr><td align="center"><input type="submit" value="inloggen"></td></tr>
        </table>
        </form>
        </div>
    </div>
    
    </body>
</html> """)
        
def main():
    application = webapp.WSGIApplication([('/', LoginForm)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()     

