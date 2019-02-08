#!/usr/bin/env python

__author__ = 'Trevor Allen'


## Standard Library
pass

## Non-Standard Imports
import nose.tools as nt
from nose.tools import raises
# If you don't use nose, you can simply replace the assertions below

## Custom Modules
from rpidevmocks import MockSMBus, MockGPIO, Mock_smbusModule
from display_example import Display


class TestDisplay(object):
    ''' Test class for SainSmart LCD Display, using I2C via smbus '''

    @classmethod
    def setup_class(klass):
        ''' This method is run once for each class before ANY tests are run. '''
        ## Create "mock instances" for the lcd display device to use
        klass.GPIO = MockGPIO()
        smbus = Mock_smbusModule()
        bus_no = 1 if klass.GPIO.RPI_REVISION >= 2 else 0
        klass.bus = smbus.SMBus(bus_no)

    @classmethod
    def teardown_class(klass):
        '''This method is run once for each class _after_ all tests are run'''
        klass.GPIO.cleanup()

    def test_init(self):
        '''
        test_init() should run w/o error, verifying object can be instantiated
        '''
        display = Display(self.bus)
        nt.assert_is_not_none(display.lcd)
        nt.assert_is_not_none(display.contents)

    @raises(AssertionError)
    def test_write_line_high_lineno(self):
        '''
        test_write_line_high_lineno()...
        '''
        display = Display(self.bus)
        display.writeLine(msg="Love's all you need", line_no=5)

    @raises(AssertionError)
    def test_write_line_low_lineno(self):
        '''
        test_write_line_low_lineno()...
        '''
        display = Display(self.bus)
        display.writeLine(msg="Whodat?!", line_no=0)

    @raises(AssertionError)
    def test_write_line_long_msg(self):
        '''
        test_write_line_long_msg()...
        '''
        display = Display(self.bus)
        display.writeLine(msg="supercalifragilisticexpialidocious", line_no=1)

    def test_write_lines(self):
        '''
        test_write_lines()...
        '''
        display = Display(self.bus)
        display.writeLines({1: 'Gummy bears', 2:'Jellbeans',
                            3:'and all kinds', 4:'of wonderful things'})