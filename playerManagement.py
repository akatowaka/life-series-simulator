import math
import random

from signallers import sig

class Player():
    def __init__(self, index, name, lives):
        self.index = index
        self.name = name
        self.lives = lives
        self.alliance = None
        self.hostile = False
        self.kills = 0

    def setLives(self, lives):
        self.lives = lives

    def getIndex(self):
        return self.index

    def getName(self):
        return self.name
    
    def getLives(self):
        return self.lives
    
    def setAlliance(self, alliance):
        self.alliance = alliance
        if (alliance):
            alliance.addMember(self)
    
    def getAlliance(self):
        return self.alliance
    
    def getAllianceName(self):
        return self.alliance.getName() if self.alliance != None else "None"

    def setHostile(self, hostile):
        self.hostile = hostile

    def isHostile(self):
        return self.hostile
    
    def getKills(self):
        return self.kills
    
    def incKills(self):
        self.kills += 1
    
    def leaveAlliance(self, relations):
        if (self.alliance != None):
            self.alliance.removeMember(self)
            if relations and self.alliance.disband(relations):
                self.alliance = None
                return True
            self.alliance = None
        return False


class Alliance():
    def __init__(self, name):
        self.name = name
        self.members = []
        self.stength = random.randint(1,3)

    def getName(self):
        return self.name

    def getMembers(self):
        return self.members
    
    def addMember(self, p):
        self.members.append(p)

    def removeMember(self, p):
        self.members.remove(p)
    
    def getStrength(self):
        return self.strength

    def checkStability(self, relations):
        perceptions = [0] * len(self.members)
        individual = [0] * len(self.members)
        overall = 0
        for i, p in enumerate(self.members):
            for j, t in enumerate(self.members):
                rel = relations[p.getIndex()][t.getIndex()]
                individual[i] += rel
                perceptions[j] += rel
                overall += rel
        
        kicked = []
        leaving = []

        for i, val in enumerate(perceptions):
            if val <= -2*len(self.members):
                kicked.append(self.members[i])

        for i, val in enumerate(individual):
            if val < -2*len(self.members) and self.members[i] not in kicked:
                leaving.append(self.members[i])

        for k in kicked:
            k.leaveAlliance([])
            sig.allianceKick(k, self.name)

        for i in leaving:
            i.leaveAlliance([])
            sig.allianceLeave(i, self.name)

        if (overall < -2*len(self.members+kicked+leaving)
                or len(kicked + leaving) >= len(self.members)):
            return True

        return False

    def disband(self, relations):
        if len(self.getMembers()) < 2 or self.checkStability(relations):
            for p in self.members:
                p.setAlliance(None)
            sig.allianceDisband(self.name)
            return True
        return False
    
    @staticmethod
    def getAllianceBonus(p1, p2):
        return (p1.getAlliance().getStrength() 
                if p1.getAlliance() == p2.getAlliance else 0)
