# -*- coding: latin-1 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import memcache
from gaesessions import get_current_session
import datetime
import entities
import webpages
import webpages
import inputFunctions


class ChatRoot(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        rooms = ["global"]
        type = session['loginType']
        if(type == 'leerling'):
            rooms.append("leerlingen")
            leerling = db.GqlQuery("SELECT * FROM Leerling where leerlingID = '"+session['id']+"'")[0]
            rooms.append(leerling.klas)
            klassen = db.GqlQuery("SELECT * FROM VakPerKlas where klas = '"+leerling.klas+"'")
            for klas in klassen:
                rooms.append(klas.vakNaam)
            
        elif(type == 'docent'):
            rooms.append("docenten")
            klassen = db.GqlQuery("SELECT * FROM VakPerKlas where docentID = '"+session['id']+"'")
            for klas in klassen:
                rooms.append(klas.klas)
        elif(type == 'beheerder'):
            rooms.append("leerlingen")
            rooms.append("docenten")
            rooms.append("beheerders")
            vakken = db.GqlQuery("SELECT * FROM Vak")
            for vak in vakken:
                rooms.append(vak.vakNaam)
            tmp = db.GqlQuery("SELECT * FROM VakPerKlas")
            klassen = []
            for klas in tmp:
                if klas not in klassen:
                    klassen.append(klas)
                    rooms.append(klas.klas)
        
        self.response.out.write("<table class='chatTable' id=chatTable'><tr><th> </th><th>Naam: </th><th>Aantal deelnemers: </th><th>Join: </th><tr>")
        for room in rooms:
            users = memcache.get(room+"Users")
            usersInRoom = 0
            if users is not None:
                usersInRoom = len(users)
            self.response.out.write("<td><form action='/chat/chat' method='post'><input type='hidden' name='room' id='room' value="+room+" /></td><td>"+room+"</td><td>"+str(usersInRoom)+"</td><td><input type='submit' value='join' /></td></tr></form>")
        self.response.out.write("</table>")
        self.response.out.write(webpages.footer())

class ChatMain(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        if(session.has_key('id')):
            self.response.out.write(webpages.chatBox(session['id'],self.request.get('room')))
        self.response.out.write(webpages.footer())

class AjaxGetMessages(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session['id'] == self.request.get('id')):
            roomGet = self.request.get('room')
            
            messages = memcache.get(roomGet+"Chat")
            if(messages == None):
                datastoreMessages = db.GqlQuery("SELECT * FROM ChatMessage where room = '"+roomGet+"'")
                messageList = []
                for message in datastoreMessages:
                    messageList.append(message)
                memcache.set(key=roomGet+"Chat",value=messageList)
                messages = messageList
                
            for message in messages:
                self.response.out.write(str(message.time)[:-7]+"-"+message.poster+": "+message.message.replace("_"," ")+"<br />")

class AjaxPostMessages(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session['id'] == self.request.get('id')):
            roomGet = self.request.get('room')
            
            messages = memcache.get(roomGet+"Chat")
            if(messages == None):
                datastoreMessages = db.GqlQuery("SELECT * FROM ChatMessage where room = '"+roomGet+"'")
                messageList = []
                for message in datastoreMessages:
                    messageList.append(message)
                memcache.set(key=roomGet+"Chat",value=messageList)
                messages = messageList
                
            message = entities.ChatMessage(poster=self.request.get('id'),room=roomGet,time=datetime.datetime.now().time(),message=self.request.get('message'))
            db.put_async(message)
            #message.put()
            messages.append(message)
            memcache.set(key=roomGet+"Chat",value=messages)


class AjaxGetUsers(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session['id'] == self.request.get('id')):
            roomGet = self.request.get('room')
            
            users = memcache.get(roomGet+"Users")
            if(users == None):
                users = []
                return
            
            for user in users:
                self.response.out.write(user+"<br />")

class AjaxQuit(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session['id'] == self.request.get('id')):
            roomGet = self.request.get('room')
            
            users = memcache.get(roomGet+"Users")
            if(users == None):
                users = []
            users.remove(session['id'])
            memcache.set(key=roomGet+"Users",value=users)
                
class AjaxJoin(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if(session['id'] == self.request.get('id')):
            roomGet = self.request.get('room')
            
            users = memcache.get(roomGet+"Users")
            if(users == None):
                users = []
            if session['id'] not in users:
                users.append(session['id'])
            memcache.set(key=roomGet+"Users",value=users)
            
        

def main():
    application = webapp.WSGIApplication([('/chat/', ChatRoot), 
                                          ('/chat/chat', ChatMain),
                                          ('/chat/ajaxgetmessages', AjaxGetMessages),
                                          ('/chat/ajaxpostmessages', AjaxPostMessages),
                                          ('/chat/ajaxjoin', AjaxJoin),
                                          ('/chat/ajaxgetusers', AjaxGetUsers),
                                          ('/chat/ajaxquit', AjaxQuit)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
