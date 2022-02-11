# -*- coding: utf-8 -*-

class Perception() :
    def __init__ (self, source, phen, lvl, t, now, dec):
        self.source = source
        self.phen = phen
        self.t = t
        self.dec = dec
        self.lvl = lvl
        self.now = now


    def getLevel(self):
        self.lvl = self.lvl - self.dec*self.now
