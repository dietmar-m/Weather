#!/usr/bin/python3
##
# \file     weather/window.py
# \brief    Top-level widget for weather-data visualisation
# \author   Dietmar Muscholik <d.muscholik@t-online.de>
# \date     2018-02-19
#           started
#
# \date     2020-11-03
#           added to version control
#
#    Copyright (C) 2018  Dietmar Muscholik
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
import tkinter
import ftplib
import re
import sys
#import logging
import os

from tkinter import filedialog
from tkinter import messagebox

from weather import *
from config import *

from graph import *
from ruler import *
from toolbar import *

class Window(tkinter.Tk):
    _file_pattern='weather-[0-9][0-9][0-9][0-9]'
    _font=('Ariel',8)
    
    #def __init__(self,width=3*Weather.year_days):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title('Weather')
        #self.wm_minsize(width=Weather.year_days+2,height=380)
        try:
            self._config=Config()
        except Exception as e:
            self.error(e)
        self._weather=Weather()
        self._resize=True
        
        self._temp=Graph(self,self._weather,
                         [(Weather.T_MAX,'red'),(Weather.T_MIN,'blue')],
                         'Temperature [°C]')
        #self._temp.pack(side=tkinter.TOP,fill=tkinter.X)
        self._temp.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=1)

        self._rain=Graph(self,self._weather,
                         [(Weather.RAIN,'blue')],
                         'Rain [l/m²]')
        #self._rain.pack(side=tkinter.TOP,fill=tkinter.X)
        self._rain.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=1)

        self._wind=Graph(self,self._weather,
                         [(Weather.WIND,'green'),(Weather.BLAST,'red')],
                         'Wind [km/h]')
        #self._wind.pack(side=tkinter.TOP,fill=tkinter.X)
        self._wind.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=1)

        self._ruler=Ruler(self,self._weather)
        self._ruler.pack(side=tkinter.TOP,fill=tkinter.X)

        self._msg=tkinter.Label(master=self,height=2,
                                font=Window._font,
                                justify=tkinter.LEFT)
        self._msg.pack(side=tkinter.TOP,fill=tkinter.X,anchor=tkinter.W)
        
        self._toolbar=Toolbar(self)
        self._toolbar.pack(side=tkinter.BOTTOM,fill=tkinter.BOTH)
        self.bind('<Configure>',self._configure)

    def update(self):
        try:
            conn=ftplib.FTP(self._config.host(),
                            self._config.user(),
                            self._config.passwd())
            names=conn.nlst()
            pat=re.compile(self._file_pattern)
            for name in names:
                if pat.match(name):
                    try:
                        file=open(name,'wb')
                        conn.retrbinary('RETR '+name,file.write)
                        file.close()
                    except Exception as e:
                        self.error('Error fetching file '+name,e)
            conn.quit()
        except Exception as e:
            self.error('Error connecting host '+self._config.host(),e)

    def load(self):
        file=filedialog.askopenfilename(
            filetypes=[('weather',self._file_pattern)])
        if type(file).__name__=='str' and file!='':
            try:
                self._weather.load(file)
                self.title('Weather '+str(self._weather.year()))
                self._temp.draw()
                self._rain.draw()
                self._wind.draw()
                self._ruler.draw()
            except Exception as e:
                self.error('Error reading file '+file,e)

    def quit(self):
        self.destroy()

    def error(self,message=None,error=None):
        #print(e,file=sys.stderr)
        if message:
            msg=message
        else:
            msg=''
        if error:
            if msg:
                msg+='\n'+str(error)
            else:
                msg=str(error)
        messagebox.showerror(title='Error',message=msg)
        
    def message(self,msg):
        #print(msg)
        self._msg.config(text=msg)
        
    def _configure(self,e):
        if e.widget==self and self._resize:
            #print('Window: width='+str(e.width)+', height='+str(e.height))
            self.wm_minsize(width=e.width,height=e.height)
            self._resize=False
        if e.widget==self._msg:
            self._msg.config(wraplength=e.width)

##logging.basicConfig(stream=sys.stderr,
##                    level=logging.DEBUG,
##                    format='%(asctime)s- %(funcName)s, %(lineno)d: %(message)s')
os.chdir(os.path.dirname(sys.argv[0]))
#print(os.getcwd())
w=Window()
w.mainloop()
