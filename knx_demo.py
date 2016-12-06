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
    return "disco, all_on"


def disco(tunnel, value=None):
    if not value:
        while True:
            value = input(
                "How many time would you like to run " + sys._getframe().f_code.co_name + " ? (put zero for timeless)\n")
            if test_only_one_value(value):
                break
            else:
                print("The value must be on number between")

    # continue to ask while you don't enter something correct
    print("Disco for " + str(value))
    sdl_knx.save_rgb_all(tunnel)
    for i in range(0, int(int(value)/3)):
        sdl_knx.set_all_rgb_random(tunnel)
        time.sleep(3)

    sdl_knx.restore_rgb_all(tunnel)
    return True


def all_on(tunnel, value=None):
    if not value:
        while not value:
            value = input("How many time would you like to run all on ? (put zero for timeless)\n")

    sdl_knx.set_all_rgb(tunnel, [0,0,0,200])
    return "All_on for " + str(value)


def multiple_choice(choice_str, tunnel, value=None):
    if choice_str == 'help':
        return_str = help_text()

    elif choice_str == 'disco':
        return_str = (disco(tunnel, value))

    elif choice_str == 'all_on':
        return_str = (all_on(tunnel, value))

    else:
        return "No command \"" + choice_str + "\" found. Please use help"

    return return_str


def main():
    """
    tunnel = sdl_knx.KNX_tunnel('192.168.1.99')
    sdl_knx.set_rgb(tunnel, toknx('14/3/1'), [0, 90, 100, 0])
    time.sleep(1)
    print(sdl_knx.get_rgb(tunnel, toknx('14/3/1')))

    return True
"""
def main():
    tunnel = sdl_knx.KNX_tunnel('192.168.1.99')
    sdl_knx.set_rgb(tunnel, toknx('14/3/21'), [0, 0, 0, 200])
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