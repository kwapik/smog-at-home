#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime
import logging
import serial
import struct
import sys



class SensorConnector(object):

    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        logging.info('Initializing SensorConnector' +
            '(port={}, baudrate={})'.format(port, baudrate))
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.open()
        self.ser.flushInput()
        logging.info('Initialized SensorConnector')

    def get_value(self):
        byte, last_byte = "\x00", "\x00"
        while True:
            lastbyte = byte
            byte = self.ser.read(size=1)

            # We got a valid packet header
            if lastbyte == "\xAA" and byte == "\xC0":
                sentence = self.ser.read(size=8)  # Read 8 more bytes
                # Decode the packet - big endian, 2 shorts for pm2.5 and pm10,
                # 2 reserved bytes, checksum, message tail
                readings = struct.unpack('<HHxxBB', sentence)

                result = {
                    'PM 2.5': readings[0]/10.0,
                    'PM 10': readings[1]/10.0
                }
                # ignoring the checksum and message tail

                logging.info('Returning {}'.format(result))
                return result
