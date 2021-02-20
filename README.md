# sca-codeinsight-restapi-example

The sca-codeinsight-restapi-example repository is provided as an example of how to interact with Revenera's Code Insight via the REST API interface.  The application itself will perform the following actions

- Create a Code Insight Project
- Upload a zip file to the Code Insight Server
- Initiate a scan
- Query the scan to determine when it has completed
- Generate and download a report based on the scan results


## Prerequisites


 **Code Insight Release Requirements**
  
This example application was written and tested using Code Insight version 2020R4.  That being said the goal was to make this release agnostic so it shoudl work with older as well as newer releases


**Python Requirements**

The Code Insight Cookbook should work with Python release 3.5 or greater and was tested with verison 3.8.1 specifically.

This repository requires a number of python modules that are not statndard libraries.  These can be installed using the pip and the supplied [requirements.txt](requierments.txt) file as follows.

    pip install -r requirements.txt


## Required Configuration

Within the [restapi_example](restapi_example.py) you will find the following items that need to be defined.

- baseURL - The base URL for the Code Insight Server
- authToken - The JWT token for the Code Insight user that is executing the script
- projectName - The name for the project to be created
- codePath - The path to the location of the archive file (zip/tar/tar.gz/7z)


## Usage

This example program can be launched via

    python restapi_example.py


## License

[MIT](LICENSE.TXT)