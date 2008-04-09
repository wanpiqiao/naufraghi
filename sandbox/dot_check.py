#!/usr/bin/python

import os, os.path, sys
import urllib
import md5, base64
import re

os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

pages = [("http://www4.unifi.it/studenti/CMpro-v-p-385.html", ["id=\"[a-z\-0-9]*\""]),
         ("http://didattica.polito.it/pls/portal30/sviluppo.scudo.dott?li=IT&cod=204", []),
         ("http://didattica.polito.it/scudo/Esami_accesso.html", []),
         ]

for page, ignore in pages:
    filename = ".%s.md5" % page.replace(":", ".").replace("/", "_")

    text = urllib.urlopen(page).read()
    for pattern in ignore:
        text = re.sub(pattern, "", text)
        assert text, text
    hash = base64.encodestring(md5.new(text).digest())

    if os.path.isfile(filename):
        f = open(filename, "r+")
        old_hash = f.read()
        f.seek(0)
    else:
        f = open(filename, "w")
        old_hash = ""

    f.write(hash)
    f.close()

    if old_hash and old_hash != hash:
        sys.stderr.write("%s changed!\n" % page)

