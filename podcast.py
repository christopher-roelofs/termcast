import feedparser
import json
from html.parser import HTMLParser

from requests.api import head
import podcastparser
import urllib.request


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
    opener = urllib.request.build_opener()
    headers = {"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
    request = urllib.request.Request(url, headers=headers)
    parsed = podcastparser.parse(url,opener.open(request))
    podcast = Podcast()
    podcast.title = parsed["title"]
    podcast.author = parsed["itunes_owner"]["name"]
    podcast.feed = url
    podcast.link = parsed["link"]
    podcast.description = parsed["description"]
    podcast.updated = parsed["episodes"][0]["published"]
    for episode in parsed["episodes"]:
        ep = Episode()
        ep.title = episode["title"]
        ep.podcast = parsed["title"]
        ep.description = episode["description"]
        ep.date = episode["published"]
        if "number" in episode:
            ep.episode = episode["number"]
        for item in episode["enclosures"]:
            if "audio" in item["mime_type"]:
                ep.url = item["url"]
        podcast.episodes.append(ep)
    return podcast


def get_podcast_old(url):
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
    url = "https://feeds.buzzsprout.com/1850247.rss"
    url = "https://audioboom.com/channels/5060313.rss"
    opener = urllib.request.build_opener()
    headers = {"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
    request = urllib.request.Request(url, headers=headers)
    parsed = podcastparser.parse(url,opener.open(request))
    print(json.dumps(parsed))

