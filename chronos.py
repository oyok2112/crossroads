# chronos
# poc - just calculate a number damnit - nothing more

import threading
import time

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


fear_chart = [ 20, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 ]
event_time = 180            # time (in minutes) of entire event
interval = event_time / len(fear_chart)
print(interval)

print("starting timer for " + " minutes")
print("death to chronos...")

for fear_level in fear_chart:
    time.sleep(interval)
    print(f"Fear reduced to " + str(fear_level))
