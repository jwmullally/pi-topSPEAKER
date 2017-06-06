# pi-topSPEAKER

![Image of pi-topSPEAKER](https://static.pi-top.com/images/speaker-small.png "Image of pi-topSPEAKER")

Visit the [<b>pi-top</b>SPEAKER product page](https://pi-top.com/products/accessories) on the <b>pi-top</b> website for more information.

## Table of Contents
* [Quick Start](#quick-start)
* [Hardware Overview](#hardware)
* [Software](#software)
    * [<b>pi-top</b>PULSE on <b>pi-top</b>OS](#software-pt-os)
    * [<b>pi-top</b>PULSE on Raspbian](#software-raspbian)
    * [Manual Installation](#software-how-it-works)
* [Documentation & Support](#support)
	* [Links](#support-links)
	* [Troubleshooting](#support-troubleshooting)

## Quick Start <a name="quick-start"></a>
### pi-topOS
* Boot into <b>pi-top</b>OS
* Plug in <b>pi-top</b>SPEAKER
* Enjoy!

### Raspbian
* Run the following commands in the terminal (with an internet connection):

```
sudo apt update
sudo apt install pt-speaker
```

* Plug in <b>pi-top</b>SPEAKER
* Reboot (if instructed to do so - you should only need to do this the first time)
* Enjoy!

## Hardware Overview <a name="hardware"></a>

<b>pi-top</b>SPEAKER is a modular, <b>pi-top</b>/<b>pi-top</b>CEED compatible speaker add-on board that is designed to fit onto a <b>pi-top</b>/<b>pi-top</b>CEED's modular rail, and can be connected with up to 2 other <b>pi-top</b>SPEAKERs in a chain. Each device has a 3-position hardware switch that the user can set to select L, M or R - left channel, mono mix or right channel respectively. <b>pi-top</b>SPEAKER needs to be initialised each time it is powered in order to function.

**NOTE: As the <b>pi-top</b>SPEAKER is an <b>pi-top</b>/<b>pi-top</b>CEED add-on, it requires a [<b>pi-top</b> hub](https://pinout.xyz/pinout/pi_top_hub_mk1) (mk1) or [<b>pi-top</b>CEED hub](https://pinout.xyz/pinout/pi_top_ceed_hub_mk1) (mk1) to function.**

### Technical Details
The 3-way hardware switch changes the primary I2C address of the <b>pi-top</b>SPEAKER on an I2C [multiplexer (mux)](https://en.wikipedia.org/wiki/Multiplexer) (TCA9543A) which sits between the Raspberry Pi I2C bus and the DAC+AMP ("[digital-to-analog converter](https://en.wikipedia.org/wiki/Digital-to-analog_converter)" and "[amplifier](https://en.wikipedia.org/wiki/Amplifier)") (TAS2505). This I2C address determines the output: left channel, mono mix or right channel, providing a direct mapping between the I2C address and the channel to be output through for each <b>pi-top</b>SPEAKER that might be in a chain. The mapping is as follows:

| Channel  | I2C Address  |
| -------- |:------------:|
|   left   |      71      |
|  right   |      72      |
| mono mix |      73      |

**Audio output on the Raspberry Pi needs to be set to HDMI.** This HDMI audio (containing 2-channel audio data) is converted by the <b>pi-top</b>/<b>pi-top</b>CEED hub mk1 into SPDIF data (BCM format). The SPDIF receiver then converts this to 24-bit I2S format. Mixed digital audio data is input to TAS2505's mono DAC Signal Processor via I2C MUX, and finally audio is amplified through a 2W D-class audio amplifier and output to the 2W (3W peak), 4Ω speaker.

As mentioned earlier, <b>pi-top</b>SPEAKER needs to be initialised each time it is powered in order to function. This is because the TAS2505's signal processing blocks are programmable, allowing for custom configuration (such as tuning for high noise rejection and low group delay, as well as various other signal processing operations, such as audio effects and frequency shaping) after manufacture.

### Advanced Configuration
See the [Manual Initialisation wiki page](https://github.com/<b>pi-top</b>/<b>pi-top</b>SPEAKER/wiki/Manual-Initialisation) for this repository.

## Software <a name="software"></a>

### pi-topSPEAKER on pi-topOS <a name="software-pt-os"></a>

All <b>pi-top</b>SPEAKER software and libraries are included and configured 'out-of-the-box' as standard on the latest version of <b>pi-top</b>OS (>= 23-06-2017). Simply connect a <b>pi-top</b>SPEAKER to your <b>pi-top</b> and - so long as you are using the default sound drivers - it will be automatically initialised and ready to make noises using the audio channel of the HDMI connection to the <b>pi-top</b>/<b>pi-top</b>CEED hub mk1. Volume control is handled by the operating system.

A reboot is usually not required, except in situations such as when used in conjunction with an I2S speaker (such as on the [<b>pi-top</b>PULSE](https://github.com/pi-top/pi-topPULSE) addon board), which uses a custom audio configuration, and where rebooting is required to return to using the default sound driver.

Download the latest version of <b>pi-top</b>OS [here](https://pi-top.com/products/os#download).

#### Technical Details
This automatic initialisation is done by a software package called `pt-peripheral-cfg`. This contains a program called `pt-peripherals-daemon`, which runs in the background, scanning for newly connected devices. If a device is detected, and the appropriate library is installed allow it to be initialised, it will run the approprate command. The `pt-speaker` package on <b>pi-top</b>OS installs and starts this background process, as well as the Python library to allow the <b>pi-top</b>SPEAKER to be initialised when detected. In the case of <b>pi-top</b>SPEAKER, it checks the I2C lines, and - on detection - will ensure that HDMI is set as audio output, and initialise.

### pi-topSPEAKER on Raspbian <a name="software-raspbian"></a>

You can add <b>pi-top</b>SPEAKER support to Raspbian by installing the `pt-speaker` software package. Then, everything will work in the same plug-and-play way as on <b>pi-top</b>OS. To do this, simply run the following commands at the terminal:

```
sudo apt update
sudo apt install pt-speaker
sudo reboot
```

### Manual Installation <a name="software-pt-os"></a>

For more information about how the <b>pi-top</b>SPEAKER is initialised, and how you can do this manually, see the wiki page [here](https://github.com/pi-top/pi-topSPEAKER/wiki/Manual-Initialisation).

## Documentation & Support <a name="support"></a>

### Useful Links <a name="support-links"></a>

* [Support](https://support.pi-top.com/)

### Troubleshooting FAQ <a name="support-troubleshooting"></a>

#### My pi-topSPEAKER is not working - what can I try?

* If you are on Raspbian, double check that you have installed the correct software packages.

* Double check that your audio output is using HDMI. This should be automatically set by the <b>pi-top</b>SPEAKER software; however, this can be manually reset.

* For more persistent issues, set the channel select switch on the <b>pi-top</b>SPEAKER to Mono, open a terminal and type:

        i2cdetect -y 1

	* If i2cdetect cannot find "/dev/i2c-1", your software configuration may be corrupted. It is recommended to download the latest version of <b>pi-top</b>OS and start over.
	* Check for `73` in the grid
		* If you cannot see `73`, check that the cable between the Raspberry Pi and the hub is connected correctly. If you still cannot see `73`, please [contact support](#support-links) with your findings.
		* If you can see `73`, your software configuration may be corrupted. It is recommended to download the latest version of <b>pi-top</b>OS and start over. If you still continue to experience issues, please [contact support](#support-links) with your findings.

#### I have multiple <b>pi-top</b>SPEAKERs plugged in at the same time and they don't work

* **[Known Issue]** Currently, if you attach two or more connected <b>pi-top</b>SPEAKERs to your <b>pi-top</b>/<b>pi-top</b>CEED hub *at the same time*, they will not be initialised correctly. To work around this, connect each <b>pi-top</b>SPEAKER to the hub one at a time.
