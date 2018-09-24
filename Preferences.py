#!/usr/bin/env python3
#
# toy210 - the team210 live shader editor
#
# Copyright (C) 2018  Alexander Kraus <nr4@z10.info>
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

class Preferences:
    def __init__(self, projectfile):
        # Project settings
        self.projectfile = projectfile
        
        # Exactly 10 recent files
        self.recentfiles = [ "None" ]*10
        
        #Open files
        self.openfiles = []
        
    def save(self):
        with open(self.projectfile, "wt") as f:
            for fil in self.recentfiles + self.openfiles:
                if fil[-1] != '\n': 
                    fil += '\n'
                    f.write(fil)
            f.writelines(self.openfiles)
            f.close()
            
    def load(self):
        try:
            with open(self.projectfile, "rt") as f:
                lines = f.readlines()
                self.recentfiles = lines[:10]
                self.openfiles = lines[10:]
                f.close()
        except:
            print("Could not load preferences file '", self.projectfile, "'. Starting up empty.")

    def hasRecents(self):
        for file in self.recentfiles:
            if file != "None":
                return True
        return False
    
    def nRecents(self):
        n = 10
        for file in self.recentfiles:
            if file == "None":
                n -= 1
        return n
    
    def addRecent(self, filename):
        if self.nRecents() != 10:
            for i in range(10):
                if self.recentfiles[i] == "None":
                    self.recentfiles[i] = filename
                    return
        else:
            for i in range(8):
                self.recentfiles[9-i] = self.recentfiles[9-i-1]
            self.recentfiles[0] = filename
        
        
