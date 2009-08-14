"""

Qaiku interface for Gwibber
SegPhault (Ryan

"""


from . import can, support
import urllib2, urllib, re, simplejson, base64
from gettext import lgettext as _

PROTOCOL_INFO = {
  "name": "Qaiku",
  "version": 0.1,
  
  "config": [
    "private:password",
    "username",
    "message_color",
    "comment_color",
    "receive_enabled",
    "send_enabled"
  ],

  "features": [
    can.SEND,
    can.RECEIVE,
    can.SEARCH,
    can.REPLY,
    #can.RESPONSES,
    can.DELETE,
    can.THREAD,
    can.THREAD_REPLY,
    can.USER_MESSAGES,
  ],
}

NICK_PARSE = re.compile("\B@([A-Za-z0-9_]+|@[A-Za-z0-9_]$)")
HASH_PARSE = re.compile("\B#([A-Za-z0-9_\-]+|@[A-Za-z0-9_\-]$)")

class Message:
  def __init__(self, client, data):
    self.client = client
    self.account = client.account
    self.protocol = client.account["protocol"]
    self.username = client.account["username"]
    self.id = data["id"] or ''
    self.time = support.parse_time(data["created_at"])
    self.is_private  = False

    user = data["user"]
    #self.reply_nick = data["in_reply_to_user_id"]
    self.reply_url = "http://qaiku.com/home/%s/show/%s" % (user["screen_name"], data["id"])
    self.reply_id = data["in_reply_to_status_id"]
    self.bgcolor = "comment_color" if self.reply_id else "message_color"

    self.sender = user["name"]
    self.sender_nick = user["screen_name"]
    self.sender_id = user["id"]
    self.sender_location = user["location"]
    self.sender_followers_count = user["followers_count"]
    self.image = user["profile_image_url"]
    self.url = "http://qaiku.com/home/%s/show/%s" % (user["screen_name"], data["id"])
    self.profile_url = "gwibber:user/%s/%s" % (self.account.id, user["screen_name"])
    self.external_profile_url = user["url"]

    self.text = data["text"]
    self.html_string = '<span class="text">%s</span>' % \
        HASH_PARSE.sub('#<a class="inlinehash" href="gwibber:tag/\\1">\\1</a>',
        NICK_PARSE.sub('@<a class="inlinenick" href="gwibber:user/'+self.account.id+'/\\1">\\1</a>',
        support.linkify(self.text)))
    self.is_reply = re.compile("@%s[\W]+|@%s$" % (self.username, self.username)).search(self.text)
    self.can_thread = True

class Client:
  def __init__(self, acct):
    self.account = acct

  def send_enabled(self):
    return self.account["send_enabled"] and \
      self.account["username"] != None and \
      self.account["private:password"] != None

  def receive_enabled(self):
    return self.account["receive_enabled"] and \
      self.account["username"] != None and \
      self.account["private:password"] != None

  def get_auth(self):
    return "Basic %s" % base64.encodestring(
      ("%s:%s" % (self.account["username"], self.account["private:password"]))).strip()

  def connect(self, url, data = None):
    return urllib2.urlopen(urllib2.Request("http://www.qaiku.com/api" + url,
      data, headers = {"Authorization": self.get_auth()}))

  def get_messages(self):
    return simplejson.load(self.connect("/statuses/friends_timeline.json"))

  def get_user_messages(self, screen_name):
    return simplejson.load(self.connect("/statuses/user_timeline.json" +'?'+
        urllib.urlencode({"screen_name": screen_name})))

  def get_search_data(self, query):
    return simplejson.load(self.connect("/search.json?" +
        urllib.urlencode({"q": query})))

  def get_thread_data(self, msg):
    return simplejson.load(self.connect(
      "/statuses/replies/%s.json" % msg.reply_id or msg.id))

  def get_message_data(self, id):
    return simplejson.load(self.connect(
      "/statuses/show/%s.json" % id))

  def get_thread(self, msg):
    yield Message(self, self.get_message_data(msg.reply_id or msg.id))
    for data in self.get_thread_data(msg):
      yield Message(self, data)

  def search(self, query):
    for data in self.get_search_data(query):
      if data["user"]:
        yield Message(self, data)

  def receive(self):
    for data in self.get_messages():
      if data["user"]:
        yield Message(self, data)

  def user_messages(self, screen_name):
    for data in self.get_user_messages(screen_name):
      yield Message(self, data)

  def delete(self, message):
    return simplejson.load(self.connect(
      "/statuses/destroy/%s.json" % message.id, {}))
  
  def send(self, message):
    data = simplejson.load(self.connect("/statuses/update.json",
      urllib.urlencode({"status":message})))
    return Message(self, data)

  def send_thread(self, message, target):
    data = simplejson.load(self.connect("/statuses/update.json",
      urllib.urlencode({"status":message, "in_reply_to_status_id": target.id})))
    return Message(self, data)

