#!/usr/bin/env python3

import RPi.GPIO as GPIO
import pygame
import time

GLOBAL_VOLUME = 0.7

LEVER = 40
DIAL = 38
BEEPER = 36

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LEVER, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(DIAL, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BEEPER, GPIO.IN, GPIO.PUD_UP)

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('before-dialing-long.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(GLOBAL_VOLUME)
pygame.mixer.music.pause()

process_dialing = pygame.mixer.Sound('process-of-dialing.wav')
beeping_dialing = pygame.mixer.Sound('beeping-of-dialing.wav')
intro           = pygame.mixer.Sound('intro-music.wav')
y1937           = pygame.mixer.Sound('years/1937.wav')
y1941           = pygame.mixer.Sound('years/1941.wav')
y1961           = pygame.mixer.Sound('years/1961.wav')
y1972           = pygame.mixer.Sound('years/1972.wav')
y2015           = pygame.mixer.Sound('years/2015.wav')
wrong_number    = pygame.mixer.Sound('wrong-number-dialed.wav')

prev_lever = GPIO.input(LEVER)
prev_dial = GPIO.input(DIAL)
prev_beeper = GPIO.input(BEEPER)

digit_counter = 0
year_string = ""

print("TAX-O-PHONE by SHKLJ for DVOREC73")
intro.play()
intro.set_volume(0.3)
time.sleep(6)

while (True):
    #entering "handset is off the lever" state
    if ((prev_lever != GPIO.input(LEVER)) and (GPIO.input(LEVER) == False)):
        prev_lever = GPIO.input(LEVER)
        pygame.mixer.music.unpause()

    if (GPIO.input(LEVER) == False):
        #entering "dialing process has started" state
        if ((prev_dial != GPIO.input(DIAL)) and (GPIO.input(DIAL) == False)):
            prev_dial = GPIO.input(DIAL)
            pygame.mixer.music.pause()
            process_dialing.play()
            process_dialing.set_volume(GLOBAL_VOLUME)

    if ((GPIO.input(LEVER) == False) and (GPIO.input(DIAL) == False)):
        #entering "couting tick-tocks" state
        if ((prev_beeper != GPIO.input(BEEPER)) and (GPIO.input(BEEPER) == False)):
            prev_beeper = GPIO.input(BEEPER)
            pygame.mixer.music.pause()
            digit_counter += 1
            beeping_dialing.play()
            beeping_dialing.set_volume(GLOBAL_VOLUME)

    #exiting "couting tick-tocks" state
    if ((prev_beeper != GPIO.input(BEEPER)) and (GPIO.input(BEEPER) == True)):
        prev_beeper = GPIO.input(BEEPER)
        pygame.mixer.stop()
        pygame.mixer.music.unpause()

    #exiting "dialing process has started" state
    if ((prev_dial != GPIO.input(DIAL)) and (GPIO.input(DIAL) == True)):
        prev_dial = GPIO.input(DIAL)
        if (digit_counter == 0):
            year_string += "1"
        elif (digit_counter >= 10):
            year_string += "0"
        else:
            year_string += str(digit_counter)
        digit_counter = 0
        pygame.mixer.stop()
        pygame.mixer.music.unpause()

    #exiting "handset is off the lever" state
    if ((prev_lever != GPIO.input(LEVER)) and (GPIO.input(LEVER) == True)):
        prev_lever = GPIO.input(LEVER)
        year_string = ""
        pygame.mixer.music.pause()
        pygame.mixer.stop()

    if (len(year_string) >= 4):
        if (year_string == "1937"):
            pygame.mixer.music.pause()
            y1937.play()
            y1937.set_volume(GLOBAL_VOLUME)
        elif (year_string == "1941"):
            pygame.mixer.music.pause()
            y1941.play()
            y1941.set_volume(GLOBAL_VOLUME)
        elif (year_string == "1961"):
            pygame.mixer.music.pause()
            y1961.play()
            y1961.set_volume(GLOBAL_VOLUME)
        elif (year_string == "1972"):
            pygame.mixer.music.pause()
            y1972.play()
            y1972.set_volume(GLOBAL_VOLUME)
        elif (year_string == "2015"):
            pygame.mixer.music.pause()
            y2015.play()
            y2015.set_volume(GLOBAL_VOLUME)
        else:
            wrong_number.play()
            wrong_number.set_volume(GLOBAL_VOLUME)
        print(year_string)
        year_string = ""


