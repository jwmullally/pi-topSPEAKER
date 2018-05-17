## Configuring Raspbian for pi-topSPEAKER v2

For those of you who like to get your hands dirty, or don't want a full installation, we have included some instructions to provide this functionality yourself. Under the hood, this is all that the `pt-speaker` package is doing anyway.

**NOTE:** _If you are running pi-topOS, you do not need to worry about this - everything is already included!_

### Supporting initialisation

* I2C is required to communicate with the function-enabling IC as part of initialisation. The simplest way to do this is by running `raspi-config`, selecting `Interfacing Options` → `I2C` → Select "Yes" to enabling I2C.

* HDMI drive will need to be activated, to allow sound to be sent over HDMI to the hub. Run the running command in the terminal:

        sudo leafpad /boot/config.txt

    Then, search for `hdmi_drive` - make sure that this line says `hdmi_drive=2` only (with no # at the start of the line). Save the file, and reboot.

### Configuring Audio

##### Configuring I2S on the original pi-top (v1) and pi-topCEED

When connecting a pi-topSPEAKER to an original pi-top or a pi-topCEED, I2S audio needs to be enabled.

I2S enabling/disabling and volume control configuration form part of the [general pi-top device management system](https://github.com/pi-top/Device-Management), however can be configured manually via the following commands, followed by a reboot, using [pt-i2s](https://github.com/pi-top/Device-Management/blob/master/src/i2s/pt-i2s):

    pt-i2s enable
    pt-i2s disable

Volume control for pi-topSPEAKER v2 can be enabled by loading soundcard device information with the following command (with a pi-topSPEAKER v2 connected, and with I2S enabled), followed by a reboot, using [hifiberry-alsactl.restore](https://github.com/pi-top/Device-Management/blob/master/src/i2s/hifiberry-alsactl.restore):

    /usr/sbin/alsactl -f hifiberry-alsactl.restore restore

##### Enabling HDMI to I2S on the pi-top v2

The new pi-top supports an HDMI to I2S audio conversion system which eliminates the need for re-configuring the operating system to use I2S and then rebooting. To enable this requires communicating with the hub. This can be by installing the following library:

    sudo apt install python3-pt-common

Now save the following script to a file, e.g. `/tmp/pt-hdmi-to-i2s`:

    #!/usr/bin/python3

    # Script to configure the new pi-top hub, enabling or disabling the
    # HDMI to I2S audio conversion.

    from ptcommon.i2c_device import I2CDevice
    import sys

    AUD__CONFIG = 0xC0
    AUD__CONFIG__HDMI = 0x01
    AUD__CONFIG__HPDET = 0x02

    if (len(sys.argv) != 2):
        print("Usage: " + sys.argv[0] + " <enable|disable>")
        sys.exit(1)
    elif (sys.argv[1] == "enable" or sys.argv[1] == "disable"):
        print("Usage: " + sys.argv[0] + " <enable|disable>")
        sys.exit(1)

    try:
        hub = I2CDevice("/dev/i2c-1", 0x10)
        hub.connect()

        audio_control = hub.read_unsigned_byte(AUD__CONFIG)

        if (sys.argv[1] == "enable"):
            hub.write_byte(AUD__CONFIG, audio_settings | AUD__CONFIG__HDMI)
        elif (sys.argv[1] == "disable"):
            hub.write_byte(AUD__CONFIG, audio_settings & (~AUD__CONFIG__HDMI & 0xFF))

    except Exception as e:

        print("Error communicating with hub: " + str(e))

Make this file executable by running:

    sudo chmod +x /tmp/pt-hdmi-to-i2s

Then run the script as follows:

    sudo /tmp/pt-hdmi-to-i2s enable

**Note:** This will be replaced with a formal method soon!

### Making the `ptspeaker` Python library accessible

The easiest way to get the pi-topSPEAKER library is to install the debian package directly:

    sudo apt install python3-pt-speaker

You can also download the library files from this repository and use them locally.

## Using the software library to manually initialise pi-topSPEAKER

Once you have placed the library files in a suitable location, you can now initialise the device yourself using the included `configuration.py`.

Assuming that you have done this correctly, you should be able to initialise the pi-topSPEAKER with a Python program that looks something like this:

    from ptspeaker import configuration as speakercfg

    # The library needs to know what hardware it is running on.
    # For the pi-top v2 use 4, for all other platforms use 1
    host_device_type = 1
    
    speakercfg.initialise(host_device_type, "pi-topSPEAKER-v2"):
    enabled, reboot_required, v2_hub_hdmi_to_i2s_required = speakercfg.enable_device()

    if (reboot_required):
        print("Reboot required")
    elif (v2_hub_hdmi_to_i2s_required):
        print("HDMI to I2S required")
    elif (enabled):
        print("Successfully enabled pi-topSPEAKER")
    else:
        print("Failed to enable pi-topSPEAKER")

This function will configure the pi-topSPEAKER to default values, and enable speaker functionality.