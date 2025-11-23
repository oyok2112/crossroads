           Crossroads
 _____ _____ _____ _____ _____ 
|     |  |  |  _  |     |   __|
|   --|     |     |  |  |__   |
|_____|__|__|__|__|_____|_____|
- for Showciety Gives Back 2025 - 

    "This world is born of impulse, not of carefully crafted plans" 
      - Chaos, Hades II

Framework for randomizing a series of challenge runs (intuitive interfaces encouraged)
Set it and forget it (nothing randomized that isn't set in stone at crossroads)
NOT a mod
NOT integrated into the Hades II .exe file at all

Runs entirely on a sqlite database created at first run (imported in [crossroads.py] from [create_db.py])

Installation Instructions:
    1. Install imports in pip
    2. Run crossroads.py
    3. Chaos

--------------------------------
Operation Instructions
--------------------------------

Commands (Case INsensitive):
    [empty input] (enter): Randomize New Run
    [CHRONOS]: starts timer system
    [F+]: increase fear
    [F-]: decrease fear

Features:
    [crossroads.py]
        - CrossroadsDaemon randomizer engine
        - Randomizes all Crossroads setup things:
            - Weapon
            - Familiar
            - Location (Underworld or Surface)
            - Arcana Cards/Grasp [WIP]
            - most importantly...VOWS
        - Vows are randomly chosen at random ranks up to a set Fear level
        - Event Timer to change fear over time [chronos]
    [toula.py]
        - Optional hotkey to randomize UP/DOWN keypresses to select boons/upgrades
        - [todo] integrate into main crossroads.py
    [_logs]
        - [crossroads_log.txt] historical log of runs
        - [crossroads_obs.txt] status bar text that can be used as a Text (GDI+) source in OBS
        - [next_run_obs.txt] status of fear and grasp that will be randomized next run
    [TODO]
        - Weapon aspects
        - Controller integration
        - Idle detection (anti-stall)
    