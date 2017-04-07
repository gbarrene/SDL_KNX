from knxip.ip import KNXIPTunnel
from random import randint
from knxip.core import parse_group_address as toknx
import time
import threading
import src.constants as constants

# All SDL constants
rgb_first = toknx(constants.RGB_FIRST_KNX)

led_first = toknx(constants.LED_FIRST_KNX)

save_var_rgb = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]


class Animation(threading.Thread):

    def __init__(self, tunnel):
        threading.Thread.__init__(self)
        self.tunnel = tunnel
        self.method_name = 'stop'

    def run(self):
        """Code that execute during the thread
        Change the "method_name" to a valid animation name before starting the thread,
        if not the thread will stop immediately.
        
        You can change the method_name during the execution to change the animation"""

        while True:
            if self.method_name == 'stop':
                return 'Animation ended'
                break
            elif self.method_name == 'disco':
                disco_animation(self.tunnel)
            elif self.method_name == 'christmas':
                christmas_animation(self.tunnel)
            else:
                return 'Not an available animation'
                break

    def stop(self):
        """Method to stop the thread rapidly
        use "Animation.join()" to be sure that the thread is stopped """
        self.method_name = 'stop'

def KNX_tunnel(knx_gw_ip):
    """Open a tunnel with the KNX ethernet/knx bus module"""

    tunnel = KNXIPTunnel(knx_gw_ip)
    if tunnel.connect():
        print('Tunnel opened')
        return tunnel
    else:
        return None

# All Led related fonction (Get, Set, Set All)


def timing_without_value(tunnel, method_name, timer):
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(method_name)
    if not method:
        raise NotImplementedError("Method %s not implemented" % method_name)
    else:
        #save_rgb_all(tunnel)

        if timer == 0:
            print("Will run %s for infinit time" % method_name)
            while True:
                method(tunnel)
        else:
            print("Will run "+method_name+" for "+ timer)
            for i in range(0, (timer / 3)):
                method(tunnel)
        restore_rgb_all(tunnel)


# All Led related fonction (Get, Set, Set All)


def get_led(tunnel, led_id):
    """Fonction that return the led value (0-255) where address for "%status" is "%%" +2"""

    try:
        return list(bytearray(tunnel.group_read(led_id + 2)))[0]
    except:
        print("Unable to read from the KNX bus")
        return None


def set_led(tunnel, led_id, w_value=None):
    """Fonction that set the led value (0-255) for address for "%%" """

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
    """Fonction that return the RGBW value (0-255) in an array, 
    where address for "%status" is "%%" +2"""

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
    """Fonction that set the RGBW value (0-255) array, for address for "%%" """

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

    for light_it in range(0, constants.RGB_TOTAL+1):
        set_rgb(tunnel, rgb_first + (constants.RGB_STEP * light_it), rgbw_value)


def set_all_rgb_random(tunnel):
    """ Set all RGB lights to a random and different RGB value """
    for light_it in range(0, constants.RGB_TOTAL):
        set_rgb(tunnel, rgb_first + (constants.RGB_STEP * light_it),[randint(0, 255), randint(0, 255), randint(0, 255), 0])
        print(rgb_first + (constants.RGB_STEP * light_it))
    return True


def save_rgb_all(tunnel):
    for light_it in range(0, constants.RGB_TOTAL):
        save_var_rgb[light_it] = get_rgb(tunnel, rgb_first + (constants.RGB_STEP * light_it))
        print(save_var_rgb[light_it])
        #time.sleep(3)


def restore_rgb_all(tunnel):
    for light_it in range(0, constants.RGB_TOTAL):
        set_rgb(tunnel, rgb_first + (constants.RGB_STEP * light_it), save_var_rgb[light_it])
        print(save_var_rgb[light_it])


def disco_animation(tunnel):
    set_all_rgb_random(tunnel)
    time.sleep(3)


def christmas_animation(tunnel):
    light_id = randint(0, 11)
    color_id = randint(0, len(constants.CHRISTMAS_COLORS)-1)
    set_rgb(tunnel, rgb_first + (constants.RGB_STEP * light_id), constants.CHRISTMAS_COLORS[color_id])
    time.sleep(3)


def christmas_loop(tunnel):

    while True:
        set_christmas(tunnel)


def all_off(tunnel):
    set_all_led(tunnel, 0)
    set_all_rgb(tunnel, [0, 0, 0, 0])


def all_on(tunnel):
    set_all_rgb(tunnel, [0, 0, 0, 200])
    #set_all_rgb(tunnel, rgbw)

