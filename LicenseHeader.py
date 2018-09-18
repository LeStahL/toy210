#!/usr/bin/env python3
#
# toy210 - the team210 live shader editor
#
# Copyright (C) 2017/2018 Alexander Kraus <nr4@z10.info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

class LicenseHeader:
    def __init__(self):
        # Demo settings
        self.demoname = ""
        self.grouphandle = ""
        self.authorhandle = ""
        self.compo = "64k Intro"
        self.party = ""
        self.license = "GPLv3"
        
        # Author settings
        self.author = ""
        self.email = ""
        self.year = ""
        
    def toString(self):
        header = "/* "
        if self.demoname == "":
            print("Warning: No demo name present.")
        header += self.demoname + " by "
        if self.authorhandle == "":
            print("Warning: No author handle present.")
        header += self.authorhandle + "/"
        if self.grouphandle == "":
            print("Warning: No group handle present.")
        header += self.grouphandle + " - " + self.compo + " at "
        if self.party == "":
            print("Warning: No party present.")
        header += self.party + "\n"
        
        header += " * Copyright (C) " + self.year + " " + self.author + " <" + self.email + ">\n"
        
        self.header += " * \n"
        self.header += ''' * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */'''
 
        return header
    
    def fromString(self, string):
        lines = string.split('\n')
        data = lines[0].split(" by ")
        self.demoname = data[0]
        data = data[1].split("/")
        self.authorhandle = data[0]
        data = data[1].split(" - ")
        self.grouphandle = data[0]
        data = data[1].split(" at ")
        self.compo = data[0]
        data = data[1].split(' ')
        self.party = ' '.join(data[:-2])
        self.year = data[-1]
        
