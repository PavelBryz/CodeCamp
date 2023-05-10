import re


class FeedDetailed:
    def __init__(self):
        self.title = None
        self.type = None
        self.first_reported = None
        self.status = None

    def parse_title(self, title: str):
        grps = re.match('(.*)\((.*)\)', title).groups()
        self.title = grps[0]
        self.type = grps[1]

    def parse_desc(self, desc: str):
        grps = re.match('First Reported: (.*)Status: (.*)Region:', desc).groups()
        self.first_reported = grps[0]
        self.status = grps[1]
