#!/usr/bin/env python
# lcd_device: driver code to interface directly with I2C-driven LCD display

''' Origin: Combined Guerreau's 'i2c_device.py' and 'lcddriver.py' into
a single script for importing & controlling. Some minor edits and restructuring,
but the majority of the code base herein is by Guerreau, as stated below.
'''

__author__ = 'Stephane Guerreau'  # Primary author of LCD driver, via GitHub & blog
__credits__ = ['Trevor Allen', ]  # Minor edits & restructuring
# Stephane Guerreau's blog post:
# http://hardware-libre.fr/2014/03/en-raspberry-pi-using-a-4x20-characters-display/
# and associated GitHub repo: https://github.com/CaptainStouf/raspberry_lcd4x20_I2C

## Standard Imports
import time


class lcd(object):
    ## Global variables for LCD object, originally from Guerreau's 'lcddriver.py'
    # LCD Address
    ADDRESS = 0x27

    # commands
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    # flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    # flags for backlight control
    LCD_BACKLIGHT = 0x08
    LCD_NOBACKLIGHT = 0x00

    En = 0b00000100 # Enable bit
    Rw = 0b00000010 # Read/Write bit
    Rs = 0b00000001 # Register select bit

    ## Modified to RECEIVE the bus upon instantiation
    def __init__(self, bus, addr=0x27, port=1):
        # Originally from i2c_lib.py
        self.addr = addr
        # self.bus = smbus.SMBus(port)
        self.bus = bus
        # self.lcd_device = i2c_lib.i2c_device(ADDRESS)

        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)

        self.lcd_write(self.LCD_FUNCTIONSET | self.LCD_2LINE | self.LCD_5x8DOTS | self.LCD_4BITMODE)
        self.lcd_write(self.LCD_DISPLAYCONTROL | self.LCD_DISPLAYON)
        self.lcd_write(self.LCD_CLEARDISPLAY)
        self.lcd_write(self.LCD_ENTRYMODESET | self.LCD_ENTRYLEFT)
        time.sleep(0.2)

    def write_cmd(self, cmd):
        # Write a single command (originally from i2c_lib.py)
        self.bus.write_byte(self.addr, cmd)
        time.sleep(0.0001)

    def write_cmd_arg(self, cmd, data):
        # Write a command and argument (originally from i2c_lib.py)
        self.bus.write_byte_data(self.addr, cmd, data)
        time.sleep(0.0001)

    def write_block_data(self, cmd, data):
        # Write a block of data (originally from i2c_lib.py)
        self.bus.write_block_data(self.addr, cmd, data)
        time.sleep(0.0001)

    def read(self):
        # Read a single byte (originally from i2c_lib.py)
        return self.bus.read_byte(self.addr)

    def read_data(self, cmd):
        # Read (originally from i2c_lib.py)
        return self.bus.read_byte_data(self.addr, cmd)

    def read_block_data(self, cmd):
        # Read a block of data (originally from i2c_lib.py)
        return self.bus.read_block_data(self.addr, cmd)

    def lcd_strobe(self, data):
        # clocks EN to latch command
        # self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
        self.write_cmd(data | self.En | self.LCD_BACKLIGHT)
        time.sleep(.0005)
        # self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
        self.write_cmd(((data & ~self.En) | self.LCD_BACKLIGHT))
        time.sleep(.0001)

    def lcd_write_four_bits(self, data):
        # self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
        self.write_cmd(data | self.LCD_BACKLIGHT)
        self.lcd_strobe(data)

    def lcd_write(self, cmd, mode=0):
        # write a command to lcd
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    def lcd_display_string(self, string, line):
        ### String & Line validation applied specifically for SainSmart 20x4 LCD,
        #   which has 4 lines of 20 characters each.
        try:
            line = int(line)
        except ValueError:
            raise ValueError('Line number must be an integer.')
        if line < 1 or line > 4:
            raise ValueError('Line number must be between 1 and 4.')
        # put string function
        if line == 1:
            self.lcd_write(0x80)
        if line == 2:
            self.lcd_write(0xC0)
        if line == 3:
            self.lcd_write(0x94)
        if line == 4:
            self.lcd_write(0xD4)

        for char in string:
            self.lcd_write(ord(char), self.Rs)

    def lcd_clear(self):
        # clear lcd and set to home
        self.lcd_write(self.LCD_CLEARDISPLAY)
        self.lcd_write(self.LCD_RETURNHOME)

