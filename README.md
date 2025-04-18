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

**Drive**
- `download` - downloads a file or folder from drive  
- `upload` - upload a file or revision to a file to drive
- `list` - list the files recently accessed in drive
- `search` - search by partial filename in drive
- `open` - open a webbrowser to a partial filename search

**Calendar**
- `schedule` - show daily calendar schedule

## Usage
### First Time Usage
You will be asked to authenticate your google account with the google simple cli application. Accept the authentication
and allow all permissions. 
A `token.json` file will be generated.

### Commands Usage
```bash
google calendar schedule 
```

```bash
google drive list <num-files-to-list>
```

```bash
google drive search <partial-filename>
```

```bash
google drive download "<file-id1/filename>" "<file-id2/filename>" ...
```

```bash
google drive upload "<filepath1>" "<filepath2>" ...
```

## To Do / Improvements

- add --rm flag to upload so that local files are removed when done uploading
- add pydantic schemas for files to ensure correct files are received
- add autocomplete + prediction to filename exploration.
