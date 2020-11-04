#!/usr/bin/python3
##
# \file     weather/fetch.py
# \brief    Fetch weather data from https://www.wdr.de
#           intended to be run from crom at least once a day
# \author   Dietmar Muscholik <d.muscholik@t-online.de>
# \date     2018-01-24
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

import os
import re
import http.client
import time
import sys


host='www1.wdr.de'
url='/wetter/wettervorhersage/'+\
'wetter_nrw_ea100~_eam-14cbe18ee4a93b404a6a4cdad12db0e3.jsp'+\
'?_query=hilden'+\
'&_type=QUERY'+\
'&_utf8=%E2%9C%93'+\
'&eap=8oI34N4hym4RDV6dhKK0OoKFhY2OtqKgKJopQeJuwvRP7LdGW7EVznDA5679U78Uhu1kc0YQZJ%2F3ln%2FJTf21ttmzjD2bFhCr4f0e9MsF53kepVCdT14U40ApDlOO8A7S%2BcXeQUgz8Ow%3D'

path=os.getenv('HOME')

re_t=re.compile('-?[0-9]+<abbr title="Grad Celsius">')
re_r=re.compile('.+<abbr title="Liter pro Quadratmeter pro Tag">')
re_s=re.compile('[0-9]+<abbr title="Kilometer pro Stunde">')
re_d=re.compile('.+headers="wind forecast-0"><.+?>')

re_c1=re.compile('</td><td class="forecast-0" headers="am forecast-0"><span class="hidden">')
re_c2=re.compile('</td><td class="forecast-0" headers="pm forecast-0"><span class="hidden">')
re_c3=re.compile('</td><td class="forecast-0" headers="evening forecast-0"><span class="hidden">')
re_c4=re.compile('</td><td class="forecast-0" headers="night forecast-0"><span class="hidden">')

try:
    conn=http.client.HTTPSConnection(host)
    conn.request('GET',url)
    resp=conn.getresponse()
    if resp.status==200:
        tm=time.localtime()
        filename=path+'/weather-'+str(tm[0])
        try:
            file=open(filename,'a')
            c_t=0
            c_r=0
            c_s=0
            body=resp.readlines()
            try:
                for line in body:
                    line=line.decode()
                    m_t=re_t.match(line)
                    m_r=re_r.match(line)
                    m_s=re_s.match(line)
                    m_d=re_d.match(line)

                    m_c1=re_c1.match(line)
                    m_c2=re_c2.match(line)
                    m_c3=re_c3.match(line)
                    m_c4=re_c4.match(line)
                    #print(line)
                    if m_t:
                        if c_t==0:
                            t_max=int(m_t.string[0:m_t.string.find('<')])
                        elif c_t==4:
                            t_min=int(m_t.string[0:m_t.string.find('<')])
                        c_t+=1
                    elif m_r:
                        if c_r==0:
                            rain=float(m_r.string[0:m_r.string.find('<')].\
                                       replace(',','.'))
                        c_r+=1
                    elif m_d:
                        w_dir=m_d.string[m_d.end():]
                        w_dir=w_dir[0:w_dir.find('<')]
                    elif m_s:
                        if c_s==0:
                            w_speed=int(m_s.string[0:m_s.string.find('<')])
                        elif c_s==4:
                            w_blast=int(m_s.string[0:m_s.string.find('<')])
                        c_s+=1
                    elif m_c1:
                        cond1=m_c1.string[m_c1.end():]
                        cond1=cond1[0:cond1.find('<')]
                        #print(cond1)
                    elif m_c2:
                        cond2=m_c2.string[m_c2.end():]
                        cond2=cond2[0:cond2.find('<')]
                        #print(cond2)
                    elif m_c3:
                        cond3=m_c3.string[m_c3.end():]
                        cond3=cond3[0:cond3.find('<')]
                        #print(cond3)
                    elif m_c4:
                        cond4=m_c4.string[m_c4.end():]
                        cond4=cond4[0:cond4.find('<')]
                        #print(cond4)

                s=('date={:04d}-{:02d}-{:02d}, '+
                   't_min={}, t_max={}, rain={}, '+
                   'w_dir={}, w_speed={}, w_blast={}, '+
                   'cond1={}, cond2={}, cond3={}, cond4={}\n').format(
                       tm.tm_year,tm.tm_mon,tm.tm_mday,
                       t_min,t_max,rain,
                       w_dir,w_speed,w_blast,
                       cond1,cond2,cond3,cond4)
                #print(s)
                file.write(s)
            except Exception as e:
                print(e,file=sys.stderr)
            #print('close file')
            file.close()
        except Exception as e:
            print(e,file=sys.stderr)
    #print('close connection')
    conn.close()
except Exception as e:
    print(e,file=sys.stderr)
#print('done')
