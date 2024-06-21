from mido import MidiFile, MidiTrack, Message

# Create a new MIDI file
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Set the program to a guitar sound (program number 25, which is acoustic guitar)
track.append(Message('program_change', program=25, time=0))

# Define the notes for a G major chord (G, B, D)
notes = [69, 59, 62]

# Set a reasonable duration for the notes (in ticks)
duration = 2000  # Adjust as needed

# Create note_on messages for each note in the chord
for note in notes:
    track.append(Message('note_on', note=note, velocity=64, time=0))

# Create note_off messages for each note after the duration
for note in notes:
    track.append(Message('note_off', note=note, velocity=64, time=duration))

# Save the MIDI file
mid.save('g_major_chord.mid')



