# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Hobgoblin General
'''
Contains the Hobgoblin_General class, a child class of Creature. Generates the
attributes and methods for the Hobgoblin General nonplayer character.
'''
# https://2e.aonprd.com/Monsters.aspx?ID=3055&Weak=true&NoRedirect=1
import dice
from creature import Creature
import helper_functions as hf
import time

class Hobgoblin_General(Creature):
    '''
    Class: Hobgoblin_General
    Attributes:
        team: used to determine whether take_turn() or ai() is called on the object's turn
        attack_bonus: attack modifier for the general's warhammer Strikes
        first_turn: controls use of the general's General Cry feature
    Methods:
        constructor: generates objects of Hobgoblin_General
        ai: controls how the general acts in combat
        warhammer_strike: makes a Strike with the general's warhammer
        raise_a_shield: raises the general's shield for a bonus to AC

    Class contains methods and attributes that are specific to the Hobgoblin General
    nonplayer character. When called, generates an object of Creature to inherit
    using a prescribed set of arguments. 
    '''
    def __init__(self):
        '''
        Method: constructor
        Parameters: self
        Returns: none; creates object of Hobgoblin_General

        Constructor function for the Hobgoblin_General class.
        '''
        super().__init__("Gnarlok the Hobgoblin General",4,3,2,0,1,2,"medium",5,70,23,2,3,3,3,1,0,2,2,0,0,0,"society",20)
        self.team = "enemy"
        self.attack_bonus = 15
        self.first_turn = True

    def ai(self, target_list, ally_list, override = 0):
        '''
        Method: ai
        Parameters: self, lists: list of PC and NPC objects; int - value to bypass rng
            Note: ally_list is included as a parameter for compatibility purposes
            with other ai() methods and is not used by this class
        Returns: none
        
        Artificial intelligence for the Hobgoblin General enemy.

        If it is the first turn of the encounter, the general uses demoralize
        for free with its General's Cry feature.

        The general does one different things depending on how many actions it 
        has remaining:

        3 actions: the hobgoblin randomly selects between attempting to 
        demoralize a random target, attempting to tumble through against the 
        target, attempting to trip the target, or making a warhammer Strike. If
        the target is ineligible for the action, makes a Strike against them.

        2 actions:the hobgoblin makes a warhammer Strike the PC with the lowest
        HP.

        1 action: the hobgoblin raises their shield.
        '''
        if override == 0:
            time.sleep(2)

        if self.first_turn == True:
            self.actions = 4
            target = hf.random_target(target_list)
            print("The general lets loose a war cry! Demoralize attempt against", target.name + "!")
            self.demoralize(target)
            self.first_turn = False

        if self.actions == 3:
            if override == 0:
                rand = dice.d4()
            else: 
                rand = override
            target = hf.random_target(target_list)

            if rand == 1:
                if target.been_demoralized == False:
                    self.demoralize(target)
                else: 
                    self.warhammer_strike(target)

            elif rand == 2:
                if target.off_guard == False:
                    self.tumble_through(target)
                else: 
                    self.warhammer_strike(target)

            elif rand == 3:
                if target.off_guard == False:
                    self.trip(target)
                else: 
                    self.warhammer_strike(target)

            elif rand == 4:
                self.warhammer_strike(target)

        elif self.actions == 2: 
            current_min = 1000
            for i in range(len(target_list)):
                if target_list[i].current_hp < current_min and target_list[i].current_hp > 0:
                    current_min = target_list[i].current_hp
                    target = target_list[i]
            if current_min == 1000:
                target = target_list[0]
            self.warhammer_strike(target)

        elif self.actions == 1:
            self.raise_a_shield()

    def warhammer_strike(self, target):
        '''
        Method: warhammer_strike
        Parameters: self, object - target of the attack
        Returns: none
        
        Functionality for the general's warhammer attack. Makes a strike using
        the general's +1 warhammer.

        Function is handled by the strike() method of Creature using its 
        parameter options: target is target, weapon_name = "Warhammer", 
        damage_dice = 1, die_size = 8, damage_type = "bludgeoning", damage_bonus
        = 8, finesse, agile, cleric, rogue, wizard = False, action_cost = 1.

        Uses standard multiple attack penalty: -5 on the second attack, -10 on third +
        '''
        super().strike(target, "Warhammer",1,8,"bludgeoning",8,False,False,False,False,False,1)

    def raise_a_shield(self): 
        # https://2e.aonprd.com/Actions.aspx?ID=2316
        '''
        Method: raise_a_shield
        Parameters: self
        Returns: none
        
        The general raises their shield, gaining a +2 circumstance bonus to AC 
        until the start of their next turn. Identical to the raise_a_shield 
        method of the Cleric PC class.
        '''
        self.actions -= 1
        print(self.name, "raises their shield! They gain +2 AC until the start of their next turn.")
        self.circumstance_bonus = 2
