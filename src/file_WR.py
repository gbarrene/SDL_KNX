import json

def RW_light_info_update(zone_name, value_name, value):
    """Loads the json text file into an object"""
    zone_name = zone_name.upper()
    light_info_deveui = RW_light_info_read()

    """Search for the right light to update the light level"""
    for x in range(1, len(light_info_deveui)):
        print(light_info_deveui[list(light_info_deveui.keys())[x]])
        if light_info_deveui[list(light_info_deveui.keys())[x]]['zone_name'].upper() == zone_name:
            light_info_deveui[list(light_info_deveui.keys())[x]][value_name] = value
            print("Updated "+zone_name+" with a new "+value_name+" at "+str(value))

    """Writes the updated object back to the file and overwrites the old infos"""
    RW_light_info_write(light_info_deveui)

    return "File well wrote"


def RW_light_info_read():
    file = open("src/Light_info_DevEUI.txt", 'r')
    light_info_deveui = json.load(file)
    file.close()
    return light_info_deveui


def RW_light_info_write(light_info_deveui):
    file = open("src/Light_info_DevEUI.txt", 'w')
    file.write(json.dumps(light_info_deveui))
    file.close()
    return 0

def RW_motion_data_update(zone_name, new_value):

    file = open("src/Motion_data.txt", 'r')
    motion_data = json.load(file)
    file.close()
    motion_data[zone_name.upper()]['last-7'] = motion_data[zone_name.upper()]['last-6']
    motion_data[zone_name.upper()]['last-6'] = motion_data[zone_name.upper()]['last-5']
    motion_data[zone_name.upper()]['last-5'] = motion_data[zone_name.upper()]['last-4']
    motion_data[zone_name.upper()]['last-4'] = motion_data[zone_name.upper()]['last-3']
    motion_data[zone_name.upper()]['last-3'] = motion_data[zone_name.upper()]['last-2']
    motion_data[zone_name.upper()]['last-2'] = motion_data[zone_name.upper()]['last-1']
    motion_data[zone_name.upper()]['last-1'] = motion_data[zone_name.upper()]['last-0']
    motion_data[zone_name.upper()]['last-0'] = new_value
    file = open("src/Motion_data.txt", 'w')
    file.write(json.dumps(motion_data))
    file.close()
    return motion_data
