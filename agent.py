# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 12:02:46 2022

@author: tospie
"""

from random import randint
from Actions.actionMappings import mappingTable
class Agent :
    
    maxFatigue : 100
    generatedRules : 3
    flippedRules : 1

    def __init__(self):
        self.locatedAt : (0,0)
        self.fatigue : 0
        self.generation : 0
        self.rules: []
        self.knownPhenomena: []
        self.currentObservations: []
        

    def createInitialAgent(self, ) :
        self.knownPhenomena.append("always")
    #######################################################
    ##
    ## PERCEPTION
    ##
    #######################################################

    def perceive(self, environment) :
        self.currentObservations.clear()
        self.perceiveCoordinate(environment, self.locatedAt)
        
    def perceiveCoordinate(self, environment, coordinate) :
        x, y = coordinate
        for phen in environment.grid[x][y]:
            self.currentObservations.append(coordinate, phen)

    #######################################################
    ##
    ## REACTION
    ##
    #######################################################
    
    def react(self, ):
        for rule in self.rules:
            for obs in self.currentObservations:
                ruleFulfilled = obs[0] == rule[0]
                if(rule[1] == 1) : ruleFulfilled = not ruleFulfilled
                if rule[0] == "always" or ruleFulfilled :
                    rule[2]() ## TODO: generalize parameters.
                    
    #######################################################
    ##
    ## REPRODUCTION RULES
    ##
    #######################################################
    
    def mutate(self, ):
        for i in range(randint(0,Agent.gegeneratedRules)):
            self.generateRule()

        for i in range(randint(0,Agent.flippedRules)):
            self.flipRuleRandom()
        
    def generateRule(self, ):
        self.rules.append("test", 0, mappingTable["move"])
        
    def flipRuleRandom(self, ):
        index = randint(0, len(self.rules) - 1)
        obs, negFlag, action = self.rules[index]
        flipped = 1 if negFlag == 0 else 0
        self.rules[index] = obs, flipped , action
