from typing import Any, List
from notifypy import Notify
from datetime import datetime, timezone

def notify_device(title: str, message: str) -> None:
  """Sends a notification to the local device 

  Args:
      title (str): the title of the notification to send
      message (str): the message contents of the notifications
      
  Returns:
      None: rather sends the notification to the local device
  """
  notification = Notify()
  notification.title = title
  notification.message = message
  notification.send()
  
  
def show_schedule(service: Any, start_time: datetime = None, end_time: datetime = None, notify:bool = True) -> List:
    """Shows the user's google calendar schedule and sends a notification to their device (if wanted).
       By default will get today's schedule until the end of the day and will notify the user.

    Args:
        service (Any): the calendar service to call from the api to get the schedule
        start_time (datetime, optional): the start time where to get the schedule starting from. Defaults to None.
        end_time (datetime, optional): the end time where to stop getting the schedule at. Defaults to None.
        notify (bool, optional): Whether or not to send notifications to the local device. Defaults to True.

    Returns:
        List: the list of events planned for the requested (start, end) schedule based on the api
    """
    # Call the Calendar API
    if not start_time:
        start_time = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    
    if not end_time:
        end_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day + 1).isoformat() + "Z" # tomorrow at 00:00:00
        
    print(f'Obtaining schedule ({datetime.fromisoformat(start_time).strftime("%m-%d-%y")}, {datetime.fromisoformat(end_time).strftime("%m-%d-%y")})')
    print("-" * 40)
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_time,
            timeMax=end_time,
            maxResults=20,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    # if no upcoming events print
    if not events:
      print("\tNo upcoming events found.")
      print("-" * 40)
      return

    # otherwise print the start of the upcoming events
    cur_time = datetime.now()
    # for all events in the events obtained
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      end = event['end'].get('dateTime', event['end'].get('date'))
      
      # print the text to demonstrates whether the end is occuring now or is scheduled to occur
      if cur_time.astimezone(timezone.utc) >= datetime.fromisoformat(start).astimezone(timezone.utc):
        event_text = f'\tCurrent event: {event["summary"]} ends at {datetime.fromisoformat(end).strftime("%I:%M %p")}'
      else:  
        event_text = f'\tUpcoming event: {event["summary"]} at {datetime.fromisoformat(start).strftime("%I:%M %p")}'
      print(event_text)
      
      # if notify then send a notification to the local device
      if notify:
        notify_device(title=event['summary'], message=event_text + "\n" + event['description'].strip('\n'))
      
    print("-" * 40)
    return events