#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ttk_yaml import TtkYaml

class ImpToMeter(TtkYaml):
    ''' the ttk feet to meter example using ttkyaml
        original example from:
            http://www.tkdocs.com/tutorial/firstexample.html
    '''
    def __init__(self):
        TtkYaml.__init__(self)
        
        # create the gui dict
        gui_dict = {
            'frame':{
                'title': 'Feet to Meters',
            },
            'inputs':{
                0:{'type': 'label',  'c': 0, 'r': 0, 'text': 'Convertor', 'foreground': 'blue'},
                1:{'type': 'entry',  'c': 0, 'r': 1, 'text': 'feet'},
                2:{'type': 'entry',  'c': 0, 'r': 2, 'text': 'meters', 'state': 'DISABLED'},
                3:{'type': 'button', 'c': 2, 'r': 3, 'text': 'Calculate'},
            },
        }
        
        # load the gui
        self.load_gui(gui_dict)
        
        # bind the calculate button
        calc_button = self.inputs[3]['button']
        calc_button['command'] = self.calculate
        
        # set fucus to the feet entry box
        feet_entry = self.inputs[1]['entry']
        feet_entry.focus()
        
        # bind the root window
        self.root.bind('<Return>', self.calculate)
        
    def calculate(self, *args):
        ''' calculate meters
        '''
        # get the vars from the gui dict
        feet = self.inputs[1]['var']
        meter = self.inputs[2]['var']
        
        # calculate meters
        try:
            value = float(feet.get())
            meter.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            meter.set('')

converter = ImpToMeter()
converter.run_gui()
