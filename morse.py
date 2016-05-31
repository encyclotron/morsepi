#!/usr/bin/python

import argparse
import sys
import time
import RPi.GPIO as io
import os

io.setwarnings(False)

parser = argparse.ArgumentParser(prog="morse.py", usage="morse.py <options> <\"message\">")
## available arguments to use to control program
parser.add_argument(
'-s', '--speed', help="speed in seconds, may be a floating point decimal or integer")
parser.add_argument(
'-m', '--message', help="quoted string of characters")
parser.add_argument(
'-p', '--pin', help="pin number to use for light")
parser.add_argument(
'-M', '--mode', help="use BCM or BOARD depending on preference")
## send all args to array
opt = parser.parse_args()
## set options if founs otherwise use defaults
if(opt.speed):
	speed = float(opt.speed)
else:
	speed = float(.1)
##
if(opt.message):
	message = opt.message
else:
	message = "Hello, World!"
##
if(opt.pin):
	pin = int(opt.pin)
else:
	pin = int(21)
##
if(opt.mode):
	mode = opt.mode
else:
	mode = "BCM"

print("Speed: " + str(speed))
print("Message: " + str(message))
print("Pin: " + str(pin))
print("Mode: " + str(mode))
time.sleep(3)
## Variables to be used
dot = speed
dash = dot*3
#numerals and alphabet
signs=['0','1','2','3','4','5','6','7','8','9',
'a','b','c','d','e','f','g','h','i','j','k','l',
'm','n','o','p','q','r','s','t','u','v','w','x','y','z']
#corresponding signals for numerals in morse
morse=['-----','.----','..---','...--','....-','.....',
'-....','--...','---..','----.','.-','-...','-.-.','-..',
'.','..-.','--.','....','..','.---','-.-','.-..','--','-.',
'---','.--.','--.-','.-.','...','-','..-','...-','.--','-..-',
'-.--','--..']

## FUNCTIONS
# is_codable(s) returns a boolean value which compares the item 
#submitted with the signs which are morse-codable
def is_codable(s):
        for i in range(0, len(signs)):
                if (s == signs[i]):
                        return True
        return False

#return the morse eqivalent of the character passed
#to the function, else return nothing 
def find_signs(letter):
        for i in range(0, len(signs)):
               if(letter == signs[i]):
                        return morse[i]
               else:
                        pass
# print to console and calls blink_light()
def print_message():
	while True:
        	os.system('clear')
        	for i in range(0, len(message)):
			if (is_codable(message[i].lower())):
		                next=str(message[i].lower())
	                        code=find_signs(message[i].lower())
        		        print (next + " " + code)
				blink_light(next)
	                else:
				pass

def blink_light(s):
		io.output(pin, 0)
		code=find_signs(s)
		for i in range(0, len(code)):
			if code[i] == ".":
				io.output(pin, 1)
				time.sleep(dot)
				io.output(pin, 0)
				time.sleep(speed)
			elif code[i] == "-":
				io.output(pin,1)
				time.sleep(dash)
				io.output(pin, 0)
				time.sleep(speed)

## setup RPi.GPIO options
try:
	if(mode == "BCM"):
		io.setmode(io.BCM)
	else:
		io.setmode(io.BOARD)

	io.setup(pin, io.OUT)
		
	io.output(pin, 0)
	count = 0
	print_message()

##
except(KeyboardInterrupt, SystemExit):
	os.system('clear')
	print("End of Transmission")
	time.sleep(speed)
	io.cleanup()

io.cleanup()
