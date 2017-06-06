import smbus
import sys
import os

############################################################
# TODO:                                                    #
# * install to /usr/lib/python2.7/dist-packages/pt-speaker #
# * put alongside playback.cfg                             #
############################################################

CHIP_ID = 0x18;
CHIP_ENABLE_REGISTER = 0x00;

PLAYBACK_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/playback.configure"

def _set_write_to_speaker_enabled(bus, address, enable):
    
    if enable:
        print("Enabling write to speaker (" + str(address) + ")")
    else:
        print("Disabling write to speaker (" + str(address) + ")")

    value = 0x01 if enable else 0x00
    bus.write_byte_data(address, CHIP_ENABLE_REGISTER, value)

    return 0


def _parse_playback_mode_file(bus, mode):

    print("Writing playback config data to speaker")

    try:
        index = 0
        with open(PLAYBACK_FILE_PATH) as file_data:
            for line in file_data:
                if (line[0] == "W") or (line[0].lower() == mode):
                    array = line.split()
                    if len(array) < 4:
                        print("Error parsing line " + str(index) + " - exiting...")
                        sys.exit(0)
                    else:
                        # Write all values from 4th to the end of the line

                        if len(array) > 3:
                            values = [int(i,16) for i in array[3:]]
                            bus.write_i2c_block_data(CHIP_ID, int(array[2],16), values)
                        else:
                            bus.write_byte_data(CHIP_ID, int(array[2],16), int(array[3],16))
                index = index + 1

        return 0

    except:
        print("Failed to write configuration data to speaker")
        return 1


def initialise_speaker(mode):

    print("Initialising speaker (mode " + mode + ")")

    if not os.path.exists(PLAYBACK_FILE_PATH):
        print("Error: playback configuration file does not exist")
        return 1

    if mode is "l" or str(mode) == "71":
        mode="l"
        address = 0x71
    elif mode is "r" or str(mode) == "72":
        mode="r"
        address = 0x72
    elif mode is "m" or str(mode) == "73":
        mode="m"
        address = 0x73
    else:
        print("Mode not recognised")
        return 1

    bus = smbus.SMBus(1)

    if (_set_write_to_speaker_enabled(bus, address, True) == 1):
        print("Error enabling write to speaker")
        return 1

    if (_parse_playback_mode_file(bus, PLAYBACK_FILE_PATH, mode) == 1):
        print("Error parsing and writing mode file to speaker")
        return 1

    if (_set_write_to_speaker_enabled(bus, address, False) == 1):
        print("Error disabling write to speaker")
        return 1

    return 0