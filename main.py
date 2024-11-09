#!/usr/bin/env python

import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth import authenticate
from drive_scripts import download_files, list_files, search_files, upload_files
from calendar_scripts import show_schedule

SERVICE_NAMES = ['drive', 'calendar']
CMD_NAMES = ['download_file', 'upload_file', 'list_files', 'search_files', 'show_schedule']

def run_service(service: str, cmd:str, args):
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  # Step 1. authenticate with the google cloud api
  creds = authenticate()  

  # Step 2. Build the respective services and run them with the args
  try:
    service = build(service, "v3", credentials=creds)
    
    if cmd == "download_file":
      if (len(args) > 0):
        for item in args:
          download_files.download_file(service, item)
      else:
        print('Please supply the file ids to download')
    
    elif cmd == "upload_file":
      if (len(args) > 0):
        for item in args:
          upload_files.upload_file(service, item)
      else:
        print('Please supply the filepaths to upload')
        
    elif cmd == "list_files":
      if len(args) > 0:
        list_files.list_files(service, int(args[0]))
      else:
        # Default list the top 10 most recent files
        list_files.list_files(service, 10)
    
    elif cmd == 'search_files':
      search_files.search_files(service, args)
    
    elif cmd == "show_schedule":
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