from knxip.ip import KNXIPTunnel
from random import randint
from knxip.core import parse_group_address as toknx
import time


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


def KNX_tunnel(knx_gw_ip):
    tunnel = KNXIPTunnel(knx_gw_ip)
    if tunnel.connect():
        print('Tunnel opened')
        return tunnel
    else:
        return None


def getled(tunnel, led_id):
    try:
        return list(bytearray(tunnel.group_read(led_id+2)))[0]
    except:
        print("Unable to read from the KNX bus")
        return None

def setled(tunnel, led_id, w_value=None):
    if not w_value:
        w_value = 0
    try:
        tunnel.group_write(led_id + 0, [0])
        tunnel.group_write(led_id + 2, [w_value])
    except:
        print("Unable to write to the KNX bus")

def setallled(tunnel, w_value=None):
    """Set all LED lights to a common [White] value. Default: all off"""

    if not w_value:
        w_value = 0

    for light_it in range(0, led_total + 1):
        setled(tunnel, led_first + (led_step * light_it), w_value)

def getrgb(tunnel, rgb_id):
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

def setrgb(tunnel, rgb_id, rgbw_value=None):
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


def setallrgb(tunnel, rgbw_value=None):
    """Set all RGB lights to a common [RGBW] value. Default: all off"""

    if not rgbw_value:
        rgbw_value = [0, 0, 0, 0]

    for light_it in range(0, rgb_total + 1):
        setrgb(tunnel, rgb_first + (rgb_step * light_it), rgbw_value)


def setallrgbrandom(tunnel):
    """ Set all RGB lights to a random and different RGB value """
    for light_it in range(0, rgb_total + 1):
        setrgb(tunnel, rgb_first + (rgb_step * light_it), [randint(0, 255), randint(0, 255), randint(0, 255), 0])
    return True


def discoRGBmode(tunnel):
    while True:
        setallrgbrandom(tunnel)
        time.sleep(3)


def alloff(tunnel):
    setallled(tunnel, 0)
    setallrgb(tunnel, [0, 0, 0, 0])
