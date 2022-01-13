# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 12:25:03 2022

@author: tospie
"""

from Actions import directionMappings
from random import randint


def move(agent, direction = None) :
    x, y = agent.locatedAt
    if not direction:
        agent.locatedAt = x + randint(-1, 1), y + randint(-1, 1)
    else:
        agent.locatedAt += directionMappings[direction]

def setToBounds(agent) :
    agent.locatedAt = agent.locatedAt ## later set Agent to grid borders

mappingTable = {

}
