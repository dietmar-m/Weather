##
# \file     weather/ruler.py
# \brief    ruler for the weather window
# \author   Dietmar Muscholik <d.muscholik@t-online.de>
# \date     2018-02-14
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
#import logging
from weather import *
from graph import *

class Ruler(tkinter.Canvas):
    _height=20
    _month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    _font=('Ariel',8)

    #def __init__(self,master,weather,width):
    def __init__(self,master,weather):
        self._weather=weather
        self._width=Weather.YEAR_DAYS
        tkinter.Canvas.__init__(self,master,
                                width=self._width,
                                height=Ruler._height,
                                bg='white',bd=0)
        self.bind('<Configure>',self._configure)

    def draw(self):
        if self._weather.year():
            self.delete(tkinter.ALL)
            #scale=self._width/Weather.YEAR_DAYS
            scale=(self._width-Graph.RULER_WIDTH)/Weather.YEAR_DAYS
            seconds=24*60*60
            t=time.mktime((self._weather.year(),1,1,0,0,0,0,0,0))
            #self.create_line(0,1,self._width,1)
            for day in range(0,Weather.YEAR_DAYS-1):
                tm=time.localtime(t)
                if tm[2]==1:
                    x=Graph.RULER_WIDTH+day*scale
                    self.create_line(x,0,x,self._height/2,fill='gray')
                    self.create_text(x+self._width/len(self._month)/2,
                                     self._height/2,
                                     text=self._month[tm[1]-1],
                                     font=Ruler._font)
                t+=seconds

    def _configure(self,e):
#        logging.debug('')
        self._width=e.width
        self.draw()
