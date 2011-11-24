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



class Main(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        if(session.has_key('id')):
            self.response.out.write(webpages.chatBox(session['id'],"global"))
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
            users.append(session['id'])
            memcache.set(key=roomGet+"Users",value=users)
            
        

def main():
    application = webapp.WSGIApplication([('/chat/', Main), 
                                          ('/chat/ajaxgetmessages', AjaxGetMessages),
                                          ('/chat/ajaxpostmessages', AjaxPostMessages),
                                          ('/chat/ajaxjoin', AjaxJoin),
                                          ('/chat/ajaxgetusers', AjaxGetUsers),
                                          ('/chat/ajaxquit', AjaxQuit)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
