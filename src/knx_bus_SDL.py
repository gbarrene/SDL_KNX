from knxip.ip import KNXIPTunnel
from random import randint
from knxip.core import parse_group_address as toknx
import time
import src.constants as constants


# All SDL constants
rgb_first = toknx(constants.RGB_FIRST_KNX)

led_first = toknx(constants.LED_FIRST_KNX)


def KNX_tunnel(knx_gw_ip):
    tunnel = KNXIPTunnel(knx_gw_ip)
    if tunnel.connect():
        print('Tunnel opened')
        return tunnel
    else:
        return None

# All Led related fonction (Get, Set, Set All)

def get_led(tunnel, led_id):
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

def set_all_led(tunnel, w_value=None):
    """Set all LED lights to a common [White] value. Default: all off"""

    if not w_value:
        w_value = 0

    for light_it in range(0, constants.LED_TOTAL + 1):
        set_led(tunnel, led_first + (constants.LED_STEP * light_it), w_value)


# All RGB related fonction (Get, Set, Set All)

def get_rgb(tunnel, rgb_id):
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

def set_rgb(tunnel, rgb_id, rgbw_value=None):
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


def set_all_rgb(tunnel, rgbw_value=None):
    """Set all RGB lights to a common [RGBW] value. Default: all off"""

    if not rgbw_value:
        rgbw_value = [0, 0, 0, 0]

    for light_it in range(0, constants.RGB_TOTAL + 1):
        setrgb(tunnel, rgb_first + (constants.RGB_STEP * light_it), rgbw_value)


def set_all_rgb_random(tunnel):
    """ Set all RGB lights to a random and different RGB value """
    for light_it in range(0, constants.RGB_TOTAL + 1):
        setrgb(tunnel, rgb_first + (constants.RGB_STEP * light_it), [randint(0, 255), randint(0, 255), randint(0, 255), 0])
    return True


def disco_RGB_mode(tunnel):
    while True:
        setallrgbrandom(tunnel)
        time.sleep(3)


def all_off(tunnel):
    setallled(tunnel, 0)
    setallrgb(tunnel, [0, 0, 0, 0])
