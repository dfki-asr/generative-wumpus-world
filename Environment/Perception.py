# -*- coding: utf-8 -*-

class Perception() :
    def __init__ (self, source, phen, lvl, t, dec):
        self.source = source
        self.phen = phen
        self.t = t
        self.dec = dec
        self.lvl = lvl


    def setLevel(self, now, scale=0):
        self.lvl = (self.lvl - (self.dec*(now-self.t))) + scale
        self.lvl = min(1, self.lvl)

    def getLevel(self, now):
        self.setLevel(now)
        return self.lvl
