########################################
# Name: Grayson Lessard, Zachary Truxillo, 
# Alayna Fielder-Fields, Justus Blanchard 
# Date: May 16th, 2024 
# Description: Paper Piano (v3).
########################################
import pineworkslabs.RPi as GPIO
from time import sleep, time
import pygame
from array import array
from waveform_vis import WaveformVis
from math import floor
from math import sin

MIXER_FREQ = 44100
MIXER_SIZE = -16
MIXER_CHANS = 1
MIXER_BUFF = 1024
waveform_name = ''

# Wave selector variable. Change this to change wave used.
# 0 = Square; 1 = Triangle; 2 = Sawtooth; 3 = Sinusoidal
useWave = 3

# the note generator class
class Note(pygame.mixer.Sound):
    # note that volume ranges from 0.0 to 1.0
    def __init__(self, frequency, volume):
        self.frequency = frequency
        
        # initialize the note using an array of samples
        pygame.mixer.Sound.__init__(self, buffer=self.build_samples())
        self.set_volume(volume)
        
    # builds an array of samples for the current note
    def build_samples(self):
        # calculate the period and amplitude of the note's wave
        period = int(round(MIXER_FREQ / self.frequency))
        amplitude = 2 ** (abs(MIXER_SIZE) - 1) - 1
        print(amplitude)

        # initialize the note's samples (using an array of
        # signed 16-bit "shorts")
        samples = array("h", [0] * period)
        
        # generate the note's samples
        # Square wave
        if useWave == 0:
            for t in range(period):
                if (t < period / 2):
                    samples[t] = amplitude
                else:
                    samples[t] =-amplitude
    
        # Triangle wave
        if useWave == 1:
            x = 0
            difference = floor(amplitude * 3.85 // len(samples))
            print(period)

            for t in range(period):
                if (t <= period / 4 and x < amplitude):
                    x += difference
                    samples[t] = x
                    print(x)
                elif (t > period / 4 and t <= period / 2  and x < amplitude):
                    x -= difference
                    samples[t] = x
                    print(x)
                elif (t > period / 2 and t <= period / 1.33 and x < amplitude):
                    x -= difference
                    samples[t] = x
                else:
                    x += difference
                    samples[t] = x

        # Sawtooth Wave
        if useWave == 2:    
            x = 0
            difference = floor(amplitude * 1 // len(samples))

        
            for t in range(period):
                if t == 85:
                    x = -x
            
                samples[t] = x
                print(x)
                x += difference
        
        # Sinusoidal Wave
        if useWave == 3:
            x = 0
            difference = floor(amplitude // len(samples))

            for t in range(period):
                x = floor(amplitude * sin(2 * 3.14159 * (t/169)))
                samples[t] = x

        # Visualize the selected waveform. Uses Tkinter to render an image
        # of the wave.
        # vis = WaveformVis()
        # vis.visSamples(samples, waveform_name)
   
        return samples
            
# waits until a note is pressed
def wait_for_note_start():
    while (True):
        # first, check for notes
        for key in range(len(keys)):
            if (GPIO.input(keys[key])):
                return key
                
        # next, check for the play button
        if (GPIO.input(play)):
            # debounce the switch
            while (GPIO.input(play)):
                sleep(0.01)
            return "play"
            
        # finally, check for the record button
        if (GPIO.input(record)):
            # debounce the switch
            while (GPIO.input(record)):
                sleep(0.01)
            return "record"
        sleep(0.01)
            
# waits until a note is released       
def wait_for_note_stop(key):
    while (GPIO.input(key)):
        sleep(0.1)
        

# plays a recorded song    
def play_song():
    # each element in the song list is a list composed of two
    # parts: a note (or silence) and a duration
    for part in song:
        note, duration = part
        # if it's a silence, delay for its duration
        if (note == "SILENCE"):
            sleep(duration)
        # otherwise, play the note for its duration
        else:
            notes[note].play(-1)
            sleep(duration)
            notes[note].stop()
            
            
# preset mixer initialization arguments: frequency (44.1K), size
# (16 bits signed), channels (mono), and buffer size (1KB)
# then, initialize the pygame library
pygame.mixer.pre_init(MIXER_FREQ, MIXER_SIZE, MIXER_CHANS,\
MIXER_BUFF)
pygame.init()

# use the Broadcom pin mode
GPIO.setmode(GPIO.LE_POTATO_LOOKUP)

# setup the pins and frequencies for the notes (C, E, G, B)
keys = [20, 16, 12, 26]
freqs = [261.6, 329.6, 392.0, 493.9]
notes = []

# setup the button pins
play = 19
record = 21

# setup the LED pins
red = 27
green = 18
blue = 17 # if red is too dim, use blue

# setup the input pins
for i in keys:
    GPIO.setup(i, GPIO.IN, GPIO.PUD_DOWN)

GPIO.setup(play, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(record, GPIO.IN, GPIO.PUD_DOWN)

# setup the output pins
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

# create the actual notes
for n in range(len(freqs)):
    notes.append(Note(freqs[n], 1))
    
# begin in a non-recording state and initialize the song
recording = False
song = []

# the main part of the program
print("Welcome to Paper Piano!")
print("Press Ctrl+C to exit...")

# detect when Ctrl+C is pressed so that we can reset the GPIO
# pins
try:
    while (True):
        # start a timer
        start = time()
        # play a note when pressed...until released (also
        # detect play/record)
        key = wait_for_note_start()
        
        # note the duration of the silence
        duration = time() - start
        
        # if recording, append the duration of the silence
        if (recording):
            song.append(["SILENCE", duration])
            
        # if the record button was pressed
        if (key == "record"):
            # if not previously recording, reset the song
            if (not recording):
                song = []
            # note the recording state and turn on the red LED
            recording = not recording
            GPIO.output(red, recording)
            
        # if the play button was pressed
        elif (key == "play"):
            # if recording, stop
            if (recording):
                recording = False
                
            # turn on the green LED
            GPIO.output(red, False)
            GPIO.output(green, True)
            
            # play the song
            play_song()
            GPIO.output(green, False)
            
        # otherwise, a piano key was pressed
        else:
            # start the timer and play the note
            start = time()
            notes[key].play(-1)
            print("Playing note...")
            wait_for_note_stop(keys[key])
            notes[key].stop()
            
            # once the note is released, stop the timer
            duration = time() - start
            
            # if recording, append the note and its duration
            if (recording):
                song.append([key, duration])
                        
except KeyboardInterrupt:
    # reset the GPIO pins
    GPIO.cleanup()
