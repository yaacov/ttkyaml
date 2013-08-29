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

import os
import sys

from Tkinter import *
import yaml

from tcp_modbus import TcpModbus
from ttkyaml.ttkyaml import TtkYaml

# base dir when using pyinstaller is different
if getattr(sys, 'frozen', None):
    basedir = sys._MEIPASS
    confpath = os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    basedir = os.path.dirname(os.path.realpath(__file__))
    confpath = basedir

# set a new ttk window and load gui
class PqSet(TtkYaml):
    ''' read and write input registers from a pq unit
    '''
        
    def __init__(self):
        TtkYaml.__init__(self)
        
        # file names
        self.conf_filename = os.path.join(confpath, 'pq_set.conf')
        self.gui_filename = os.path.join(basedir, 'pq_set.yaml')
        
        # load configure file
        self.load_conf()
        
        # load gui
        self.load_gui(self.gui_filename)
        
        # extra gui settings
        self.mainframe.columnconfigure(2, weight=1, minsize=30)
        
        # reset the icon, in case we are using pyinstaller
        # and the icon file in not in current path
        frame = self.gui['frame']
        if 'ico' in frame.keys():
            full_icon_path = os.path.join(basedir, frame['ico'])
            self.root.iconbitmap(full_icon_path)
            
        # init the ip entry and the reload button
        inputs = self.inputs
        inputs[20001]['var'].set(self.ip)
        inputs[20002]['button']['command'] = self.update_ip
        
        # read registers from unit
        self.com = TcpModbus(self.ip)
        self.get_reg()
    
    def load_conf(self):
        ''' load configuration file
        '''
        
        # load configure file
        try:
            f = open(self.conf_filename)
            self.conf = yaml.safe_load(f)
            f.close()
        except:
            self.conf = {'ip': '127.0.0.1'}
        
        self.ip = self.conf['ip']
    
    def save_conf(self):
        ''' save configuration file
        '''
        
        # save configure file
        try:
            f = open(self.conf_filename, 'wb')
            yaml.dump(self.conf, f, default_flow_style=False)
            f.close()
        except:
            pass
    
    def update_ip(self):
        ''' update the ip, using user entry
        '''
        
        inputs = self.inputs
        self.ip = inputs[20001]['var'].get()
        self.conf['ip'] = self.ip
        
        # save new ip
        self.save_conf()
        
        # try to reload registers
        self.set_ip()
        
    def set_ip(self, ip = None):
        ''' change the ip
        '''
        
        # set the ip
        try:
            self.com.set_ip(self.ip)
            self.get_reg()
        except:
            pass

    def input_changed(self, *args):
        ''' called when an input has changed
        
        in our case, we send all the data to the unit
        '''
        com = self.com
        buttons = self.inputs
        
        # for each gui var, get value and send it to unit
        for reg, button in buttons.items():
            if 'reg' in button.keys():
                val = float(button['var'].get())
                try:
                    com.write_registers(31, reg * 2 - 2, val)
                except:
                    self.set_ip(self.ip)
                
    def get_reg(self):
        ''' call unit and ask for en registers
        '''
        com = self.com
        inputs = self.inputs
        
        # read unit info
        try:
            en_reg = com.read_registers(31, 187, 2)
            inputs[20187]['var'].set('%0.2f' % en_reg[0])
        except:
            inputs[20187]['var'].set('')
        
        # read registers from unit
        try:
            en_reg = com.read_registers(31, 6001 * 2 - 2, 20 * 2)
        except:
            en_reg = ['',] * 20
        
        # set the gui vars
        for i, val in enumerate(en_reg):
            reg = i + 6001
            if reg in inputs.keys():
                inputs[reg]['var'].set(val)

def main():
    pq_set = PqSet()
    
    # run gui
    pq_set.run_gui()
                    
if __name__ == '__main__':
    main()
