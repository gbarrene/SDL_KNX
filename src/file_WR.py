import json

def RW_light_info(zone_name, value_name, value):
    """Loads the json text file into an object"""
    zone_name = zone_name.upper()
    file = open("src/Light_info_DevEUI.txt", 'r')
    light_info_deveui = json.load(file)
    file.close()

    """Search for the right light to update the light level"""
    for x in range(0, len(light_info_deveui)):
        if light_info_deveui[list(light_info_deveui.keys())[x]]['zone_name'].upper() == zone_name:
            light_info_deveui[list(light_info_deveui.keys())[x]][value_name] = value

    """Writes the updated object back to the file and overwrites the old infos"""
    file = open("src/Light_info_DevEUI.txt", 'w')
    file.write(json.dumps(light_info_deveui))
    file.close()

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