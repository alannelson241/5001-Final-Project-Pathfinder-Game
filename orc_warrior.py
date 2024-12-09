# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Orc Warrior
'''
Contains the Orc Warrior class, a child class of Creature. Generates the 
attributes and methods for the Orc Warrior nonplayer character.
'''
# https://2e.aonprd.com/Monsters.aspx?ID=325&Elite=true&NoRedirect=1
import dice
from creature import Creature
import helper_functions as hf
import time

class Orc_Warrior(Creature):
    '''
    Class: Orc_Warrior
    Attributes: 
        name: appends " the Orc Warrior" to whatever is passed to Creature's __init__ for name
        team: used to determine whether take_turn() or ai() is called on the object's turn
        attack_bonus: attack modifier for the warrior's battleaxe Strikes
        dex_attack_bonus: attack modifier for the warrior's shortsword Strikes
    Methods:
        constructor - generates objects of Orc_Warrior 
        ai - controls what the warrior does in combat
        battkeaxe_strike - makes a Strike with the warrior's battleaxe
        shortsword_strike - makes a Strike with the warrior's shortsword

    Class contains methods and attributes that are specific to the Orc Warrior
    nonplayer character. When called, generates an object of Creature to inherit
    using a prescribed set of arguments. 
    '''
    def __init__(self, name):
        '''
        Method: constructor
        Parameters: self, str - name of the warrior
        Returns: none; creates object of Orc_Warrior
        
        Constructor function for the Orc_Warrior class.
        '''
        super().__init__(name,4,2,3,-1,1,0,"medium",2,33,20,3,1,2,2,0,0,2,2,0,0,0,"society",16)
        self.name += " the Orc Warrior"
        self.team = "enemy"
        self.attack_bonus = 9
        self.dex_attack_bonus = 9
    
    def ai(self, target_list, ally_list, override = -1):
        '''
        Method: ai
        Parameters: self, lists - lists of PC and NPC objects; int - value to bypass RNG
            Note: ally_list is included as a parameter for compatibility purposes
            with other ai() methods and is not used by this class
        Returns: none
        
        Artificial intelligence for the Orc Warrior enemy.

        The warrior takes different actions based on how many actions it has remaining:

        3 actions: 50% chance to either attempt a debuff (demoralize or trip)
        or make a strike. The orc warrior always targets the PC with the 
        highest remaining HP. When selecting a debuff, will check if the target
        has had a demoralize attempt made against them. If not, attempts 
        demoralize; if yes, attempts to trip.

        2 actions: Makes a Strike. If attacks_made = 0, uses battleaxe; if not,
        uses shortsword.

        1 action: makes a shortsword Strike.
        '''
        if override == -1:
            time.sleep(1)
        current_max = 0
        for i in range(len(target_list)):
            if target_list[i].current_hp > current_max:
                current_max = target_list[i].current_hp
                target = target_list[i]
        if current_max == 0:
            target = target_list[0]

        if self.actions == 3:
            if override == -1:
                debuff_chance = dice.d4() % 2
            else: 
                debuff_chance = override
            if debuff_chance == 0:
                if target.been_demoralized == False:
                    self.demoralize(target)
                else: 
                    self.trip(target)
            else:
                self.battleaxe_strike(target)
        
        elif self.actions == 2:
            if self.attacks_made == 0:
                self.battleaxe_strike(target)
            else: 
                self.shortsword_strike(target)
        
        else:
            self.shortsword_strike(target)

    def battleaxe_strike(self, target): 
        '''
        Method: battleaxe_strike
        Parameters: self, object - target of the attack
        Returns: none
        
        Functionality for the warrior's battleaxe attack. Makes a Strike using
        the warrior's battleaxe.
        
        Function is handled by the strike() method of Creature using its 
        parameter options: target = target, weapon_name = "Battleaxe",
        damage_dice = 1, die_size = 8, damage_type = "slashing", damage_bonus
        = 6, finesse, agile, cleric, rogue, wizard = False, action_cost = 1.

        Uses standard multiple attack penalty: -5 on the second attack, -10 on third +
        '''
        super().strike(target,"Battleaxe",1,8,"slashing",6,False,False,False,False,False,1)
    def shortsword_strike(self, target): 
        '''
        Method: shortsword_strike
        Parameters: self, object - target of the attack
        Returns: none
        
        Functionality for the warrior's shortsword attack. Makes a strike using
        the warrior's shortsword.
        
        Function is handled by the strike() method of Creature using its 
        parameter options: target = target, weapon_name = "Shortsword", 
        damage_dice = 1, die_size = 6, damage_type = "piercing", damage_bonus
        = 6, finesse, agile = True, cleric, rogue, wizard = False, 
        action_cost = 1.
        
        Uses agile multiple attack penalty: -4 on second attack, -8 on third+
        '''
        super().strike(target,"Shortsword",1,6,"piercing",6,True,True,False,False,False,1)
