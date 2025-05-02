## Links: 
1. [Enable UART communication on Pi4 Ubuntu](https://askubuntu.com/questions/1254376/enable-uart-communication-on-pi4-ubuntu-20-04)
2. [Fixes for RPI 5 UART over GPIO](https://askubuntu.com/questions/1496927/raspberry-pi-5-uart2-and-uart4-problem)

## 5 Setting up serial communication on the RPi

The RPi will talk to the motor controllers over serial.

### 5.1 Disable serial-getty@ttyS0.service

Because we are using the serial port for communicating with the roboclaw motor controllers, we have to disable the serial-getty@ttyS0.service service. This service has some level of control over serial devices that we use, so if we leave it on it we'll get weird errors ([source](https://spellfoundry.com/2016/05/29/configuring-gpio-serial-port-raspbian-jessie-including-pi-3-4/)). Note that the masking step was suggested [here](https://stackoverflow.com/a/43633467/4292910). It seems to be necessary for some setups of the rpi4 - just using `systemctl disable` won't cut it for disabling the service.

**Note that the following will stop you from being able to communicate with the RPi over the serial, wired connection. However, it won't affect communication with the rpi with SSH over wifi.**

```
sudo systemctl stop serial-getty@ttyS0.service
sudo systemctl disable serial-getty@ttyS0.service
sudo systemctl mask serial-getty@ttyS0.service
```

### 5.2 Copy udev rules

Now we'll need to copy over a udev rules file, which is used to configure needed device files in `/dev`; namely, `ttyS0 and ttyAMA0`. Here's a [good primer](http://reactivated.net/writing_udev_rules.html) on udev. 

```
# copy udev file from the repo to your system
cd ~/osr_ws/src/osr-rover-code/config
sudo cp serial_udev_ubuntu.rules /etc/udev/rules.d/10-local.rules

# reload the udev rules so that the devices files are set up correctly.
sudo udevadm control --reload-rules && sudo udevadm trigger
```

This configuration should persist across RPi reboots.

### 5.3 Add user to tty and dialout groups

Finally, add the user to the `tty` and `dialout` groups:
```
sudo adduser $USER tty
sudo adduser $USER dialout
```
You might have to create the dialout group if it doesn't already exist.

<!-- You'll need to log out of your ssh session and log back in for this to take effect. Or you can restart Ubuntu. -->

### 5.4 Remove console line in cmdline.txt boot config file

Do the following steps:

```
cd /boot/firmware
sudo cp cmdline.txt cmdline.txt.bak
sudo nano cmdline.txt
```

- And then delete the substring `console=serial0,115200` from the single line of text in the file. Save and exit.

You can confirm that you edited the file correctly using `cat cmdline.txt` from the command line, and inspecting the output.

Note that the cmdline.txt.bak is just a backup file in case you need to revert this change at some point (that file won't affect the boot process)

For more background on why we do this, see [serial_config_info.md](serial_config_info.md)

### 5.5 Disable bluetooth in config.txt boot config file

Execute the following commands

```
cd /boot/firmware
sudo cp config.txt config.txt.bak
sudo nano config.txt
```

- And then add the new line `dtoverlay=disable-bt` immediately after the existing line `cmdline=cmdline.txt` towards the bottom of the file
- NOTE: For RPI-5, add `dtoverlay=uart0-pi5` also under `[all]` 

### 5.6 Restart the RPi

We need to restart for all of these changes to take effect. Execute: `sudo reboot now`

GPIO 14-15 Serial Port will be on `ttyAMA0`


## Testing Serial Connection: 

1. Install Minicom: `sudo apt update && sudo apt install minicom`
2. [Optional] Connect a GPIO between GPIO 14 and 15 to test loopback (RX and TX)
3. Run `sudo minicom -D /dev/ttyAMA0`. What you type should appear on the screen. 
