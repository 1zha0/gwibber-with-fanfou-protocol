"""
puny.sl.pt interface for Gwibber
microft (Luis Miguel Braga) - 19/04/2009
"""
import urllib2
import re

PROTOCOL_INFO = {

  "name": "puny.sl.pt",
  "version": 0.1,
  "fqdn" : "http://puny.sl.pt",
  
}

class URLShorter:

  use_utf = False

  def short(self, text):
    response = urllib2.urlopen("http://services.sapo.pt/PunyURL/GetCompressedURLByURL?url=%s" % urllib2.quote(text)).read()
    if self.use_utf:
      p = re.compile(r'.*<puny>(.*)</puny>.*', re.DOTALL)
    else:
      p = re.compile(r'.*<ascii>(.*)</ascii>.*', re.DOTALL)
    return p.sub( r'\1', response) 
