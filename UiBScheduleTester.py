from http import client 
from IcsParser import IcsParser
from collections import namedtuple
from datetime import datetime
from global_config import StringTable as word

class UiBScheduleTester:
    groups={}
    emne1=""
    emne2=""
    emne3=""

    def __init__(self,emne1,emne2,emne3):
        self.emne1=emne1
        self.emne2=emne2
        self.emne3=emne3
    
    def get_from_uib_calender(self,url):
        url=url.split("https://mitt.uib.no")[1]
        try:
            conn = client.HTTPSConnection("mitt.uib.no")
            conn.request("GET", url)
        except Exception as ex:
            print(ex)
        text = str(conn.getresponse().read().decode('utf8'))
        event_data=IcsParser(text).get_events()

        for e in event_data:
            if not e.SUMMARY in self.groups: self.groups[e.SUMMARY]=[]
            self.groups[e.SUMMARY].append(e)

    def get_emner(self):
        try:
            conn = client.HTTPSConnection("tp.uio.no")
            url=f"/uib/timeplan/ical.php?sem=20v&id%5B0%5D={self.emne1}%2C&id%5B1%5D={self.emne2}%2C&type=course"
            if self.emne3 !=None: url=f"/uib/timeplan/ical.php?sem=20v&id%5B0%5D={self.emne1}%2C&id%5B1%5D={self.emne2}%2C&id%5B2%5D={self.emne3}%2C&type=course" 
            conn.request("GET", url)
        except Exception as ex:
            print(ex)
        text = str(conn.getresponse().read().decode('utf8'))
        event_data=IcsParser(text).get_events()

        for e in event_data:
            if not e.SUMMARY in self.groups: self.groups[e.SUMMARY]=[]
            self.groups[e.SUMMARY].append(e)



    def is_groups_overplaping(self):
        group_overlaps=[]
         
        for group in self.groups:
            for group2 in self.groups:
                if group == group2: continue 
                is_overlap=self.is_group_overplaping(self.groups[group],self.groups[group2])
                if is_overlap["overlap"]>0:group_overlaps.append({"Group1":group,"Group2":group2,"Time":is_overlap["time"]})
        return group_overlaps



    def is_group_overplaping(self,group1,group2):
        return_time=None
        is_overlap=0
        for time in group1:
            for time2 in group2:
                is_overlap=self.is_overlap_single_date(time.DTSTART,time.DTEND,time2.DTSTART,time2.DTEND)
                return_time=time.DTSTART
        return {"overlap":is_overlap,"time":return_time}

    def is_overlap_single_date(self,date_start1,date_end1,date_start2,date_end2):
        Range = namedtuple('Range', ['start', 'end'])
        r1 = Range(start=date_start1, end=date_end1)
        r2 = Range(start=date_start2, end=date_end2)
        latest_start = max(r1.start, r2.start)
        earliest_end = min(r1.end, r2.end)
        delta = (earliest_end - latest_start).days + 1
        overlap = max(0, delta)
        return overlap

def main():
    print("# %s #"%(word.get('title')))
    emne1=input("%s: "%(word.get('subject1input')))
    emne2=input("%s: "%(word.get('subject2input')))
    emne3=None
    use_uib=input("%s: "%(word.get('use_calender')))
    kalender_url=""
    if use_uib.upper()=="Y":
        kalender_url=input("%s: "%(word.get('mittUiBics')))
    else:
        use_emne3=input("%s: "%(word.get('extrasubject')))
        if use_emne3.upper()=="Y":
            emne3=input("%s: "%(word.get('subject3input')))



    b=UiBScheduleTester(emne1,emne2,emne3)
    b.get_emner()
    overlaps=list = b.is_groups_overplaping()
    if use_uib.upper()=="Y":
        b.get_from_uib_calender(kalender_url)

    if len(overlaps)<=0: 
        print(word.get('noOverLap'))
    else:
        for emne in overlaps:
            grupe1=emne['Group1'].replace("\\n","").replace("\\r","").replace("\r","")
            grupe2=emne['Group2'].replace("\\n","").replace("\\r","").replace("\r","")
            overlap=emne['Time'].strftime("%H:%M - %A")

            print(f"    !WARNING! - {grupe1} overlapper tiden til {grupe2} - e.g: {overlap}")
    main()
main()

