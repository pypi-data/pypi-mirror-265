# -*- coding: utf-8 -*
import time
import datetime
import RPi.GPIO as GPIO
from smbus2 import SMBus


FullSine5Bit = [
    2048, 2447, 2831, 3185, 3495, 3750, 3939, 4056,
    4095, 4056, 3939, 3750, 3495, 3185, 2831, 2447,
    2048, 1648, 1264, 910, 600, 345, 156,  39,
    0,  39, 156, 345, 600, 910, 1264, 1648]

FullSine6Bit = [
    2048, 2248, 2447, 2642, 2831, 3013, 3185, 3346,
    3495, 3630, 3750, 3853, 3939, 4007, 4056, 4085,
    4095, 4085, 4056, 4007, 3939, 3853, 3750, 3630,
    3495, 3346, 3185, 3013, 2831, 2642, 2447, 2248,
    2048, 1847, 1648, 1453, 1264, 1082,  910,  749,
    600,  465,  345,  242,  156,   88,   39,   10,
    0,   10,   39,   88,  156,  242,  345,  465,
    600,  749,  910, 1082, 1264, 1453, 1648, 1847]

FullSine7Bit = [
    2048, 2148, 2248, 2348, 2447, 2545, 2642, 2737,
    2831, 2923, 3013, 3100, 3185, 3267, 3346, 3423,
    3495, 3565, 3630, 3692, 3750, 3804, 3853, 3898,
    3939, 3975, 4007, 4034, 4056, 4073, 4085, 4093,
    4095, 4093, 4085, 4073, 4056, 4034, 4007, 3975,
    3939, 3898, 3853, 3804, 3750, 3692, 3630, 3565,
    3495, 3423, 3346, 3267, 3185, 3100, 3013, 2923,
    2831, 2737, 2642, 2545, 2447, 2348, 2248, 2148,
    2048, 1947, 1847, 1747, 1648, 1550, 1453, 1358,
    1264, 1172, 1082,  995,  910,  828,  749,  672,
    600,  530,  465,  403,  345,  291,  242,  197,
    156,  120,   88,   61,   39,   22,   10,    2,
    0,    2,   10,   22,   39,   61,   88,  120,
    156,  197,  242,  291,  345,  403,  465,  530,
    600,  672,  749,  828,  910,  995, 1082, 1172,
    1264, 1358, 1453, 1550, 1648, 1747, 1847, 1947]

FullSine8Bit = [
    2048, 2098, 2148, 2198, 2248, 2298, 2348, 2398,
    2447, 2496, 2545, 2594, 2642, 2690, 2737, 2784,
    2831, 2877, 2923, 2968, 3013, 3057, 3100, 3143,
    3185, 3226, 3267, 3307, 3346, 3385, 3423, 3459,
    3495, 3530, 3565, 3598, 3630, 3662, 3692, 3722,
    3750, 3777, 3804, 3829, 3853, 3876, 3898, 3919,
    3939, 3958, 3975, 3992, 4007, 4021, 4034, 4045,
    4056, 4065, 4073, 4080, 4085, 4089, 4093, 4094,
    4095, 4094, 4093, 4089, 4085, 4080, 4073, 4065,
    4056, 4045, 4034, 4021, 4007, 3992, 3975, 3958,
    3939, 3919, 3898, 3876, 3853, 3829, 3804, 3777,
    3750, 3722, 3692, 3662, 3630, 3598, 3565, 3530,
    3495, 3459, 3423, 3385, 3346, 3307, 3267, 3226,
    3185, 3143, 3100, 3057, 3013, 2968, 2923, 2877,
    2831, 2784, 2737, 2690, 2642, 2594, 2545, 2496,
    2447, 2398, 2348, 2298, 2248, 2198, 2148, 2098,
    2048, 1997, 1947, 1897, 1847, 1797, 1747, 1697,
    1648, 1599, 1550, 1501, 1453, 1405, 1358, 1311,
    1264, 1218, 1172, 1127, 1082, 1038,  995,  952,
    910,  869,  828,  788,  749,  710,  672,  636,
    600,  565,  530,  497,  465,  433,  403,  373,
    345,  318,  291,  266,  242,  219,  197,  176,
    156,  137,  120,  103,   88,   74,   61,   50,
    39,   30,   22,   15,   10,    6,    2,    1,
    0,    1,    2,    6,   10,   15,   22,   30,
    39,   50,   61,   74,   88,  103,  120,  137,
    156,  176,  197,  219,  242,  266,  291,  318,
    345,  373,  403,  433,  465,  497,  530,  565,
    600,  636,  672,  710,  749,  788,  828,  869,
    910,  952,  995, 1038, 1082, 1127, 1172, 1218,
    1264, 1311, 1358, 1405, 1453, 1501, 1550, 1599,
    1648, 1697, 1747, 1797, 1847, 1897, 1947, 1997]



class GP8403():
    # Select DAC output voltage of 0-5V
    OUTPUT_RANGE_5V = 0
    # Select DAC output voltage of 0-10V
    OUTPUT_RANGE_10V = 17
    # Select to output from channel 0
    CHANNEL0 = 0
    # Select to output from channel 1
    CHANNEL1 = 1
    # Select to output from all the channels
    CHANNELALL = 2

    # Configure current sensor register
    GP8403_CONFIG_CURRENT_REG = 0x02
    # Store function timing start head
    GP8302_STORE_TIMING_HEAD = 0x02
    # The first address for entering store timing
    GP8302_STORE_TIMING_ADDR = 0x10
    # The command 1 to enter store timing
    GP8302_STORE_TIMING_CMD1 = 0x03
    # The command 2 to enter store timing
    GP8302_STORE_TIMING_CMD2 = 0x00
    # Total I2C communication cycle 5us
    I2C_CYCLE_TOTAL = 0.000005
    # The first half cycle of the total I2C communication cycle 2us
    I2C_CYCLE_BEFORE = 0.000002
    # The second half cycle of the total I2C communication cycle 3us
    I2C_CYCLE_AFTER = 0.000003

    # Store procedure interval delay time: 10ms (1000us)
    # (should be more than 7ms according to spec)
    GP8302_STORE_TIMING_DELAY = 0.0000010

    def __init__(self, bus=1, addr=0x58):
        """Keyword arguments:
        bus - bus ID
        addr - I2C Adress
        """

        self._addr = addr
        self.output_setrange = 0x01
        self.voltage = 5000
        self._scl = 3
        self._sda = 2
        self.data_transmission = 0
        self.i2c = SMBus(bus)

    def begin(self):
        """Initialize the sensor"""
        if self.i2c.read_byte(self._addr) != 0:
            return 0
        return 1

    def set_DAC_outrange(self, mode: int = OUTPUT_RANGE_10V):
        """Set DAC output range

        Keyword arguments:
        mode - OUTPUT_RANGE_5V or OUTPUT_RANGE_10V (default)
        """
        if mode == self.OUTPUT_RANGE_5V:
            self.voltage = 5000
        elif mode == self.OUTPUT_RANGE_10V:
            self.voltage = 10000
        self.i2c.write_word_data(self._addr, self.output_setrange, mode)

    def set_DAC_out_voltage(self, data, channel):
        """Select DAC output channel & range

        Keyword arguments:
        data - Set output data
        channel - Set output channel
        """
        self.data_transmission = (float(data) / self.voltage) * 4095
        self.data_transmission = int(self.data_transmission) << 4
        self._send_data(self.data_transmission, channel)

    def store(self):
        """
        Save the present current config, 
        after the config is saved successfully,
        it will be enabled when the module is powered
        down and restarts
        """
        self._start_signal()
        self._send_byte(self.GP8302_STORE_TIMING_HEAD, 0, 3, False)
        self._stop_signal()
        self._start_signal()
        self._send_byte(self.GP8302_STORE_TIMING_ADDR)
        self._send_byte(self.GP8302_STORE_TIMING_CMD1)
        self._stop_signal()

        self._start_signal()
        self._send_byte(self._addr << 1, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._stop_signal()

        time.sleep(self.GP8302_STORE_TIMING_DELAY)

        self._start_signal()
        self._send_byte(self.GP8302_STORE_TIMING_HEAD, 0, 3, False)
        self._stop_signal()
        self._start_signal()
        self._send_byte(self.GP8302_STORE_TIMING_ADDR)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2)
        self._stop_signal()

    def output_sin(self, amp, freq, offset, channel):
        """Set the sensor outputs sine wave

        Keyword arguments:
        amp - Set sine wave amplitude Vp
        freq - Set sine wave frequency f
        offset -  Set sine wave DC offset Voffset
        channel - Output channel CHANNEL0, CHANNEL1, CHANNELALL
        """
        if freq < 6:
            num = 256
        elif 6 <= freq and freq <= 10:
            num = 128
        elif 10 < freq and freq < 22:
            num = 64
        elif 22 <= freq and freq <= 42:
            num = 32
        else:
            num = 32
        if freq > 42:
            freq = 42
        frame = int(1000000/(freq*(num+1)))
        for i in range(0, num-1):
            start = datetime.datetime.now()
            if num == 256:
                data = (FullSine8Bit[i] - 2047) * (amp/float(self.voltage)) * 2
            elif num == 128:
                data = (FullSine7Bit[i] - 2047) * (amp/float(self.voltage)) * 2
            elif num == 64:
                data = (FullSine6Bit[i] - 2047) * (amp/float(self.voltage)) * 2
            elif num == 32:
                data = (FullSine5Bit[i] - 2047) * (amp/float(self.voltage)) * 2
            else:
                data = (FullSine5Bit[i] - 2047) * (amp/float(self.voltage)) * 2
            data = int(data + offset*(4096/float(self.voltage)))
            if data <= 0:
                data = 0
            if data >= 4095:
                data = 4095
            data = data << 4
            self._send_data(data, channel)
            endtime = datetime.datetime.now()
            looptime = (endtime - start).microseconds
            while looptime <= frame:
                endtime = datetime.datetime.now()
                looptime = (endtime - start).microseconds

    def output_triangle(self, amp, freq, offset, duty_cycle, channel):
        """Call the function to output triangle wave

        Keyword arguments:
        amp - Set triangle wave amplitude Vp
        freq - Set triangle wave frequency f
        offset - Set triangle wave DC offset Voffset
        duty_cycle - Set triangle (sawtooth) wave duty cycle
        channel - Output channel CHANNEL0, CHANNEL1, CHANNELALL
        """
        max_v = int(amp*(4096/float(self.voltage)))
        if freq > 20:
            num = 16
        elif freq >= 11 and freq <= 20:
            num = 32
        else:
            num = 64
        frame = 1000000/(freq*num*2)
        if duty_cycle > 100:
            duty_cycle = 100
        if duty_cycle < 0:
            duty_cycle = 0
        up_num = (2*num)*(float(duty_cycle)/100)
        down_num = (2*num) - up_num
        if up_num == 0:
            up_num = 1
        for i in range(0, (max_v-int(max_v/up_num)-1), int(max_v/up_num)):
            starttime = datetime.datetime.now()
            enter_v = i + int(offset*(4096/float(self.voltage)))
            if enter_v > 4095:
                enter_v = 4095
            elif enter_v < 0:
                enter_v = 0
            enter_v = enter_v << 4
            self._send_data(enter_v, channel)
            endtime = datetime.datetime.now()
            looptime = (endtime - starttime).microseconds
            while looptime <= frame:
                endtime = datetime.datetime.now()
                looptime = (endtime - starttime).microseconds

        for i in range(0, int(down_num)):
            starttime = datetime.datetime.now()
            enter_v = max_v-1-(i*int(max_v/down_num)) + \
                int(offset*(4096/float(self.voltage)))
            if enter_v > 4095:
                enter_v = 4095
            elif enter_v < 0:
                enter_v = 0
            enter_v = enter_v << 4
            self._send_data(enter_v, channel)
            endtime = datetime.datetime.now()
            looptime = (endtime - starttime).microseconds
            while looptime <= frame:
                endtime = datetime.datetime.now()
                looptime = (endtime - starttime).microseconds

    def output_square(self, amp, freq, offset, duty_cycle, channel):
        """Call the function to output square wave

        Keyword arguments:
        amp - Set square wave amplitude Vp
        freq - Set square wave frequency f
        offset - Set square wave DC offset Voffset
        duty_cycle - Set square wave duty cycle
        channel - Output channel CHANNEL0, CHANNEL1, CHANNELALL
        """
        max_v = int(amp*(4096/float(self.voltage)))
        if freq > 20:
            num = 16
        elif freq >= 11 and freq <= 20:
            num = 32
        else:
            num = 64
        frame = 1000000/(freq*num*2)
        if duty_cycle > 100:
            duty_cycle = 100
        if duty_cycle < 0:
            duty_cycle = 0
        up_num = (2*num)*(float(duty_cycle)/100)
        down_num = (2*num) - up_num
        if up_num == 0:
            up_num = 1
        for _ in range(int(up_num)):
            starttime = datetime.datetime.now()
            enter_v = int(max_v + offset*(4096/float(self.voltage)))
            if enter_v > 4095:
                enter_v = 4095
            elif enter_v < 0:
                enter_v = 0
            enter_v = enter_v << 4
            self._send_data(enter_v, channel)
            endtime = datetime.datetime.now()
            looptime = (endtime - starttime).microseconds
            while looptime <= frame:
                endtime = datetime.datetime.now()
                looptime = (endtime - starttime).microseconds
        for _ in range(int(down_num)):
            starttime = datetime.datetime.now()
            enter_v = int(max_v - offset*(4096/float(self.voltage)))
            if enter_v > 4095:
                enter_v = 4095
            elif enter_v < 0:
                enter_v = 0
            self._send_data(enter_v, channel)
            endtime = datetime.datetime.now()
            looptime = (endtime - starttime).microseconds
            while looptime <= frame:
                endtime = datetime.datetime.now()
                looptime = (endtime - starttime).microseconds

    def _send_data(self, data, channel):
        if channel == 0:
            self.i2c.write_word_data(
                self._addr, self.GP8403_CONFIG_CURRENT_REG, data)

        elif channel == 1:
            self.i2c.write_word_data(
                self._addr, self.GP8403_CONFIG_CURRENT_REG << 1, data)
        else:
            self.i2c.write_word_data(
                self._addr, self.GP8403_CONFIG_CURRENT_REG, data)
            self.i2c.write_word_data(
                self._addr, self.GP8403_CONFIG_CURRENT_REG << 1, data)

    def _start_signal(self):
        GPIO.output(self._scl, GPIO.HIGH)
        GPIO.output(self._sda, GPIO.HIGH)
        time.sleep(self.I2C_CYCLE_BEFORE)
        GPIO.output(self._sda, GPIO.LOW)
        time.sleep(self.I2C_CYCLE_AFTER)
        GPIO.output(self._scl, GPIO.LOW)
        time.sleep(self.I2C_CYCLE_TOTAL)

    def _stop_signal(self):
        GPIO.output(self._sda, GPIO.LOW)
        time.sleep(self.I2C_CYCLE_BEFORE)
        GPIO.output(self._scl, GPIO.HIGH)
        time.sleep(self.I2C_CYCLE_TOTAL)
        GPIO.output(self._sda, GPIO.HIGH)
        time.sleep(self.I2C_CYCLE_TOTAL)

    def _recv_ack(self, ack=0):
        ack_ = 0
        error_time = 0
        GPIO.setup(self._sda, GPIO.IN)
        time.sleep(self.I2C_CYCLE_BEFORE)
        GPIO.output(self._scl, GPIO.HIGH)
        time.sleep(self.I2C_CYCLE_AFTER)
        while GPIO.input(self._sda) != ack:
            time.sleep(0.000001)
            error_time += 1
            if error_time > 250:
                break
        ack_ = GPIO.input(self._sda)
        time.sleep(self.I2C_CYCLE_BEFORE)
        GPIO.output(self._scl, GPIO.LOW)
        time.sleep(self.I2C_CYCLE_AFTER)
        GPIO.setup(self._sda, GPIO.OUT)
        return ack_

    def _send_byte(self, data, ack=0, bits=8, flag=True):
        i = bits
        data = data & 0xFF
        while i > 0:
            i -= 1
            if data & (1 << i):
                GPIO.output(self._sda, GPIO.HIGH)
            else:
                GPIO.output(self._sda, GPIO.LOW)
            time.sleep(self.I2C_CYCLE_BEFORE)
            GPIO.output(self._scl, GPIO.HIGH)
            time.sleep(self.I2C_CYCLE_TOTAL)
            GPIO.output(self._scl, GPIO.LOW)
            time.sleep(self.I2C_CYCLE_AFTER)
        if flag:
            return self._recv_ack(ack)
        else:
            GPIO.output(self._sda, GPIO.LOW)
            GPIO.output(self._scl, GPIO.HIGH)
        return ack
