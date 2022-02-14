# -*- coding: utf-8 -*-

class Perception() :
    def __init__ (self, source, phen, lvl, t, dec):
        self.source = source
        self.phen = phen
        self.t = t
        self.dec = dec
        self.lvl = lvl


    def getLevel(self, now):
        self.lvl = self.lvl - (self.dec*(now-self.t))
        return self.lvl
