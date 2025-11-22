# CrossroadsDaemon by oyok for Super Mario Showciety Gives Back 2025
#
# future:
#   weapon mods
#   fear calculator


#import psycopg2
#import twitch_chat_irc
import random
import os
import re
import create_db
import sqlite3
import threading
import time
from datetime import datetime

class CountdownTimer:
    def __init__(self, seconds):
        self.seconds = seconds
        self.running = False
        self.thread = None
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
    
    def _run(self):
        while self.seconds > 0 and self.running:
            time.sleep(self.seconds)
            self.seconds -= 1
        if self.running:
            print("Time's up!")
    
    def stop(self):
        self.running = False
    
    def get_time_remaining(self):
        return self.seconds

def test():
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print(f"PostgreSQL database version: {db_version}")

def randomize():
    print("generating chaos...")
    random.seed()
    cur = conn.cursor()
    cur.execute("select card, grasp, sort from arcana where banished = 0 order by sort")
    tmp = cur.fetchall()
    arcana = []
    for row in tmp:
        arcana.append(row)
    cur.execute("select weapon from arms where banished = 0")
    tmp = cur.fetchall()
    arms = []
    for row in tmp:
        arms.append(row)
    cur.execute("select familiar from familiars where banished = 0")
    tmp = cur.fetchall()
    familiars = []
    for row in tmp:
        familiars.append(row)
    cur.execute("select location from locations where banished = 0")
    tmp = cur.fetchall()
    locations = []
    for row in tmp:
        locations.append(row)
    cur.execute("select vow, fear1, fear2, fear3, fear4, maxlevel from vows where banished = 0")
    tmp = cur.fetchall()
    vows = []
    for row in tmp:
        vows.append(row)

    # location
    location = " ".join(random.choice(locations))

    # weapon
    weapon = " ".join(random.choice(arms))

    # familiar
    familiar = " ".join(random.choice(familiars))
    if familiar == "Gale":
        familiar = "Toula"

    # arcana
    card_list = []
    total_grasp = 0
    rand_max_grasp = random.randint(0, max_grasp)
    while total_grasp < rand_max_grasp:
        arcana_row = random.choice(arcana)
        card = arcana_row[0]
        grasp = arcana_row[1]
        sort = arcana_row[2]
        sort_card = f"{sort:02d}" + ". " + card
        if total_grasp + grasp > max_grasp:
            break
        else:
            if card_list.__contains__(sort_card):
                continue
            card_list.append(sort_card)
            total_grasp = total_grasp + grasp


    # vows
    total_fear = 0
    vows_list = []
    check_list = []
    while total_fear < max_fear:
        #print("total fear: " + str(total_fear))
        vow_row = random.choice(vows)
        if check_list.__contains__(vow_row[0]):
            continue
        vow = vow_row[0]
        fear = [ vow_row[1], vow_row[2], vow_row[3], vow_row[4] ]
        max_rank = vow_row[5]
        rank = random.randint(1,max_rank)
        fear = fear[:rank]
        #print(vow + " " + str(rank) + " | " + str(sum(fear)))
        vow_fear = sum(fear)
        if vow_fear + total_fear <= max_fear:
            total_fear = vow_fear + total_fear
            rank_disp = "+" * rank
            disp_string = vow + " " + rank_disp
            check_list.append(vow)
            vows_list.append(disp_string)
 
    
    timestamp = datetime.now().strftime("%m/%d %I:%M:%S %p") 

    print("complete :)")
    print("embrace the chaos...")
    print("--------------------")
    print(timestamp + "")
    print("--------------------")
    print("LWF:\t" + location + " | " + weapon + " | " + familiar)
    vows = " | ".join(vows_list)
    print("VOWS:\t" + vows)
    print("FEAR: " + str(total_fear) + " | " "GRASP: " + str(rand_max_grasp) + "                  ")
    #card_list.sort()
    #card_list_string = " | ".join(card_list)
    #print("CARD SUG:\t" + card_list_string)
    print("--------------------")

    with (open("crossroads_log.txt","a") as f):
        f.write("embrace the chaos...\n")
        f.write("--------------------\n")
        f.write(timestamp + "\n")
        f.write("--------------------\n")
        f.write("LWF:\t" + location + " | " + weapon + " | " + familiar + "\n")
        vows = " | ".join(vows_list)
        print("VOWS:\t" + vows)
        card_list.sort()
        card_list_string = " | ".join(card_list)
        f.write("CARDS:\t" + card_list_string + "\n")
        f.write("--------------------\n")

    with (open("crossroads_obs.txt","w") as f):
        f.write("Crossroads Chaos TEST for SGB2025")
        f.write("    |    Incentives: $$ Increase Fear  |  $$ Decrease Fear  |  $$ Unlock Surface  |  $$ Unlock Death Defies              ")
        f.write(location + " | " + weapon + " | " + familiar + "                    ")
        for vow in vows_list:
            f.write(vow + "    ")
        f.write("                    ")
        #i = 0
        #card_list.sort()
        #card_list_string = " ".join(card_list)
        #output_list = re.split(r"\d\d.", card_list_string)
        #for card in output_list:
            #f.write(card + "  ")
            #i = i + 1
        #f.write("                    ")

def spawn_overlord(disp):
    cur = conn.cursor()
    cur.execute("""
        select 'locations', location, banished from locations union
        select 'arms', weapon, banished from arms union
        select 'familiars', familiar, banished from familiars union
        select 'vows', vow, banished from vows union
        select 'arcana', card, banished from arcana
    """)
    overlord = cur.fetchall()
    
    # Print or process the results
    if disp is True:
        for row in overlord:
            print(row)
    
    return overlord

def db_connect():
    db_path = 'crossroads.db'

    # Check if database needs to be created
    if not os.path.exists(db_path):
        print("Database not found, creating...")
        create_db.create_database(db_path)

    conn = sqlite3.connect(db_path)
    return conn

def dice_roll(sides):
    print ("rolling " + str(sides) + " sided di(c)e...")
    res = random.randint(1,sides)
    print ("result: " + str(res))


def run_query(query):
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    print(result)
    return

def banish(thing,value):
    ol = spawn_overlord(disp=False)
    cur = conn.cursor()
    
    table = ""
    column = ""
    
    # ------ new way
    hits = 0
    tables = []
    for row in ol:
        if thing in row[1].upper():
            table = row[0]
            tables.append(table)
            hits = hits + 1
    if hits > 1:
        print("multiple table matches found...")
        return
    elif hits == 0:
        print("no table matches found...")
        return
    else:
        table = tables[0]
        print("table match found: " + table) 

    if table == "locations":
        column = "location"
    elif table == "arms":
        column = "weapon"
    elif table == "familiars":
        column = "familiar"
    elif table == "vows":
        column = "vow"
    elif table == "arcana":
        column = "card"    
    
    # DEBUG
    query = "update " + table + " set banished = " + str(value) + " where " + column + " like '%" + thing + "%'"
    #print (query)
    cur.execute(query)
    conn.commit()
    rows_affected = cur.rowcount
    if value == 1:
        print("! banished !")
    if value == 0:
        print("- unbanished -")
    print("category: " + table.capitalize() + " | " + column + ": " + thing)
    
    return

def chronos(duration, chart):
    global max_fear
    interval = duration / len(fear_chart)
    print("chronos set for: " + str(len(chart)) + " intervals at " + str(interval) + " minutes each (" + str(duration) + " total minutes)")
    print(chart)

    for amt in chart:
        time.sleep(interval * 60)
        max_fear += amt
        if max_fear > 67:
            max_fear = 67
        if max_fear < 0:
            max_fear = 0
        sign = ""
        if amt > 0:
            sign = "+"
        #print(f"Fear " + sign + str(amt) + " to " + str(max_fear))
    
    print("death to chronos...")

def reset():
    d = input("this will unban all things, proceed? (y/n): ")
    if d.upper() == "Y":
        cur = conn.cursor()
        cur.execute("update locations set banished = 0")
        cur.execute("update arms set banished = 0")
        cur.execute("update familiars set banished = 0")
        cur.execute("update vows set banished = 0")
        cur.execute("update arcana set banished = 0")
        conn.commit()
        print("all items unbanished!")

def next_run():
    while True:
        with (open("next_run_obs.txt", "w") as f):
            f.write("Next Run:\nFear: " + str(max_fear) + "\nGrasp (Max): " + str(max_grasp))
        time.sleep(1)


#  -------  default values and such
conn = db_connect()
starting_fear = 10
fear_chart = [ -1, -1, -1, -1, -1, -1, -2, -2, -3 ]
max_fear = starting_fear
max_grasp = 30

next_run_thread = threading.Thread(target=next_run)
next_run_thread.start()

os.system("CLS")
while True:
    print("CrossroadsDaemon v0.1 by oyok for SGB2025")
    sel = input(">:) ")
    sel = sel.upper()
    if sel == "":
        randomize()
    if sel == "F":
        print("current fear level: " + str(max_fear))
    if sel == "F+":
        max_fear += 1
        print("max fear set to " + str(max_fear))
    if sel == "F-":
        max_fear -= 1
        print("max fear set to " + str(max_fear))
    if sel == "R":
        randomize()
    if sel == "CHRONOS":
        duration = input("enter total event time (in minutes): ")
        chronos_thread = threading.Thread(target=chronos, args=(int(duration), fear_chart))
        chronos_thread.start()
    if "BAN" in sel and sel[0] != "U":
        sel_split = sel.split(" ")
        category = sel_split[1]
        banish(category,1)
    if "UBAN" in sel:
        sel_split = sel.split(" ")
        category = sel_split[1]
        banish(category,0)
    if sel == "O":
        spawn_overlord(disp=True)
    if "DICE" in sel:
        sides = sel.split(".")[1]
        dice_roll(int(sides))
    if sel == "C":
        os.system("CLS")
    if sel == "0" or sel == "Q":
        quit()
    if sel == "RESET":
        reset()
