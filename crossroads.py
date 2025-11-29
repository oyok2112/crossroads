# CrossroadsDaemon by oyok for Super Mario Showciety Gives Back 2025
#
# future:
#   weapon mods


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
import matplotlib.pyplot as plt

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

    with (open("_logs/crossroads_log.txt","a") as f):
        f.write("embrace the chaos...\n")
        f.write("--------------------\n")
        f.write(timestamp + "\n")
        f.write("--------------------\n")
        f.write("LWF:\t" + location + " | " + weapon + " | " + familiar + "\n")
        vows = " | ".join(vows_list)
        f.write("VOWS:\t" + vows)
        card_list.sort()
        card_list_string = " | ".join(card_list)
        f.write("CARDS:\t" + card_list_string + "\n")
        f.write("--------------------\n")

    with (open("_logs/crossroads_obs.txt","w") as f):
        f.write("Crossroads Chaos for SGB2025    - -  DONATE NOW!   www.showciety.gives     - -     trans rights are human rights     - -      ")
        f.write("                    ")
        f.write(location + " | " + weapon + " | " + familiar + "                    ")
        for vow in vows_list:
            f.write(vow + "    ")
        quip = get_quip()
        f.write("        ")
        f.write("   " + quip + "   ")
        f.write("        ")
        #i = 0
        #card_list.sort()
        #card_list_string = " ".join(card_list)
        #output_list = re.split(r"\d\d.", card_list_string)
        #for card in output_list:
            #f.write(card + "  ")
            #i = i + 1
        #f.write("                    ")

def get_quip():
    quip_list = [
        "'The task of art today is to bring chaos into order.'  -- Theodore Adorno",
        "'Chaos is the score upon which reality is written.'  -- Henry Miller",
        "'In the beginning there was chaos.'  -- Hesiod"
        "'...and you know the thing about chaos? It's fair!'  -- Jonathan Nolan and Christopher Nolan, The Dark Knight"
        "'WHO SUMMONS CHAOS? Oh, hey there, New Kid.'  -- Leopold 'Butters' Stotch, South Park"
        "'I went down to the crossroads, fell down on my knees.  -- Eric Johnson, Crossroads"
    ]

    return random.choice(quip_list)

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
    fields = []
    for row in ol:
        if thing in row[1].upper():
            table = row[0]
            field = row[1]
            tables.append(table)
            fields.append(field)
            hits = hits + 1
    if hits > 1:
        print("multiple table matches found, perhaps you misspelled the thing?")
        return
    elif hits == 0:
        print("no table matches found, perhaps you misspelled the thing?")
        return
    else:
        table = tables[0]
        field = fields[0]
        #print("table match found: " + table + " | field: " + field) 

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
    query = "update " + table + " set banished = " + str(value) + " where " + column + " = '" + field + "';"
   #print (query)
    cur.execute(query)
    conn.commit()
    rows_affected = cur.rowcount
    if rows_affected == 0:
        print("no rows affected (perhaps the name was typed incorrectly?)")
    if rows_affected > 1:
        print("multiple rows affected (perhaps the name was typed incorrectly?)")
    if value == 1:
        print("! banished !")
    if value == 0:
        print("- unbanished -")
    print("category: " + table.capitalize() + " | " + column + ": " + field)
    
    return

class chronos:
    def __init__(self, duration, chart):
        global e_time
        self.duration = duration
        self.chart = chart
        self.e_time = 0.0
        self.prev_mod = 0
        self.fear_index = 0
        self.interval = int(duration) / len(self.chart)
        self.interval *= 60
        print("chronos set for: " + str(len(self.chart)) + " intervals at " + str(self.interval) + " minutes each (" + str(self.duration) + " total minutes)")
        print(self.chart)
        self.display_chart()
        self.chronos_thread = threading.Thread(target=self.run)
        self.chronos_thread.start()
    
    def run(self):
        global max_fear
        while True:
            time.sleep(1)
            self.e_time += 1
            #print(str(e_time % interval) + " / " + str(interval))
            mod = self.e_time % self.interval
            if self.prev_mod > mod and max_fear > min_fear:
                amt = self.chart[self.fear_index]
                amt *= polarity
                max_fear += amt
                if max_fear > 67:
                    max_fear = 67
                if max_fear <= min_fear:
                    max_fear = min_fear
                print("fear changed to " + str(max_fear))
                self.fear_index += 1
                if self.fear_index > len(self.chart) - 1:
                    self.fear_index = len(self.chart) - 1

            self.prev_mod = mod
        # unreachable, but left in for poetic reasons (you can't defeat chronos)
        print("death to chronos...")


    def display_chart(self, save_path="_logs/fear_chart.png"):
        tmp_chart = self.chart[self.fear_index:len(self.chart)]
        potential_fear = max_fear
        
        # Collect data for plotting
        deltas = []
        fear_levels = [max_fear]  # Start with current fear
        time_points = [0]  # Start at 0 minutes
        
        interval_minutes = self.interval / 60  # Convert interval from seconds to minutes
        
        for i, item in enumerate(tmp_chart):
            delta = int(item) * polarity
            deltas.append(delta)
            potential_fear = potential_fear + delta
            if potential_fear <= 0: 
                potential_fear = 0
            fear_levels.append(potential_fear)
            time_points.append((i + 1) * interval_minutes)  # Each interval in minutes
        
        # Set dark style
        plt.style.use('dark_background')
        
        # Create the plot with dark theme colors
        fig, ax = plt.subplots(figsize=(12, 7), facecolor='#1a1a1a')
        ax.set_facecolor('#0d0d0d')
        
        # Plot the fear levels as a line with markers
        ax.plot(time_points, fear_levels, color='#00d4ff', linewidth=3, marker='o', 
                markersize=10, markerfacecolor='#00ff88', markeredgecolor='#ffffff', 
                markeredgewidth=2, alpha=0.9)
        
        # Add fear level labels on points
        for time, fear in zip(time_points, fear_levels):
            ax.text(time, fear, f'{fear}', 
                    ha='center', 
                    va='bottom',
                    fontweight='bold',
                    fontsize=11,
                    color='#ffffff',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#2a2a2a', edgecolor='none', alpha=0.7))
        
        # Stylish axes
        ax.set_xlabel('Time Elapsed (minutes)', fontsize=12, color='#b0b0b0', fontweight='bold')
        ax.set_ylabel('Total Fear', fontsize=12, color='#b0b0b0', fontweight='bold')
        ax.set_title('Fear Progression Over Time', fontsize=16, color='#ffffff', fontweight='bold', pad=20)
        
        # Grid for that pro look
        ax.grid(True, alpha=0.15, linestyle='--', linewidth=0.5, color='#444444')
        ax.set_axisbelow(True)
        
        # Style the spines
        for spine in ax.spines.values():
            spine.set_color('#444444')
            spine.set_linewidth(1)
        
        # Tick styling
        ax.tick_params(colors='#888888', which='both', labelsize=10)
        
        # Start y-axis at 0
        plt.ylim(bottom=0, top=max(fear_levels) + 2)
        plt.xlim(left=0, right=max(time_points) + (interval_minutes * 0.1))  # Add slight padding
        plt.tight_layout()
        
        # Save with high quality
        plt.savefig(save_path, dpi=150, facecolor='#1a1a1a', edgecolor='none')
        plt.close()
        print(f"⏱ Chart saved to {save_path}")

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
        with (open("_logs/next_run_obs.txt", "w") as f):
            f.write("Next Run:\nFear: " + str(max_fear))
        time.sleep(1)


#  -------  default values and such
conn = db_connect()
starting_fear = 10
fear_chart = [ 1, 1, 1, 1, 1, 1, 2, 2, 3 ]
max_fear = starting_fear
min_fear = 0
max_grasp = 30
polarity = -1

random.seed("buffalo nuggets")

next_run_thread = threading.Thread(target=next_run)
next_run_thread.start()

os.system("CLS")
while True:
    print("CrossroadsDaemon v0.1 by oyok for SGB2025")
    print(">:)")
    sel = input()
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
        Chronos = chronos(duration, fear_chart)
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
    if "DICE." in sel:
        sides = sel.split(".")[1]
        dice_roll(int(sides))
    if sel == "C":
        os.system("CLS")
    if sel == "0" or sel == "Q":
        quit()
    if sel == "RESET":
        reset()
    if sel == "ET":
        print(e_time)
    if sel == "POLAR":
        polarity *= -1
    if sel == "CHART" or sel == "LOOKATTHISGRAPH":
        Chronos.display_chart()

