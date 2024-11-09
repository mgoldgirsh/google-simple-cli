# Google API Scripts
Plays around with the Google API so that I can create scripts on my laptop for 
daily routine tasks. 

## Methodology 
I created this simple google command line interface in order to download files from my google drive and view 
my schedule from my google calendar in the terminal. This small package is intended to be a lightweight way to 
access the google drive/calendar to make scheduling easier and downloading/uploading content easier. 

## Installation 
Follow tutorials to setup the Google Developer platform, and Google Cloud platform. 
https://developers.google.com/calendar/api/quickstart/python 
> Remember to obtain a `credentials.json` file when running through the tutorial

Then navigate to the directory and run the `install.bash` script
```bash
./install.bash
```

## Current Implementation
Services used:
- Google Calendar (`calendar`)
- Google Drive (`drive`)

Commands Implemented:
- `download_file` - downloads a file from drive  
- `upload_file` - upload a file to drive
- `list_files` - list the files recently accessed in drive
- `search_files` - search by partial filename in drive
- `show_schedule` - show daily calendar schedule

## Usage
### First Time Usage
You will be asked to authenticate your google account with the google simple cli application. Accept the authentication
and allow all permissions. 
A `token.json` file will be generated.

### Commands
```bash
google calendar show_schedule 
```

```bash
google drive list_files <num-files-to-list>
```

```bash
google drive search_files <partial-filename>
```

```bash
google drive download_file <file-id1> <file-id2> ...
```

```bash
google drive upload_file <filepath1> <filepath2> ...
```
