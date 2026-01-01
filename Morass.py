import random as r
import math as m
import traceback
import copy as c
import tkinter as tk
import time
import sys
import os
import threading
from queue import Queue
import builtins
from pathlib import Path
presavecode = "" # <---- !!! Enter Save Code Here !!! #
script_dir = Path(__file__).parent
file_path = script_dir / "saveFile.txt"
#Welcome to the labyrinth, Roamer! 
#Cheatcode = 
#st-mp;999000000008989:in-Roamer's Revival;1:in-weapon knowledge;5:in-Bear Traps;3:in-Sharp Fangs;5:in-Komodo Jaws;4:in-Quick SetUp;1:in-The Flamer;1:in-Compressed Canisters;3:in-Cleansing Flames;2:in-終わり [Owari];1:in-Cloudfire Ejection System;1:in-Frozen Growth;1:in-Heavy Caliber;1:in-Targeting System;1:in-Endless Replication;3:in-Gifts of Nothing;2:bo-1;3:bo-4;3:bo-3;3;*:bo-2;3:se-1;0:se-2;0:se-3;0:se-4;d;*:se-5;a;*:se-6;w;*:se-7;s;*:se-8;f;*:se-9;ft;*:se-10;o;*:se-11;t;*:ti-1

class TkConsole:
    def __init__(self, root):
        self.root = root
        root.title("Python Console")
        root.geometry("700x400")

        self.text = tk.Text(
            root,
            bg="black",
            fg="white",
            insertbackground="white",
            wrap="word"
        )
        self.text.pack(fill="both", expand=True)

        self.entry = tk.Entry(
            root,
            bg="black",
            fg="white",
            insertbackground="white"
        )
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self._on_enter)

        self.input_queue = Queue()

        sys.stdout = self
        sys.stderr = self

        self._real_input = builtins.input
        builtins.input = self.input

    # stdout / stderr redirection
    def write(self, msg):
        self.text.insert("end", msg)
        self.text.see("end")

    def flush(self):
        pass

    # input() support
    def _on_enter(self, event):
        value = self.entry.get()
        self.entry.delete(0, "end")
        self.write(value + "\n")
        self.input_queue.put(value)

    def input(self, prompt=""):
        if prompt:
            self.write(prompt)
        return self.input_queue.get()

#Bug Fixing ::  //  //
#To-Do ::  phase through wall single-use item, random teleport item, random upgrades in the labyrinth, increase higher tier upgrade price, restock, Jailer
#NOW To-Do NOW :: hidden shelves
#Bug Report:: beast crash, sheep teleport
""" map coords
    #ABCD
    1####
    2####
    3####
    4####
"""
areamap = {} # if a custom map was made, insert here
walker_pos_list = []
mapsize = [5, 75]
mapmid = [round(mapsize[0] / 2), round(mapsize[1] / 2)]
oldpp = [3, 37] # INITIAL PLAYER POSITION
wasd_converter = {
    "w": [-1,0],
    "a": [0,-1],
    "s": [1,0],
    "d": [0,1],
}
origin = oldpp
newpp = oldpp
forced_quit = False
player = "○"
alt_player = "◙"
alt_alt_player = "¤"
alt_alt_alt_player = "●"
blank = "■"
star = "✯"
flower = "✿"
diamond = "❖"
skull = "Ɏ"
ex_skull = "⚵"
nuclear = "✇"
rifle = "︻デ═一"
reversed_gun = "一═デ︻"
fox = "Ɏ"
fence = "ỻ"
xd = "×"
extra_skull = "\u2620"
extra_extra_skull = "㋱"
bear_trap = "\u01B1"
fire = "ỽ"
enemy_bear_trap = "\u01FE"
walkable = " "
mastery_orb = "۝ "

tutorials = { #   "" : [""," \n"],
    "1" : ["Infinite labyrinth", "The labyrinth is a dangerous journey for those cursed to roam it. your quest is to avoid continual death and reincarnation through escaping the labyrinth. while it has no exit, there are other means. Every venture into the labyrinth is different, with no confort of past knowledge helping navigate the dangers of it. \n"],
    "2" : ["The Roamer", "A being cursed to eternal damnation in the labyrinth. If you are reading this, it's already too late, your only path now is true death. \n"],
    "3" : ["The Predators", "The Predators hunt those in the labyrinth, relentlessly chasing those in their sights. every journey in the labyrinth may have a different Predator, each with their own abilities and weaknesses, only learnt through clues in the labyrinth. The predators are souls who chose violence and slaughter over Eternal Absence. They treat the labyrinth as a hunting ground rather than a second chance, and are only allowed due to Morrows connection to the God of Pain, Marrow. \n"],
    "4" : ["Morrow's Gifts", "To create hope for improvement, the master of the labyrinth will bestow gifts of strength and power for those in the labyrinth, to have a glimmer of hope that they can beat the Predator. \n"],
    "5" : ["Roamer's instinct", "Roamers are equipped with instincts of the past, suited to deal with what their future might hold. every death means more mastery of life, allowing the Roamer to gain an edge in the labyrinth through instincts created through mastery. \n"],
    "6" : ["Daemon's Boons", "Daemons, entities with the most control of the labyrinth, often speak with Roamers, giving them a challenge to entertain the Daemons. Doing so will reward a special gift, boons of incomparable power. \n"],
    "7" : ["Morrows's Contributions", "As a first generation god, Morrow had much significance in the world. But different from other gods, Morrow was the god of all that was gone, or didn't exist. Morrow built the labyrinth as a young child to entertain himself in the Rove, the space outside reality. As morrow grew older, the labyrinth became a prison for those he deemed unworthy of Eternal Absence. \n While Morrow was a harsh god, he was also a fair one. Every soul in the labyrinth has a chance to reach Eternal Absence by self improvement.  \n"],
    "8" : ["Morrow, God of Absence","Morrow was born of nothing, from a mother that didn't yet exist. Morrow's mother is a being that exists in limbo between reality and nothing, between life and death. As such, Morrow became absent, only existing in The Rove, a sliver of nothing that surrounds reality. He controls all that is absent from existence. Dreams, Death, the Past, and the Future all are in his domain, the Rove. \n Morrow lacks connection to the mortal realm, as all he touches becomes absent. To compensate, he communicates through his twin born from the same mother, Marrow, God of Pain. \n Morrow is the only being capable of giving Eternal Absence, known as death to mortals and gods alike. Without Eternal Absence, there would be no relief from pain, only suffering.  \n"],
    "9" : ["The Flamer", "Forged on a lonely nomadic planet, this weapon of mass destruction only awakens in the hands of those who oppose gods and the like. The smith, Ferius, was a genius, only matched by his own curse of insanity. To remove the curse he had to kill the god responsible, so he sought the impossible; to kill the immortal. \n"],
    "10" : ["Roamer's Traps","The greatest tool is one forged for it's purpose. No matter the skill of the smith, weaver, or leatherworker, a weapon crafted for a different purpose isn't effective, no matter its history. \n"],
    "11" : ["Ferius, the Insane", "A talented genius beyond compare. Ferius was a mortal who ascended, gaining godlike smithing abilities. But many were opposed to a mortal with such power, and one such was a god named Medatio, God of Curses.\nTo stop Ferius from turning his abilities against the gods, Medatio cursed him to have his mind shattered into immeasurable peices, and Ferius sanity with thousands of his minds in his small human brain. \nHowever, Ferius was a genius, and with so many minds, he quickly surpassed the smithing ability of many gods. He took to a distant, frozen, roaming planet to forge a weapon to kill Medatio.\nEnamored with the heat of his forge, he hammered out  a trigger, then a barrel, and finally, thirteen Bottles of Sky. \nThe heat of his forge and the fire in his eyes flickered out, as he finally escapes his god-given insanity, leaving his last piece of being for his final masterpiece. \n"],
    "12" : ["Reep","Born in nothing, Reep was a special child. At the flick of a wrist, any living matter would lose all energy, even in the Rove. His parents both passed away during his birth, along with anything living in a small vicinity. Those who feared Reep fueled him, driving him mad with the lonely truth he faced. He begun to thirst for death, as food no longer sustained him. To be quell his hunger, he hunted, learning of his weapon, the Sythe of Death. Morrow saw this cursed child, and gave him the only chance at hand, sending him to the Infinite Labyrinth. \n"],
    "13" : ["The Beest King","All a beast knows is the hunt. On a lonely forest planet, a secret of live hides below the soil. Beings half human, half beast roam, the only food being their own brethren. The king of these monsters is deemed The Beest King, and can only claim the title through strength and violence. But what strength is prized is unknown to all but the King themselves. \n"],
    "14" : ["The Huntsman","\"We do not dirty our hands with the blood of our enemies. We take them down from a distance, with a single pull of a trigger. As it hides, we break its cover. As it runs, we focus our aim. As it  evolves, so do we. \" \n"],
    "15" : ["終わり", "A weapon truly made from nature, signifying the end of those in its sights. Grown from cold corpses, this weapon is a true marksman's charm. The 終わり [Owari] is a sniper rifle crafted from ice capable firing traceless bullets through the toughest of objects, and is so mighty even the best hunter in the world praised its strength. "],
    "16" : ["Cloudfire Ejection System","Bottles of boundless clouds to fuel the perpetual feeding of the fire. To harness godly power, one must hold its vessel and give it nourishment. \n"],
    "17" : ["Patience","The Daemon of Patience is the richest Daemon, with power and wealth beyond the stars, only shackled by time as the only mortal Daemon.\n"],
    "18" : ["Seraphim's Extinction","as Apostles of Gods, Seraphims had three pairs of wings, each with their own abilities. But without any children, they were doomed to disappear. \n"],
    "19" : ["The Immortal Ender","Are you blessed if you cannot die? Those who are trapped in an inescapable hell would always wish for a way out. \n"],
    "20" : ["Ovid the Sheep","Do not turn your back to the Sheep, else it will shed it's fur. Watch, and wait for a chance to exploit it's weakness. \n"],
    
}
#"ex":{"name":0, "level":0, "max level":0, "price":0, "effect":0, "description":0, "prereq":0, "status":"ex"},
instincts_unbought = {
    "0":{"name":"Roamer's Revival", "level":1, "max level":1, "price":0, "effect":"The Roamer will never face death", "description":"Learn, for there is no other escape. ", "prereq":0, "status":"0"}, 
    "1":{"name":"weapon knowledge", "level":0, "max level":10, "price":3,"effect":"+10% damage per level", "description":" knowledge over weapons.", "prereq":0, "status":"1"},
    "2":{"name":"Bear Traps", "level":0, "max level":3, "price":15, "effect":"gains one trap per level - [t] use", "description":"One must use wits to outsmart a hunter", "prereq":1, "status":"2"},
    "3":{"name":"The Flamer", "level":0, "max level":1, "price":50, "effect":"Obtain a dangerous Flamethrower, stunning roamers, clearing the cold, and injuring Predators - [f + {w,a,s,d}] use in direction. ex.) [fw] to fire up.", "description": "capable of burning the gods, the flamethrower shall purify all with its flames. ", "prereq":1, "status":"3"},
    "4":{"name":"Sharp Fangs", "level":0, "max level":5, "price":3, "effect":"Increases trap damage", "description":"One must sharpen their fangs to draw blood. ", "prereq":2, "status":"4"},
    "5":{"name":"Compressed Canisters", "level":0, "max level":11, "price":7, "effect":"Increases the Flamer ammo storage", "description":"The Origin of Fire is fuel. Let it burn. ", "prereq":3, "status":"5"},
    "6":{"name":"終わり [Owari]", "level":0, "max level":1, "price":50, "effect":"unlocks the frozen sniper rifle used to freeze enemies in the column and row of the Roamer. [p] - use", "description":"To stop the unkillable, one must use time. ", "prereq":3, "status":"6"},
    "7":{"name":"Frozen Growth", "level":0, "max level":2, "price":25, "effect":"Increases Owari sniper ammo. ", "description":"The cold seeps into all. ", "prereq":6, "status":"7"},
    "8":{"name":"Cleansing Flames", "level":0, "max level":5, "price":5, "effect":"increases Flamer damage by 10%", "description":"The flames crave inpurity.", "prereq":5, "status":"8"},
    "9":{"name":"Komodo Jaws", "level":0, "max level":4, "price":15, "effect":"Traps stops the predator for longer", "description":"With jaws like a Komodo, they will never let go. ", "prereq":4, "status":"9"},
    "10":{"name":"Gifts of Nothing", "level":0, "max level":3, "price":500, "effect":"Creates pick-ups to replenish ammo", "description":"To run out of supplies is to break universal laws. Balance must be established.", "prereq":1, "status":"10"},
    "11":{"name":"Release Relentless", "level":0, "max level":1, "price":13000, "effect":"Allows the predator to be stunned for longer", "description":"You are as relentless as your living space.", "prereq":15, "status":"11"},
    "12":{"name":"Release the Flames", "level":0, "max level":1, "price":13000, "effect":"allows more fire at once", "description":"Do not let the fire die.", "prereq":16, "status":"12"},
    "13":{"name":"13 13 13", "level":0, "max level":1, "price":13000000, "effect":"Stay in the Labyrinth and Become Insane.", "description":"13 13 13 13 13 13 13 13 13 13 13 13 13", "prereq":20, "status":"13"},
    "14":{"name":"Cloudfire Ejection System", "level":0, "max level":1, "price":50, "effect":"Allows user to eject a bottle of fuel with [ft]", "description":"The fire wishes for more fuel, more food, and more flesh. ", "prereq":8, "status":"14"},
    "15":{"name":"Quick SetUp", "level":0, "max level":1, "price":75, "effect":"Allows movement after placing a trap in the same turn", "description":"Careful, too many have lost fingers with these bad boys. ", "prereq":9, "status":"15"},
    "16":{"name":"Purified", "level":0, "max level":1, "price":213, "effect":"Makes one Immune to the flame", "description":"Only the purifed could escape unscathed. ", "prereq":14, "status":"16"},
    "17":{"name":"Heavy Caliber", "level":0, "max level":3, "price":25, "effect":"increases damage by 100%", "description":"Larger the beast, larger the bullet. ", "prereq":7, "status":"17"},
    "18":{"name":"Targeting System", "level":0, "max level":1, "price":100, "effect":"Allows you to move after firing. ", "description":"\"Too long in the past makes for attachment. Instead, we must modernize to improve what was always there. This is the mark of the best tool.\" - The Huntsman", "prereq":17, "status":"18"},
    "19":{"name":"Endless Replication", "level":0, "max level":3, "price":250, "effect":"Ammo Regenerates.", "description":"The main limitation of weaponry is those that hold it. ", "prereq":18, "status":"19"},
    "20":{"name":"Daemon's Curse", "level":0, "max level":2, "price":100000, "effect":"Increases the max amount of boons to be equipped at once.", "description":"The Daemon of Insanity wished to bring others its curse.", "prereq":10, "status":"20"},
    "100":{"name":"Become Mortal", "level":0, "max level":1, "price":5000000, "effect":"Finish the Game and Escape the Labyrinth.", "description":"To be both Mortal and a Roamer is to become something more. ", "prereq":20, "status":"100"},
}
hidden_texts = {
    "0":["Hunter and Prey","WIP"]
}

instincts = {
    "0":["Roamer's Revival",1]
}
boons = { #"ex":[0"name", 1"description", 2on state, 3unlocked state, 4"1 : \n2 : \n3 : "],
    "1" : ["Boon of Fortune","Brings immeasureable wealth from the Deamon of Patience, your pile of riches growing the more you survive. ", False, 0, "1 : gather 100 mastery in a single run. \n2 : gather 1,000 mastery in a single run. \n3 : gather 5,000 mastery in a single run. "],
    "2" : ["Boon of Harvests", "Allows you to harness the chilling powers of a Reaper with the deathly stiletto, freezing the predator with [r]", False, 0, "1 : Freeze the predator 15 cycles in one run.\n2 : Freeze the predator 30 cycles in one run.\n3 : Freeze the predator 60 cycles in one run."],
    "3" : ["Boon of Beests", "Achieve the terrifying speed of a Beest King", False, 0, "1 : Survive 30 cycles in one run.\n2 : Survive 60 cycles in one run.\n3 : Survive 113 cycles in one run."],
    "4" : ["Boon of the Seraphim", "A Blessing of Flight from a Seraphim's second pair of wings. ", False, 0, "1 : Light the predator on fire for 20 turns in one run.\n2 : Light the predator on fire for 40 turns in one run.\n3 : Light the predator on fire for 80 turns in one run."],
}
boon_notification = ""
oblivion_choice = ""
pred_variations = ["Reaper", "Beest", "Huntsman", "Sheep"]
#pred_variations = ["Beest"] # for testing
status = {
    "mastery points":0,
}
settings = { # "num":["name","desc",value]
    "1":["Predator size compensation", "Changes the amount of extra space in lines not including predator. Ex.) Chromebooks have the predator skull as two spaces, Mac has them as one space, etc. ", 0],
    "2":["Secret character mode", "Just wait and see. 0 - 3", 0],
    "3":["Secret predator mode", "Just wait and see. 0 - 7", 0],
    "4":["Right hotkey","Enter hotkey for moving right.","d","*"],
    "5":["Left hotkey","Enter hotkey for moving left.","a","*"],
    "6":["Up hotkey","Enter hotkey for moving up.","w","*"],
    "7":["Down hotkey","Enter hotkey for moving down.","s","*"],
    "8":["Flamer hotkey","Enter hotkey for using the Flamer.","f","*"],
    "9":["Cloudfire hotkey","Enter hotkey for dropping a fire bottle.","ft","*"],
    "10":["Owari hotkey","Enter hotkey for using the Owari.","o","*"],
    "11":["Trap hotkey","Enter hotkey for placing a trap.","t","*"],
    "12":["Stiletto hotkey","Enter hotkey for placing using the Reaper's Stiletto.","r","*"],
}
player_traps = []
hidden_shelves = 0
tanks = [] #[[0x,0y,]]
active_moving_projectiles = [] # [[posx,posy],[oldposx,oldposy],direction_travelling,name]]
deathzones = [] #[[0x,1y,2oldx, 4time]]
beestjumpswitch = 0
hs_text = ""
breakcheck = False
#   へ
# (` - フ
# |   \  
# U  U ) ノ
def mainGame(console):
    global areamap
    global presavecode
    global walker_pos_list
    global mapsize
    global mapmid
    global oldpp
    global wasd_converter
    global origin
    global newpp
    global forced_quit
    global player
    global alt_player
    global alt_alt_player
    global alt_alt_alt_player
    global blank
    global star
    global flower
    global diamond
    global skull
    global ex_skull
    global nuclear
    global rifle
    global reversed_gun
    global fox
    global fence
    global xd
    global extra_skull
    global extra_extra_skull
    global bear_trap
    global fire
    global enemy_bear_trap
    global walkable
    global mastery_orb
    global tutorials
    global instincts_unbought
    global hidden_texts
    global instincts
    global boons 
    global boon_notification
    global pred_variations
    global status
    global settings
    global player_traps
    global hidden_shelves
    global tanks
    global active_moving_projectiles
    global deathzones
    global beestjumpswitch
    global hs_text
    global breakcheck 
    global boon_notification
    global presavecode
    global newpp
    global inv
    global forced_quit
    global Last_Land
    global active_moving_projectiles
    global pred_frozen
    global mastery_pool
    global oldmapp
    global wings_length
    global wings_cooldown
    global dash_charge
    global Stilleto_cooldown
    global breakcheck
    global ready_for_path_final
    global Predator_loc
    global pred_frozen
    global pred_type
    global x
    global pathoptions
    global pathchoices
    global pathfinal
    global currentpathchoices
    global temppathchoices
    global oldpredloc
    global beestjumpswitch
    global Frozen_time
    global beestjumpinterval
    global mastery_pool
    global sheep_distance
    global sheep_sprint
    global pred_leap_length
    global Sheep_flop
    global mastery_pool
    global status
    global boons
    global hidden_shelves
    global hidden_shelves_notification
    global hs_text
    global time_survived
    global boon_notification
    global script_dir
    global file_path
    global oblivion_choice
    def loadSave(code):
        try:
            theload = code
            theload = theload.split(":")
            for x in theload:
                if "st-" in x:
                    if "mp" in x:
                        tempx = x.split(";")
                        status["mastery points"] = int(tempx[1])
                if "in-" in x:
                    tempx = x.split("-")
                    #print(tempx)
                    tempx = tempx[1]
                    tempx = tempx.split(";")
                    for key in instincts_unbought:
                        if instincts_unbought[key]["name"] == tempx[0]:
                            inspot = key
                    instincts[str(inspot)] = [tempx[0],tempx[1]]
                    instincts_unbought[inspot]["level"] = tempx[1]
                    if int(instincts_unbought[inspot]["level"]) == int(instincts_unbought[inspot]["max level"]):
                        instincts_unbought[inspot]["status"] = "×"*len(instincts_unbought[inspot]["status"])
                if "bo-" in x:
                    tempx = x.split("-")
                    tempx = tempx[1]
                    tempx = tempx.split(";")
                    tempxx = tempx[0]
                    tempxx = str(tempxx)
                    boons[tempxx][3] = int(tempx[1])
                    if len(tempx) == 3:
                        if tempx[2] == "*" and boon_donut_cheat == 0:
                            boons[tempxx][2] = True
                            boon_donut_cheat = 1
                if "se-" in x:
                    tempx = x.split(";")
                    settingtemp = tempx[0].split("-")
                    if "*" in tempx:
                        settings[settingtemp[1]][2] = str(tempx[1])
                    else:
                        settings[settingtemp[1]][2] = int(tempx[1])
                if "ti-" in x:
                    settingtemp = x.split("-")
                    all_gone = round(time.time() - float(settingtemp[1]))
                    all_gone = round(time.time() - float(settingtemp[1]))
                    days_gone = m.floor(all_gone / 86400)
                    if days_gone == 0:
                        hours_gone = m.floor((all_gone) / 3600)
                    else:
                        hours_gone = m.floor((all_gone % days_gone) / 3600)
                    minutes_gone = m.floor((all_gone % 3600)/ 60)
                    seconds_gone = ((all_gone - hours_gone) - minutes_gone) % 60
                    print(f"\nWelcome back Roamer! You have been gone {days_gone} days, {hours_gone} hours, {minutes_gone} minutes, and {seconds_gone} seconds.\n")
                    time.sleep(1)
                if "hs" in x:
                    settingtemp = x.split("-")
                    hidden_shelves = int(settingtemp[1])
        except Exception as exc: #SWITCH TO EXCEPT WHEN DONE
            print(exc)
            traceback.print_exc()
            print("Bad Savecode: Fix it or contact Dev")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if content != "":
        loadSave(content)
        

    def saveGame(code):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

    def makemap(x, y, item):
        for i in range(x):
            areamap[i] = item * y
    def printmap():
        if settings["1"][2] <= 0:
            for key in areamap:
                print(areamap[key])
        else:
            for key in areamap:
                if key == Predator_loc[0] - 1:
                    print(areamap[key])
                else:
                    print((" "*settings["1"][2]) + areamap[key])
            print("")
            
    def readmap(length, height, returnfalse = True):
        "returns icon at location, tends to be wrong"
        global areamap
        try:
            length -= 1
            height -= 1
            expandedmap = list(areamap[height])
            readoutput = expandedmap[length]
            print(readoutput)
            return readoutput
        except KeyError:
            if returnfalse == True:
                return blank
    def editmap(height, length, insert, playermovement = False):
        """making changes in map, insert is the text added and playermovement can be ignored unless it changes the player position. """
        global oldpp
        if playermovement == True:
            oldpp = [height, length]
        length -= 1
        height -= 1
        editmap = list(areamap[height])
        editmap[length] = insert
        editmap = "".join(editmap)
        areamap[height] = editmap
        
    def ppmovemap():
        global newpp
        global inv
        global forced_quit
        global Last_Land
        global active_moving_projectiles
        global pred_frozen
        global mastery_pool
        global oldmapp
        global wings_length
        global wings_cooldown
        global dash_charge
        global Stilleto_cooldown
        if boons["2"][2] == True and Stilleto_cooldown > 0:
            print(f"{m.ceil(Stilleto_cooldown)} cycles cooldown")
        if wings_cooldown > 0 and boons["4"][2] == True:
            print(f"{wings_cooldown} Cycles cooldown")
        if wings_length > 0 and boons["4"][2] == True and oldpp not in walker_pos_list:
            print(f"{wings_length} Cycles left")
        direinput = input()
        #MOVEMENT
        if direinput == settings["6"][2]:
            #editmap(oldpp[0], oldpp[1], walkable, True)
            oldmapp = oldpp.copy()
            newpp = oldpp.copy()
            if boons["4"][2] == True and wings_cooldown == 0:
                if newpp[0] > 1:
                    newpp[0] -= 1
                else:
                    print("Out of Bounds")
            elif boons["3"][2] == True and dash_charge >= 1:
                if newpp[0] > 1 and [newpp[0] - 2, newpp[1]] in walker_pos_list:
                    newpp[0] -= 2
                    dash_charge -= 1
                elif newpp[0] > 1 and [newpp[0] - 1, newpp[1]] in walker_pos_list:
                    newpp[0] -= 1
                else:
                    print("Out of Bounds")
            elif newpp[0] > 1 and [newpp[0] - 1, newpp[1]] in walker_pos_list:
                    newpp[0] -= 1
            else:
                print("Out of Bounds")
            #editmap(newpp[0], newpp[1], player, True)
        if direinput == settings["5"][2]:
            #editmap(oldpp[0], oldpp[1], walkable, True)
            newpp = oldpp.copy()
            oldmapp = oldpp.copy()
            if boons["4"][2] == True and wings_cooldown == 0:
                if newpp[1] > 1:
                    newpp[1] -= 1
                else:
                    print("Out of Bounds")
            elif boons["3"][2] == True and dash_charge >= 1:
                if newpp[1] > 1 and [newpp[0], newpp[1] - 2] in walker_pos_list:
                    newpp[1] -= 2
                    dash_charge -= 1
                elif newpp[1] > 1 and [newpp[0], newpp[1] - 1] in walker_pos_list:
                    newpp[1] -= 1
                else:
                    print("Out of Bounds")
            elif newpp[1] > 1 and [newpp[0], newpp[1] - 1] in walker_pos_list:
                    newpp[1] -= 1
            else:
                print("Out of Bounds")
            #editmap(newpp[0], newpp[1], player, True)
        if direinput == settings["7"][2]:
            #editmap(oldpp[0], oldpp[1], walkable, True)
            newpp = oldpp.copy()
            oldmapp = oldpp.copy()
            if boons["4"][2] == True and wings_cooldown == 0:
                if newpp[0] < mapsize[0]:
                    newpp[0] += 1
                else:
                    print("Out of Bounds")
            elif boons["3"][2] == True and dash_charge >= 1:
                if newpp[0] < mapsize[0] and [newpp[0] + 2, newpp[1]] in walker_pos_list:
                    newpp[0] += 2
                    dash_charge -= 1
                elif newpp[0] < mapsize[0] and [newpp[0] + 1, newpp[1]] in walker_pos_list:
                    newpp[0] += 1
                else:
                    print("Out of Bounds")
            elif newpp[0] < mapsize[0] and [newpp[0] + 1, newpp[1]] in walker_pos_list:
                    newpp[0] += 1
            else:
                print("Out of Bounds")
            #editmap(newpp[0], newpp[1], player, True)
        if direinput == settings["4"][2]: #d
            #editmap(oldpp[0], oldpp[1], walkable, True)
            newpp = oldpp.copy()
            oldmapp = oldpp.copy()
            if boons["4"][2] == True and wings_cooldown == 0:
                if newpp[1] < mapsize[1]:
                    newpp[1] += 1
                else:
                    print("Out of Bounds")
            elif boons["3"][2] == True and dash_charge >= 1:
                if newpp[1] < mapsize[1] and [newpp[0], newpp[1] + 2] in walker_pos_list:
                    newpp[1] += 2
                    dash_charge -= 1
                elif newpp[1] < mapsize[1] and [newpp[0], newpp[1] + 1] in walker_pos_list:
                    newpp[1] += 1
                else:
                    print("Out of Bounds")
            elif newpp[1] < mapsize[1] and [newpp[0], newpp[1] + 1] in walker_pos_list:
                    newpp[1] += 1
            else:
                print("Out of Bounds")
                
        #MAP EDIT STUFF + WINGS
        if oldpp not in walker_pos_list:
            if wings_length > 0 and wings_cooldown == 0:
                editmap(oldmapp[0], oldmapp[1], blank, True)
                wings_length -= 1
                if wings_length <= 0 and wings_cooldown <= 0:
                    wings_cooldown = 15 - round(int(boons["4"][3])/1.5)
            else:
                editmap(oldpp[0], oldpp[1], blank, True)
                newpp = Last_Land.copy()
        else:
            editmap(oldpp[0], oldpp[1], walkable, True)
            Last_Land = oldpp.copy()
            wings_cooldown -= 1
            if wings_cooldown <= 0:
                wings_cooldown = 0
                wings_length = int(boons["4"][3])*2
        editmap(newpp[0], newpp[1], player, True)
        
        #TRAPS
        if direinput == settings["11"][2] and "2" in instincts and int(inv["traps"]) > 0 or direinput == "traps" and "2" in instincts and int(inv["traps"]) > 0:
            print("Trap placed - "+str(int(inv["traps"]) - 1)+" left")
            inv["traps"] = int(inv["traps"]) - 1
            player_traps.append(oldpp)
            if "15" in instincts:
                ppmovemap()
        #THE FLAMER
        if "3" in instincts and int(inv["Flamer Gas"]) > 0:
            for x in [settings["4"][2],settings["5"][2],settings["6"][2],settings["7"][2]]:
                if settings["8"][2] + x in direinput:
                    active_moving_projectiles.append([oldpp,oldpp,x, fire])
                    inv["Flamer Gas"] -= 1
                    print(str(inv["Flamer Gas"])+" Gas left")
        #OWARI
        if "6" in instincts:
            if direinput == settings["10"][2] and int(inv["終わり Rounds"]) > 0:
                if Predator_loc[0] == oldpp[0] or Predator_loc[1] == oldpp[1]:
                    pred_frozen += 5
                    inv["終わり Rounds"] -= 1
                    print(str(inv["終わり Rounds"])+" Rounds left")
                    if "17" in instincts:
                        mastery_pool += 10*(int(instincts_unbought["17"]["level"]) + 1) * (1+(.1*int(instincts_unbought["1"]["level"])))
                    else:
                        mastery_pool += 10 * (1+(.1*int(instincts_unbought["1"]["level"])))
                    if "18" in instincts:
                        ppmovemap()
        #BAG
        if direinput == "inv" or direinput == "i" or direinput == "inventory" or direinput == "bag":
            print(str(round(mastery_pool))+" Mastery")
            for x in inv:
                print(str(x)+" - "+str(inv[x]))
            ppmovemap()
        #Cloudfire
        if "14" in instincts and int(inv["Fire Bottles"]) > 0:
            if direinput == settings["9"][2]:
                tanks.append(oldpp)
                inv["Fire Bottles"] -= 1
                print(str(inv["Fire Bottles"])+" Bottles left")
        if direinput == "quit":
            forced_quit = True
            
        #?
        if direinput == "?" or direinput == "help":
            hotkeynum = 4
            while hotkeynum <= 12:
                if hotkeynum in [4,5,6,7]:
                    print(f"{settings[str(hotkeynum)][0]} - {settings[str(hotkeynum)][2]}")
                elif hotkeynum == 8 and "3" in instincts:
                    print("Flamer hotkey - "+settings["8"][2]+ "[" +str(settings["4"][2])+","+str(settings["5"][2])+","+str(settings["6"][2])+","+str(settings["7"][2])+"]")
                elif hotkeynum == 9 and "14" in instincts:
                    print(f"{settings[str(hotkeynum)][0]} - {settings[str(hotkeynum)][2]}")
                elif hotkeynum == 10 and "5" in instincts:
                    print(f"{settings[str(hotkeynum)][0]} - {settings[str(hotkeynum)][2]}")
                elif hotkeynum == 11 and "2" in instincts:
                    print(f"{settings[str(hotkeynum)][0]} - {settings[str(hotkeynum)][2]}")
                elif hotkeynum == 12 and boons["2"][2] == True:
                    print(f"{settings[str(hotkeynum)][0]} - {settings[str(hotkeynum)][2]}")
                hotkeynum += 1
            print("Bag hotkey - i")
            print(f"Forced quit - quit")
            ppmovemap()
            
        #Stilleto
        if direinput == settings["12"][2] and boons["2"][2] == True and Stilleto_cooldown <= 0:
            pred_frozen += round(int(boons["2"][3])*2.5)
            Stilleto_cooldown = 10 - (int(boons["2"][3])/2)
        elif boons["2"][2] == True and Stilleto_cooldown > 0:
            Stilleto_cooldown -= 1
    def move_projectile(index):
        global active_moving_projectiles
        global explosion_loc
        global active_fire
        if active_moving_projectiles[index] != "Removed":
            #active_moving_projectiles[index][3] == fire and 
            if active_moving_projectiles[index][0] in tanks:
                explosion_point = [active_moving_projectiles[index][0][0], active_moving_projectiles[index][0][1]]
                for i in active_moving_projectiles:
                    if i[0] == explosion_point:
                        explosion_removal = i
                active_moving_projectiles[active_moving_projectiles.index(i)] = "Removed"
                tanks.remove(explosion_point)
                temp_point = [explosion_point]
                for x in range(3):
                    explosion_loc = temp_point.copy()
                    for i in explosion_loc:
                        temp_point.append([i[0] - 1, i[1]])
                        temp_point.append([i[0] + 1, i[1]])
                        temp_point.append([i[0], i[1] - 1])
                        temp_point.append([i[0], i[1] + 1])
                for x in explosion_loc:
                    if x[0] <= mapsize[0] and x[1] <= mapsize[1] and x[0] >= 1 and x[1] >= 1 and x in walker_pos_list:
                        active_fire.append(x)
            else:
                direction = wasd_converter[active_moving_projectiles[index][2]]
                temp_active_moving_projectiles = c.deepcopy(active_moving_projectiles)
                for i in range(2):
                    x = 1 - i
                    temp_active_moving_projectiles[index][0][x] += direction[x]
                    if 0 < temp_active_moving_projectiles[index][0][x] <= mapsize[x] and temp_active_moving_projectiles[index][0] in walker_pos_list and direction[x] != 0:
                        active_moving_projectiles[index][0][x] += direction[x]
                        #print(temp_active_moving_projectiles[index][0][x])
                        #print(active_moving_projectiles[index][0][x])
                    elif not temp_active_moving_projectiles[index][0] in walker_pos_list:
                        #editmap(active_moving_projectiles[index][0][x],active_moving_projectiles[index][0][x],walkable)
                        #active_moving_projectiles.remove(active_moving_projectiles[index])
                        active_moving_projectiles[index] = "Removed"
                        break
    def pathgen(path_length,path_stretch = 1, path_bias_x = 0, path_bias_y = 0):
        global walker_pos_list
        global oldpp
        """creates randomized paths using [walkable] variable as the path, and path stretch is the linear distance covered before changing direction.  path bias is if the path leans towards verticality or horizontal movement, with a higher or lower ratio changing the amount of times it re-rolls the direction"""
        oldpp = origin
        random_walkers = [oldpp[0], oldpp[1]]
        walker_pos_list = [[oldpp[0], oldpp[1]]]
        print("Loading...")
        while path_length > 0:
            cwbiasx = path_bias_x
            cwbiasy = path_bias_y
            walker_direction = r.choice(([1]*(cwbiasx + 1))+([0]*(cwbiasy + 1)))
            """while walker_direction != 2 and cwbiasx > 0:
                walker_direction = r.randint(1,2)
                cwbiasx -= 1
            while walker_direction != 1 and cwbiasy > 0:
                walker_direction = r.randint(1,2)
                cwbiasy -= 1"""
            walker_speed = r.choice([-1, 1])
            random_walkers[walker_direction] += walker_speed
            temp_rando_pos = random_walkers.copy()
            random_walkers[walker_direction] -= walker_speed
            #for x? in path_stretch # tab # add check for re_using same spots
            if 1 <= random_walkers[walker_direction] + walker_speed <= mapsize[walker_direction] and temp_rando_pos not in walker_pos_list:
                random_walkers[walker_direction] += walker_speed
                walker_pos_list.append([random_walkers[0], random_walkers[1]])
                path_length -= 1
            elif temp_rando_pos in walker_pos_list:
                random_walkers[walker_direction] += walker_speed
            for x in range(len(walker_pos_list)):
                editmap(walker_pos_list[x][0], walker_pos_list[x][1], walkable)
    def savingcode():
        global status
        global hidden_shelves
        thecode = []
        boonon = ""
        for x in status:
            if x != "mastery points":
                thecode.append("st-"+str(status[x][0])+";"+str(status[x][1]))
            else:
                thecode.append("st-"+"mp;"+str(status["mastery points"]))
        for x in instincts:
            thecode.append("in-"+str(instincts[x][0])+";"+str(instincts[x][1]))
        for x in boons: #["ex"]:[0"name", 1"description", 2on state, 3unlocked state, 4unlock requirement]
            if boons[x][2] == True:
                boonon = ";*"
            if boons[x][3] > 0:
                thecode.append("bo-"+str(x)+";"+str(boons[x][3])+str(boonon))
        for x in settings:
            if len(settings[x]) == 4:
                thecode.append("se-"+str(x)+";"+str(settings[x][2])+";*")
            else:
                thecode.append("se-"+str(x)+";"+str(settings[x][2]))
        thecode.append(f"hs-{hidden_shelves}")
        if thecode != "st-mp;0:in-Roamer's Revival;1:se-1;0:se-2;0:se-3;0:se-4;d;*:se-5;a;*:se-6;w;*:se-7;s;*:se-8;f;*:se-9;ft;*:se-10;o;*:se-11;t;*":
            thecode.append("ti-"+str(time.time()))
        thecode = ":".join(thecode)
        # print(thecode)
        saveGame(thecode)
        
    def notdeath():
        global mastery_pool
        global status
        global boons
        global hidden_shelves
        global hidden_shelves_notification
        global hs_text
        global time_survived
        global boon_notification
        print(str(time_survived)+" Cycles survived")
        print(str(round(mastery_pool))+" Mastery gained")
        status["mastery points"] += round(mastery_pool)
        #WEALTH
        if mastery_pool >= 5000 and boons["1"][3] < 3:
            boons["1"][3] = 3
            boon_notification = "!"
        elif mastery_pool >= 1000 and boons["1"][3] < 2:
            boons["1"][3] = 2
            boon_notification = "!"
        elif mastery_pool >= 100 and boons["1"][3] < 1:
            boons["1"][3] = 1
            boon_notification = "!"
        #WINGS
        if flame_count >= 80 and boons["4"][3] < 3:
            boons["4"][3] = 3
            boon_notification = "!"
        elif flame_count >= 40 and boons["4"][3] < 2:
            boons["4"][3] = 2
            boon_notification = "!"
        elif flame_count >= 20 and boons["4"][3] < 1:
            boons["4"][3] = 1
            boon_notification = "!"
        #GALE
        if time_survived >= 113 and boons["3"][3] < 3:
            boons["3"][3] = 3
            boon_notification = "!"
        elif time_survived >= 60 and boons["3"][3] < 2:
            boons["3"][3] = 2
            boon_notification = "!"
        elif time_survived >= 30 and boons["3"][3] < 1:
            boons["3"][3] = 1
            boon_notification = "!"
        #REAPER
        if Frozen_time >= 60 and boons["2"][3] < 3:
            boons["2"][3] = 3
            boon_notification = "!"
        elif Frozen_time >= 30 and boons["2"][3] < 2:
            boons["2"][3] = 2
            boon_notification = "!"
        elif Frozen_time >= 15 and boons["2"][3] < 1:
            boons["2"][3] = 1
            boon_notification = "!"
        mastery_pool = 0
        #HIDDEN SHELVES
        """if hidden_shelves < m.floor(mastery_pool / 100):
            hidden_shelves_notification = "!"
            hs_text = "|| [8] Hidden Shelves"
            hidden_shelves = m.floor(mastery_pool / 100)
            if hidden_shelves > len(hidden_texts):
                hidden_shelves = len(hidden_texts)"""
    def pred_walk():
        global breakcheck
        global ready_for_path_final
        global Predator_loc
        global pred_frozen
        global pred_type
        global x
        global pathoptions
        global pathchoices
        global pathfinal
        global currentpathchoices
        global temppathchoices
        global oldpredloc
        global beestjumpswitch
        global Frozen_time
        global beestjumpinterval
        global mastery_pool
        global sheep_distance
        global sheep_sprint
        global pred_leap_length
        global Sheep_flop
        while ready_for_path_final == False and Predator_loc not in player_traps and pred_frozen <= 0:
            x += 1
            for items in currentpathchoices:
                currentpathpos = items
                adjancentPred = [[currentpathpos[0] - 1, currentpathpos[1]], [currentpathpos[0] + 1, currentpathpos[1]], [currentpathpos[0], currentpathpos[1] - 1], [currentpathpos[0], currentpathpos[1] + 1]]
                for i in adjancentPred:
                    if i in pathoptions:
                        pathchoices.append([i[0],i[1],x, currentpathpos])
                        temppathchoices.append([i[0],i[1],x])
                        pathoptions.remove(i)
            currentpathchoices = temppathchoices.copy()
            temppathchoices = []
            #path-printer
            #print(pathchoices)
            for i in pathchoices:
                if oldpp[0] == i[0] and oldpp[1] == i[1]:
                    ready_for_path_final = True
            if x >= 100:
                break
        else:
            if Predator_loc not in player_traps and pred_frozen <= 0:
                #print(pathchoices)
                #print(str(len(pathchoices))+" options")
                pathl = [oldpp[0],oldpp[1],pathchoices[-1][2]] # current point in line to oldpp
                adjapath_length = pathchoices[-1][2]
                sheep_distance.append(adjapath_length)
                while adjapath_length != 0: # while there is still path length:
                    adjapath_length -= 1
                    lastl = "Origin" #last item
                    currentpathpos = [pathl[0],pathl[1]]
                    adjancentopen = [[currentpathpos[0] - 1, currentpathpos[1]], [currentpathpos[0] + 1, currentpathpos[1]], [currentpathpos[0], currentpathpos[1] - 1], [currentpathpos[0], currentpathpos[1] + 1]]
                    for x in adjancentopen: 
                            for i in pathchoices:
                                if x[0] == i[0] and x[1] == i[1] and adjapath_length == i[2]:# check if adja. tile matches the next number:
                                    if i[3] != "Origin" or i[3] == lastl or lastl == "Origin" :
                                        pathfinal.append(i)
                                        pathl = i.copy()
                                        lastl == i[3]
                #print(str(pathchoices)+" - choices")
                """try:
                    for x in range(5):
                        print(str(pathfinal[x])+" - final")
                except:
                    pass"""
                #print(str(len(pathchoices)) + " - choices length")
                #print(str(len(pathfinal)) + " - final length")
                #print(str(oldpp) + " - player position")
                if Predator_loc in [[oldpp[0] - 1, oldpp[1]], [oldpp[0] + 1, oldpp[1]], [oldpp[0], oldpp[1] - 1], [oldpp[0], oldpp[1] + 1]]:
                    print("The Predator has killed you. ")
                    notdeath()
                    breakcheck = True
                else:
                    if len(pathfinal) >= 2:
                        oldpredloc = Predator_loc
                        if pred_type == "Beest":
                            try:
                                if beestjumpswitch < 1:
                                    beestjumpswitch += beestjumpinterval
                                    if beestjumpinterval < 1:
                                        beestjumpinterval += .1
                                    Predator_loc = [pathfinal[-2][0], pathfinal[-2][1]]
                                else:
                                    pred_leap_length = round(pred_leap_length + (.05))
                                    if pred_leap_length > 10:
                                        pred_leap_length = 10
                                    Predator_loc = [pathfinal[pred_leap_length * -1][0], pathfinal[pred_leap_length * -1][1]]
                                    beestjumpswitch = 0
                            except IndexError:
                                print("The Beest Leaps, Unavoidable")
                                notdeath()
                                breakcheck = True
                        elif pred_type == "Sheep" and len(sheep_distance) >= 2:
                            if sheep_distance[-2] - 1 <= sheep_distance[-1] or Sheep_flop == 1:
                                try:
                                    Predator_loc = [pathfinal[-(sheep_sprint + 1)][0], pathfinal[-(sheep_sprint + 1)][1]]
                                    sheep_sprint += 2
                                    if sheep_distance[-2] - 1 <= sheep_distance[-1] and Sheep_flop == 0:
                                        Sheep_flop = 1
                                    else:
                                        Sheep_flop = 0
                                except IndexError:
                                    print("Ovid has found you. ")
                                    notdeath()
                                    breakcheck = True
                            else:
                                Predator_loc = [pathfinal[-2][0], pathfinal[-2][1]]
                                sheep_sprint = 0
                        else:
                            Predator_loc = [pathfinal[-2][0], pathfinal[-2][1]]
                    elif oldpp == Predator_loc:
                        print("You ran into the predator.")
                        notdeath()
                        breakcheck = True
            elif Predator_loc in player_traps:
                player_traps.remove(Predator_loc)
                mastery_pool += 10 + (10*(int(instincts_unbought["1"]["level"]) * .1)) + (10*(int(instincts_unbought["4"]["level"]) * .5))
                if "9" not in instincts:
                    pred_frozen += 1
                else:
                    pred_frozen += int(instincts_unbought["9"]["level"]) + 1
            elif pred_frozen >= 1:
                pred_frozen -= 1
                Frozen_time += 1
        try:
            editmap(oldpredloc[0], oldpredloc[1], walkable)
        except Exception as exc:
            print("Small Error:")
            print(exc)
            notdeath()
            breakcheck = True
    
    while True:
        if oblivion_choice :
            if oblivion_choice == "7":
                print("Data Wiped.")
                os.execv(sys.executable, [sys.executable] + sys.argv)
            else:
                print("Game Saved.")
                savingcode()
        else:
            print("Game Saved.")
            savingcode()
        print(f"\nWelcome to the Oblivion. [1] Enter the labyrinth || [2] The Library || [3] Roamer's Instincts || {boon_notification}{boon_notification} [4] Boons {boon_notification}{boon_notification} || [5] Status || [6] Settings || [7] Clear Save {hs_text}")
        if presavecode == "":
            oblivion_choice = input()
        else:
            oblivion_choice = "7"
        #oblivion_choice = "1"
        if oblivion_choice == "1":
            mastery_passive_gain = 0
            time_survived = 0
            makemap(mapsize[0],mapsize[1], blank)
            pathgenspecs = [r.randint(75,125), r.choice([1,1,2,2,2]), r.choice([2])]
            #print(pathgenspecs)
            pred_type = str(r.choice(pred_variations))
            # ERROR ERROR ERROR #
            pathgen(pathgenspecs[0], pathgenspecs[1], pathgenspecs[2])
            editmap(oldpp[0], oldpp[1], player, True)
            Predator_loc = r.choice(walker_pos_list)
            oldpredloc = Predator_loc
            while Predator_loc == oldpp:
                Predator_loc = r.choice(walker_pos_list)
            editmap(Predator_loc[0], Predator_loc[1], skull)
            pred_frozen = 0
            inv = {}
            mastery_pool = 0
            if "2" in instincts:
                inv["traps"] = instincts_unbought["2"]["level"]
            if "6" in instincts and "7" in instincts:
                inv["終わり Rounds"] = int(instincts_unbought["7"]["level"]) + 1
            elif "6" in instincts:
                inv["終わり Rounds"] = 1
            if "3" in instincts and "14" in instincts:
                inv["Fire Bottles"] = int(instincts_unbought["5"]["level"]) + 1
            if "3" in instincts:
                inv["Flamer Gas"] = 5*(int(instincts_unbought["5"]["level"]) + 1)
            player_traps = []
            active_moving_projectiles = []
            deathzones = []
            huntsaim = []
            explosion_loc = []
            active_fire = []
            deathzonefreq = 0
            deathzonecounter = 0
            deathzonefreqincrements = .1
            beestjumpswitch = 0
            personaldeathzone = 0
            huntsmanguncounter = 0
            huntsmanaimval = 5
            dash_charge = 0
            Stilleto_cooldown = 10 - (int(boons["2"][3])/2)
            beestjumpinterval = .1
            gon = []
            sheep_distance = []
            sheep_sprint = 0
            Sheep_flop = 0
            player_on_fire = 0
            owariregen = 0
            flame_count = 0
            pred_leap_length = 3
            Frozen_time = 0
            tanks = []
            wings_length = int(boons["4"][3]) * 2
            wings_cooldown = 0
            oldmapp = oldpp
            Last_Land = oldpp
            printmap()
            print("The "+str(pred_type)+" is hunting you. ")
            print("Controls - [?]")
            while True:
                if player_on_fire == 0:
                    ppmovemap()
                else:
                    print("On Fire: Movement uncontrollable.")
                    player_on_fire -= 1
                    editmap(oldpp[0], oldpp[1], walkable, True)
                    newpp = oldpp
                    firep = []
                    firep.append([newpp[0] - 1, newpp[1]])
                    firep.append([newpp[0] + 1, newpp[1]])
                    firep.append([newpp[0], newpp[1] - 1])
                    firep.append([newpp[0], newpp[1] + 1])
                    tempoldmapp = []
                    for x in firep:
                        if x in walker_pos_list:
                            tempoldmapp.append(x)
                    newpp = r.choice(tempoldmapp)
                    editmap(newpp[0], newpp[1], player, True)
                if forced_quit == True:
                    forced_quit = False
                    notdeath()
                    break
                for x in walker_pos_list:
                    editmap(x[0], x[1], walkable)
                movecounter = 0
                pathoptions = walker_pos_list.copy()
                currentpathchoices = [[Predator_loc[0],Predator_loc[1], 0]]
                pathchoices = [[Predator_loc[0],Predator_loc[1], 0, "Origin"]]
                pathoptions.remove([Predator_loc[0], Predator_loc[1]])
                pathfinal = []
                huntsaim = []
                x = 0
                temppathchoices = []
                ready_for_path_final = False
                if pred_type == "Huntsman":
                    pred_walk()
                    if oldpp[0] == Predator_loc[0] and pred_frozen == 0 or oldpp[1] == Predator_loc[1] and pred_frozen == 0:
                        #print(oldpp)
                        #print(Predator_loc)
                        if huntsmanguncounter >= huntsmanaimval:
                            print("The Huntsman has pulled the trigger. ")
                            notdeath()
                            break
                        else:
                            huntsmanguncounter += 1
                            huntsmanaimval -= .25
                            if huntsmanaimval < 2:
                                huntsmanaimval = 2
                    else:
                        huntsmanguncounter -= 2.5
                        if huntsmanguncounter < 0:
                            huntsmanguncounter = 0
                else:
                    pred_walk()
                if breakcheck == True:
                    breakcheck = False
                    break
                if pred_type == "Huntsman":
                    for x in range(2):
                        for i in walker_pos_list:
                            if i[x] == Predator_loc[x]:
                                huntsaim.append(i)
                for x in range(len(active_fire)):
                    editmap(active_fire[x][0],active_fire[x][1],fire)
                for x in huntsaim:
                    editmap(x[0],x[1],"×")
                if settings["3"][2] == 0:
                    editmap(Predator_loc[0], Predator_loc[1], skull)    
                if settings["3"][2] == 1:
                    editmap(Predator_loc[0], Predator_loc[1], "㋱")    
                if settings["3"][2] == 2:
                    editmap(Predator_loc[0], Predator_loc[1], "×")   
                if settings["3"][2] == 3:
                    editmap(Predator_loc[0], Predator_loc[1], " ")   
                if settings["3"][2] == 4:
                    editmap(Predator_loc[0], Predator_loc[1], "☠")   
                if settings["3"][2] == 5:
                    editmap(Predator_loc[0], Predator_loc[1], "ౡ")   
                if settings["3"][2] == 6:
                    editmap(Predator_loc[0], Predator_loc[1], "ఈ")   
                if settings["3"][2] == 7:
                    editmap(Predator_loc[0], Predator_loc[1], "ఓ")   
                for x in player_traps:
                    editmap(x[0], x[1], bear_trap)
                for x in tanks:
                    editmap(x[0], x[1], nuclear)
                if pred_type == "Reaper": # [[0x,1y,2oldx,4time]]
                    for x in range(len(deathzones)):
                        editmap(deathzones[x][0][0],deathzones[x][0][1], "×")
                for x in gon:
                    editmap(x[0],x[1], "ж")
                for i in range(len(active_moving_projectiles)):
                    editmap(active_moving_projectiles[i][1][0], active_moving_projectiles[i][1][1], walkable)
                    editmap(active_moving_projectiles[i][0][0], active_moving_projectiles[i][0][1], active_moving_projectiles[i][3])
                if settings["2"][2] == 0:
                    editmap(oldpp[0], oldpp[1], player, True)
                if settings["2"][2] == 1:
                    editmap(oldpp[0], oldpp[1], "ɷ", True)
                if settings["2"][2] == 2:
                    editmap(oldpp[0], oldpp[1], "ඞ", True)
                printmap()
                if "19" in instincts:
                    if owariregen >= 24:
                        inv["終わり Rounds"] = int(instincts_unbought["7"]["level"]) + 1 
                        owariregen = 0
                    else:
                        owariregen += int(instincts_unbought["19"]["level"])/2
                if oldpp in active_fire and "16" not in instincts:
                    player_on_fire += 1
                if Predator_loc in active_fire:
                    if "8" in instincts:
                        mastery_pool += (5 + (.5*int(instincts_unbought["8"]["level"]))) * (1+(.1*int(instincts_unbought["1"]["level"])))
                    else:
                        mastery_pool + 5 *  (1+(.1*int(instincts_unbought["1"]["level"])))
                    flame_count += 1.5
                if boons["3"][2] == True:
                    dash_charge += boons["3"][3]/10
                    if dash_charge > boons["3"][3]*3:
                        dash_charge = boons["3"][3]*3
                    print(f"{m.floor(dash_charge)} Dashes")
                for x in active_moving_projectiles:
                    if Predator_loc[0] in x and Predator_loc[1] in x and fire in x:
                        if "8" in instincts:
                            mastery_pool += (5 + (.5*int(instincts_unbought["8"]["level"]))) * (1+(.1*int(instincts_unbought["1"]["level"])))
                        else:
                            mastery_pool + 5 * (1+(.1*int(instincts_unbought["1"]["level"])))
                        flame_count += 1
                mastery_pool += round(mastery_passive_gain)
                if not time_survived == 0:
                    mastery_passive_gain += .1
                    if boons["1"][2] == True:
                        mastery_passive_gain += (.01*(boons["1"][3]**2))*time_survived
                    #print(mastery_pool)
                time_survived += 1 
                for x in range(len(active_moving_projectiles)):
                    move_projectile(x)
                fake_active_moving_projectiles = c.deepcopy(active_moving_projectiles)
                for x in range(len(active_moving_projectiles)):
                    if active_moving_projectiles[x] == "Removed":
                        fake_active_moving_projectiles.remove(active_moving_projectiles[x])
                active_moving_projectiles = c.deepcopy(fake_active_moving_projectiles)
                if pred_frozen > 10 and not "11" in instincts:
                    pred_frozen = 10
                if active_fire:
                    active_fire.remove(active_fire[0])
                    while len(active_fire) > 25 and not "12" in instincts:
                        active_fire.remove(active_fire[0])
                if "10" in instincts: #GIFTS OF NOTHING
                    for x in range(int(instincts_unbought["10"]["level"]) - len(gon)):
                        gon.append(r.choice(walker_pos_list))
                if oldpp in gon:
                    print("Gift Obtained")
                    if "2" in instincts and int(inv["traps"]) + 1 <= int(instincts_unbought["5"]["level"]) + 1:
                        inv["traps"] = int(inv["traps"]) + 1
                    if "3" in instincts and "14" in instincts and inv["Fire Bottles"] + 1 <= int(instincts_unbought["5"]["level"]) + 1:
                        inv["Fire Bottles"] += 1
                    if "3" in instincts and inv["Flamer Gas"] + 3 <= 5*(int(instincts_unbought["5"]["level"]) + 1):
                        inv["Flamer Gas"] += 3
                    gon.remove(oldpp) 
                if pred_type == "Reaper":
                    deathzonecountercheck = False
                    for x in range(len(deathzones)):
                        if oldpp == deathzones[x][0]:
                            deathzonecounter += 1
                            deathzonecountercheck = True
                    if deathzonecountercheck == False:
                        if deathzonecounter != 0:
                            deathzonecounter -= .5
                    if deathzonecounter >= 3:
                        print("Reep's scythe of death has claimed its bounty.")
                        notdeath()
                        break
                    deathzonefreq += deathzonefreqincrements
                    if deathzonefreqincrements < 25:
                        deathzonefreqincrements += .1
                    if deathzonefreq >= 1:
                        deathzones.append([r.choice(walker_pos_list), 25])
                        if personaldeathzone == 3:
                            deathzones.append([oldpp, 25])
                            personaldeathzone = 0
                        else:
                            personaldeathzone += 1
                        deathzonefreq = 0
                    while len(deathzones) >= round(pathgenspecs[0] / 1.5):
                        deathzones.remove(deathzones[0])
                    tempdeathzones = deathzones.copy()
                    for x in range(len(deathzones)):
                        deathzones[x][1] -= 1
                        if deathzones[x][1] == 0:
                            if deathzones[x][0] in walker_pos_list:
                                editmap(deathzones[x][0][0],deathzones[x][0][1],walkable)
                            else:
                                editmap(deathzones[x][0][0],deathzones[x][0][1],blank)
                            tempdeathzones.remove(deathzones[x])
                    deathzones = tempdeathzones.copy()
                    tempdeathzones = deathzones.copy()
                    for x in deathzones:
                        for i in active_fire:
                            if x[0] == i:
                                editmap(x[0][0],x[0][1],walkable)
                                tempdeathzones.remove(x)
                                break
                    deathzones = tempdeathzones.copy()
                    tempdeathzones = deathzones.copy()
                    for x in deathzones:
                        for i in active_moving_projectiles:
                            if x[0] == i[0]:
                                editmap(x[0][0],x[0][1],walkable)
                                try:
                                    tempdeathzones.remove(x)
                                except:
                                    pass
                    deathzones = tempdeathzones.copy()
        if oblivion_choice == "2":
            for key in tutorials:
                print(str(key) +" - "+ tutorials[key][0])
            tutorials_choice = input("Enter Book Index:")
            try:
                print(tutorials[tutorials_choice][1])
            except:
                print("No such book index exists.")
        if oblivion_choice == "3":
            ns = {}
            for x in instincts_unbought:
                ns[int(x)] = instincts_unbought[x]["status"]
            """
            ns = {
            0:instincts_unbought["0"]["status"],
            1:instincts_unbought["1"]["status"],
            2:instincts_unbought["2"]["status"],
            3:instincts_unbought["3"]["status"],
            4:instincts_unbought["4"]["status"],
            5:instincts_unbought["5"]["status"],
            6:instincts_unbought["6"]["status"],
            7:instincts_unbought["7"]["status"],
            8:instincts_unbought["8"]["status"],
            9:instincts_unbought["9"]["status"],
            10:instincts_unbought["10"]["status"],
            11:instincts_unbought["11"]["status"],
            12:instincts_unbought["12"]["status"],
            13:instincts_unbought["13"]["status"],
            14:instincts_unbought["14"]["status"],
            15:instincts_unbought["15"]["status"],
            16:instincts_unbought["16"]["status"],
            17:instincts_unbought["17"]["status"],
            18:instincts_unbought["18"]["status"],
            19:instincts_unbought["19"]["status"],
            20:instincts_unbought["20"]["status"],
            100:instincts_unbought["100"]["status"],
            }
            """
            instinct_tree = {
            1:"     "+str(ns[2])+" - "+str(ns[4])+" - "+str(ns[9])+" - "+str(ns[15])+" - "+str(ns[11])+"               ",
            2:"    /                                ",
            3:str(ns[0])+" - "+str(ns[1])+" - "+str(ns[10])+" - "+str(ns[20])+" - "+str(ns[100])+"  ",
            4:"   \                             ",
            5:"    "+str(ns[3])+" - "+str(ns[5])+" - "+str(ns[8])+" - "+str(ns[14])+" - "+str(ns[16])+" -  "+str(ns[12])+"          ",
            6:"      \                           ",
            7:"        "+str(ns[6])+" - "+str(ns[7])+" - "+str(ns[17])+" - "+str(ns[18])+" - "+str(ns[19])+"      ",
            }
            
            """Real instinct_tree = {
            1:"     2 - 4 - 9 - 15 - 11                ",
            2:"    /                                 ",
            3:"0- 1 - 10 - 20 - 100 ",
            4:"   \                             ",
            5:"    3 - 5 - 8 - 14 - 16 - 12          ",
            6:"      \                           ",
            7:"        6 - 7 -17 - 18 - 19        ",
            }"""
            for key in instinct_tree:
                print(instinct_tree[key])
            instinct_choice = input("choose node, [enter] to leave")
            try:
                print(instincts_unbought[instinct_choice]["name"])
                print(str(instincts_unbought[instinct_choice]["level"])+"/"+str(instincts_unbought[instinct_choice]["max level"])+" levels")
                print("Cost: "+str(instincts_unbought[instinct_choice]["price"]) + " Mastery Points")
                print("You have: "+str(status["mastery points"]) + " Mastery Points")
                print(instincts_unbought[instinct_choice]["effect"])
                print(instincts_unbought[instinct_choice]["description"])
                print("Requires instinct "+str(instincts_unbought[instinct_choice]["prereq"])+" - "+str(instincts_unbought[str(instincts_unbought[instinct_choice]["prereq"])]["name"]))
                buychoice = input("Would you like to buy? y|n")
                if buychoice == "y" and int(status["mastery points"]) >= int(instincts_unbought[instinct_choice]["price"]) and int(instincts_unbought[instinct_choice]["level"]) < int(instincts_unbought[instinct_choice]["max level"]):
                    if str(instincts_unbought[instinct_choice]["prereq"]) in instincts or instincts_unbought[instinct_choice]["prereq"] == 0:
                        print("upgrade purchased")
                        status["mastery points"] -= instincts_unbought[instinct_choice]["price"]
                        instincts_unbought[instinct_choice]["level"] = int(instincts_unbought[instinct_choice]["level"]) + 1
                        if instincts_unbought[instinct_choice]["level"] == instincts_unbought[instinct_choice]["max level"]:
                            instincts_unbought[instinct_choice]["status"] = xd*len(instincts_unbought[instinct_choice]["status"])
                        instincts[str(instinct_choice)] = [instincts_unbought[instinct_choice]["name"],instincts_unbought[instinct_choice]["level"]]
                        if instinct_choice == "100":
                            print("\nRoamers only have one way out of the Labyrinth, and that is to become mortal, then to accept their fate. to pass away in the Labyrinth is to die in the Rove, and to die in the Rove is to live once again. We all must overcome our challenges, or we will become the challenge . \n")
                            time.sleep(20)
                            print("\nCongrats and Thank You for Playing my Game!\n")
                            time.sleep(10)
                            savingcode()
                            break
                        if instinct_choice == "13":
                            print("\nAll Roamers have a choice to stay, but are you strong enough to not become twisted like those before and hunt your brethren?\n")
                            time.sleep(20)
                            print("\nCongrats and Thank You for Playing my Game, and Congrats for Finding the Hidden Ending!\n")
                            time.sleep(10)
                            savingcode()
                            break
                    elif buychoice == "y":
                        print("Does not meet prerequisite requirements. ")
                elif buychoice == "y" and int(status["mastery points"]) >= int(instincts_unbought[instinct_choice]["price"]):
                    print("Max level")
                elif buychoice == "y" and int(instincts_unbought[instinct_choice]["level"]) < int(instincts_unbought[instinct_choice]["max level"]):
                    print("Does not meet mastery requirements. ")
                if buychoice == "n":
                    print("Not puchasing, returning to oblivion. ")
            except Exception as exc:
                if instinct_choice != "":
                    print(exc)
                    print("incorrect skill name entered, returning to Oblivion. ")
                else:
                    print("returning to Oblivion. ")
        if oblivion_choice == "4": # Boons Section
            #["ex"]:[0"name", 1"description", 2on state, 3unlocked state, 4unlock requirement]
            boon_notification = ""
            for x in boons:
                xnum = x
                x = boons[x]
                if x[3] > 0:
                    onstate = "Off"
                    if x[2] == True:
                        onstate = "On"
                    print(str(xnum)+" : "+str(x[0])+" - "+onstate)
                elif x[3] == 0:
                    print(str(xnum) + " : ???")
            boon_choice = input("input boon number || [enter] to exit") 
            try:
                if boon_choice != "" and boons[boon_choice][3] > 0:
                    onstate = "Off"
                    if boons[boon_choice][2] == True:
                        onstate = "On"
                    print(str(boons[boon_choice][0])+" : "+onstate)
                    print(boons[boon_choice][1])
                    print(boons[boon_choice][4])
                    print("level - "+str(boons[boon_choice][3]))
                    boon_on_choice = input("Turn on, [y] || Turn off, [n]")
                    if boon_on_choice == "y":
                        boon_limit = int(instincts_unbought["20"]["level"])
                        for x in boons:
                            if boons[x][2] == True and boon_limit <= 0:
                                boons[x][2] = False
                            elif boons[x][2] == True and boon_limit > 0:
                                boon_limit -= 1
                        boons[boon_choice][2] = True
                        print("Boon Activated")
                    elif boon_on_choice == "n":
                        boons[boon_choice][2] = False
                elif boon_choice != "" and boons[boon_choice][3] == 0:
                    print("")
                    print(boons[boon_choice][4])
                    print("")
            except:
                print("Bad input: Exiting Boons")
        if oblivion_choice == "5":
            for key in status:
                print(str(key) +" - "+ str(status[key]))
            print("")
            for key in instincts:
                print(str(key) +" - "+ str(instincts[key]))
            print("")
        if oblivion_choice == "6":
            for key in settings:
                print(str(key)+" - "+str(settings[key][0]))
            settings_choice = input("which setting:")
            for key in settings:
                if key == settings_choice:
                    print(str(settings[key][1])+"\ncurrent setting: "+str(settings[key][2]))
                    setting_value = input("Input new value:")
                    try:
                        if len(settings[key]) == 4:
                            settings[key][2] = str(setting_value)
                        else:
                            settings[key][2] = int(setting_value)
                    except ValueError:
                        print("Bad Input")
        if oblivion_choice == "7":
            saveGame('')
        #     boon_donut_cheat = 0
        #     try:
        #         if presavecode == "":
        #             theload = input("Enter Code:")
        #         else:
        #             theload = presavecode
        #         theload = theload.split(":")
        #         for x in theload:
        #             if "st-" in x:
        #                 if "mp" in x:
        #                     tempx = x.split(";")
        #                     status["mastery points"] = int(tempx[1])
        #             if "in-" in x:
        #                 tempx = x.split("-")
        #                 #print(tempx)
        #                 tempx = tempx[1]
        #                 tempx = tempx.split(";")
        #                 for key in instincts_unbought:
        #                     if instincts_unbought[key]["name"] == tempx[0]:
        #                         inspot = key
        #                 instincts[str(inspot)] = [tempx[0],tempx[1]]
        #                 instincts_unbought[inspot]["level"] = tempx[1]
        #                 if int(instincts_unbought[inspot]["level"]) == int(instincts_unbought[inspot]["max level"]):
        #                     instincts_unbought[inspot]["status"] = "×"*len(instincts_unbought[inspot]["status"])
        #             if "bo-" in x:
        #                 tempx = x.split("-")
        #                 tempx = tempx[1]
        #                 tempx = tempx.split(";")
        #                 tempxx = tempx[0]
        #                 tempxx = str(tempxx)
        #                 boons[tempxx][3] = int(tempx[1])
        #                 if len(tempx) == 3:
        #                     if tempx[2] == "*" and boon_donut_cheat == 0:
        #                         boons[tempxx][2] = True
        #                         boon_donut_cheat = 1
        #             if "se-" in x:
        #                 tempx = x.split(";")
        #                 settingtemp = tempx[0].split("-")
        #                 if "*" in tempx:
        #                     settings[settingtemp[1]][2] = str(tempx[1])
        #                 else:
        #                     settings[settingtemp[1]][2] = int(tempx[1])
        #             if "ti-" in x:
        #                 settingtemp = x.split("-")
        #                 all_gone = round(time.time() - float(settingtemp[1]))
        #                 all_gone = round(time.time() - float(settingtemp[1]))
        #                 days_gone = m.floor(all_gone / 86400)
        #                 if days_gone == 0:
        #                     hours_gone = m.floor((all_gone) / 3600)
        #                 else:
        #                     hours_gone = m.floor((all_gone % days_gone) / 3600)
        #                 minutes_gone = m.floor((all_gone % 3600)/ 60)
        #                 seconds_gone = ((all_gone - hours_gone) - minutes_gone) % 60
        #                 print(f"\nWelcome back Roamer! You have been gone {days_gone} days, {hours_gone} hours, {minutes_gone} minutes, and {seconds_gone} seconds.\n")
        #                 time.sleep(1)
        #             if "hs" in x:
        #                 settingtemp = x.split("-")
        #                 hidden_shelves = int(settingtemp[1])
        #     except Exception as exc: #SWITCH TO EXCEPT WHEN DONE
        #         print(exc)
        #         traceback.print_exc()
        #         print("Bad Savecode: Fix it or contact Dev")
        #     presavecode = ""
        if oblivion_choice == "8" and hidden_shelves < 0:
            for key in hidden_texts:
                if int(key) <= hidden_shelves:
                    print(str(key) +" - "+ hidden_texts[key][0])
            tutorials_choice = input("Enter Book Index:")
            try:
                if int(hidden_texts) <= hidden_shelves:
                    print(hidden_texts[tutorials_choice][1])
            except:
                print("No such book index exists.")

if __name__ == "__main__":
    root = tk.Tk()
    console = TkConsole(root)

    threading.Thread(
        target=mainGame,
        args=(console,),
        daemon=True
    ).start()

    root.mainloop()