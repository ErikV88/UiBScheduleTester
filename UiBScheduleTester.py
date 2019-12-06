from http import client 
from IcsParser import IcsParser
from collections import namedtuple
from datetime import datetime

class UiBScheduleTester:
    groups={}
    emne1=""
    emne1=""

    def __init__(self,emne1,emne2):
        self.emne1=emne1
        self.emne2=emne2

    def get_emner(self):
        try:
            conn = client.HTTPSConnection("tp.uio.no")
            conn.request("GET", f"/uib/timeplan/ical.php?sem=20v&id%5B0%5D={self.emne1}%2C&id%5B1%5D={self.emne2}%2C&type=course")
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
                if is_overlap>0:group_overlaps.append({"Group1":group,"Group2":group2})
        return group_overlaps



    def is_group_overplaping(self,group1,group2):
        is_overlap=0
        for time in group1:
            for time2 in group2:
                is_overlap=self.is_overlap_single_date(time.DTSTART,time.DTEND,time2.DTSTART,time2.DTEND)
        return is_overlap

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
    print("# UiB - Test om emner overlapper på tid #")
    emne1=input("Velg emne-kode 1: ")
    emne2=input("Velg emne-kode 2: ")

    b=UiBScheduleTester(emne1,emne2)
    b.get_emner()
    overlaps=list = b.is_groups_overplaping()

    if len(overlaps)<=0: 
        print("Ingen emener overlapper")
    else:
        for emne in overlaps:
            grupe1=emne['Group1'].replace("\\n","").replace("\\r","").replace("\r","")
            grupe2=emne['Group2']

            print(f"    !WARNING! - {grupe1} overlapper tiden til {grupe2}")
    main()
main()

