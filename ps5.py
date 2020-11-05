# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from tkinter import *
from datetime import datetime
import pytz


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
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
        print(ret)
    return ret

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid=guid
        self.title=title
        self.description=description
        self.link=link
        self.pubdate=pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate


class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase=phrase
    def is_phrase_in(self, story):
        phrase=self.phrase.lower()
        story= story.lower()
        for char in string.punctuation:
            story= story.replace(char, " ")
        story_list = story.split()
        phrase_list = phrase.split()
        for i in range(0,len(story_list)):
            possible_match="".join(story_list[i:i+len(phrase_list)])
            if possible_match=="".join(phrase_list):
                return True
        return False 
        

class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())
        
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

class TimeTrigger(Trigger):
    def __init__(self, time):
        time = datetime.strptime(time, "%d %b %Y %X")
        time = time.replace(tzinfo=pytz.timezone("EST"))
        self.time = time
        
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        story = story.get_pubdate()
        story = story.replace(tzinfo=pytz.timezone("EST"))
        if story < self.time:
            return True
        else: 
            return False
        
class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        story = story.get_pubdate()
        story = story.replace(tzinfo=pytz.timezone("EST"))
        if story > self.time:
            return True
        else: 
            return False
            
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger=trigger
    def evaluate(self, story):
        return not self.trigger.evaluate(story)
    
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.Trigger1=trigger1
        self.Trigger2=trigger2
        
    def evaluate(self, story):
        return self.Trigger1.evaluate(story) and self.Trigger2.evaluate(story)
    
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.Trigger1 = trigger1
        self.Trigger2 = trigger2
    def evaluate(self, story):
        return self.Trigger1.evaluate(story) or self.Trigger2.evaluate(story)
    
        
def filter_stories(stories, triggerlist):
    
    filtered_stories = []
    for story in stories:
        if any (trigger.evaluate(story) for trigger in triggerlist):
            filtered_stories.append(story)
    return filtered_stories
       

def read_trigger_config(filename):

    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            #each line contains: "trigger name, trigger type, trigger arg"
            lines.append(line)
    trigger_name_dict= {}
    triggerlist = []
    trigger_type_dict = {"DESCRIPTION":DescriptionTrigger, "TITLE":TitleTrigger, "BEFORE":BeforeTrigger, "AFTER":AfterTrigger, "NOT":NotTrigger, "AND":AndTrigger, "OR":OrTrigger}
    for line in lines:
        contents = line.split(",")
        if contents[0] == "ADD":
            for i in range (1, len(contents)):
                trigger = trigger_name_dict [contents[i]]
                triggerlist.append(trigger)
        else: 
            if contents[1] == "OR" or contents[1] == "AND":
                trigger_name_dict[contents[0]] = trigger_type_dict[contents[1]](trigger_name_dict[contents[2]], trigger_name_dict[contents[3]])
            else:
                trigger_name_dict[contents[0]] = trigger_type_dict.get(contents[1])(contents[2])


    
#having issues with mtTkinter-- the following is mtTkinter code

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("debate")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Biden")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())
        while True:
        
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
