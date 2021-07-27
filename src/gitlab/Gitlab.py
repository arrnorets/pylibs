#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# An object that stores information about project in Gitlab. It uses API v4.

from configparser import ConfigParser
import json
import requests
import shutil
import sys
import urllib.parse
import zipfile

class GitlabProjectMeta():
    def __init__(self, *args, **kwargs):
        self.accesstoken = self.__getToken(kwargs["cfgfile"])
        self.gitlaburl = kwargs["gitlaburl"]
        self.projectapi = "api/v4/projects"
        self.projectname = kwargs["projectname"]
        self.projectmetadata = self.__getProjectMeta()

    # /* Gets token for Gitlab access */
    def __getToken(self, cfgfile):
        try:
            # instantiate
            config = ConfigParser()

            # parse existing file
            config.read(cfgfile)

            # read values from a section
            token = config.get('credentials', 'token')

            return token
        except:
            print("Unable to get Gitlab token")
            sys.exit(3)
    # /* END BLOCK */

    # /* Get project metadata */
    def __getProjectMeta(self):
        try:
            projectSearchUrl = F"{self.gitlaburl}/{self.projectapi}/?search={self.projectname}"
            print(F"Requesting {self.gitlaburl}/{self.projectapi}/?search={self.projectname}")
    
            req = requests.get( projectSearchUrl, headers = { "Private-Token" : self.accesstoken } )
            if( req.status_code == 200 ):
                search_result_json = req.json()
                for project in search_result_json:
                    if project['name'] == self.projectname:
                        print(F"Repo information retrieved: OK. RepoID is {project['id']}")
                        return project
            else:
                print( F"Bad answer from {self.gitlaburl}/{self.projectapi} : {req.headers}" )
                sys.exit(6)
        except:
            print( F"Problem occured while accessing {self.gitlaburl}/{self.projectapi} endpoint. Exiting." )
            sys.exit(4)
    # /* END BLOCK */

    # /* Get file from project by its relative path in repository and branch and save it to filename */
    def getFileByBranchAndFilename(self, branch, relativePath, filename):
        try:
            encodedRelativePath = urllib.parse.quote_plus(relativePath)
            fetchUrl = F"{self.gitlaburl}/{self.projectapi}/{self.projectmetadata['id']}/repository/files/{encodedRelativePath}/raw?ref={branch}"
            print(F"Requesting {self.gitlaburl}/{self.projectapi}/{self.projectmetadata['id']}/repository/files/{encodedRelativePath}/raw?ref={branch}")

            req = requests.get( fetchUrl, headers = { "Private-Token" : self.accesstoken } )
            print(F"Result HTTP code is {req.status_code}")
            if( req.status_code == 200 ):
                print(F"Downloading file {relativePath}... Ok.")
                with open(filename, 'wb') as fd:
                    for chunk in req.iter_content(chunk_size=1024):
                        fd.write(chunk)
                fd.close()
                return 0
            else:
                print(F"Could not download file {relativePath}")
                return 1

        except:
            print( F"Problem occured while accessing {self.gitlaburl}/{self.projectapi}/{self.projectmetadata['id']}/repository/files/{relativePath}/raw?ref={branch} endpoint." )
            return 2
    # /* END BLOCK */

    # /* Get the whole project as a .zip archive and save it to filename */
    def getWholeProjectByBranch(self, branch, filename):
        try:
            archiveUrl = F"{self.gitlaburl}/{self.projectapi}/{self.projectmetadata['id']}/repository/archive.zip?sha={branch}"
            print(F"Requesting {self.gitlaburl}/{self.projectapi}/{self.projectmetadata['id']}/repository/archive.zip?sha={branch}")

            req = requests.get( archiveUrl, headers = { "Private-Token" : self.accesstoken } )
            print(req.status_code)
            if( req.status_code == 200 ):
                print("Downloading archive... Ok.")
                with open(filename, 'wb') as fd:
                    for chunk in req.iter_content(chunk_size=1024):
                        fd.write(chunk)
                fd.close()
                return 0
            else:
                print(F"Could not download archive")
                return 1

        except:
            print( F"Problem occured while accessing {self.gitlaburl}/{self.projectapi}/{self.projectmetadata['id']}/repository/archive.zip?sha={branch} endpoint." )
            return 2
    # /* END BLOCK */

    def getProjectId(self):
        return self.projectmetadata['id']


