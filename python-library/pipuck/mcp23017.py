# The MIT License (MIT)
#
# Copyright (c) 2017 Tony DiCola for Adafruit Industries
#                    refactor by Carter Nelson
#                    modified into a single file that uses SMBus by Russell Joyce (2020)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""Python module for the MCP23017 I2C I/O extender.

Based on https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx.git
"""

# __version__ = "0.0.0-auto.0"
# __repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx.git"

# pylint: disable=bad-whitespace
_MCP23017_ADDRESS = 0x20
_MCP23017_IODIRA = 0x00
_MCP23017_IODIRB = 0x01
_MCP23017_IPOLA = 0x02
_MCP23017_GPINTENA = 0x04
_MCP23017_DEFVALA = 0x06
_MCP23017_INTCONA = 0x08
_MCP23017_IOCON = 0x0A
_MCP23017_GPPUA = 0x0C
_MCP23017_GPPUB = 0x0D
_MCP23017_GPIOA = 0x12
_MCP23017_GPIOB = 0x13
_MCP23017_INTFA = 0x0E
_MCP23017_INTFB = 0x0F
_MCP23017_INTCAPA = 0x10
_MCP23017_INTCAPB = 0x11

_MCP23017_INPUT = 0
_MCP23017_OUTPUT = 1
_MCP23017_PULL_UP = 0
_MCP23017_PULL_DOWN = 1


class MCP23017:
    """Supports MCP23017 instance on specified I2C bus and optionally
    at the specified I2C address.
    """

    def __init__(self, i2c_bus, address=_MCP23017_ADDRESS):
        self._bus = i2c_bus
        self._address = address
        # Reset to all inputs with no pull-ups and no inverted polarity.
        self.iodir = 0xFFFF
        self.gppu = 0x0000
        self.iocon = 0x4  # turn on IRQ Pins as open drain
        self._write_u16le(_MCP23017_IPOLA, 0x0000)

    def _read_u16le(self, register):
        # Read an unsigned 16 bit little endian value from the specified 8-bit
        # register.
        return self._bus.read_word_data(self._address, register)

    def _write_u16le(self, register, val):
        # Write an unsigned 16 bit little endian value to the specified 8-bit
        # register.
        self._bus.write_word_data(self._address, register, val)

    def _read_u8(self, register):
        # Read an unsigned 8 bit value from the specified 8-bit register.
        return self._bus.read_byte_data(self._address, register)

    def _write_u8(self, register, val):
        # Write an 8 bit value to the specified 8-bit register.
        self._bus.write_byte_data(self._address, register, val)

    @property
    def gpio(self):
        """The raw GPIO output register.  Each bit represents the
        output value of the associated pin (0 = low, 1 = high), assuming that
        pin has been configured as an output previously.
        """
        return self._read_u16le(_MCP23017_GPIOA)

    @gpio.setter
    def gpio(self, val):
        self._write_u16le(_MCP23017_GPIOA, val)

    @property
    def gpioa(self):
        """The raw GPIO A output register.  Each bit represents the
        output value of the associated pin (0 = low, 1 = high), assuming that
        pin has been configured as an output previously.
        """
        return self._read_u8(_MCP23017_GPIOA)

    @gpioa.setter
    def gpioa(self, val):
        self._write_u8(_MCP23017_GPIOA, val)

    @property
    def gpiob(self):
        """The raw GPIO B output register.  Each bit represents the
        output value of the associated pin (0 = low, 1 = high), assuming that
        pin has been configured as an output previously.
        """
        return self._read_u8(_MCP23017_GPIOB)

    @gpiob.setter
    def gpiob(self, val):
        self._write_u8(_MCP23017_GPIOB, val)

    @property
    def iodir(self):
        """The raw IODIR direction register.  Each bit represents
        direction of a pin, either 1 for an input or 0 for an output mode.
        """
        return self._read_u16le(_MCP23017_IODIRA)

    @iodir.setter
    def iodir(self, val):
        self._write_u16le(_MCP23017_IODIRA, val)

    @property
    def iodira(self):
        """The raw IODIR A direction register.  Each bit represents
        direction of a pin, either 1 for an input or 0 for an output mode.
        """
        return self._read_u8(_MCP23017_IODIRA)

    @iodira.setter
    def iodira(self, val):
        self._write_u8(_MCP23017_IODIRA, val)

    @property
    def iodirb(self):
        """The raw IODIR B direction register.  Each bit represents
        direction of a pin, either 1 for an input or 0 for an output mode.
        """
        return self._read_u8(_MCP23017_IODIRB)

    @iodirb.setter
    def iodirb(self, val):
        self._write_u8(_MCP23017_IODIRB, val)

    @property
    def gppu(self):
        """The raw GPPU pull-up register.  Each bit represents
        if a pull-up is enabled on the specified pin (1 = pull-up enabled,
        0 = pull-up disabled).  Note pull-down resistors are NOT supported!
        """
        return self._read_u16le(_MCP23017_GPPUA)

    @gppu.setter
    def gppu(self, val):
        self._write_u16le(_MCP23017_GPPUA, val)

    @property
    def gppua(self):
        """The raw GPPU A pull-up register.  Each bit represents
        if a pull-up is enabled on the specified pin (1 = pull-up enabled,
        0 = pull-up disabled).  Note pull-down resistors are NOT supported!
        """
        return self._read_u8(_MCP23017_GPPUA)

    @gppua.setter
    def gppua(self, val):
        self._write_u8(_MCP23017_GPPUA, val)

    @property
    def gppub(self):
        """The raw GPPU B pull-up register.  Each bit represents
        if a pull-up is enabled on the specified pin (1 = pull-up enabled,
        0 = pull-up disabled).  Note pull-down resistors are NOT supported!
        """
        return self._read_u8(_MCP23017_GPPUB)

    @gppub.setter
    def gppub(self, val):
        self._write_u8(_MCP23017_GPPUB, val)

    def get_pin(self, pin):
        """Convenience function to create an instance of the DigitalInOut class
        pointing at the specified pin of this MCP23017 device.
        """
        assert 0 <= pin <= 15
        return DigitalInOut(pin, self)

    @property
    def interrupt_configuration(self):
        """The raw INTCON interrupt control register. The INTCON register
        controls how the associated pin value is compared for the
        interrupt-on-change feature. If  a  bit  is  set,  the  corresponding
        I/O  pin  is  compared against the associated bit in the DEFVAL
        register. If a bit value is clear, the corresponding I/O pin is
        compared against the previous value.
        """
        return self._read_u16le(_MCP23017_INTCONA)

    @interrupt_configuration.setter
    def interrupt_configuration(self, val):
        self._write_u16le(_MCP23017_INTCONA, val)

    @property
    def interrupt_enable(self):
        """The raw GPINTEN interrupt control register. The GPINTEN register
        controls the interrupt-on-change feature for each pin. If a bit is
        set, the corresponding pin is enabled for interrupt-on-change.
        The DEFVAL and INTCON registers must also be configured if any pins
        are enabled for interrupt-on-change.
        """
        return self._read_u16le(_MCP23017_GPINTENA)

    @interrupt_enable.setter
    def interrupt_enable(self, val):
        self._write_u16le(_MCP23017_GPINTENA, val)

    @property
    def default_value(self):
        """The raw DEFVAL interrupt control register. The default comparison
        value is configured in the DEFVAL register. If enabled (via GPINTEN
        and INTCON) to compare against the DEFVAL register, an opposite value
        on the associated pin will cause an interrupt to occur.
        """
        return self._read_u16le(_MCP23017_DEFVALA)

    @default_value.setter
    def default_value(self, val):
        self._write_u16le(_MCP23017_DEFVALA, val)

    @property
    def io_control(self):
        """The raw IOCON configuration register. Bit 1 controls interrupt
        polarity (1 = active-high, 0 = active-low). Bit 2 is whether irq pin
        is open drain (1 = open drain, 0 = push-pull). Bit 3 is unused.
        Bit 4 is whether SDA slew rate is enabled (1 = yes). Bit 5 is if I2C
        address pointer auto-increments (1 = no). Bit 6 is whether interrupt
        pins are internally connected (1 = yes). Bit 7 is whether registers
        are all in one bank (1 = no).
        """
        return self._read_u8(_MCP23017_IOCON)

    @io_control.setter
    def io_control(self, val):
        self._write_u8(_MCP23017_IOCON, val)

    @property
    def int_flag(self):
        """Returns a list with the pin numbers that caused an interrupt
        port A ----> pins 0-7
        port B ----> pins 8-15
        """
        intf = self._read_u16le(_MCP23017_INTFA)
        flags = [pin for pin in range(16) if intf & (1 << pin)]
        return flags

    @property
    def int_flaga(self):
        """Returns a list of pin numbers that caused an interrupt in port A
        pins: 0-7
        """
        intfa = self._read_u8(_MCP23017_INTFA)
        flags = [pin for pin in range(8) if intfa & (1 << pin)]
        return flags

    @property
    def int_flagb(self):
        """Returns a list of pin numbers that caused an interrupt in port B
        pins: 8-15
        """
        intfb = self._read_u8(_MCP23017_INTFB)
        flags = [pin + 8 for pin in range(8) if intfb & (1 << pin)]
        return flags

    def clear_ints(self):
        """Clears interrupts by reading INTCAP."""
        self._read_u16le(_MCP23017_INTCAPA)

    def clear_inta(self):
        """Clears port A interrupts."""
        self._read_u8(_MCP23017_INTCAPA)

    def clear_intb(self):
        """Clears port B interrupts."""
        self._read_u8(_MCP23017_INTCAPB)


class DigitalInOut:
    """Digital input/output of the MCP230xx.  The interface is exactly the
    same as the digitalio.DigitalInOut class (however the MCP230xx does not
    support pull-down resistors and an exception will be thrown
    attempting to set one).
    """

    # Internal helpers to simplify setting and getting a bit inside an integer.
    @staticmethod
    def _get_bit(val, bit):
        return val & (1 << bit) > 0

    @staticmethod
    def _enable_bit(val, bit):
        return val | (1 << bit)

    @staticmethod
    def _clear_bit(val, bit):
        return val & ~(1 << bit)

    def __init__(self, pin_number, mcp230xx):
        """Specify the pin number of the MCP230xx (0...7 for MCP23008, or 0...15
        for MCP23017) and MCP23008 instance.
        """
        self._pin = pin_number
        self._mcp = mcp230xx

    # kwargs in switch functions below are _necessary_ for compatibility
    # with DigitalInout class (which allows specifying pull, etc. which
    # is unused by this class).  Do not remove them, instead turn off pylint
    # in this case.
    # pylint: disable=unused-argument
    def switch_to_output(self, value=False):
        """Switch the pin state to a digital output with the provided starting
        value (True/False for high or low, default is False/low).
        """
        self.direction = _MCP23017_OUTPUT
        self.value = value

    def switch_to_input(self, pull=None):
        """Switch the pin state to a digital input with the provided starting
        pull-up resistor state (optional, no pull-up by default).  Note that
        pull-down resistors are NOT supported!
        """
        self.direction = _MCP23017_INPUT
        self.pull = pull

    # pylint: enable=unused-argument

    @property
    def value(self):
        """The value of the pin, either True for high or False for
        low.  Note you must configure as an output or input appropriately
        before reading and writing this value.
        """
        return self._get_bit(self._mcp.gpio, self._pin)

    @value.setter
    def value(self, val):
        if val:
            self._mcp.gpio = self._enable_bit(self._mcp.gpio, self._pin)
        else:
            self._mcp.gpio = self._clear_bit(self._mcp.gpio, self._pin)

    @property
    def direction(self):
        """The direction of the pin, either True for an input or
        False for an output.
        """
        if self._get_bit(self._mcp.iodir, self._pin):
            return _MCP23017_INPUT
        return _MCP23017_OUTPUT

    @direction.setter
    def direction(self, val):
        if val == _MCP23017_INPUT:
            self._mcp.iodir = self._enable_bit(self._mcp.iodir, self._pin)
        elif val == _MCP23017_OUTPUT:
            self._mcp.iodir = self._clear_bit(self._mcp.iodir, self._pin)
        else:
            raise ValueError("Expected INPUT or OUTPUT direction!")

    @property
    def pull(self):
        """Enable or disable internal pull-up resistors for this pin.  A
        value of _MCP23017_PULL_UP will enable a pull-up resistor, and None will
        disable it.  Pull-down resistors are NOT supported!
        """
        if self._get_bit(self._mcp.gppu, self._pin):
            return _MCP23017_PULL_UP
        return None

    @pull.setter
    def pull(self, val):
        if val is None:
            self._mcp.gppu = self._clear_bit(self._mcp.gppu, self._pin)
        elif val == _MCP23017_PULL_UP:
            self._mcp.gppu = self._enable_bit(self._mcp.gppu, self._pin)
        elif val == _MCP23017_PULL_DOWN:
            raise ValueError("Pull-down resistors are not supported!")
        else:
            raise ValueError("Expected UP, DOWN, or None for pull state!")
