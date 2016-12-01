from knxip.ip import KNXIPTunnel
import knxip.core
from random import randint
import time

tunnel = KNXIPTunnel('192.168.1.99')
if tunnel.connect():
    print('Tunnel opened')

# All SDL constants
rgb_first_knx = '14/3/1'
rgb_total = 11
rgb_step = 20
rgb_first = knxip.core.parse_group_address(rgb_first_knx)

led_first_knx = '14/2/11'
#squad_1 = ['14/2/11', '14/2/16']
led_total = 14
led_step = 5
led_first = knxip.core.parse_group_address(led_first_knx)

wikihouse_1 = '14/2/61'
wikihouse_2 = '14/2/56'
wikihouse_3 = '14/2/51'
couloir = '14/2/166'
squad_3 = '14/2/111'
squad_2 = '14/2/121'
squad_1 = '14/2/131'

def setled(led_id, w_value=None):
    if not w_value:
        w_value = 0
    tunnel.group_write(led_id + 0, [0])
    tunnel.group_write(led_id + 2, [w_value])


def setallled(w_value=None):
    """Set all LED lights to a common [White] value. Default: all off"""

    if not w_value:
        w_value = 0

    for light_it in range(0, led_total + 1):
        setled(led_first + (led_step * light_it), w_value)


def setrgb(rgb_id, rgbw_value=None):
    if not rgbw_value:
        rgbw_value = [0, 0, 0, 0]
    tunnel.group_write(rgb_id + 0, [0])
    tunnel.group_write(rgb_id + 2, [rgbw_value[0]])
    tunnel.group_write(rgb_id + 5, [0])
    tunnel.group_write(rgb_id + 7, [rgbw_value[1]])
    tunnel.group_write(rgb_id + 10, [0])
    tunnel.group_write(rgb_id + 12, [rgbw_value[2]])
    tunnel.group_write(rgb_id + 15, [0])
    tunnel.group_write(rgb_id + 17, [rgbw_value[3]])


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


def main():

    setallrgb([0, 0, 0, 0])

    #while True:
    #    setallrgbrandom()
    #    time.sleep(3)

    # setrgb(knxip.core.parse_group_address('14/3/21'), [0, 0, 0, 0])
    # setled(knxip.core.parse_group_address('14/2/11'), 200)
    setled(knxip.core.parse_group_address(squad_3), 200)

if __name__ == "__main__":
    main()
