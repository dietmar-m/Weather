##
# \file     weather/graph.py
# \brief    actualy draws the graph for the weather data
# \author   Dietmar Muscholik <d.muscholik@t-online.de>
# \date     2018-01-24
#           started
#
# \date     2018-02-14
#           completely rewritten
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

class Graph(tkinter.Canvas):
    RULER_WIDTH=30
    _ruler_font=('Ariel',8)
    _title_font=('Ariel',10)
    
    def __init__(self,master,weather,plot,title):
        self._master=master
        self._weather=weather
        self._plot=plot
        self._title=title
        (self._y_min,self._y_max)=Weather.minmax(plot[0][0])
        self._width=Graph.RULER_WIDTH+Weather.YEAR_DAYS
        self._height=self._y_max-self._y_min
        self._day=None
        self._ruler_step=25
        if self._height<100:
            self._ruler_step=10
            if self._height<50:
                self._height*=3
            else:
                self._height*=2
        tkinter.Canvas.__init__(self,master,
                                width=self._width,height=self._height,
                                bg='white',bd=0)
        self.bind('<Configure>',self._configure)
        #self.bind('<Button-1>',self._string)
        self.bind('<Motion>',self._string)

    def draw(self):
        self.delete(tkinter.ALL)
        self.create_text(self._width/2,8,text=self._title,font=Graph._title_font)
        self._ruler()
        if self._weather.year():
            dx=self._xscale()
            dy=self._yscale()
            for (index,color) in self._plot:
                x0=None
                y0=None
                for day in range(0,Weather.YEAR_DAYS-1):
                    w=self._weather.weather(day)
                    if w:
                        if x0:
                            x1=Graph.RULER_WIDTH+day*dx
                            y1=(self._y_max-w[index])*dy
                            self.create_line(x0,y0,x1,y1,fill=color)
                            x0=x1
                            y0=y1
                        else:
                            x0=Graph.RULER_WIDTH+day*dx
                            y0=(self._y_max-w[index])*dy

    def _ruler(self):
        self.create_line(Graph.RULER_WIDTH,0,Graph.RULER_WIDTH,self._height,fill='gray')
        dx=3
        dy=self._yscale()
        step=5
        for y in range(self._y_min+step,self._y_max,step):
            if y%self._ruler_step==0:
                self.create_text(Graph.RULER_WIDTH/2,(self._y_max-y)*dy,
                                 text=str(y),font=Graph._ruler_font)
                self.create_line(Graph.RULER_WIDTH-1.5*dx,(self._y_max-y)*dy,
                                 Graph.RULER_WIDTH,(self._y_max-y)*dy,fill='gray')
            else:
                self.create_line(Graph.RULER_WIDTH-dx,(self._y_max-y)*dy,
                                 Graph.RULER_WIDTH,(self._y_max-y)*dy,fill='gray')
        if self._y_min < 0:
            y=self._y_max*self._height/(self._y_max-self._y_min)
            self.create_line(Graph.RULER_WIDTH,y,self._width,y,fill='gray')
        
    def _xscale(self):
        return (self._width-Graph.RULER_WIDTH)/Weather.YEAR_DAYS

    def _yscale(self):
        return self._height/(self._y_max-self._y_min)
    
    def _configure(self,e):
#        logging.debug('')
        #print('Graph: width='+str(e.width)+', height='+str(e.height))
        self._width=e.width
        self._height=e.height
        self.draw()
        
    def _string(self,e):
        #day=int(e.x/self._xscale())+1
        day=int((e.x-Graph.RULER_WIDTH)/self._xscale())+1
        if day != self._day:
            str=self._weather.string(day)
            if str!="":
                self._master.message(str)
            self._day=day
        
