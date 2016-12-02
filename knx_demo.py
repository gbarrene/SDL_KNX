#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  
#  


import src.knx_bus_SDL as sdl_knx
from knxip.core import parse_group_address as toknx
import time
import src.constants as constants


def main():

    tunnel = sdl_knx.KNX_tunnel('192.168.1.99')
    
    sdl_knx.set_rgb(tunnel, toknx('14/3/21'), [123, 200, 50, 20])
    time.sleep(1)
    print(sdl_knx.get_rgb(tunnel, toknx('14/3/21')))
"""
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
