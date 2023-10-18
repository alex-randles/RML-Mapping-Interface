# RML-Mapping-Interface
An interface which allows RML mappings and associated source data to be executed and resulting RDF data output.

## Online Version 
An online version of the application is available at the following link: https://rml-mapper.adaptcentre.ie/

## Local Version
### Installation Guide
The following sections cover the installation and running of the application. The application requires `python 3.10` or greater to run.
### Downloading Source Code 
The following command can be used to download this repository: `git clone https://github.com/alex-randles/RML-Mapping-Interface.git`

Alternatively, you can download a ZIP file containing the code here: [https://github.com/alex-randles/RML-Mapping-Interface/archive/refs/heads/main.zip](https://github.com/alex-randles/RML-Mapping-Interface/archive/refs/heads/main.zip)
### Requirements 
The `requirements.txt` file contains the four packages which are required to run the application. 
* [Flask](https://pythonbasics.org/what-is-flask-python/): Responsible for hosting the web application. 
* [RDFLib](https://rdflib.readthedocs.io/en/stable/): Responsible for loading the generated RDF graph. 
* [Morph-KGC](https://github.com/morph-kgc/morph-kgc): Responsible for executing the RML mapping. 
* [Werkzeug](https://werkzeug.palletsprojects.com/en/3.0.x/): Responsible for processing file uploads. 

The packages can be installed using the following command: `pip3 install -r requirements.txt` 
### Running the Application
The application can be started using the following command: `python3 main.py`

The interface of the application will run on localhost port 5000 by default [127.0.0.1:5000](http://127.0.0.1:5000).

The port can be configured on line 125 of `main.py` by changing the respective variable `app.run(debug=True, host="127.0.0.1", port=5000, threaded=True)`

### Sample Mappings 
Sample Mappings and Data sources can be found in the  [sample-mappings](./sample-mappings) directory. 

### Video Demonstration
A video demonstration of the application can be found here: https://drive.google.com/file/d/1IW--40hAaRCww_52P9fTOchVX_u7y7ow/view?usp=sharing
