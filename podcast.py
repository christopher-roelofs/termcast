import feedparser
import json
from html.parser import HTMLParser



class Podcast:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.author = ""
        self.feed = ""  
        self.link = ""
        self.updated = ""
        self.episodes = []

class Episode:
    def __init__(self):
        self.podcast = ""
        self.listened = False
        self.title = ""
        self.url = ""
        self.episode = ""  
        self.duration = ""
        self.description = ""
        self.date = ""

def filter_html(text):
    class HTMLFilter(HTMLParser):
        text = ""
        def handle_data(self, data):
            self.text += data
    f = HTMLFilter()
    f.feed(text)
    return f.text
    

def get_podcast(url):
    f = feedparser.parse(url)
    #print(json.dumps(f))
    podcast = Podcast()
    feed = f["feed"]
    podcast.title = feed["title"]
    podcast.author = feed["author"]
    podcast.feed = feed["title_detail"]["base"]
    podcast.link = feed["link"]
    if "subtitle" in feed:
        podcast.description = filter_html(feed["subtitle"])
    if "summary" in feed:
        podcast.description = feed["summary"]
    if "updated" in f:
        podcast.updated = f["updated"]
    if "updated" in feed:
        podcast.updated = feed["updated"]
    for entry in f["entries"]:
        episode = Episode()
        episode.title = entry['title']
        episode.podcast = feed["title"]
        episode.description = filter_html(entry["summary"])
        episode.date = entry["published"]
        if "itunes_episode" in entry:
            episode.episode = entry["itunes_episode"]
        for link in entry["links"]:
            if "type" in link:
                if "audio" in link["type"]:
                    episode.url = link["href"]
        podcast.episodes.append(episode)
            
    return podcast

if __name__ == "__main__":
    import database
    feeds = []

    for feed in feeds:
        cast = get_podcast(feed)
        database.add_podcast(cast)
        for episode in cast.episodes:
            database.add_episode(episode)


