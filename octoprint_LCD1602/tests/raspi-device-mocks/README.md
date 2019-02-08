RasPi Device Mocks
==================
*Fake libraries for low-level device interfaces for Raspberry Pi development on a non-Linux platform*

This package provides a set of "fake" modules to some replace low-level device-interfacing Python packages for
use in development or testing of code that requires those interfaces. Its original intent was to allow me
to write & test Raspberry Pi code on a non-Linux platform, specifically in Mac OSX. Packages like [RPi.GPIO](http://sourceforge.net/projects/raspberry-gpio-python/)
and `smbus` and others can be a pain to get installed & configured on a Mac, particularly if it's just
to fill a dependency in order to run higher-level code or unit tests.

Example Usage
-------------

One can use a try/except to prefer the actual interacing modules if the code is run on a supported
platform, but upon failure fall back to these fake modules.

```
## Try/Except to prefer "real" packages on supported platforms
try:
    import RPi.GPIO as GPIO
    import smbus
    import spi
except ImportError:
    from rpidevmocks import MockGPIO, Mock_smbusModule, MockSPI
    GPIO = MockGPIO()
    smbus = Mock_smbusModule()
    spi = MockSPI()
```

Below is an example of using the mocks for unit tests on code that requires one or more such packages.
This was written for a [SainSmart LCD display](http://www.amazon.com/SainSmart-Module-Arduino-Board-White/dp/B003B22UR0/ref=sr_1_4?ie=UTF8&qid=1427462020&sr=8-4&keywords=lcd+display+arduino)
which uses `smbus` for I2C communication, but also references `RPi.GPIO` to get the RasPi board revision number.

```
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
```

Additional example code for the unit tests and for the lcd display itself are included in the repo.

The provided code is to get started, it's by no means complete, but I'm expanding functionality as I go.

On a final note, the mock classes were written specifically for a project I'm working on (shameless plug for
[Zenith Project: Data-Driven Fitness](http://www.zenith.fitness>)), so some attributes provide specific
registers or references to hardware. I'll probably replace that in subsequent updates.

