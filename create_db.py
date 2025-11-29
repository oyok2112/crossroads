import sqlite3

def create_database(db_path='crossroads.db'):
    """Create and populate the CrossroadsDemon database"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Drop existing tables
    cur.execute("DROP TABLE IF EXISTS arcana")
    cur.execute("DROP TABLE IF EXISTS arms")
    cur.execute("DROP TABLE IF EXISTS familiars")
    cur.execute("DROP TABLE IF EXISTS locations")
    cur.execute("DROP TABLE IF EXISTS vows")
    
    # Create tables
    cur.execute('''
        CREATE TABLE locations (
            location TEXT,
            banished INTEGER
        )
    ''')
    
    cur.execute('''
        CREATE TABLE arms (
            weapon TEXT,
            banished INTEGER
        )
    ''')
    
    cur.execute('''
        CREATE TABLE familiars (
            familiar TEXT,
            banished INTEGER
        )
    ''')
    
    cur.execute('''
        CREATE TABLE vows (
            vow TEXT,
            fear1 INTEGER,
            fear2 INTEGER,
            fear3 INTEGER,
            fear4 INTEGER,
            maxlevel INTEGER,
            sort INTEGER,
            banished INTEGER
        )
    ''')
    
    cur.execute('''
        CREATE TABLE arcana (
            card TEXT,
            grasp INTEGER,
            sort INTEGER,
            banished INTEGER
        )
    ''')

    # Insert locations
    cur.execute("INSERT INTO locations VALUES (?, ?)", ('Underworld', 0))
    cur.execute("INSERT INTO locations VALUES (?, ?)", ('Surface', 0))
    
    # Insert arms
    arms_data = [
        ('Descura - Staff', 0),
        ('Lim and Oros - Blades', 0),
        ('Ygnium - Flames', 0),
        ('Zorephet - Axe', 0),
        ('Revvaal - Argent Skull', 0),
        ('Xinth - Coat', 0)
    ]
    cur.executemany("INSERT INTO arms VALUES (?, ?)", arms_data)
    
    # Insert familiars
    familiars_data = [
        ('Frinos', 0),
        ('Toula', 0),
        ('Raki', 0),
        ('Hecuba', 0),
        ('Gale', 1)
    ]
    cur.executemany("INSERT INTO familiars VALUES (?, ?)", familiars_data)
    
    # Insert vows
    vows_data = [
        ('Pain', 1, 2, 2, 0, 3, 1, 0),
        ('Grit', 1, 1, 1, 0, 3, 2, 0),
        ('Wards', 1, 1, 0, 0, 2, 3, 0),
        ('Frenzy', 3, 3, 0, 0, 2, 4, 0),
        ('Hordes', 1, 1, 1, 0, 3, 5, 0),
        ('Menace', 1, 2, 0, 0, 2, 6, 0),
        ('Return', 1, 1, 0, 0, 2, 7, 0),
        ('Fangs', 2, 3, 0, 0, 2, 8, 0),
        ('Scars', 1, 1, 2, 0, 3, 9, 0),
        ('Debt', 1, 1, 0, 0, 2, 10, 0),
        ('Shadow', 2, 0, 0, 0, 1, 11, 0),
        ('Forfeit', 3, 0, 0, 0, 1, 12, 0),
        ('Time', 1, 2, 3, 0, 3, 13, 0),
        ('Void', 1, 1, 1, 2, 4, 14, 0),
        ('Hubris', 1, 1, 0, 0, 2, 15, 0),
        ('Denial', 2, 0, 0, 0, 1, 16, 0),
        ('Rivals', 2, 3, 3, 4, 4, 17, 0)

    ]
    cur.executemany("INSERT INTO vows VALUES (?, ?, ?, ?, ?, ?, ?, ?)", vows_data)
    
    # Insert arcana
    arcana_data = [
        ('The Sorceress', 1, 1, 0),
        ('The Wayward Son', 1, 2, 0),
        ('The Huntress', 2, 3, 0),
        ('Eternity', 3, 4, 0),
        ('The Moon', 0, 5, 0),
        ('The Furies', 2, 6, 0),
        ('Persistence', 2, 7, 0),
        ('The Messenger', 1, 8, 0),
        ('The Unseen', 5, 9, 0),
        ('Night', 2, 10, 0),
        ('The Swift Runner', 1, 11, 0),
        ('Death', 4, 12, 0),
        ('The Centaur', 0, 13, 0),
        ('Origination', 5, 14, 0),
        ('The Lovers', 3, 15, 0),
        ('The Enchantress', 3, 16, 0),
        ('The Boatman', 5, 17, 0),
        ('The Artificer', 3, 18, 0),
        ('Excellence', 5, 19, 0),
        ('The Queen', 0, 20, 0),
        ('The Fates', 0, 21, 0),
        ('The Champions', 4, 22, 0),
        ('Strength', 4, 23, 0),
        ('Divinity', 0, 24, 0),
        ('Judgement', 0, 25, 0)
    ]
    cur.executemany("INSERT INTO arcana VALUES (?, ?, ?, ?)", arcana_data)
    
    conn.commit()
    conn.close()
    print("Database created successfully!")

if __name__ == "__main__":
    create_database()