
"""
Facebook interface for Gwibber
SegPhault (Ryan Paul) - 12/22/2007
"""

from . import can, support
import urllib2, urllib, re, mx.DateTime, simplejson, time

PROTOCOL_INFO = {
  "name": "Facebook",
  "version": 0.1,
  
  "config": [
    "message_color",
    "receive_enabled",
    "send_enabled"
  ],

  "features": [
    can.SEND,
    can.REPLY,
    can.RECEIVE,
    can.THREAD,
    can.THREAD_REPLY,
  ],
}

APP_KEY = "71b85c6d8cb5bbb9f1a3f8bbdcdd4b05"
SECRET_KEY = "41e43c90f429a21e55c7ff67aa0dc201"

class Message:
  def __init__(self, client, data, profiles):
    try:
      self.client = client
      self.account = client.account
      self.protocol = client.account["protocol"]
      self.username = client.account["username"]
      self.data = data

      sender = profiles[data["actor_id"]]
      self.sender = sender["name"]
      self.sender_nick = sender["name"]
      self.sender_id = sender["id"]
      self.profile_url = sender['url']
      self.can_thread = True

      self.url = data['permalink']
      self.id = data["post_id"]
      self.time = mx.DateTime.DateTimeFrom(data['created_time']).gmtime()
      
      if "message" in data:
        self.text = data["message"]
        self.html_string = '<span class="text">%s</span>' % support.linkify(self.text)
      else:
        self.text = data["post_id"]
        self.html_string = ""

      self.bgcolor = "message_color"
      self.image = sender["pic_square"]

      if data["comments"]:
        self.comments = [InlineComment(client, i, profiles) for i in data["comments"]["posts"]]

      if "count" in data["likes"] and data["likes"]["count"] > 0:
        self.liked_by = data["likes"]["count"]

      self.thumbnails = []
      self.extended_text = ""

      if data["attachment"]:
        if "name" in data["attachment"]:
          self.extended_text += "<b>%s</b> " % data["attachment"]["name"]

        if "description" in data["attachment"]:
          self.extended_text += data["attachment"]["description"]

        for m in data["attachment"]["media"]:
          if m["type"] in ["photo", "video", "link"]:
            if m["src"] and m["src"][0] == "/":
              m["src"] = "http://facebook.com" + m["src"]
            self.thumbnails.append(m)

    except Exception:
      from traceback import format_exc
      print(format_exc())

class InlineComment:
  def __init__(self, client, data, profiles):
    self.client = client
    self.account = client.account
    self.protocol = client.account["protocol"]
    self.username = client.account["username"]
    
    sender = profiles[data["fromid"]]
    self.sender = sender["name"]
    self.sender_nick = sender["name"]
    self.sender_id = sender["id"]
    self.profile_url = sender["url"]

    self.text = data["text"] or ""
    self.time = mx.DateTime.DateTimeFrom(data["time"]).gmtime()
    self.id = data["id"]

class Comment:
  def __init__(self, client, data, sender):
    self.client = client
    self.account = client.account
    self.protocol = client.account["protocol"]
    self.username = client.account["username"]
    
    self.sender_id = sender["uid"]
    self.bgcolor = "message_color"
    
    self.sender = sender["name"] or "?" # data["username"]
    self.sender_nick = sender["name"] or "?" #data["username"]

    self.profile_url = sender["profile_url"] or "http://facebook.com"
    self.image = sender["pic_square"] or "http://static.ak.fbcdn.net/pics/t_silhouette.jpg"

    self.text = data["text"]
    self.time = mx.DateTime.DateTimeFrom(data["time"]).gmtime()
    self.id = data["id"]

class Client:
  def __init__(self, acct):
    self.account = acct
    
    self.facebook = support.facelib.Facebook(APP_KEY, SECRET_KEY)
    self.facebook.session_key = self.account["session_key"]
    self.facebook.uid = self.account["session_key"].split('-')[1]
    self.facebook.secret = self.account["private:secret_key"]

  def send_enabled(self):
    return self.account["send_enabled"] and \
      self.account["session_key"] != None and \
      self.account["private:secret_key"] != None

  def receive_enabled(self):
    return self.account["receive_enabled"] and \
      self.account["session_key"] != None and \
      self.account["secret_key"] != None

  def get_thread_data(self, msg):
    user_info = self.facebook.fql.query("SELECT name, profile_url, pic_square, uid FROM user WHERE uid in (SELECT fromid FROM comment WHERE post_id = '%s')" % msg.id)
    comments = self.facebook.stream.getComments(msg.id)
    return {"profiles": user_info, "comments": comments}

  def get_thread(self, msg):
    thread_data = self.get_thread_data(msg)
    yield msg
    
    for msg in thread_data["comments"]:
      for p in thread_data["profiles"]:
        if msg["fromid"] == p["uid"]:
          yield Comment(self, msg, p)

  def get_messages(self):
    return self.facebook.stream.get(self.facebook.uid, limit=80)

  def receive(self):
    stream = self.get_messages()
    profiles = dict((p["id"], p) for p in stream["profiles"])
    for data in stream["posts"]:
      yield Message(self, data, profiles)

  def send(self, message):
    self.facebook.users.setStatus(message, False)

  def send_thread(self, message, target):
    self.facebook.stream.addComment(target.id, message)
