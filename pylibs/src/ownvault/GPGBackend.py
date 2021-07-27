#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# A simple GPG-based vault backend for data extracting.
# An example of usage: 
# gpg = GPGVaultStorage(GPG = "/usr/bin/gpg", PASS = "mypass.gpg")
# print(gpg.getpassbyname("IPMI"))

import sys
import os
import re

class GPGVaultStorage():

    def __init__(self, *args, **kwargs):
        self.pwds = list()

        try:
            proc = os.popen(kwargs["GPG"] + " -d " + kwargs["PASS"], 'r', 1)
            for l in proc:
                line = l.split(':')[2].lstrip()
                m = re.search('^(\S+)\t(.+)$', line)
                if m:
                    self.pwds.append({"passname": l.split(':')[0].rstrip(), "re": m.group(1), "pass": m.group(2).split(':')[0].strip(' ')})
 
        except:
           sys.stderr.write(F'Cannot decrypt {kwargs["PASS"]}\n')
           sys.exit(1)

    def getpassbyname(self, passname):
        for v in self.pwds:
            if v["passname"] == passname:
                return v["pass"]

    def getpassbyhost(self, host):
        for v in self.pwds:
            if v["re"] == host:
                return v["pass"]

            if re.match(v["re"], host):
                return v["pass"]
