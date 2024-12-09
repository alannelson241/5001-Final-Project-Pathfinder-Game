# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Goblin
'''
Contains the Goblin class, a child class of Creature. Generates the attributes 
and methods for the Goblin nonplayer character.
'''
# https://2e.aonprd.com/NPCs.aspx?ID=3025
import dice
from creature import Creature
import helper_functions as hf
import time

class Goblin(Creature):
    '''
    Class: Goblin
    Attributes: 
        name: appends " the Goblin" to whatever is passed to Creature's __init__ for name
        team: used to determine whether take_turn() or ai() is called on the object's turn
        attack_bonus: attack modifier for the goblin's spear Strikes
        hide_attempt, records if the goblin has attempted the hide action already this turn.
    Methods:
        constructor: generates objects of Goblin
        start_turn: inherits functionality from Creature and resets the 
            hide_attempt attribute
        ai: controls how the goblin acts in combat.
        spear_strike: makes a Strike with the goblin's spear

    Class contains methods and attributes that are specific to the Goblin 
    nonplayer character. When called, generates an object of Creature to inherit
    using a prescribed set of arguments. 
    '''
    def __init__(self, name):
        '''
        Method: constructor
        Parameters: self, str - name of the Goblin
        Returns: none; creates object of Goblin

        Constructor function for the Goblin class.
        '''
        super().__init__(name,3,3,2,-1,0,2,"small",1,18,17,2,2,2,2,0,0,1,0,0,0,1,"society",15)
        self.name += " the Goblin"
        self.team = "enemy"
        self.attack_bonus = 8
        self.hide_attempt = False

    def start_turn(self):
        '''
        Method: start_turn
        Parameters: self
        Returns: none
        
        Adds Goblin specific functionality to start_turn(). Resets the value of 
        hide_attempt to False.
        '''
        super().start_turn()
        self.hide_attempt = False
    
    def ai(self, target_list, ally_list, override = -1):
        '''
        Method: ai
        Parameters: self, lists - list of PC and NPC objects; int - value to bypass rng
            Note: ally_list is included as a parameter for compatibility purposes
            with other ai() methods and is not used by this class
        Returns: none

        Artificial intelligence for the Goblin enemy.

        For each action on its turn, the goblin randomly chooses between using
        a spear Strike, a trip Strike, or hiding. If the goblin has already 
        tried to hide on a given turn or attempts to trip an off-guard target,
        attacks instead.
        '''
        if override == -1:
            time.sleep(2)
            rand = dice.d6() % 3
        else:
            rand = override
        target = hf.random_target(target_list)

        if rand == 0:
            if self.hide_attempt == False:
                self.hide(target_list)
                self.hide_attempt = True
            else: 
                self.spear_strike(target)

        elif rand == 1:
            if target.off_guard == False:
                self.trip(target)
            else:
                self.spear_strike(target)

        elif rand == 2:
            self.spear_strike(target)
        
    def spear_strike(self, target):
        '''
        Method: spear_strike
        Parameters: self, object - target of the attack
        Returns: none

        Functionality for the goblin's spear attack. Makes a strike using
        the goblin's spear.

        Function is handled by the strike() method of Creature using its 
        parameter options: target is target, weapon_name = "Spear", 
        damage_dice = 1, die_size = 6, damage_type = "piercing", damage_bonus
        = 3, finesse, agile, cleric, rogue, wizard = False, action_cost = 1.

        Uses standard multiple attack penalty: -5 on the second attack, -10 on third +
        '''
        super().strike(target,"Spear",1,6,"piercing",3,False,False,False,False,False,1)
