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

from Tkinter import *
import ttk

# try to load pyYaml
# if the module is missing, we can use a dict
# instead
try:
    import yaml
except:
    pass
    
class TtkYaml:
    ''' a class to build simple ttk frames with buttons
        using yaml gui files
    '''
    
    def __init__(self):
        self.root = Tk()
    
    def load_gui(self, data):
        ''' load a yaml file as the gui
        
        @param filename the file gui yaml name 
                        or the data dict
        '''
        
        # load gui file
        # if data is not a file name - use data as a gui dict
        if isinstance(data, str):
            f = open(data)
            self.gui = yaml.safe_load(f)
            f.close()
        else:
            self.gui = data
        
        # alias the gui inputs as self.inputs
        self.inputs = self.gui['inputs']
        
        # set the main frame and the inputs
        self.set_mainframe()
        self.set_inputs()
        
        # extra styling
        self.set_style()
    
    def run_gui(self):
        ''' start running the program
        '''
        
        self.root.mainloop()
        
    def input_changed(self, *args):
        ''' called when an input is changed,
            
            inherit and overload this function if you want to call
            somthing when an input has changed
        '''
        
        # default is to do nothing
        pass
    
    def set_style(self):
        ''' do extra styling
        '''
        
        parent = self.mainframe
        parent['padding'] = '5 5 5 5'
        for child in parent.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        
    def set_mainframe(self):
        ''' set a ttk main frame
        '''
        
        # get locale parameters
        root = self.root
        frame = self.gui['frame']
        
        # create main window
        if 'ico' in frame.keys():
            root.iconbitmap(default=frame['ico'])
        if 'title' in frame.keys():
            root.title(frame['title'])
        
        # set the main frame
        self.mainframe = ttk.Frame(root)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        
    def set_inputs(self):
        ''' set the ttk inputs and buttons
        '''
        
        # get locale parameters
        parent = self.mainframe
        inputs = self.inputs
        call_back = self.input_changed
        
        # create all the inputs / buttons
        # and position them in the frame
        # TODO: create a separate function call for the creation 
        #       of each widget
        for reg, button in inputs.items():
            # checkbox
            # --------
            if button['type'] == 'checkbox':
                # this input has a var
                var = StringVar()
                button['var'] = var
                
                # create the widget
                check = ttk.Checkbutton(parent, text=button['text'], 
                    variable=button['var'],
                    command=call_back,
                    onvalue='1.0', offvalue='0.0')
                button['checkbox'] = check
                check.grid(column=button['c'], row=button['r'], sticky=(W, E))
            
            # radiobox
            # --------
            elif button['type'] == 'radio':
                # this input has a var
                var = StringVar()
                button['var'] = var
                
                # create a label
                label = ttk.Label(parent, text=button['text'])
                label.grid(column=button['c'], row=button['r'], sticky=W)
                
                # create the widget                
                r1 = ttk.Radiobutton(parent, 
                    command=call_back, text=button['text1'], 
                    variable=button['var'], value=button['val1'])
                r2 = ttk.Radiobutton(parent, 
                    command=call_back, text=button['text2'], 
                    variable=button['var'], value=button['val2'])
                r1.grid(column=(button['c'] + 1), row=button['r'], sticky=(W, E))
                r2.grid(column=(button['c'] + 1), row=(button['r'] + 1), sticky=(W, E))
            
            # entry
            # -----
            elif button['type'] == 'entry':
                # this input has a var
                var = StringVar()
                button['var'] = var
                
                # create a lable
                label = ttk.Label(parent, text=button['text'])
                label.grid(column=button['c'], row=button['r'], sticky=W)
                
                # create the widget
                entry = ttk.Entry(parent, width=18,
                    textvariable=button['var'])
                button['entry'] = entry
                
                # check state
                if 'state' in button.keys(): 
                    if button['state'] == 'DISABLED':
                        entry['state'] = DISABLED
                    else:
                        entry['state'] = button['state']
                
                # bind change to call back function
                entry.bind('<Return>', call_back)
                
                entry.grid(column=(button['c'] + 1), row=button['r'], sticky=(W, E))
            
            # button
            # -----
            elif button['type'] == 'button':
                # create the widget
                mybutton = ttk.Button(parent, text=button['text'], command=call_back)
                button['button'] = mybutton
                
                # add to parent
                mybutton.grid(column=button['c'], row=button['r'], sticky=W)
            
            # label
            # -----
            elif button['type'] == 'label':
                # create the widget
                label = ttk.Label(parent, text=button['text'])
                button['label'] = label
                
                # set style
                if 'color' in button.keys():
                    style = ttk.Style()
                    style.configure('%s.TLabel' % button['color'], foreground=button['color'])
                    label.configure(style='%s.TLabel' % button['color'])
                
                # add to parent
                label.grid(column=button['c'], row=button['r'], sticky=W)
            else:
                pass
        