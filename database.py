from tinydb import TinyDB, Query


podcast_db = TinyDB('podcast.json')
episode_db = TinyDB('epipsode.json')

def add_podcast(podcast):
    global podcast_db
    podcasts = Query()
    if len(podcast_db.search(podcasts.title == podcast.title)) < 1:
        podcast_db.insert({"title": podcast.title,"description": podcast.description,"author": podcast.author,"feed": podcast.feed,"link": podcast.link,"updated":podcast.updated})

def remove_podcast(podcast):
    pass

def get_podcasts():
    return podcast_db.all()

def get_podcast(title):
    podcasts = Query()
    return podcast_db.search(podcasts.title == title)[0]

def add_episode(episode):
    global episode_db
    episodes = Query()
    if len(episode_db.search(episodes.title == episode.title)) < 1:
        episode_db.insert({"title": episode.title,"podcast":episode.podcast, "url": episode.url,"episode": episode.episode,"duration": episode.duration,"description": episode.description,"date": episode.date})

def update_episode(episode):
    pass

def get_episodes(podcast):
        episodes = Query()
        return episode_db.search(episodes.podcast == podcast)

def get_episode(title):
    episodes = Query()
    return episode_db.search(episodes.title == title)[0]

if __name__ == "__main__":
    pass