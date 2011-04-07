"""
u.nu interface for Gwibber
microft (Luis Miguel Braga) - 27/04/2009
"""
import urllib
import urllib2

PROTOCOL_INFO = {

  "name": "u.nu",
  "version": 0.1,
  "fqdn" : "http://u.nu",
  
}

class URLShorter:

  def short(self, text):
    url = "http://u.nu/unu-api-simple"
    values = {
        'url' : text,
        }
    data = urllib.urlencode(values)
    response = urllib2.urlopen( url, data ).read()
    return response.replace('\n','')

