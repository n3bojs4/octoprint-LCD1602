# coding=utf-8

"""
  LCD1602 Plugin for Octoprint
  Written by: n3bojs4
  https://github.com/n3bojs4/octoprint-LCD1602

  Forked on 2021-12-17 by GrooveServer

  Notes: This plugin as written did not support Python 3 (Current default in OctoPrint)
  Modified to support Python 3, removed refrences to fakePi that were causing the plugin to fail to load.

"""

from __future__ import absolute_import

import threading
from octoprint.printer.estimation import PrintTimeEstimator
import octoprint.plugin
import octoprint.events
from RPLCD.i2c import CharLCD
import time
import datetime
import os
import sys

__plugin_pythoncompat__ = ">=2.7,<4"

class LCD1602Plugin(octoprint.plugin.StartupPlugin,
                    octoprint.plugin.EventHandlerPlugin,
                    octoprint.plugin.ProgressPlugin,
                    octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.TemplatePlugin,
                    octoprint.plugin.AssetPlugin
                    ):

  def __init__(self):
      self.mylcd = None
      self.block = None

      # init vars
      self.start_date = 0
      # Creating lock for threads
      self.lock = threading.Lock()
      self.displayLine1 = None
      self.displayLine2 = None
      self.currentLayerInformation = None

  def initialize(self):
    try:
        self.mylcd = CharLCD(i2c_expander='PCF8574',
                             address=0x27,
                             cols=16, rows=2,
                             backlight_enabled=True,
                             charmap='A00')
        # create block for progress bar
        self.block = bytearray(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
        self.block.append(255)
        self.mylcd.create_char(1, self.block)
    except Exception as e:
        self._logger.exception("Exception during initialisation of the LCD-Driver")

  def jobIsDone(self):

    # create final anim
    self.birdy = [ '^_-' , '^_^', '-_^' , '^_^', '0_0', '-_-', '^_-', '^_^','@_@','*_*','$_$','<_<','>_>']

    for pos in range(0,13):
      self.lcd.cursor_pos = (1,pos)
      self.lcd.write_string(self.birdy[pos])
      time.sleep(0.5)
      self.lcd.clear()
    self.lcd.write_string('Job is Done    \,,/(^_^)\,,/')

  def sendToDisplay(self):
    if self.mylcd != None:
        self.lock.acquire()
        self.mylcd.clear()
        self.mylcd.write_string(self.displayLine1)
        if self.displayLine2 != None:
            self.mylcd.cursor_pos = (1, 0)
            self.mylcd.write_string(self.displayLine2)
        self.lock.release()

  def resetLayerInformations(self):
      self.currentLayerInformation = None

  def on_after_startup(self):
    self._logger.info("plugin initialized !")

  def on_print_progress(self, storage, path, progress):
    if progress == 100:
      self.jobIsDone()
      return

    percent = int(progress / 6.25) + 1
    completed = '\x01' * percent
    self.displayLine1 = 'Completed: ' + str(progress) + '%'

    if progress == 1:
      self.start_date = time.time()

    remaining = None
    if progress > 10 and progress < 100:
      now = time.time()
      elapsed = now - self.start_date
      average = elapsed / (progress - 1)
      remaining = int((100 - progress) * average)
      remaining = str(datetime.timedelta(seconds=remaining))

    line2 = None
    if self._settings.get_boolean(["showLayerInformationIfAvailable"]) and self.currentLayerInformation != None:
        line2 = self._merge_strings("                ", completed, "   _" + self.currentLayerInformation + "_")
    else:
      if remaining != None:
        line2 = self._merge_strings("                ", completed, "   _" + remaining + "_")
      else:
        line2 = completed

    self.displayLine2 = line2
    self.sendToDisplay()

  def _merge_strings(self, targetString, string1, string2):

    def replace_str_index(text, index=0, replacement=''):
      return '%s%s%s' % (text[:index], replacement, text[index + 1:])

    for index in range(len(targetString)):
        if (index < len(string1)):
            targetString = replace_str_index(targetString, index, string1[index])
        if (index < len(string2) and string2[index] != " "):
            targetString = replace_str_index(targetString, index, string2[index])
    # insert spaces
    targetString = targetString.replace("_"," ")
    return targetString

  def on_event(self,event,payload):
    mylcd = self.mylcd

    if event in "DisplayLayerProgress_layerChanged":
      if self._settings.get_boolean(["showLayerInformationIfAvailable"]):
        self.currentLayerInformation = str(payload["currentLayer"]) + "/" + str(payload["totalLayer"])

    if event in "Connected":
      self.resetLayerInformations()
      mylcd.clear()
      mylcd.write_string('Connected to:')
      mylcd.cursor_pos = (1,0)
      portName = payload["port"] if payload["port"] != None else ""
      mylcd.write_string(portName)

    if event in "Shutdown":
      mylcd.clear()
      mylcd.write_string('Bye bye ^_^')
      time.sleep(1)
      mylcd._set_backlight_enabled(False)
      mylcd.close()

    if event in "PrinterStateChanged":

        if payload["state_string"] in "Offline":
            self.resetLayerInformations()
            mylcd.clear()
            mylcd.write_string('Octoprint is not connected')
            time.sleep(2)
            mylcd.clear()
            mylcd.write_string('saving a polar bear, eco mode ON')
            time.sleep(5)
            mylcd._set_backlight_enabled(False)

        if payload["state_string"] in "Operational":
            self.resetLayerInformations()
            mylcd._set_backlight_enabled(True)
            mylcd.clear()
            mylcd.write_string('Printer is       Operational')

        if payload["state_string"] in "Cancelling":
            mylcd.clear()
            mylcd.write_string('Printer  is Cancelling job')
            time.sleep(0.2)

        if payload["state_string"] in "PrintCancelled":
            mylcd.clear()
            time.sleep(0.5)
            mylcd.write_string(' Job has been Cancelled (0_0) ')
            time.sleep(2)

        if payload["state_string"] in "Paused":
            mylcd.clear()
            time.sleep(0.5)
            mylcd.write_string('Printer is  Paused')

        if payload["state_string"] in "Resuming":
            mylcd.clear()
            mylcd.write_string('Printer is Resuming its job')
            time.sleep(0.2)

  def get_update_information(self):
      return dict(
          LCD1602Plugin=dict(
              displayName="LCD1602 display",
              displayVersion=self._plugin_version,

              type="github_release",
              current=self._plugin_version,
              user="n3bojs4",
              repo="OctoPrint-Lcd1602",

              pip="https://github.com/n3bojs4/octoprint-LCD1602/archive/{target}.zip"
          )
      )

  ##~~ SettingsPlugin mixin
  def get_settings_defaults(self):
    settings = dict(
        installedVersion=self._plugin_version,
        showLayerInformationIfAvailable=False
    )
    return settings

# ~~ AssetPlugin mixin
  def get_assets(self):
    # Define your plugin's asset files to automatically include in the
    # core UI here.
    return dict(
        js=["js/LCD1602.js"],
        css=[],
        less=[]
    )


__plugin_name__ = "LCD1602 I2c display"

def __plugin_load__():
  global __plugin_implementation__
  __plugin_implementation__ = LCD1602Plugin()

  global __plugin_hooks__
  __plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
  }
