
from __init__ import *

url = 'http://microft.org'

for p in PROTOCOLS.keys():
    print PROTOCOLS[p].URLShorter().short(url)
