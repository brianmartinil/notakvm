# notaKVM

notaKVM allows you to fake a two computer, one monitor KVM with a [cheap USB switch](https://www.amazon.com/s?k=usb+3+switch) and a monitor that has two inputs and supports [DDC/CI](https://en.wikipedia.org/wiki/Display_Data_Channel).

Both computers are connected to different inputs on the monitor.  This script runs on one of the computers and detects the keyboard being plugged in / unplugged via the USB switch, then uses DDC/CI to tell the monitor to switch to the appropriate input.

## Requirements

* A Windows computer with Python 3 that can run this script
* A monitor with multiple inputs that supports DDC/CI (you can test this with ControlMyMonitor or ScreenBright).
* A USB switch

## Usage

### Hardware setup

* Connect each computer to a different input on the monitor and see both desktops by switching inputs on the monitor
* Set up your USB switch to allow switching a keyboard and mouse between the computers

### Software setup

* Install the `psutil` and `wmi` Python packages
* Put this script into a directory somewhere
* Download [ControlMyMonitor](https://www.nirsoft.net/utils/control_my_monitor.html) and put the exe in the same directory as the script
* At the top of the script, change `THIS_COMPUTER_INPUT_ID` and `OTHER_COMPUTER_INPUT_ID` as appropriate for your monitor.  These are the values that tell your monitor what input to use.  They aren't always logical.  My monitor, for example, uses 15 for DisplayPort and 17 for HDMI1.  You can check these values with ControlMyMonitor or ScreenBright (look for VCP Code 60 "Input Select").
* Run `python notakvm.py launch` to have the script launch itself in the background.  Leave off the `launch` parameter to keep it in the foreground (if you want to see debugging output, for example).
* Optionally, use Task Scheduler to automatically launch the script when you log on.

The script should only be installed on one computer.

Once the script is up and running, the active monitor should follow the USB switch.

## Limitations

* On my monitor, switching between sources takes about 6 seconds.  This is on par with the cheap ($100) 4K / 60hz DisplayPort KVM I tried, but is slower than higher-end KVMs.

* You may need to disable input auto-switching on your monitor to prevent switching if the active computer goes to sleep.

* I've had the keyboard/mouse and visible screen get out-of-sync a couple of times.  It seems to be rare, and it always fixed itself by switching back and forth a couple of times.

* The script will use the connection of any USB keyboard as a signal to switch to itself, and a disconnect of any USB keyboard to switch away.  If you have multiple peripherals that identify themselves as keyboards this might cause issues.  You may be able to solve it by using more specific WMI query strings.

* I turned off the device-added and device-removed Windows system sounds because it was annoying.

* The script is Windows only because the mechanisms for detecting USB devices and sending DDC/CI commands are completely different on Linux and Mac, and I don't have either of those computers handy to test.  Patches accepted.