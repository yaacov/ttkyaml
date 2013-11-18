#!/usr/bin/env python
# -*- coding:utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Copyright (C) 2013 Yaacov Zamir <kobi.zamir@gmail.com>
# Author: Yaacov Zamir (2013)

import socket
from struct import pack, unpack

class TcpModbus():
    ''' a class to read and write input registers as floats
        
        floats are two registers ">f"
    '''
    
    def __init__(self, tcp_ip):
        # defults modbus port
        self.tcp_port = 502
        
        # open socket
        self.set_ip(tcp_ip)
    
    def set_ip(self, tcp_ip):
        ''' set new ip
        '''
        
        try:
            self.soc.close()
        except:
            pass
        
        try:
            # open socket
            self.ip = tcp_ip
            self.open()
        except:
            pass
        
    def open(self):
        ''' close socket
        '''
        
        # open socket
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.settimeout(2)
            self.soc.connect((self.ip, self.tcp_port))
        except socket.error:
            raise Exception("Can't connect to unit")
        
    def close(self):
        ''' close socket
        '''
        
        self.soc.close()
        
    def write_registers(self, unit, addr, value):
        ''' write input registers to a modbus unit
        '''
        command = 0x10
        soc = self.soc
        count = 1
        value_array = [value, ]
        
        # sent one float, use two registers
        message = pack(">3H2B2HB%df" % count, 1, 0, 7 + 4 * count, 
            unit, command, addr, 2 * count, 4 * count, *value_array)
        soc.send(message)
        replay = soc.recv(1024)

        # parse response: adress and count
        try:
            data = unpack('>2H', replay[8:])
        except Exception, e:
            raise Exception("No responce from unit")
        
        return

    def read_registers(self, unit, addr, count):
        ''' read input registers from modbus unit
        '''
        command = 0x04
        soc = self.soc
        
        # get registers from unit as floats
        message = pack(">3H2B2H", 1, 0, 6, unit, command, addr, count)
        soc.send(message)
        replay = soc.recv(1024)

        # parse response as list of floats
        try:
            data = unpack(">%df" % (count / 2), replay[9:])
        except Exception, e:
            raise Exception("No responce from unit")
        
        return data
     
