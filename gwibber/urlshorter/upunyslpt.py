"""
puny.sl.pt unicode interface for Gwibber
microft (Luis Miguel Braga) - 19/04/2009
"""
import punyslpt

PROTOCOL_INFO = {

  "name": "puny.sl.pt (unicode)",
  "version": 0.1,
  "fqdn" : "http://puny.sl.pt",
  
}

class URLShorter( punyslpt.URLShorter):

  use_utf = True

