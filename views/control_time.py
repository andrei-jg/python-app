import threading
import time
import views.utils.utils as utils

class TimeCounter:
    """
    A thread-safe class to track elapsed time since initialization,
    with support for pausing and resuming the timer.
    """

    def __init__(self, chords_data: dict, duration_each_notes: dict):
        """
        Initialize the TimeCounter instance.
        
        Attributes:
        - start_time (float): Time when TimeCounter was initialized (Unix timestamp).
        - elapsed_time (float): Total elapsed time in seconds since start_time.
        - last_updated_time (float): Time when elapsed_time was last updated.
        - lock (threading.Lock): Threading lock for ensuring thread safety.
        - running (bool): Flag indicating whether the timer is running.
        - paused (bool): Flag indicating whether the timer is currently paused.
        - condition (threading.Condition): Condition variable for pausing/resuming.
        """
        self.start_time = time.time()
        self.elapsed_time = 0
        self.last_updated_time = self.start_time
        self.lock = threading.Lock()
        self.running = True
        self.paused = False
        self.condition = threading.Condition(self.lock)
        self.duration_each_notes = duration_each_notes

        self.chord = chords_data
        self.position_chord = 0

    def update_time(self):
        """
        Method executed by the timer thread to continuously update elapsed_time.
        """
        while self.running:
            with self.condition:
                while self.paused:
                    self.condition.wait()  # Wait until notified to resume
                current_time = time.time()
                self.elapsed_time += current_time - self.last_updated_time
                self.last_updated_time = current_time
            # time.sleep(0.1)  # Avoid busy-waiting

    def get_time(self):
        """
        Returns the current elapsed time in seconds.
        
        Returns:
        - float: Current elapsed time.
        """
        with self.lock:
            return self.elapsed_time

    def stop(self):
        """
        Stops the timer thread and ends the update_time loop.
        """
        self.running = False
        self.resume()  # Ensure thread is not stuck in wait state

    def pause(self):
        """
        Pauses the timer thread.
        """
        with self.condition:
            self.paused = True

    def get_chord(self):
        return self.chord


    def resume(self):
        """
        Resumes the paused timer thread.
        """
        with self.condition:
            if self.paused:
                self.last_updated_time = time.time()  # Update last_updated_time to current time
                self.paused = False
                self.condition.notify_all()  # Wake up waiting thread

    def get_data(self):
        return self.get_chord()

# if __name__ == "__main__":

song_title = "rem-losing_my_religion.json"
chords_data = utils.send_uri('GET', {"song": song_title}, 'get-song')['message']



title = chords_data['title']
tempo = chords_data['tempo']
chords_data = chords_data['tracks'][1]["Guitar 2"]

total_elements = len(chords_data)

print(title)
print(tempo)
print(total_elements)


notas = print(chords_data)['notes']

for i in range(len(notas)):
    print(notas[i])


for i in range(265):
    print(f"{i + 1}: {chords_data[i]['time']} / {chords_data[i]['notes']} / {float(chords_data[i]['time'])*60/tempo}" )

input()

time_counter = TimeCounter(chords_data=chords_data)
counter_thread = threading.Thread(target=time_counter.update_time)
counter_thread.start()

try:
    while True:
        print(f"Elapsed time: {time_counter.get_time():.3f} seconds")
except KeyboardInterrupt:
    time_counter.stop()
    counter_thread.join()
    print("Timer stopped.")
