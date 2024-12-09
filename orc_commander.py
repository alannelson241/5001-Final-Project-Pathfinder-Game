# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Orc Commander
'''
Contains the Orc Commander class, a child class of Creature. Generates the 
attributes and methods for the Orc Commander nonplayer character.
'''
# https://2e.aonprd.com/NPCs.aspx?ID=3132&Elite=true&NoRedirect=1
import dice
from creature import Creature
import helper_functions as hf
import time

class Orc_Commander(Creature):
    '''
    Class: Orc_Commander
    Attributes:
        team: used to determine whether take_turn() or ai() is called on the object's turn
        attack_bonus: attack modifier for the warrior's maul Strikes
        battle_cry_used: Boolean indicating if battle_cry() has been used
    Methods:
        ai: controls what the commander does in combat
        maul_strike: makes a Strike with the commander's maul
        battle_cry: grants all allies a +1 bonus to attack rolls 

    Class contains methods and attributes that are specific to the Orc Commander
    nonplayer character. When called, generates an object of Creature to inherit
    using a prescribed set of arguments. 
    '''
    def __init__(self):
        '''
        Method: constructor
        Parameters: self, str - name of the commander
        Returns: none; creates object of Orc_Commander
        
        Constructor function for the Orc_Commander class.
        '''
        super().__init__("Katthok, the Orc Commander",4,2,1,-1,1,2,"medium",3,47,21,3,3,2,4,0,0,2,2,0,0,0,"society",18)
        self.team = "enemy"
        self.attack_bonus = 12
        self.battle_cry_used = False

    def ai(self, target_list, ally_list, override = -1): 
        '''
        Method: ai
        Parameters: self, lists - lists of PC and NPC objects; int, value to bypass RNG
        Returns: none

        Artificial intelligence for the Orc Commander enemy.

        The commander takes different actions based on how many actions it has 
        remaining:

        3 actions: if the commander hasn't used Battle Cry yet, uses Battle Cry.
        If it has, 50% chance to either attempt a debuff (demoralize or trip)
        or make a Strike. The orc commander always targets the PC with the 
        lowest remaining HP. When selecting a debuff, will check if the target
        has had a demoralize attempt made against them. If not, attempts 
        demoralize; if yes, attempts to trip.

        1-2 actions: makes a maul Strike.
        '''
        if override == -1:
            time.sleep(1)
        current_min = 1000
        for i in range(len(target_list)):
            if target_list[i].current_hp < current_min and target_list[i].current_hp > 0:
                current_min = target_list[i].current_hp
                target = target_list[i]
        if current_min == 1000:
            target = target_list[0]

        if self.actions == 3:
            if self.battle_cry_used == False:
                self.battle_cry(ally_list)
            else:
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
                    self.maul_strike(target)
        
        else:
            self.maul_strike(target)

    def maul_strike(self, target): 
        '''
        Method: maul_strike
        Parameters: self, object - target of the attack
        Returns: none
        
        Functionality for the commander's maul attack. Makes a Strike using
        the commander's maul.
        
        Function is handled by the strike() method of Creature using its 
        parameter options: target = target, weapon_name = "Maul",
        damage_dice = 1, die_size = 12, damage_type = "bludgeoning", damage_bonus
        = 6, finesse, agile, cleric, rogue, wizard = False, action_cost = 1.

        Uses standard multiple attack penalty: -5 on the second attack, -10 on third +
        '''
        super().strike(target,"Maul",1,12,"bludgeoning",6,False,False,False,False,False,1)

    def battle_cry(self, target_list): 
        '''
        Method: battle_cry
        Parameters: self, list - list of all NPC objects
        Returns: none
        
        Grants each ally a +1 status bonus to attack rolls for the remainder of
        the encounter. Costs 1 action.
        '''
        self.actions -= 1
        self.battle_cry_used = True
        print(self.name, "bellows a Battle Cry! Their allies gain a +1 bonus to attack rolls!")
        for ally in range(len(target_list)):
            target_list[ally].status_bonus = 1