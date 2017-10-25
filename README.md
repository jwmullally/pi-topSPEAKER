# pi-topSPEAKER

![Image of pi-topSPEAKER](https://static.pi-top.com/images/speaker-small.png "Image of pi-topSPEAKER")

Visit the [pi-topSPEAKER product page](https://pi-top.com/products/accessories) on the pi-top website for more information.

## Table of Contents
* [Quick Start](#quick-start)
* [Hardware](#hardware)
* [Software](#software)
    * [pi-topPULSE on pi-topOS](#software-pt-os)
    * [pi-topPULSE on Raspbian](#software-raspbian)
    * [Manual Installation](#software-how-it-works)
* [Documentation & Support](#support)
    * [Links](#support-links)
    * [Troubleshooting](#support-troubleshooting)

## <a name="quick-start"></a> Quick Start
#### pi-topOS
* Boot into pi-topOS
* Plug in pi-topSPEAKER
* Enjoy!

#### Raspbian
* Run the following commands in the terminal (with an internet connection):

```
sudo apt update
sudo apt install pt-speaker
```

* Plug in pi-topSPEAKER
* Reboot (if instructed to do so - you should only need to do this the first time)
* Enjoy!

## <a name="hardware"></a> Hardware

There are two pi-topSPEAKER models. The easiest way to identify which model you have is to look on the underside. pi-topSPEAKER v1 looks like this:

![Image of pi-topSPEAKER v1 underside](https://static.pi-top.com/images/speaker-v1-reverse-small.png "Image of pi-topSPEAKER v1 underside")

* The **pi-topSPEAKER v1** is designed to work with the original pi-top and the pi-topCEED. The device has a 3-position hardware switch that the user can set to select L, M or R - left channel, mono mix or right channel respectively. The pi-topSPEAKER v1 is a pure HDMI audio device, so requires pi-topOS or Raspbian to be set to HDMI audio output.

* The **pi-topSPEAKER v2** is designed to work with the original pi-top, the pi-topCEED and the new pi-top. In contrast to the previous model, the pi-topSPEAKER v2 outputs higher fidelity I2S audio. On the new pi-top, an HDMI to I2S conversion system means that HDMI audio from the Raspberry Pi is converted automatically to I2S, and therefore pi-topOS only needs to be configured to HDMI audio output to use the speaker. On the original pi-top and pi-topCEED, the pi-topSPEAKER v2 requires I2S audio input. This is configured automatically on pi-topOS, however a reboot may be required to enable the speaker after this change.

* Both versions of the pi-topSPEAKER have been designed to fit onto the pi-top modular rail and can be connected directly to the pi-top hub, or by being chained together with other speakers.

#### Technical Details

##### pi-topSPEAKER v2

TBA

##### pi-topSPEAKER v1

The 3-way hardware switch changes the primary I2C address of the pi-topSPEAKER on an I2C [multiplexer (mux)](https://en.wikipedia.org/wiki/Multiplexer) (TCA9543A) which sits between the Raspberry Pi I2C bus and the DAC+AMP ("[digital-to-analog converter](https://en.wikipedia.org/wiki/Digital-to-analog_converter)" and "[amplifier](https://en.wikipedia.org/wiki/Amplifier)") (TAS2505). This I2C address determines the output: left channel, mono mix or right channel, providing a direct mapping between the I2C address and the channel to be output through for each pi-topSPEAKER that might be in a chain. The mapping is as follows:

| Channel  | I2C Address  |
| -------- |:------------:|
|   left   |      71      |
|  right   |      72      |
| mono mix |      73      |

**Note:** _Audio output on the Raspberry Pi needs to be set to HDMI_. This HDMI audio (containing 2-channel audio data) is converted by the pi-top/pi-topCEED hub mk1 into SPDIF data (BCM format). The SPDIF receiver then converts this to 24-bit I2S format. Mixed digital audio data is input to TAS2505's mono DAC Signal Processor via I2C MUX, and finally audio is amplified through a 2W D-class audio amplifier and output to the 2W (3W peak), 4Ω speaker.

As mentioned earlier, pi-topSPEAKER needs to be initialised each time it is powered in order to function. This is because the TAS2505's signal processing blocks are programmable, allowing for custom configuration (such as tuning for high noise rejection and low group delay, as well as various other signal processing operations, such as audio effects and frequency shaping) after manufacture.

#### Advanced Configuration
See the [Manual Initialisation instructions](https://github.com/pi-top/pi-topSPEAKER/tree/master/manual-install) for advanced configuration information.

## <a name="software"></a> Software

#### <a name="software-pt-os"></a> pi-topSPEAKER on pi-topOS

All pi-topSPEAKER software and libraries are included and configured 'out-of-the-box' as standard on the latest version of pi-topOS (>= 23-06-2017). Simply connect a pi-topSPEAKER to your pi-top and - so long as you are using the default sound drivers - it will be automatically initialised and ready to make noises using the audio channel of the HDMI connection to the pi-top/pi-topCEED hub mk1. Volume control is handled by the operating system.

A reboot is usually not required, except in situations such as when used in conjunction with an I2S speaker (such as on the [pi-topPULSE](https://github.com/pi-top/pi-topPULSE) addon board), which uses a custom audio configuration, and where rebooting is required to return to using the default sound driver.

Download the latest version of pi-topOS [here](https://pi-top.com/products/os#download).

##### Technical Details
Automatic initialisation is performed by the software contained in the package called `pt-device-manager`. This installs a program called `pt-device-manager`, which runs in the background and scans for newly connected devices. If a device is detected (and its supporing library is installed), it will be initialised and enabled automatically.

When the `pt-speaker` package is installed, `pt-device-manager` will also be installed as dependency, thus starting the background process. Depending on whether running on an original pi-top or a new pi-top the user will be notified if a reboot is required when the device is connected. If a reboot is not required, the device will be initialised and ready to use.

For more information about pt-device-manager, see [this repository](https://github.com/pi-top/Device-Management).

#### <a name="software-raspbian"></a> pi-topSPEAKER on Raspbian
You can add pi-topSPEAKER support to Raspbian by installing the `pt-speaker` software package. Then, everything will work in the same plug-and-play way as on pi-topOS. To do this, simply run the following commands at the terminal:

```
sudo apt update
sudo apt install pt-speaker
sudo reboot
```

This will install the ptspeaker Python library, as well as its dependencies, including pt-device-manager (see above).

#### <a name="software-pt-os"></a> Manual Installation

For more information about how the pi-topSPEAKER is initialised, and how you can do this manually, see the Manual Initialisation instructions in [this](https://github.com/pi-top/pi-topSPEAKER/tree/master/manual-install) folder.

## <a name="support"></a> Documentation & Support

#### <a name="support-links"></a> Useful Links
* [Device Management (pt-device-manager)](https://github.com/pi-top/Device-Management)
* [Support](https://support.pi-top.com/)

#### <a name="support-troubleshooting"></a> Troubleshooting FAQ

##### My pi-topSPEAKER is not working - what can I try?

* If you are on Raspbian, double check that you have installed the correct software packages.

* Check the version of the pi-topSPEAKER that is in use. If your device requires HDMI audio, double check that your audio output is using HDMI. This should be automatically set by the pi-topSPEAKER software; however, this can be manually reset. If your device requires I2S audio, you can check that I2S audio has been enabled by running:

        pt-i2s

* For more persistent issues, open a terminal and type:

        i2cdetect -y 1

    * If i2cdetect cannot find "/dev/i2c-1", your software configuration may be corrupted. It is recommended to download the latest version of pi-topOS and start over.
    * Check for the I2C address of your speaker in the grid:
        * See the [Hardware](#hardware) section of this file for I2C addresses for the two devices.
        * If you can see the appropriate address listed, check that the cable between the Raspberry Pi and the hub is connected correctly. If you still cannot see the address, please [contact support](#support-links) with your findings.
        * If you can see the appropriate address listed, your software configuration may be corrupted. It is recommended to download the latest version of pi-topOS and start over. If you still continue to experience issues, please [contact support](#support-links) with your findings.

##### I have multiple pi-topSPEAKERs plugged in at the same time and they don't work

* **[Known Issue]** Currently, if you attach two or more connected pi-topSPEAKERs to your pi-top/pi-topCEED hub *at the same time*, they will not be initialised correctly. To work around this, connect each pi-topSPEAKER to the hub one at a time.
