from knxip.ip import KNXIPTunnel
from knxip.core import parse_group_address as toknx
from random import randint
import time

tunnel = KNXIPTunnel('192.168.1.99')
if tunnel.connect():
    print('Tunnel opened')

# All SDL constants
rgb_first_knx = '14/3/1'
rgb_total = 11
rgb_step = 20
rgb_first = toknx(rgb_first_knx)

led_first_knx = '14/2/11'
#squad_1 = ['14/2/11', '14/2/16']
led_total = 14
led_step = 5
led_first = toknx(led_first_knx)

wikihouse_1 = '14/2/61'
wikihouse_2 = '14/2/56'
wikihouse_3 = '14/2/51'
couloir = '14/2/166'
squad_1 = '14/2/131'
squad_2 = '14/2/121'
squad_3 = '14/2/111'



def getled(led_id):
    try:
        return list(bytearray(tunnel.group_read(led_id+2)))[0]
    except:
        print("Unable to read from the KNX bus")
        return None

def setled(led_id, w_value=None):
    if not w_value:
        w_value = 0
    try:
        tunnel.group_write(led_id + 0, [0])
        tunnel.group_write(led_id + 2, [w_value])
    except:
        print("Unable to write to the KNX bus")

def setallled(w_value=None):
    """Set all LED lights to a common [White] value. Default: all off"""

    if not w_value:
        w_value = 0

    for light_it in range(0, led_total + 1):
        setled(led_first + (led_step * light_it), w_value)

def getrgb(rgb_id):
    rgbw_value = [0, 0, 0, 0]
    try:
        rgbw_value[0] = list(bytearray(tunnel.group_read(rgb_id + 2)))[0]
        rgbw_value[1] = list(bytearray(tunnel.group_read(rgb_id + 7)))[0]
        rgbw_value[2] = list(bytearray(tunnel.group_read(rgb_id + 12)))[0]
        rgbw_value[3] = list(bytearray(tunnel.group_read(rgb_id + 17)))[0]
    except:
        print("Unable to read from the KNX bus")
        return None
    return rgbw_value

def setrgb(rgb_id, rgbw_value=None):
    if not rgbw_value:
        rgbw_value = [0, 0, 0, 0]
    try:
        tunnel.group_write(rgb_id + 0, [0])
        tunnel.group_write(rgb_id + 2, [rgbw_value[0]])
        tunnel.group_write(rgb_id + 5, [0])
        tunnel.group_write(rgb_id + 7, [rgbw_value[1]])
        tunnel.group_write(rgb_id + 10, [0])
        tunnel.group_write(rgb_id + 12, [rgbw_value[2]])
        tunnel.group_write(rgb_id + 15, [0])
        tunnel.group_write(rgb_id + 17, [rgbw_value[3]])
    except:
        print("Unable to write to the KNX bus")


def setallrgb(rgbw_value=None):
    """Set all RGB lights to a common [RGBW] value. Default: all off"""

    if not rgbw_value:
        rgbw_value = [0, 0, 0, 0]

    for light_it in range(0, rgb_total + 1):
        setrgb(rgb_first + (rgb_step * light_it), rgbw_value)


def setallrgbrandom():
    """ Set all RGB lights to a random and different RGB value """
    for light_it in range(0, rgb_total + 1):
        setrgb(rgb_first + (rgb_step * light_it), [randint(0, 255), randint(0, 255), randint(0, 255), 0])
    return True


def discoRGBmode():
    while True:
        setallrgbrandom()
        time.sleep(3)


def alloff():
    setallled(0)
    setallrgb([0, 0, 0, 0])



def main():

    setrgb(toknx('14/3/21'), [123, 200, 50, 20])
    time.sleep(1)
    print(getrgb(toknx('14/3/21')))

    setled(toknx(wikihouse_1), 255)
    time.sleep(1)
    print(getled(toknx(wikihouse_1)))

    time.sleep(1)
    alloff()
    time.sleep(3)  # 3 secs seems to be the min to be sure setall is working properly...
    setallled(200)
    time.sleep(3)
    setallrgb([0, 0, 0, 200])



if __name__ == "__main__":
    main()
