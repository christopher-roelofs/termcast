import database
import os
import datetime
import podcast as _podcast
from time import sleep
import audio


logs = []
quit = False
player = None
episode_list = []
episode_index = -1

def log(message,type):
    global logs
    log = {}
    log["timestamp"] = datetime.datetime.now()
    log["message"] = message
    log["type"] = type
    logs.append(log)

def screen_clear():
    # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows platfrom
        _ = os.system('cls')

def draw_player():
    global player
    screen_clear()
    print("--------------------------------------------------------------")
    print(f"Podcast:       {episode_list[episode_index]['podcast']}")
    print(f"Episode:       {episode_list[episode_index]['title']}")
    print(f"Date:          {datetime.datetime.fromtimestamp(episode_list[episode_index]['date'])}")
    print(f"Listened:      {database.get_episode(episode_list[episode_index]['title'])['listened']}")
    print(f"Status:        {player.get_status()}")
    print(f"Volume:        {player.get_volume()}")
    print(f"Description:   {episode_list[episode_index]['description']}")
    print("--------------------------------------------------------------")
    print("P: Play/Pause | S: Stop | N: Next | R: Previous | Q: Back")
    print("--------------------------------------------------------------")
    print("V: Volume | D: Download Episode | L: Mark As Listened")
    print("--------------------------------------------------------------")
    
def error_callback(event):
    log("Issue playing episode, skipping to next episode.","error")

def play_next_episode(event=None):
    global player
    global episode_index
    episode_index += 1
    if player != None:
        player.stop_audio()
    del player    
    if episode_index + 1 > len(episode_list):
        episode_index -= 1
    else:
        player = audio.Player()
        #player.set_end_callback(play_next_episode)
        player.set_error_callback(error_callback)
        player.play_audio(episode_list[episode_index]["url"])
    draw_player()

def update_podcast(podcast):
    current = database.get_podcast(podcast)
    new =_podcast.get_podcast(current["feed"])
    if current["updated"] != new.updated:
        for episode in new.episodes:
            database.add_episode(episode)

def log_menu():
    quit = False
    log_page = 1
    sorted_logs = sorted(logs, key=lambda k: k['timestamp'], reverse=True)
    while not quit:
        screen_clear()
        print("------------------------------------------")
        print("                  Logs                    ")
        print("------------------------------------------")
        index = 0
        max = log_page * 10
        for log in sorted_logs[max - 10:max]:
            print(f"{log['timestamp']} - {log['type']} - {log['message']}")
            index += 1
        print("------------------------------------------")
        print("N: Next Page | P: Previous Page | Q: Quit ")
        print("------------------------------------------")
        val = input()
        if val.lower() == "n" or val == "":
            if log_page <= (len(sorted_logs) / 10):
                log_page += 1
        if val.lower() == "p":
            if log_page > 1:
                log_page -= 1
        if val.lower() == "q":
                quit = True

def player_menu():
    global player
    quit = False
    while not quit:
        draw_player()
        val = input().lower()
        if val == "q":
            player.stop_audio()
            quit = True
        if val == "x":
            speed = input("Speed: ")
            try:
                player.set_speed(float(speed))
            except Exception as e:
                pass
        if val == "p":
            player.pause_audio()
        if val == "l":
            database.set_as_listened(episode_list[episode_index]["title"])
        if val == "r":
            pass
            #play_previous_track()
        if val == "s":
            player.stop_audio()
        if val == "n":
            play_next_episode()
        if val == "b":
            player.stop_audio()
        if val == "v":
            volume = input("Volume: ")
            try:
                player.set_volume(int(volume))
                log(f"Updated volume to {volume}","info")
            except Exception as e:
                log(f"Failed to set volume: {e}","error")
        sleep(1)

def add_podcast_menu():
    quit = False
    while not quit:
        screen_clear()
        print("------------------------------")
        print("         Add Podcast          ")
        print("------------------------------")
        print("Enter podcast rss feed")
        val = input()
        if val != "":
            print("Importing episodes...")
            podcast = _podcast.get_podcast(val)
            database.add_podcast(podcast)
            for episode in podcast.episodes:
                database.add_episode(episode)
            quit = True


def episode_menu(podcast):
    quit = False
    current_page = 1
    reverse_order = False
    global show_player
    while not quit:
        global episode_list
        episodes = database.get_episodes(podcast)
        if reverse_order:
            episodes.reverse()
        screen_clear()
        print("-----------------------------------------------------------------")
        print("                         Episodes                                ")
        print("-----------------------------------------------------------------")
        max = current_page * 10
        index = 0
        for episode in episodes[max - 10:max]:
            print(f"{index}: {episode['title']}")
            index +=1
        print("-----------------------------------------------------------------")
        print("N: Next Page | P: Previous Page | Q: Quit | L: Hide/Show Listened | R: Reverse Order")
        print("-----------------------------------------------------------------")
        val = input()
        if val.lower() == "n" or val == "":
            if current_page <= (len(episodes) / 10):
                current_page += 1
        if val.lower() == "p":
            if current_page > 1:
                current_page -= 1
        if val.lower() == "q":
                quit = True
        if val.lower() == "r":
            reverse_order = not reverse_order
        if val in "0123456789":
                title = episodes[max - 10:max][int(val)]["title"]
                episode = database.get_episode(title)
                episode_list = []
                episode_list.append(episode)
                show_player = True
                play_next_episode()
                player_menu()


def podcast_menu():
    quit = False
    podcasts = database.get_podcasts()
    current_page = 1
    while not quit:
        screen_clear()
        print("------------------------------")
        print("         Podcasts             ")
        print("------------------------------")
        index = 0
        max = current_page * 10
        for podcast in podcasts[max - 10:max]:
            print(f"{index}: {podcast['title']}")
            index += 1
        print("------------------------------------------")
        print("N: Next Page | P: Previous Page | Q: Quit ")
        print("------------------------------------------")
        val = input()
        if val.lower() == "n" or val == "":
            if current_page <= (len(podcasts) / 10):
                current_page += 1
        if val.lower() == "p":
            if current_page > 1:
                current_page -= 1
        if val.lower() == "q":
                quit = True
        if val in "0123456789":
                podcast = podcasts[max - 10:max][int(val)]["title"]
                update_podcast(podcast)
                episode_menu(podcast)
 
        

def main_menu():
    quit = False
    while not quit:
        screen_clear()
        print("------------------------------")
        print("         Term Cast            ")
        print("------------------------------")
        print("1: Podcasts")
        print("2: Add Podcast")
        print("3: Logs")
        print("4: Quit")
        val = input().lower() or "1"
        if val == "1":
            podcast_menu()
        if val == "2":
            add_podcast_menu()
        if val == "3":
            log_menu()
        if val == "4":
            screen_clear()
            quit = True



main_menu()