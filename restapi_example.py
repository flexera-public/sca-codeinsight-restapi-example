'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Sat Feb 20 2021
File : restapi_example.py
'''
import sys
import os
import logging
import requests

###################################################################################
# Test the version of python to make sure it's at least the version the script
# was tested on, otherwise there could be unexpected results
if sys.version_info <= (3, 5):
    raise Exception("The current version of Python is less than 3.5 which is unsupported.\n Script created/tested against python version 3.8.1. ")
else:
    pass

logfileName = os.path.dirname(os.path.realpath(__file__)) + "/_restapi_example.log"

###################################################################################
#  Set up logging handler to allow for different levels of logging to be capture
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S', filename=logfileName, filemode='w',level=logging.DEBUG)
logger = logging.getLogger(__name__)

#----------------------------------------------------------------------#
def main():
    
    # Configuration Options

    baseURL = "http://localhost:8888"
    authToken = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJzZ2VhcnkiLCJ1c2VySWQiOjksImlhdCI6MTYwODU1MTIxN30.L43qItUKJv6QGH1fMC_tyGDRbqnoJU1DHECCVYODfTzLsPGlwSzWf1pZSMuOM5burXAFrrntxN6bTFbkWSn83g"
    projectName = "testproject"
    codePath = "D:/testproject_code.zip"

    #projectID = create_project(projectName, baseURL, authToken)
    projectID = "39"

    print(projectID)

    upload_project_codebase(projectID, codePath, baseURL, authToken)



#----------------------------------------------------------------------#
def create_project(projectName, baseURL, authToken):
    logger.debug("Entering create_project")

    RESTAPI_URL = baseURL + "/codeinsight/api/projects"
    logger.debug("    RESTAPI_URL:  %s" %RESTAPI_URL)

    projectCreateBody = '''{"name" : "''' + projectName + '''"}'''  # Using project default for majority of configuration
    logger.debug("    projectCreateBody:  %s" %projectCreateBody)

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 

    # Call REST API  
    try:
        response = requests.post(RESTAPI_URL, headers=headers, data=projectCreateBody)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        print(error)
        return

    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 201:
        logger.info("    Sucessfully created project: %s" %projectName)
        print("Sucessfully created project: %s" %projectName)
        projectID = response.json()["id"]
        return projectID
    else: 
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Failed to created project: %s" %projectName)
        print("    Response code %s - %s" %(response.status_code, response.text))
        sys.exit()
    
#----------------------------------------------------------------------#
def upload_project_codebase(projectID, codePath, baseURL, authToken):
    logger.debug("Entering upload_project_codebase")

    # Open the zipfile to provide to open
    try:
        with open(codePath, mode='rb') as file: # b is important -> binary
            projectCodeBase = file.read()
        logger.info("Successfully opened %s" %codePath)
    except:
        logger.error("Failed to open %s" %codePath)
        sys.exit()

    uploadOptions = "&deleteExistingFileOnServer=true"
    uploadOptions += "&expansionLevel=1"

    RESTAPI_URL = baseURL + "/codeinsight/api/project/uploadProjectCodebase"
    RESTAPI_URL += "?projectId=" + projectID
    RESTAPI_URL += uploadOptions

    logger.debug("    RESTAPI_URL:  %s" %RESTAPI_URL)

    headers = {'Content-Type': 'application/octet-stream', 'Authorization': 'Bearer ' + authToken}  

    try:
        response = requests.post(RESTAPI_URL, headers=headers, data=projectCodeBase)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        print("Failed to upload code base: %s" %codePath)
        print("    %s" %error)
        return

    ###############################################################################
    # We at least received a response from Code Insight so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    Project code base uploaded successfully")
        print("Project code base uploaded successfully")
        return

    else: 
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Failed to upload code base: %s" %codePath)
        print("    Response code %s - %s" %(response.status_code, response.text))
        sys.exit()

#----------------------------------------------------------------------#    
if __name__ == "__main__":
    main()  