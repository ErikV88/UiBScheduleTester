current_lang="en"
string_table={
        "title":{"no":"UiB - Test om emner overlapper på tid",
                 "en":"UiB - Test if subjects overlap on time"},
        "subject1input":{"no":"Velg emne-kode 1",
                         "en":"Select topic code 1"},
        "subject2input":{"no":"Velg emne-kode 2",
                         "en":"Select topic code 2"},
        "subject3input":{"no":"Velg emne-kode 3",
                         "en":"Select topic code 3"},   
        "use_calender":{"no":"Ønsker du å bruke kalenderen til UiB også ? (Y=Ja,N=Nei)",
                        "en":"Do you want to use UiB's calendar as well? (Y = Yes, N = No)"},
        "mittUiBics":{"no":"Kalenderstrømen url fra MittUiB.no",
                      "en":"Calendar stream url from MittUiB.no"},
        "noOverLap":{"no":"Ingen emener overlapper",
                     "en":"No subjects overlap"},
        "extrasubject":{"no":"Ønsker du å teste for et emet til (Y=Ja,N=Nei)",
                        "en":"Do you want to test for another topic (Y = Yes, N = No)"},
        "overlap":{"no":"overlapper tiden til",
                   "en":"time overlaps to"}   
    }

class StringTable:
    def get(key):
        global string_table,current_lang

        return string_table.get(f"{key}").get(f"{current_lang}")