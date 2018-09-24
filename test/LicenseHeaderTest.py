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

import unittest
import sys

sys.path.append("..")

from LicenseHeader import *

class LicenseHeaderTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        
        self.header = LicenseHeader()
        
        self.header.demoname = "Eternal Darkness"
        self.header.grouphandle = "Team210"
        self.header.authorhandle = "NR4^QM"
        self.header.compo = "64k Intro"
        self.header.party = "Evoke 2018"
        self.header.license = "GPLv3"
        
        self.header.author = "Alexander Kraus"
        self.header.email = "nr4@z10.info"
        self.header.year = "2018"
        
        self.expectedText = ""
        with open("TestHeader.txt", "rt") as f:
            self.expectedText = f.read().strip()
            f.close()

    def testToString(self):
        self.assertEqual(self.header.toString(), self.expectedText)
        
    def testFromString(self):
        self.header.fromString(self.expectedText)
        
        self.assertEqual(self.header.demoname, "Eternal Darkness")
        self.assertEqual(self.header.grouphandle, "Team210")
        self.assertEqual(self.header.authorhandle, "NR4^QM")
        self.assertEqual(self.header.compo, "64k Intro")
        self.assertEqual(self.header.party, "Evoke 2018")
        self.assertEqual(self.header.license, "GPLv3")
        self.assertEqual(self.header.author, "Alexander Kraus")
        self.assertEqual(self.header.email, "nr4@z10.info")
        self.assertEqual(self.header.year, "2018")

if __name__ == '__main__':
    unittest.main()
