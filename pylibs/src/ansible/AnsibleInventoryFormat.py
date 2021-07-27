#!/usr/bin/python3

# -*- coding: utf-8 -*-

# Simple formatter for Ansible inventory. 
# Just initializes a dictionary "inv" during creation
# with "hosts" list and "hostvars" dictionary
# and prints JSON output

import json

class AnsibleInventoryFormatter():
    def __init__(self, *args, **kwargs):
        self.inv = {
            "_meta": {
                "hostvars": kwargs["hostvars"]
            },
            "all": {
                "hosts":    kwargs["hosts"],
                "vars":     {
                    "ansible_become_method":    "su",
                    "ansible_become_user":      "root",
                }
            }
        }

    def printJSON(self):
        print( json.dumps(self.inv, indent=4) )

