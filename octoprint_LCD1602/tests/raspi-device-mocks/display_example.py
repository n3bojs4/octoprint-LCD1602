#!/usr/bin/env python
'''
Note: some pieces of code referencing buttons, cursor, and/or menu capability were
removed for the purpose of this example. Shouldn't affect code's intended functionality.
'''

__author__ = 'Trevor Allen'

## Standard Library
import time
from collections import deque

## Non-Standard Imports
pass

## Custom Modules
import lcd_device


class Display(lcd_device.lcd):
    ''' Wrapper for lcd_device.py, structured for Zenith Project '''

    def __init__(self, bus):
        self.lcd = lcd_device.lcd(bus=bus, addr=0x27, port=1)
        self.lcd.lcd_clear()
        self.contents = {1:'', 2:'', 3:'', 4:''}
        self.menu_mode = False  # Regarding line length & prepended space
        self.cursor_loc = 0   # Which line is the cursor on
        self.cursor_opts = [0]  # What lines is the cursor allowed on

    def __repr__(self):
        lines = ', '.join([':'.join((str(k),v[:5]+'-')) for k,v in d.contents.items()])
        return '''<LCDdisplay(%s)>''' % lines

    def clearScreen(self):
        self.lcd.lcd_clear()
        self.contents = {i:'' for i in range(1,5)}

    def finishUp(self):
        self.clearScreen()

    def initialScreen(self, weight=0, user='Unknown'):
        # Initialize screen: weight, sets, reps, user (if available)
        self.menu_mode = False
        self.writeUser(user=user, line_no=1)
        self.writeSetRep(exset=0, exrep=0, line_no=2)
        self.writeWeight(weight=weight, line_no=3)
        self.writeLine('', 4)  # Empty line

    def emptyLine(self, line_no):
        self.writeLine('', line_no)

    def getLine(self, line_no):
        return self.contents[line_no]

    def writeLine(self, msg, line_no):
        msg = msg.rstrip()  # Remove existing right padding
        assert line_no in range(1,5), "Line number must be 1-4."
        max_len = 19 if self.menu_mode else 20
        assert len(msg) <= max_len, "Too long: %s is %d chars." % (str(msg), len(msg))
        # Right padding to either 19 or 20 chars
        if len(msg) < max_len:
            msg = msg + (' '*(max_len-len(msg)) )
        self.contents[line_no] = msg
        self.lcd.lcd_display_string(msg, line_no)

    def writeLines(self, msgs):
        # Accepts dictionary of multiple lines to write
        ## If I want to add empty lines, can use this:
        # if len(msgs) < 4:
        #     empties = 4 - len(options)
        #     [options.append('') for x in range(empties)]
        for k,v in msgs.items():
            self.writeLine(msg=v, line_no=k)

    def validateMsg(self, msg):
        ## Lots of need to verify several aspects of message/contents
        # Msg type - should be dict
        if not isinstance(msg, dict):
            raise TypeError('Message must be in form of a dictionary.')
        # Msg size - only four lines of text
        if len(msg) > 4:
            raise UserWarning('Message too long, only using first 4 elements.')
            msg = msg[:4]
        # Msg lines/keys - dict keys must be 1, 2, 3, or 4
        if not all([k in self.contents.keys() for k in msg.keys()]):
            raise KeyError('One or more message keys invalid: %s' % str(msg.keys()))
        # Msg text - warn of trimming if message is too long
        for k,v in msg.items():
            max_len = 19 if self.menu_mode else 20
            if len(v) > max_len:
                raise UserWarning('Line %d message too long, will be trimmed: %s' % (k,v))
        return msg


