#!/usr/bin/env python

import argparse
import os
from typing import List
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError

from auth import authenticate
from drive_scripts import download, list_files, search_files, open_file, upload
from calendar_scripts import show_schedule

SERVICE_NAMES = ['drive', 'calendar']
CMD_NAMES = ['download', 'upload', 'list', 'search', 'open', 'schedule']

def run_service(service: str, cmd: str, args: List):
  """
  Run the specified service and the command inputted with the args passed.
  """
  # Step 1. authenticate with the google cloud api
  try: 
    creds = authenticate()  
  except RefreshError:
    os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.json'))
    creds = authenticate()
  
  # Step 2. Build the respective services and run them with the args
  try:
    service = build(service, "v3", credentials=creds)
    
    if cmd == "download":
      if (len(args) > 0):
        for item in args:
          download.download_file(service, item)
      else:
        print('Please supply the file ids to download')
    
    elif cmd == "upload":
      if (len(args) > 0):
        for item in args:
          upload.upload_file(service, item)
      else:
        print('Please supply the filepaths to upload')
        
    elif cmd == "list":
      if len(args) > 0:
        list_files.list_files(service, int(args[0]))
      else:
        # Default list the top 10 most recent files
        list_files.list_files(service, 10)
    
    elif cmd == 'search':
      search_files.search_files(service, args)
      
    elif cmd == 'open':
      open_file.open_file(service, args)
    
    elif cmd == "schedule":
      # TODO - figure out how to make specific show schedule command args
      show_schedule.show_schedule(service, *args)
    
    else:
      print('Command not accepted')
    
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")

if __name__ == "__main__":
  # Obtain the arguments from the command line
  parser = argparse.ArgumentParser()
  parser.add_argument("service", type=str, choices=SERVICE_NAMES, help='the name of the service to use with the api')
  parser.add_argument("cmd", type=str, choices=CMD_NAMES, help='the name of the command to use with the serivce')
  parser.add_argument("args", nargs='*')
  args = parser.parse_args()
  
  # Debug output print the arguments inputted
  print(args)
  
  # Run the service and command with specified arguments
  run_service(args.service, args.cmd, args.args)