import sys
import re

class GenderData:
    def __init__(self):
        yobdata = map(lambda x:x.strip().split(","), open('yob1995.txt').readlines()[1:])
        self.names_gender = {}
        for name, gender, countstr in yobdata:
            count = int(countstr)
            if (name in self.names_gender and count > self.names_gender[name][1]) \
                    or name not in self.names_gender:
                self.names_gender[name] = (gender, count)
        self.usergender = {}
    
    def assign(self, username, userid=None):
        if userid:
            if userid in self.usergender:
                return self.usergender[userid]
        username = username.strip()
        if username=='':
            return "U"
        username = username.split()
        regex_name = re.sub(r'\W+', '', username[0].lower()) # get rid of characters not a-z
        first_name = re.sub(r'[0-9]', '', regex_name).capitalize() # get rid of numbers, capitalize first letter
        if first_name in self.names_gender:
            return self.names_gender[first_name][0]
        elif first_name == 'The':
            if len(username)>1:
                return self.assign(' '.join(username[1:]))
            else:
                return "U"
        elif first_name == 'Mr':
            return "M"
        elif first_name == 'Mrs' or first_name == 'Ms' or first_name == 'Miss':
            return "F"
        else:
            return "U"
    
