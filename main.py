import database
import os
import datetime

logs = []
quit = False
player = None

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

def draw_player(episode):
    screen_clear()
    print("--------------------------------------------------------------")
    print(f"Podcast:   {episode['podcast']}")
    print(f"Episode:   {episode['title']}")
    #print(f"Listened:  {episode['listened']}")
    print(f"Status:    {player.get_status()}")
    print(f"Volume:    {player.get_volume()}")
    print("--------------------------------------------------------------")
    print("P: Play/Pause | S: Stop | N: Next | R: Previous | Q: Back")
    print("--------------------------------------------------------------")
    print("V: Volume | D: Download Episode | L: Mark As Listened")
    print("--------------------------------------------------------------")



def episode_menu(podcast):
    global quit
    while not quit:
        screen_clear()
        print("------------------------------")
        print("         Episodes             ")
        print("------------------------------")
        episodes = database.get_episodes(podcast)
        current_page = 1
        index = 0
        max = current_page * 10
        for episode in episodes[max - 10:max]:
            print(f"{index}: {episode['title']}")
            index +=1
        print("------------------------------------------")
        print("N: Next Page | P: Previous Page | Q: Quit ")
        print("------------------------------------------")
        val = input()
        if val.lower() == "n" or val == "":
            if current_page <= (len(episodes) / 10):
                current_page += 1
        if val.lower() == "p":
            if current_page > 1:
                current_page -= 1
        if val.lower() == "q":
                quit = True
        if val in "0123456789":
            try:
                episode = episodes[max - 10:max][int(val)]["title"]
                print(database.get_episode(episode))
            except Exception as e:
                pass
        val = input()


def podcast_menu():
    global quit
    while not quit:
        screen_clear()
        print("------------------------------")
        print("         Podcasts             ")
        print("------------------------------")
        podcasts = database.get_podcasts()
        current_page = 1
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
            try:
                podcast = podcasts[max - 10:max][int(val)]["title"]
                episode_menu(podcast)
            except Exception as e:
                pass

def main_menu():
    global quit
    while not quit:
        screen_clear()
        print("------------------------------")
        print("         Term Cast            ")
        print("------------------------------")
        print("1: Podcasts")
        print("2: Add Podcast")
        print("3: Quit")
        val = input().lower() or "1"
        if val == "1":
            podcast_menu()
        if val == "2":
            pass
        if val == "3":
            screen_clear()
            quit = True



main_menu()