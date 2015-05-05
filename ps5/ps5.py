# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
import re
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):

    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
        
    def get_guid(self):
        return self.guid
        
    def get_title(self):
        return self.title
        
    def get_subject(self):
        return self.subject
        
    def get_summary(self):
        return self.summary
        
    def get_link(self):
        return self.link
        

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):
    
    def __init__(self, word):
        self.word = word
        
    def is_word_in(self, text):
        if re.search("\W" + self.word + "\W", text, flags=re.IGNORECASE):
            return True
        elif re.match("\W" + self.word + "\Z", text, flags=re.IGNORECASE):
            return True
        elif re.match("\A" + self.word + "\W", text, flags=re.IGNORECASE):
            return True
        return False
        
# TODO: TitleTrigger
class TitleTrigger(WordTrigger):
    
    def evaluate(self, story):
        return self.is_word_in(story.get_title())        
        
# TODO: SubjectTrigger
class SubjectTrigger(WordTrigger):

    def evaluate(self, story):
        return self.is_word_in(story.get_subject())
    
# TODO: SummaryTrigger
class SummaryTrigger(WordTrigger):
    
    def evaluate(self, story):
        return self.is_word_in(story.get_summary())


# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
class NotTrigger(Trigger):
    
        def __init__(self, trigger):
            self.trig = trigger
            
        def evaluate(self, story):
            return not self.trig.evaluate(story)
            
# TODO: AndTrigger
class AndTrigger(Trigger):
    
    def __init__(self, trigger1, trigger2):
        self.trig1 = trigger1
        self.trig2 = trigger2
        
    def evaluate(self, story):
        return self.trig1.evaluate(story) and self.trig2.evaluate(story)
        
# TODO: OrTrigger
class OrTrigger(Trigger):

    def __init__(self, trigger1, trigger2):
        self.trig1 = trigger1
        self.trig2 = trigger2
        
    def evaluate(self, story):
        return self.trig1.evaluate(story) or self.trig2.evaluate(story)

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger
class PhraseTrigger(Trigger):

    def __init__(self, phrase):
        self.phrase = phrase
        
    def evaluate(self, story):
        return self.phrase in story.get_title() or \
               self.phrase in story.get_summary() or \
               self.phrase in story.get_subject()

#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder (we're just returning all the stories, with no filtering) 
    # Feel free to change this line!
    triggeredStories = []
    for story in stories:
        for trig in triggerlist:
            if trig.evaluate(story) == True:
                triggeredStories.append(story)
    return triggeredStories

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones
    triggers = []
    trig_set = {}
    for line in all:
        if re.match("t[0-9]", line):
            tags = line.split(None, 2)
            name, trig_type, term = tags
            if trig_type == "TITLE":
                trig_set[name] = TitleTrigger(term)
            elif trig_type == "SUBJECT":
                trig_set[name] = SubjectTrigger(term)
            elif trig_type == "SUMMARY":
                trig_set[name] = SummaryTrigger(term)
            elif trig_type =="PHRASE":
                trig_set[name] = PhraseTrigger(term)
            elif trig_type == "NOT":
                trig_set[name] = NotTrigger(term)
            elif trig_type == "AND":
                name1, name2 = term.split()
                trig_set[name] = AndTrigger(trig_set[name1], trig_set[name2])
            elif trig_type == "OR":
                name1, name2 = term.split()
                trig_set[name] = OrTrigger(trig_set[name1], trig_set[name2])
        if re.match("ADD", line):
            linesplit = line.split()
            for name in linesplit[1:]:
                triggers.append(trig_set[name])
        #else:
            #print trig_set
    return triggers
            
    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Obama")
    t2 = SummaryTrigger("MIT")
    t3 = PhraseTrigger("Supreme Court")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

