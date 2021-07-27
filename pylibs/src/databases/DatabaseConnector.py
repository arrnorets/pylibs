#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Simple class that stores connector to database.

import configparser
import sys

# /* Databases related modules */
import pymysql
# /* END BLOCK */

class DBConnector():
    def __init__(self, *args, **kwargs ):
        self.connector = None
        self.cfgfile = None
        self.kwargs = kwargs

        if not "dbtype" in kwargs.keys():
            print("Need to pass dbtype parameter. Supported values are: mysql.")
            sys.exit(1)
        if str(kwargs["dbtype"]) == "mysql":
            if not "cfgfile" in kwargs.keys():
                print("MySQL: cfgfile parameter with path to .cnf file must be passed.")
                sys.exit(2)

            self.cfgfile = kwargs["cfgfile"]
            self.__initializeMySQL()

    def __initializeMySQL(self):
        config = configparser.ConfigParser()
        try:
            config.read(self.cfgfile)
        except:
            print(F"Error reading configfile {self.cfgfile}")
            return 

        if 'client' not in config.sections():
            return

        if 'socket' in config['client'].keys():
            self.connector = pymysql.connect(unix_socket=config['client']['socket'],
                             database=config['client']['database'])
        else:
            self.connector = pymysql.connect(host=config['client']['host'],
                             user=config['client']['user'],
                             password=config['client']['password'],
                             database=config['client']['database'],
                             cursorclass=pymysql.cursors.DictCursor)

    def getConnector(self):
        return self.connector

