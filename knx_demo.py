#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  
#  


import src.knx_bus_SDL as sdl_knx
from knxip.core import parse_group_address as toknx
import time
import sys
import src.constants as constants


def test_only_one_value(value=None):
    if not value:
        return 0
    if len(value.split(' ')) == 1:
        try:
            value = int(value)
            return 1
        except ValueError:
            return 0
    else:
        return 0


def help_text():
    return "disco, christmas, all_on, all_off"


def lunch_method_without_value(tunnel, method_name, timer=None):
    if not timer:
        while True:
            timer = input("How many time would you like to run " + method_name + " ? (put zero for timeless)\n")
            if test_only_one_value(timer):
                break
            else:
                print("The value must be a number")

    # continue to ask while you don't enter something correct
    sdl_knx.timing_without_value(tunnel, method_name, int(timer))
    return True

def multiple_choice(choice_str, tunnel, value=None):
    if choice_str == 'help':
        return_str = help_text()

    elif choice_str == 'disco':
        while True:
            sdl_knx.disco_animation(tunnel)
        #return_str = lunch_method_without_value(tunnel, 'disco_animation', value)

    elif choice_str == 'all_on':
        return_str = lunch_method_without_value(tunnel, 'all_on', value)

    elif choice_str == 'christmas':

        while True:
            sdl_knx.christmas_animation(tunnel)
        #return_str = lunch_method_without_value(tunnel, 'christmas_animation', value)


    elif choice_str == 'all_off':
        return_str = lunch_method_without_value(tunnel, 'all_off', value)

    else:
        return "No command \"" + choice_str + "\" found. Please use help"

    return return_str

"""
def main():

    tunnel = sdl_knx.KNX_tunnel('192.168.1.99')
    time.sleep(1)
    #sdl_knx.timing('set_christmas', tunnel, 0)
    sdl_knx.set_rgb(tunnel, toknx('14/3/41'), [0, 0, 0, 0])
    print(sdl_knx.possibles)
    #sdl_knx.set_all_rgb(tunnel, [200,0,0,0])

    #tunnel.disconnect()

    return True
"""


def main():
    tunnel = sdl_knx.KNX_tunnel('192.168.1.99')
    #sdl_knx.set_rgb(tunnel, toknx('14/3/61'), [0, 0, 0, 50])
    #sdl_knx.set_rgb(tunnel, toknx('14/3/41'), [0, 0, 0, 50])
    #sdl_knx.set_rgb(tunnel, toknx('14/3/21'), [0, 0, 0, 50])
    #sdl_knx.set_rgb(tunnel, toknx('14/3/1'), [0, 0, 0, 50])
    while True:
        choice_str = None
        if not choice_str:
            while not choice_str:
                choice_str = input("Witch demo would you like to run? (help for more infos) \n")

        if choice_str == 'exit':
            while True:
                choice_str = input("Exiting the app. Are you sure (y/n)? ")
                if choice_str in ['y', 'Y', 'yes', 'Yes']:
                    return 0
                elif choice_str in ['n', 'N', 'no', 'No']:
                    break
        else:
            split_str = choice_str.split(' ', 1)
            if len(split_str) == 2:
                print(multiple_choice(split_str[0], tunnel, split_str[1]))
            elif len(split_str) == 1:
                print(multiple_choice(split_str[0], tunnel))
            time.sleep(2)

    time.sleep(2)

"""

    sdl_knx.set_rgb(tunnel, toknx('14/3/21'), [0, 0, 0, 50])
    time.sleep(1)
    print(sdl_knx.get_rgb(tunnel, toknx('14/3/21')))
    sdl_knx.setrgb(tunnel, toknx('14/3/21'), [123, 200, 50, 20])
    time.sleep(1)
    print(sdl_knx.getrgb(tunnel, toknx('14/3/21')))
    sdl_knx.setled(tunnel, toknx(constants.WIKIHOUSE_1), 255)
    time.sleep(1)
    print(sdl_knx.getled(tunnel, toknx(constants.WIKIHOUSE_1)))

    time.sleep(1)
    #sdl_knx.alloff(tunnel)
    time.sleep(3)  # 3 secs seems to be the min to be sure setall is working properly...
    #sdl_knx.setallled(tunnel, 200)
    time.sleep(3)
    #sdl_knx.setallrgb(tunnel, [0, 0, 0, 200])
    
    sdl_knx.setled(tunnel, toknx(constants.WIKIHOUSE_1), 0)
    time.sleep(1)
    print(sdl_knx.getled(tunnel, toknx(constants.WIKIHOUSE_1)))
    sdl_knx.setled(tunnel, toknx(constants.WIKIHOUSE_2), 0)
    time.sleep(1)
    print(sdl_knx.getled(tunnel, toknx(constants.WIKIHOUSE_2)))
"""

if __name__ == "__main__":
    main()
