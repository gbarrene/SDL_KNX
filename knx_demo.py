import src.knx_bus_SDL as sdl_knx
from knxip.core import parse_group_address as toknx
import time

wikihouse_1 = '14/2/61'
wikihouse_2 = '14/2/56'
wikihouse_3 = '14/2/51'
couloir = '14/2/166'
squad_1 = '14/2/131'
squad_2 = '14/2/121'
squad_3 = '14/2/111'


def main():

    tunnel = sdl_knx.KNX_tunnel('192.168.1.99')

    sdl_knx.setrgb(tunnel, toknx('14/3/21'), [123, 200, 50, 20])
    time.sleep(1)
    print(sdl_knx.getrgb(tunnel, toknx('14/3/21')))

    sdl_knx.setled(tunnel, toknx(wikihouse_1), 255)
    time.sleep(1)
    print(sdl_knx.getled(tunnel, toknx(wikihouse_1)))

    time.sleep(1)
    sdl_knx.alloff(tunnel)
    time.sleep(3)  # 3 secs seems to be the min to be sure setall is working properly...
    sdl_knx.setallled(tunnel, 200)
    time.sleep(3)
    sdl_knx.setallrgb(tunnel, [0, 0, 0, 200])

    sdl_knx.setled(tunnel, toknx(wikihouse_1), 0)
    time.sleep(1)
    print(sdl_knx.getled(tunnel, toknx(wikihouse_1)))

    sdl_knx.setled(tunnel, toknx(wikihouse_2), 0)
    time.sleep(1)
    print(sdl_knx.getled(tunnel, toknx(wikihouse_2)))




if __name__ == "__main__":
    main()