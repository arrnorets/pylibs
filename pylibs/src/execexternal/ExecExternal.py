#!/usr/bin/python3

# -*- coding: utf-8 -*-

# Simple external command executor

import subprocess

class ExecExternalCommand():
    def __init__(self, *args, **kwargs):
        self.cmd = kwargs["cmd"]
        process = subprocess.Popen(kwargs["cmd"], stdout=subprocess.PIPE)
        (self.output, self.error) = process.communicate()
        self.retcode = process.wait()

    def PrintRetcode(self):
        return self.retcode

    def PrintCmd(self):
        return self.cmd

    def PrintOutput(self):
        try:
            return self.output.decode("utf-8").rstrip()
        except:
            return "No standard output."

    def PrintError(self):
        try:
            return self.error.decode("utf-8").rstrip()
        except:
            return "No error output."

