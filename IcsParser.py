import re
from IcsEvent import IcsEvent

class IcsParser:
    data=[]
    filename=""

    def __init__(self,filename):
        self.filename=filename
        self.from_ical(filename)

    def get_value_by_key(self,key,text):
       key=key.replace(":","")
       return re.search("%s:(?:.*(?:\n )?)*"%(key),text,re.IGNORECASE)[0].replace(key+":","")

    def get_keys(self,event_data):
       return re.findall("([a-z]+:)",event_data,re.IGNORECASE)
  
    def get_events_metadata(self,sr):
        events=[]
        for i,d in enumerate(sr.split("BEGIN:VEVENT")):
            data= sr.split("BEGIN:VEVENT")[i].split("END:VEVENT")[0]
           
            values={}
            for key in  self.get_keys(self.replace_html(data)):
                key=key.replace(":","")
                values[key]=self.get_value_by_key(key,data)
            events.append(values)
        return events

    def replace_html(self,text):
      text= re.sub('<[^<]+?>', '', str(text))
      return text.replace("\\n"," ").replace("\n"," ")

    def from_ical(self,data_string):
        result=self.get_events_metadata(data_string)
        self.data=result

    def get_events(self):
        result=[]
        for event_data in self.data: 
            if [e for e in event_data if "DTSTART" in e]:
                result.append(IcsEvent(event_data.get("DTSTART"),event_data.get("DTEND"),event_data.get("SUMMARY")))
            
        return result

