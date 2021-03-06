#!/usr/bin/env python3
# from subprocess import Popen, PIPE
from time import sleep
from datetime import datetime
import os
import subprocess
import board
import digitalio 
import adafruit_character_lcd.character_lcd as characterlcd
 
# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2
 
# compatible with all versions of RPI as of Jan. 2019
# v1 - v3B+
lcd_rs = digitalio.DigitalInOut(board.D17)
lcd_en = digitalio.DigitalInOut(board.D18)
lcd_d4 = digitalio.DigitalInOut(board.D21)
lcd_d5 = digitalio.DigitalInOut(board.D22)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D24)
 
 
# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, lcd_columns, lcd_rows)
 
# Looking for an active Ethernet or WiFi device
def find_interface():
    find_device = "ip addr show"
    interface_parse = run_cmd(find_device)
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(':')[1]
    return dev_name
 
# find an active IP on the first LIVE network device
def parse_ip():
    find_ip = "ip addr show %s" % interface
    find_ip = "ip addr show %s" % interface
    ip_parse = run_cmd(find_ip)
    for line in ip_parse.splitlines():
        if "inet " in line:
            ip = line.split(' ')[5]
            ip = ip.split('/')[0]
    return ip


def load_average():
    load1, load5, load15 = os.getloadavg()
    if (load1 < 1.0):
        pips = int(16 * load1)
        if (pips == 0):
            pips = 1
        string = ("*" * pips) + ("-" * (16-pips))
    else:
        string = string(load5)
    return string


# run unix shell command, return as ASCII
def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = p.communicate()[0]
    return output.decode('ascii')



# wipe LCD screen before we start
lcd.clear()
 
# before we start the main loop - detect active network device and ip address
sleep(2)
interface = find_interface()
ip_address = parse_ip()
 
while True:
 
    # date and time
    lcd_line_1 = datetime.now().strftime('%b %d  %H:%M:%S\n')
 
    # current ip address
    lcd_line_2 = load_average();
 
    # combine both lines into one update to the display
    lcd.message = lcd_line_1 + lcd_line_2
    sleep(1)
