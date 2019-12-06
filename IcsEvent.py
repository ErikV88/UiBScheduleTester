import re,datetime

class IcsEvent:
    def __init__(self,DTSTART,DTEND,SUMMARY):
        self.DTSTART=self.parse_toDate(DTSTART)
        self.DTEND=self.parse_toDate(DTEND)
        self.SUMMARY=SUMMARY

    def parse_toDate(self,date_string):
        regex = r"([0-9]{4})([0-9]{2})([0-9]{2})T([0-9]{2})([0-9]{2})"
        groups = re.search(regex, date_string, re.MULTILINE).groups()

        return datetime.datetime(int(groups[0]),int(groups[1]),int(groups[2]),int(groups[3]),int(groups[4]))