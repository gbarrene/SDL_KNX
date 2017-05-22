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
        self.exit_method = 'all_on'

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
        if self.exit_method == 'all_on':
            all_rgb_on(self.tunnel)
        elif self.exit_method == 'all_off':
            all_rgb_off(self.tunnel)


def KNX_tunnel(knx_gw_ip):
    """Open a tunnel with the KNX ethernet/knx bus module"""

    tunnel = KNXIPTunnel(knx_gw_ip)
    if tunnel.connect():
        print('Tunnel opened')
        return tunnel
    else:
        return None

# All Led related fonction (Get, Set, Set All)


def set_light_zone(tunnel, zone_name, color):
    addresses = []

    if len(zone_name.split('_')) == 3:
        name0 = zone_name.split('_')[0].upper()
        name1 = zone_name.split('_')[1].upper()
        name2 = zone_name.split('_')[2].upper()

        i = 0
        for x in range(0, len(constants.LIGHT_LOOKUP_TABLE)):
            if constants.LIGHT_LOOKUP_TABLE[x][0].split('_')[0] == name0:
                if constants.LIGHT_LOOKUP_TABLE[x][0].split('_')[1] == name1:
                    if constants.LIGHT_LOOKUP_TABLE[x][0].split('_')[2] == name2:
                        addresses.append([constants.LIGHT_LOOKUP_TABLE[x][1], constants.LIGHT_LOOKUP_TABLE[x][2]])
                        i = i + 1

    elif len(zone_name.split('_')) == 2:
        name0 = zone_name.split('_')[0].upper()
        name1 = zone_name.split('_')[1].upper()

        i = 0
        for x in range(0, len(constants.LIGHT_LOOKUP_TABLE)):
            if constants.LIGHT_LOOKUP_TABLE[x][0].split('_')[0] == name0:
                if constants.LIGHT_LOOKUP_TABLE[x][0].split('_')[1] == name1:
                    addresses.append([constants.LIGHT_LOOKUP_TABLE[x][1], constants.LIGHT_LOOKUP_TABLE[x][2]])
                    i = i + 1

    elif len(zone_name.split('_')) == 1:
        name0 = zone_name.split('_')[0].upper()

        i = 0
        for x in range(0, len(constants.LIGHT_LOOKUP_TABLE)):
            if constants.LIGHT_LOOKUP_TABLE[x][0].split('_')[0] == name0:
                addresses.append([constants.LIGHT_LOOKUP_TABLE[x][1], constants.LIGHT_LOOKUP_TABLE[x][2]])
                i = i + 1

    for x in range(0, len(addresses)):
        print(addresses[x][0])
        if addresses[x][1] == 1:
            if set_led(tunnel, toknx(addresses[x][0]), color[3]):
                return 1
        elif addresses[x][1] == 4:
            if set_rgb(tunnel, toknx(addresses[x][0]), color):
                return 1
    return 0


def set_light_position(tunnel, x, y, color):
    addresses = []
    print(range(x + constants.RADIUS, x - constants.RADIUS))

    for j in range(0, len(constants.LED_POSITION)):
        if constants.LED_POSITION[j][0] <= x + constants.RADIUS and (constants.LED_POSITION[j][0] >= x - constants.RADIUS):
            if constants.LED_POSITION[j][1] <= y + constants.RADIUS and constants.LED_POSITION[j][1] >= y - constants.RADIUS:
                print(constants.LED_POSITION[j][2])
                for i in range(0, len(constants.LIGHT_LOOKUP_TABLE)):
                    if constants.LIGHT_LOOKUP_TABLE[i][0] == constants.LED_POSITION[j][2]:
                        print(constants.LIGHT_LOOKUP_TABLE[i][1])
                        if constants.LIGHT_LOOKUP_TABLE[i][2] == 1:
                            if set_led(tunnel, toknx(constants.LIGHT_LOOKUP_TABLE[i][1]), color[3]):
                                return 1
                        elif constants.LIGHT_LOOKUP_TABLE[i][2] == 4:
                            if set_rgb(tunnel, toknx(constants.LIGHT_LOOKUP_TABLE[i][1]), color):
                                return 1
    return 0


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
    if not w_value:
        w_value = 0
    try:
        tunnel.group_write(led_id + 0, [0])
        tunnel.group_write(led_id + 2, [w_value])
        return 0
    except:
        if tunnel.check_connection_state():
            print("Unable to write to the KNX bus")
        else:
            #tunnel.disconnect()
            time.sleep(3)
            tunnel.connect()
        return 1


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
        return 0
    except:
        if tunnel.check_connection_state():
            print("Unable to write to the KNX bus")
        else:
            #tunnel.disconnect()
            time.sleep(3)
            tunnel.connect()
        return 1


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


def all_off(tunnel):
    set_all_led(tunnel, 0)
    set_all_rgb(tunnel, [0, 0, 0, 0])


def all_on(tunnel):
    set_all_led(tunnel, 200)
    set_all_rgb(tunnel, [0, 0, 0, 200])


def all_rgb_off(tunnel):
    set_all_rgb(tunnel, [0, 0, 0, 0])


def all_rgb_on(tunnel):
    set_all_rgb(tunnel, [0, 0, 0, 200])