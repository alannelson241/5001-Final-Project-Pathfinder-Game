# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Hobgoblin Soldier
'''
Contains the Hobgoblin_Soldier class, a child class of Creature. Generates the 
attributes and methods for the Hobgoblin Soldier nonplayer character.
'''
# https://2e.aonprd.com/Monsters.aspx?ID=3053&Elite=true&NoRedirect=1
import dice
from creature import Creature
import helper_functions as hf
import time

class Hobgoblin_Soldier(Creature):
    '''
    Class: Hobgoblin_Soldier
    Attributes: 
        team: used to determine whether take_turn() or ai() is called on the object's turn
        attack_bonus: attack modifier for the soldier's longsword Strikes
        focus - if an enemy is off-guard, stored in this variable so the soldier can focus their attacks on them
    Methods:
        constructor: generates objects of Hobgoblin_Soldier
        start_turn - inherits functionality from Creature and resets value of focus each turn
        ai - controls what the soldier does in combat
        longsword_strike - makes a Strike with the soldier's longsword
        raise_a_shield - raises the soldier's shield for a bonus to AC

    Class contains methods and attributes that are specific to the Hobgoblin Soldier
    nonplayer character. When called, generates an object of Creature to inherit
    using a prescribed set of arguments. 
    '''
    def __init__(self):
        '''
        Method: constructor
        Parameters: self
        Returns: none; creates object of Hobgoblin_Soldier
        
        Constructor function for the Hobgoblin_Soldier class.
        '''
        super().__init__("Hobbes the Hobgoblin Soldier",3,3,2,0,2,-1,"medium",2,30,20,1,2,2,2,0,0,2,0,0,0,0,"society",16)
        self.team = "enemy"
        self.attack_bonus = 10
        self.focus = None

    def start_turn(self):
        '''
        Method: start_turn
        Parameters: self
        Returns: none
        
        Modifies functionality of the start_turn() method of Creature. Adds the
        ability to reset the focus attribute each turn.
        '''
        super().start_turn()
        self.focus = None

    def ai(self, target_list, ally_list):
        '''
        Method: ai
        Parameters: self, lists - list of PC and NPC objects
            Note: ally_list is included as a parameter for compatibility purposes
            with other ai() methods and is not used by this class
        Returns: none
        
        Artificial intelligence for the Hobgoblin Soldier enemy.
        
        The soldier takes different actions based on how many actions it has:
        
        3 actions: If any PC is off-guard, the soldier will prioritize making 
        Strikes against them. If not, they will attempt to trip a random 
        target.

        2 actions: If a PC is off-guard, the soldier attacks them. If not, 
        makes a Strike against a random target.

        1 action: The soldier raises their shield.
        '''
        time.sleep(2)
        if self.actions == 1:
            self.raise_a_shield()
        elif self.actions > 1:
            for i in range(len(target_list)):
                if target_list[i].off_guard == True and target_list[i].current_hp > 0:
                    self.focus = target_list[i]
                    # use this break statement to exit the for loop as soon as a valid target is found
                    break
        if self.focus:
            self.longsword_strike(self.focus)
        elif self.actions == 2:
            target = hf.random_target(target_list)
            self.longsword_strike(target)
        else:
            target = hf.random_target(target_list)
            self.trip(target)

    def longsword_strike(self, target):
        '''
        Method: longsword_strike
        Parameters: self, object - target of the attack
        Returns: none
        
        Functionality for the soldier's longsword attack.
        '''
        super().strike(target,"Longsword",1,8,"slashing",5,False,False,False,False,False,1)

    def raise_a_shield(self): 
        # https://2e.aonprd.com/Actions.aspx?ID=2316
        '''
        Method: raise_a_shield
        Parameters: self
        Returns: none
        
        The cleric raises their shield, gaining a +2 circumstance bonus to AC 
        until the start of their next turn. Identical to the raise_a_shield 
        method of the Cleric PC class.
        '''
        self.actions -= 1
        print(self.name, "raises their shield! They gain +2 AC until the start of their next turn.")
        self.circumstance_bonus = 2
