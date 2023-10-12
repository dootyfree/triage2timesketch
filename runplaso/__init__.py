# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import sys 

import logging
import time
import os
import base64
import glob
import subprocess
import json
import shutil
from zipfile import ZipFile
from plaso import dependencies
from plaso.cli import log2timeline_tool
from timesketch_api_client import config
from timesketch_api_client import client
from timesketch_import_client import importer
from timesketch_api_client import credentials as ts_credentials
from timesketch_api_client.client import TimesketchApi




def main(body: dict) -> dict:


    try: 
        shutil.rmtree("/tmp/triage/")
    except:
        pass

    try:
        os.remove("/tmp/temp.zip")
    except:
        pass

    try:
        os.remove("/tmp/triage.plaso")
    except:
        pass

    try:
        os.remove("/tmp/plaso.log")
    except:
        pass

    try:
        for f in glob.glob("/tmp/Work*"):
            os.remove(f)
    except:
        pass
    
    
    tfile = body['zipfile']
    hname = body['hostname']
    type = body['type']


    
    
    
    decodedpackage = base64.b64decode(tfile)

    with open('/tmp/temp.zip', 'wb') as triage_package:
        triage_package.write(decodedpackage)
        
    

    os.mkdir("/tmp/triage")

    with ZipFile("/tmp/temp.zip", 'r') as zTriage:
        zTriage.extractall(path = "/tmp/triage")


    tool = log2timeline_tool.Log2TimelineTool()
    tparse = tool.ParseArguments(["--logfile","/tmp/plaso.log","--temporary_directory", "/tmp", "--storage-file", "/tmp/triage.plaso", "/tmp/triage"])
    trun = tool.ExtractEventsFromSources()

 
    timestr = time.strftime("%Y%m%d-%H%M%S")
    sketchname = hname  
  
    ts_client = TimesketchApi('https://timesketchurl',username='username',password='password',verify=False)


    

    sketches = ts_client.list_sketches()
    sketch_dict = dict((x.name, x) for x in sketches)

    if (sketch_dict.get(hname)):
        mysketch = sketch_dict[hname]
        sketch_id = mysketch.id
        sketch = ts_client.get_sketch(sketch_id)
    else:
        sketch = ts_client.create_sketch(sketchname,"created by .....")   
        
    acl = sketch.acl

    if not (acl.get('group/analysts')):
        sketch.add_to_acl(group_list='analysts')
     
 
 
 
    with importer.ImportStreamer() as streamer:
        streamer.set_sketch(sketch)
        streamer.set_timeline_name(type)
        streamer.add_file("/tmp/triage.plaso")

    response = streamer.response    
    timeline = streamer.timeline
      
    while True:
        status = timeline.status
        if status in ("archived", "failed", "fail"):
            output = print(
                "Unable to index timeline"
                )
            return output

        if status not in ("ready", "success"):
            time.sleep(3)
            continue

        api_root = sketch.api.api_root
        host_url = "https://timesketchurl"
        sketch_url = '{0:s}sketches/{1:d}/'.format(host_url, sketch.id)
        output = 'Your Timesketch URL is: {0:s}'.format(sketch_url)
        break

    streamer.flush()
    

          
    
    #output = json.dumps(subprocess.check_output(["ls", "/tmp"],  stderr=subprocess.STDOUT).decode("utf-8"))

    shutil.rmtree("/tmp/triage/")
    os.remove("/tmp/temp.zip")
    os.remove("/tmp/triage.plaso")
    os.remove("/tmp/plaso.log")
  

    

    return output