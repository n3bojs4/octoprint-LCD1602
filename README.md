# OctoPrint-Lcd1602

PYTHON3

This plug-in allows you to control a 16X2 lcd display (hd44780 connected to port I2C) to display the octoprint status. It is useful for people like me who have a printer without a display.
It indicates on which port the printer is connected, the progress of printing. It also displays the remaining print time (thanks to a simple method).

LCD1602 Plugin for Octoprint
  Written by: n3bojs4
  https://github.com/n3bojs4/octoprint-LCD1602

  Forked on 2021-12-17 by GrooveServer

  Notes: This plugin as written did not support Python 3 (Current default in OctoPrint)
  Modified to support Python 3, removed refrences to fakePi that were causing the plugin to fail to load.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/GrooveServer/octoprint-LCD1602/archive/refs/heads/master.zip

**MANUAL INSTALL:** 

clone the repo :

`git clone https://github.com/GrooveServer/octoprint-LCD1602  `

install :

`cd OctoPrint-Lcd1602 && python3 setup.py install`

## Configuration

Nothing to do