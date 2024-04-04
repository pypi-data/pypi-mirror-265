from abc import ABC
from smbus2 import SMBus

# i2c address
GP8XXX_I2C_DEVICE_ADDR = 0x58


class GP8XXX(ABC):
    # Select DAC output voltage of 0-5V
    OUTPUT_RANGE_2_5V = 0
    # Select DAC output voltage of 0-5V
    OUTPUT_RANGE_5V = 1
    # Select DAC output voltage of 0-10V
    OUTPUT_RANGE_10V = 2
    # Select DAC output voltage of 0-VCC
    OUTPUT_RANGE_VCC = 3
    RESOLUTION_12_BIT = 0x0FFF
    RESOLUTION_15_BIT = 0x7FFF

    def __init__(self):
        pass

    def begin(self):
        pass

    def set_dac_out_voltage(self, voltage, channel):
        pass

class GP8XXX_IIC(GP8XXX):
    """
    I2C class initialization
    - param resolution: the resolution of the chip
    - param bus: the i2c bus number
    - param device_addr: the I2C device address 
    - param auto_range: automatically selects the correct output range 
    """
    GP8XXX_CONFIG_REG = 0x02

    def __init__(self, resolution, bus=1, device_addr=GP8XXX_I2C_DEVICE_ADDR, auto_range=True):
        self._resolution = resolution
        self._bus = bus
        self._device_addr = device_addr
        self._auto_range = auto_range
        self.channel0 = 0
        self.channel1 = 0

        self._i2c = SMBus(self._bus)

        self._dac_voltage = None

    def begin(self):
        """
        Initialize the function returns true for success
        """
        return not self._i2c.read_byte(self._device_addr) != 0

    def set_dac_outrange(self, output_range: int = GP8XXX.OUTPUT_RANGE_10V):
        """
        Set the DAC output range
        - param output_range [int]: DAC output range
        """
        if output_range == self.OUTPUT_RANGE_5V:
            self._dac_voltage = 5000
            self._i2c.write_byte_data(
                self._device_addr, self.GP8XXX_CONFIG_REG >> 1, 0x00)
        elif output_range == self.OUTPUT_RANGE_10V:
            self._dac_voltage = 10000
            self._i2c.write_byte_data(
                self._device_addr, self.GP8XXX_CONFIG_REG >> 1, 0x11)

    def set_dac_out_voltage(self, voltage: float, channel: int = 0):
        """
        Set different channel output DAC values
        - param voltage [int]: value corresponding to the output voltage value (e.g. 4.321V is 4321)
        - param channel [int]: integer representing the output channel
          - 0: Channel 0
          - 1: Channel 1
          - 2: All channels
        """
        voltage = float(voltage)

        if channel == 0:
            self.channel0 = voltage
        
        if channel == 1:
            self.channel1 = voltage

        max_voltage = max(self.channel0, self.channel1)

        if self._auto_range and 0 <= max_voltage <= 5000:
            self.set_dac_outrange(self.OUTPUT_RANGE_5V)
        elif self._auto_range and 5000 <= max_voltage <= 10000:
            self.set_dac_outrange(self.OUTPUT_RANGE_10V)

        output_value = (voltage / self._dac_voltage) * self._resolution

        if self._resolution == self.RESOLUTION_12_BIT:
            output_value = int(output_value) << 4
        elif self._resolution == self.RESOLUTION_15_BIT:
            output_value = int(output_value) << 1

        if channel == 0:
            self._i2c.write_word_data(
                self._device_addr, self.GP8XXX_CONFIG_REG, output_value)
        elif channel == 1:
            self._i2c.write_word_data(
                self._device_addr, self.GP8XXX_CONFIG_REG << 1, output_value)
        elif channel == 2:
            self._i2c.write_word_data(
                self._device_addr, self.GP8XXX_CONFIG_REG, output_value)
            self._i2c.write_word_data(
                self._device_addr, self.GP8XXX_CONFIG_REG << 1, output_value)

    def store(self):
        """
        FIXME: Unfortunately, I can't get the chip to store the values
        """
        raise NotImplementedError

class GP8503(GP8XXX_IIC):
    """
    12bit DAC Dual Channel I2C to 0-2.5V/0-VCC
    - param bus: the i2c bus number
    """

    def __init__(self, bus=1):
        super().__init__(bus=bus, resolution=self.RESOLUTION_12_BIT, auto_range=False)
        self.voltage = 2500

class GP8211S(GP8XXX_IIC):
    """
    15 bit DAC I2C to 0-5V/0-10V
    - param bus: the i2c bus number
    - param auto_range: automatically selects the correct output range 
    """

    def __init__(self, bus=1, auto_range=True):
        super().__init__(bus=bus, resolution=self.RESOLUTION_15_BIT, auto_range=auto_range)

class GP8512(GP8XXX_IIC):
    """
    15bit DAC I2C to 0-2.5V/0-VCC
    - param bus: the i2c bus number
    """

    def __init__(self, bus=1):
        super().__init__(bus=bus, resolution=self.RESOLUTION_15_BIT, auto_range=False)
        self.dac_voltage = 2500

class GP8413(GP8XXX_IIC):
    """
    15bit DAC Dual Channel I2C to 0-10V
    - param bus: the i2c bus number
    - param i2c_addr: the I2C device address 
    """

    def __init__(self, bus=1, i2c_addr=0x58):
        super().__init__(bus=bus, resolution=self.RESOLUTION_15_BIT,
                         device_addr=i2c_addr, auto_range=False)
        self.set_dac_outrange(self.OUTPUT_RANGE_10V)

class GP8403(GP8XXX_IIC):
    """
    12bit DAC Dual Channel I2C to 0-5V/0-10V
    - param bus: the i2c bus number
    - param i2c_addr: the I2C device address 
    - param auto_range: automatically selects the correct output range 
    """

    def __init__(self, bus=1, i2c_addr=0x58, auto_range=True):
        super().__init__(bus=bus, resolution=self.RESOLUTION_12_BIT,
                         device_addr=i2c_addr, auto_range=auto_range)

class GP8302(GP8XXX_IIC):
    """
    12bit DAC Dual Channel I2C to 0-5V/0-10V
    - param bus: the i2c bus number
    - param i2c_addr: the I2C device address 
    - param auto_range: automatically selects the correct output range 
    """

    def __init__(self, bus=1, i2c_addr=0x58, auto_range=True):
        super().__init__(bus=bus, resolution=self.RESOLUTION_12_BIT,
                         device_addr=i2c_addr, auto_range=auto_range)

    def set_dac_out_electric_current(self, current):
        """
        Set different channel output DAC values
        - param current [int]: value corresponding to the output current value (e.g. 1.321A is 1321)
        """
        return self.set_dac_out_voltage(current)
