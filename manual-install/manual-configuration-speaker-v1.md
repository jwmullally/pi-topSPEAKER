## Configuring Raspbian for pi-topSPEAKER

For those of you who like to get your hands dirty, or don't want a full installation, we have included some instructions to provide this functionality yourself. Under the hood, this is all that the `pt-speaker` package is doing anyway.

**NOTE:** _If you are running pi-topOS, you do not need to worry about this - everything is already included!_
**NOTE:** _The pi-topSPEAKER v1 is no longer supported on a pi-top V2._

### Supporting initialisation

* I2C is required to communicate with the function-enabling IC as part of initialisation. The simplest way to do this is by running `raspi-config`, selecting `Interfacing Options` → `I2C` → Select "Yes" to enabling I2C.

* HDMI drive will need to be activated, to allow sound to be sent over HDMI to the hub. Run the running command in the terminal:

        sudo leafpad /boot/config.txt

    Then, search for `hdmi_drive` - make sure that this line says `hdmi_drive=2` only (with no # at the start of the line). Save the file, and reboot.

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
    
    speakercfg.initialise(host_device_type, "pi-topSPEAKER-v1"):
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

## What's Going On Under The Hood

The enable function reads the `setup.cfg` file in the library folder (which is a series of instructions to configure the pi-topSPEAKER) and sending corresponding commands to the device.

### Some More Detail
*Note: This section explains a bit about how this method actually works. You won't need this unless you're delving in deep!*

In order to initialise pi-topSPEAKER, a proxy needs to be opened by writing which channel is to be opened up (this is always channel 0) to the I2C address exposed by the channel select switch. This then connects the pi-topSPEAKER brain directly to the I2C bus, and communication can be carried out as normal. The proxy must be closed before trying to communicate with other pi-topSPEAKERs.

While this proxy is open, the DAC+AMP (TAS2505) will be visible on its own I2C address (0x18) - communication can now be carried out as if it was connected directly to the I2C bus.

When the device has been programmed, this proxy must be closed by writing to the I2C MUX before attempting to communicate with any other device - otherwise there will be address overlap and they will interfere with each other.

The settings that are configured on the device are handled via the memory address space of the TAS2505, which is set up in pages, with each page containing a number of registers. So when wanting to write to (or read from) a register within a certain page, the page to be accessed must first be written to the device. Register 0x00 on every page is set up as a page select, so no matter which page you are currently in, writing to register `0x00` with the next page you want to access as data will cause a page change. For example: moving to page `0x01`, you would write to register 0x00 with `0x01` as the data. Page selection is persistent, so it only needs to be done once prior to writing to registers within that page.