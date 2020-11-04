##
# \file     weather/toolbar.py
# \brief    toolbar for the weather window
# \author   Dietmar Muscholik <d.muscholik@t-online.de>
# \date     2018-01-30
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
#import sys

class Toolbar(tkinter.Frame):
    #def __init__(self,master,width):
    def __init__(self,master):
        tkinter.Frame.__init__(self,master=master,
                               #width=width,
                               relief=tkinter.RAISED,bd=2)
        self._master=master
        b=tkinter.Button(master=self,text='Load',command=self._load)
        b.pack(side=tkinter.LEFT,anchor=tkinter.W)
        b=tkinter.Button(master=self,text='Update',command=self._update)
        b.pack(side=tkinter.LEFT,anchor=tkinter.W)
        b=tkinter.Button(master=self,text='Quit',command=self._quit)
        b.pack(side=tkinter.RIGHT,anchor=tkinter.E)
        

    def _load(self):
        self._master.load()

    def _update(self):
        self._master.update()
    
    def _quit(self):
        self._master.quit()
