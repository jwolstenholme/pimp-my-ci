# Pimp My CI

Designed to provide full control over a LED-strip as a means of representing a build pipeline and responding to its changes.

An example in action: http://youtu.be/3Q9-lJn2KD8


####Features
* Full control over each LED - all colours, all brightness levels
* A set of LED animations are available (many more are possible)
* Can play a sound (or a random selection from a group of sounds) for each pipleline event - start/end build, success, failure, etc
* Jenkins support ready - more on the way!
* Way **less hassle and cost** than some of the existing build lights.. The entire kit - including the Pi - should only be a bit over $100
* No need for a cumbersome dedicated monitor and all that goes along with it


####What do you need?
**Raspberry Pi (Type B)** running [Occidentalis v0.2](http://learn.adafruit.com/adafruit-raspberry-pi-educational-linux-distro/overview)

Follow the wiring and hardware setup instructions detailed [here](http://learn.adafruit.com/light-painting-with-raspberry-pi/hardware).
Yes, a little soldering may be required, but it takes all of five minutes and it's part of the fun!

Besides the Pi itself, these components or equivalents (which are detailed in the above Adafruit article) are required:

* https://www.adafruit.com/products/306 (Digital RGB LED Weatherproof Strip 32 LED - (1m))
* http://www.adafruit.com/products/914 (Adafruit Pi Cobbler Breakout Kit for Raspberry Pi)
* https://www.adafruit.com/products/276 (5V 2A (2000mA) switching power supply - UL Listed)
* https://www.adafruit.com/products/368 (Female DC Power adapter - 2.1mm jack to screw terminal block)
* http://www.adafruit.com/products/578 (4-pin JST SM Plug + Receptacle Cable Set)

Once you're all soldered up, plugged in and powered on, ```ssh pi@raspberrypi.local``` using password ```raspberry``` and do some (or all) of the following:


If you want to play sounds at all (mp3's only):
```
$ sudo apt-get update
$ sudo apt-get install alsa-utils
$ sudo apt-get install mpg321
```

Then:
```
$ git clone https://github.com/jwolstenholme/pimp-my-ci.git
$ cd pimp-my-ci
$ sudo cp scripts/pimp-my-ci /etc/init.d/
$ sudo vi /etc/init.d/pimp-my-ci
$ sudo update-rc.d pimp-my-ci defaults
$ sudo service start pimp-my-ci
```

Then watch (and maybe hear) the fate of each of your builds!
