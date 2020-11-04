##
# \file     weather/config.py
# \brief    read configuration data
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
import sys
import os

class Config:
    _filename='weather.conf'
    def __init__(self):
        self._host=''
        self._user=''
        self._passwd=''
        self._load()

    def _load(self):
        file=open(self._filename,'r')
        #line=' '
        try:
            while True:#line!='':
                line=file.readline()
                #print(line)
                if line=='':
                    break
                if line=='\n' or line[0]=='#':
                    continue
                d=line.find('=')
                if d<0:
                    raise SyntaxError("missing '='")
                key=line[0:d].strip()
                val=line[d+1:].strip()
                if key=='host':
                    self._host=val
                elif key=='user':
                    self._user=val
                elif key=='passwd':
                    self._passwd=val
                else:
                    raise SyntaxError('invalid keyword: '+key)
        except Exception as e:
            file.close()
            raise e
        file.close()

    def host(self):
        return self._host
    def user(self):
        return self._user
    def passwd(self):
        return self._passwd
    

#config=Config()
#print(config.host())
#print(config.user())
#print(config.passwd())
