#!/usr/bin/env python
#
# setup.py for gnuConcept

from distutils.core import setup
from DistUtilsExtra.command import *
from glob import glob

setup(name="gwibber",
      version="1.2.0",
      author="Ryan Paul",
      author_email="segphault@arstechnica.com",
      url="http://launchpad.net/gwibber/",
      license="GNU General Public License (GPL)",
      packages=['gwibber', 'gwibber.microblog',
          'gwibber.microblog.support', 'gwibber.urlshorter'],
      data_files=[
    ('share/gwibber/ui/', glob("ui/*.glade")),
    ('share/gwibber/ui/', glob("ui/*.png")),
    ('share/gwibber/ui/templates/', glob("ui/templates/*.mako")),
    ('share/gwibber/ui/themes/bluelines', glob("ui/themes/bluelines/*")),
    ('share/gwibber/ui/themes/gwilouche', glob("ui/themes/gwilouche/*")),
    ('share/gwibber/ui/themes/dark-gwilouche', glob("ui/themes/dark-gwilouche/*")),
    ('share/gwibber/ui', ['ui/progress.gif']),
    ('share/gwibber/ui', ['ui/gwibber.svg']),
    ('share/pixmaps', ['ui/gwibber.svg'])
    ],
      scripts=['bin/gwibber'],
      cmdclass = { "build" :  build_extra.build_extra,
                   "build_i18n" :  build_i18n.build_i18n,
                   "build_help" :  build_help.build_help,
                   "build_icons" :  build_icons.build_icons
                 }
)
