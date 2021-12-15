# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 15:28:06 2021

@author: student2
"""

def _parse_lines(self):
    self.comment = False
    self._iter_lines(self._parse_line)

def _parse_line(self, line, p, o):
    i = 0
    l = ""
    while i < len(line) - 1:
        p = line[i] + line[i + 1]
        
        if self.comment == False and p == "*/":
            self._flag = False
            self._line1 = o
            self._errm = "unbalanced comment identifier"
        elif(p == "/*" and self.comment == False) or (p == "*/" and self.comment == True):
            self.comment = not self.comment
            i = i + 1
        elif (p == "//"):
            break
        elif line[i].isspace() == False and self.comment == False:
            l += line[i]
        i += 1
            
    return l