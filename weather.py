##
# \file     weather/weather.py
# \brief    class for weather data
# \author   Dietmar Muscholik <d.muscholik@t-online.de>
#
# \date     2018-02-05
#           started
#
# \date     2018-03-13
#           weather condition added
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
import sys
#import os
import time

class Weather:
    DATE=0
    T_MIN=1
    T_MAX=2
    RAIN=3
    DIR=4
    WIND=5
    BLAST=6
    COND1=7
    COND2=8
    COND3=9
    COND4=10
    YEAR_DAYS=366
    
    _min_temp=-15
    _max_temp=40
    _max_rain=50
    _max_wind=120
    _months=['Jan','Feb','Mar','Apr','May','Jun',
             'Jul','Aug','Sep','Oct','Nov','Dec']
    _dirs={'N':'north','NO':'northeast','O':'east','SO':'southeast',
           'S':'south','SW':'southwest','W':'west','NW':'northwest'}
    _templ="""{day:02d}.{month}.{year:04d}: \
temp: {t_min}°C - {t_max}°C, \
rain: {rain}l/m², \
wind: {wind}km/h from {dir}, \
blasts: {blast}km/h, \
cond: {cond1}, {cond2}, {cond3}, {cond4}"""
    
    def __init__(self):
        self._weather=list()
        for i in range(Weather.YEAR_DAYS):
            self._weather.append(None)
        self._year=None

    def load(self,filename=None,year=None):
        if filename==None:
            if year==None:
                year=time.localtime()[0]
            #filename=os.getenv('HOME')+'/weather-'+str(year)
            filename='weather-'+str(year)

        self.__init__()
        self._year=year

        file=open(filename,'r')
        data='\n'
        try:
            while data!='':
                data=file.readline()
                #print(data)
                if data!='':
                    pairs=data.split(',')
                    day=None
                    #weather=[None,None,None,None,None,None,None]
                    weather=[None,None,None,None,None,None,None,None,None,None,None]
                    for pair in pairs:
                        words=pair.strip().split('=')
                        #print(words)
                        if words[0]=='date':
                            date=words[1].split('-')
                            weather[Weather.DATE]=(int(date[0]),
                                                     int(date[1]),
                                                     int(date[2]))
                            #print(date)
                            day=time.localtime(time.mktime(
                                (weather[Weather.DATE][0],
                                 weather[Weather.DATE][1],
                                 weather[Weather.DATE][2],
                                 0,0,0,0,0,0)))[7]
                            if not self._year:
                                self._year=int(date[0])
                        elif words[0]=='t_min':
                            weather[Weather.T_MIN]=int(words[1])
                        elif words[0]=='t_max':
                            weather[Weather.T_MAX]=int(words[1])
                        elif words[0]=='rain':
                            weather[Weather.RAIN]=float(words[1])
                        elif words[0]=='w_dir':
                            weather[Weather.DIR]=words[1]
                        elif words[0]=='w_speed':
                            weather[Weather.WIND]=int(words[1])
                        elif words[0]=='w_blast':
                            weather[Weather.BLAST]=int(words[1])
                        elif words[0]=='cond1':
                            weather[Weather.COND1]=words[1]
                        elif words[0]=='cond2':
                            weather[Weather.COND2]=words[1]
                        elif words[0]=='cond3':
                            weather[Weather.COND3]=words[1]
                        elif words[0]=='cond4':
                            weather[Weather.COND4]=words[1]
                    if day!=None:
                        self._weather[day-1]=weather
        except Exception as e:
            file.close()
            raise e
        file.close()
        print("Year:",self._year)
        print("Min temp:",self.min_temp())
        print("Max temp:",self.max_temp())
        print("Avg temp:",self.avg_temp())
        print("Min rain:",self.min_rain())
        print("Max rain:",self.max_rain())
        print("Avg rain:",self.avg_rain())
        print("Min wind:",self.min_wind())
        print("Max wind:",self.max_wind())
        print("Avg wind:",self.avg_wind())
        
    def weather(self,day):
        if day<1 or day>=len(self._weather):
            return None
        return self._weather[day-1]

    def year(self):
        return self._year

    def string(self,day):
        if day<1 or day>=len(self._weather):
            return ""
        weather=self._weather[day-1]
        if weather:
            str=Weather._templ.format(day=weather[Weather.DATE][2],
                                      month=self._months[weather[Weather.DATE][1]-1],
                                      year=weather[Weather.DATE][0],
                                      t_min=weather[Weather.T_MIN],
                                      t_max=weather[Weather.T_MAX],
                                      rain=weather[Weather.RAIN],
                                      wind=weather[Weather.WIND],
                                      dir=Weather._dirs[weather[Weather.DIR]],
                                      blast=weather[Weather.BLAST],
                                      cond1=weather[Weather.COND1],
                                      cond2=weather[Weather.COND2],
                                      cond3=weather[Weather.COND3],
                                      cond4=weather[Weather.COND4])
            return str
        else:
            return ""
        
    def min(self,day):
        if day<1 or day>=len(self._weather):
            return None
        return self._weather[day-1][Weather.T_MIN]

    def max(self,day):
        if day<1 or day>=len(self._weather):
            return None
        return self._weather[day-1][Weather.T_MAX]

    def rain(self,day):
        if day<1 or day>=len(self._weather):
            return None
        return self._weather[day-1][Weather.RAIN]

    def dir(self,day):
        if day<1 or day>=len(self._weather):
            return None
        return self._weather[day-1][Weather.DIR]

    def speed(self,day):
        if day<1 or day>=len(self._weather):
            return None
        return self._weather[day-1][Weather.WIND]

    def blast(self,day):
        if day<1 or day>=len(self._weather):
            return None
        return self._weather[day-1][Weather.BLAST]

    def minmax(index):
        if index==Weather.T_MIN or index==Weather.T_MAX:
            return (Weather._min_temp,Weather._max_temp)
        elif index==Weather.RAIN:
            return (0,Weather._max_rain)
        elif index==Weather.WIND or index==Weather.BLAST:
            return (0,Weather._max_wind)
        else:
            return (0,0)

    def min_temp(self):
        return self._min(Weather.T_MIN)

    def max_temp(self):
        return self._max(Weather.T_MAX)

    def avg_temp(self):
        return self._avg(Weather.T_MAX)-self._avg(Weather.T_MIN)

    def min_rain(self):
        return self._min(Weather.RAIN)

    def max_rain(self):
        return self._max(Weather.RAIN)

    def avg_rain(self):
        return self._avg(Weather.RAIN)

    def min_wind(self):
        return self._min(Weather.WIND)

    def max_wind(self):
        return self._max(Weather.BLAST)

    def avg_wind(self):
        return self._avg(Weather.WIND)

    def _min(self,index):
        min=None
        for n in range(Weather.YEAR_DAYS):
            w=self._weather[n]
            if w and (min==None or min>w[index]):
                min=w[index]
        return min

    def _max(self,index):
        max=None
        for n in range(Weather.YEAR_DAYS):
            w=self._weather[n]
            if w and (max==None or max<w[index]):
                max=w[index]
        return max

    def _avg(self,index):
        sum=0
        count=0
        for n in range(Weather.YEAR_DAYS):
            w=self._weather[n]
            if w:
                sum+=w[index]
                count+=1
        return sum/count
