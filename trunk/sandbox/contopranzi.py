#!/usr/bin/env python
#-*- coding: utf-8 -*-

prezzi = {
         "P": 3.5,
         "S": 5.0,
         "D": 1.5,
         "OKT": 7.0,
         "OKtoberFest": 7.0,
         }       

alias = {
        "mandingo": "lmancini",
        "mand":     "lmancini",
        "giovanni": "rasky",
        }

import sys
import re

mese = open(sys.argv[1]).read()
lista_presenze = re.findall(r"\*[\s]+([^\s]+)[\s]+([^\s]*)", mese)
presenze = {}
[presenze.setdefault(alias.get(k.lower(), k.lower()), []).append(v.strip() and v or "??") for k,v in lista_presenze]

for persona, pasti in sorted(presenze.items()):
    print "-"*40
    print "Conto per:", persona, pasti
    tot = 0.0
    for pasto in pasti:
        if pasto in prezzi:
            tot += prezzi[pasto]
        else:
            for k in pasto: # può essere sia P che PD, che...
                _tot = 0.0
                if k in prezzi:
                    _tot += prezzi[k]
                else:
                    print " "*4, pasto, "Non standard, aggiungere a mano!"
                    break #se non riesce a convertire tutto, esce
                tot += _tot
    print " "*4, "Totale:", tot
    print "-"*40
