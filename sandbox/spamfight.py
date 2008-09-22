#!/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import mailbox
import re
import urllib

def run():
    get_href = re.compile("http://[^\s\"\"=<>]*")
    mbox = mailbox.Maildir(os.path.expanduser("~/Maildir"),
                           factory=mailbox.MaildirMessage) # use newer email.message.Message
    junk = mbox.get_folder("Junk.Both")
    def get_body(message):
        if message.is_multipart():
            for p in message.get_payload():
                for b in get_body(p):
                    yield b
        else:
            yield message.get_payload(decode=True)
    for message in junk:
        for body in get_body(message):
            uris = set(get_href.findall(body))
            for uri in uris:
                print uri

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print "SpamFight, generate traffic against spammed urls!"
        print "Usage:"
        print "  python %s | xargs curl > /dev/null" % sys.argv[0]
    else:
        run()
