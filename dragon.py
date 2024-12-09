# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Dragon
'''
Contains the Dragon class, a child class of Creature. Generates the attributes
and methods for the Dragon nonplayer character.
'''
# https://2e.aonprd.com/Monsters.aspx?ID=133
import dice
from creature import Creature
import helper_functions as hf
import time

class Dragon(Creature):
    '''
    Class: Dragon
    Attributes: 
        team: used to determine whether take_turn() or ai() is called on the object's turn
        spell_dc: used as the DC for the dragon's breath weapon
        attack_bonus: attack modifier for jaws and claw Strikes
        dex_attack_bonus: attack modifier for horn Strikes
        breath_available: Boolean determining if the dragon can use its breath weapon
        breath_timer: number of turns until the dragon can use its breath weapon again
        first_turn: determines if the dragon uses Frightful Presence
    Methods:
        constructor: generates objects of Dragon
        start_turn: inherits functionality from Creature and decrements value of breath_timer. If it reaches 0, sets breath_available to True
        ai: controls what the dragon does in combat
        jaws: makes a Strike with the dragon's jaws
        claw: makes a Strike with the dragon's claw
        horn: makes a strike with the dragon's horn
        breath_weapon: all PC's make a DC25 Fortitude save or take 9d6 poison damage.
        draconic_frenzy: chains a horn attack and two claw attacks, only costs 2 actions
        frightful_presence: on the first turn of an encounter, attempts to demoralize all PC's

    Class contains methods and attributes that are specific to the Dragon
    nonplayer character. When called, generates an object of Creature to inherit
    using a prescribed set of arguments. 
    '''
    def __init__(self):
        '''
        Method: constructor
        Parameters: self
        Returns: none; creates objects of Dragon

        Constructor function for the Dragon class.
        '''
        super().__init__("Zelos the Green Dragon",5,1,3,2,2,4,"large",8,135,28,3,3,3,3,0,0,2,3,0,2,0,"arcana",24)
        self.team = "enemy"
        self.spell_dc = 25
        self.attack_bonus = 18
        self.dex_attack_bonus = 16
        self.breath_available = True
        self.breath_timer = 0
        self.first_turn = True

    def start_turn(self):
        '''
        Method: start_turn
        Parameters: self
        Returns: none

        Adds Dragon specific functionality to the Creature method start_turn().
        If breath_timer is greater than 0, decrements it; then, if it equals 0,
        sets breath_available to True.
        '''
        super().start_turn()
        if self.breath_timer > 0:
            self.breath_timer -= 1
            print(self.name + "'s breath weapon will be usable again in", self.breath_timer, "turns!")
        if self.breath_timer == 0:
            self.breath_available = True
    
    def ai(self, target_list, ally_list):
        '''
        Method: ai
        Parameters: self, lists - list of all PC's and NPC's
            Note: ally_list is included as a parameter for compatibility purposes
            with other ai() methods and is not used by this class
        Returns: none

        Artificial intelligence for the Dragon enemy. 

        On the first turn of combat, uses Frightful Presence to try to 
        Demoralize all PC's. After that, does different things based on how
        many actions are remaining and if the breath weapon is usable.
        
        If the dragon's breath weapon is available, it will select a random 
        target and check if it is valid to use Recall Knowledge on. If yes,
        attempts Recall Knowledge then uses the breath weapon; if no, uses the 
        breath weapon and makes a jaws attack against the PC with the lowest
        non-zero HP.

        If the breath weapon is not available, selects a random target and 
        checks if it can be Demoralized. If yes, attempts Demoralize and uses
        Draconic Frenzy; if no, uses Draconic Frenzy and makes a jaws attack
        with the same target criteria as above.
        '''
        time.sleep(2)
        if self.first_turn == True:
            self.frightful_presence(target_list)
            self.first_turn = False

        if self.actions == 3 and self.breath_available == True:
            target = hf.random_target(target_list)
            if target.been_rk == True or target.current_hp <= 0:
                self.breath_weapon(target_list)
            else:
                self.recall_knowledge(target)

        elif self.actions == 3 and self.breath_available == False:
            target = hf.random_target(target_list)
            if target.been_demoralized == True or target.current_hp <= 0:
                self.draconic_frenzy(target_list)
            else:
                self.demoralize(target)

        elif self.actions == 2 and self.breath_available == True:
            self.breath_weapon(target_list)

        elif self.actions == 2 and self.breath_available == False:
            self.draconic_frenzy(target_list)
        
        elif self.actions == 1:
            current_min = 1000
            for i in range(len(target_list)):
                if target_list[i].current_hp < current_min and target_list[i].current_hp > 0:
                    current_min = target_list[i].current_hp
                    target = target_list[i]
            if current_min == 1000:
                target = target_list[0]
            self.jaws(target)

    def jaws(self, target, override = 0):
        '''
        Method: jaws
        Parameters: self, object - target of the attack, int - value to force a result
        Returns: none

        Functionality for the dragon's jaws attack. Needs to be bespoke because
        it deals bonus poison damage.

        First, deducts the action cost and prints a message, then checks the 
        current MAP level. If no argument for override is provided, makes an 
        attack roll, rolls damage, and increments attacks+made, then checks the
        degree of success for the attack. If the attack roll is less than the
        target's AC or override = 3, attack misses; if the attack roll is 
        greater than or equal to the target's AC or override = 2, attack hits
        and deals normal (2d10+8 + 2d4) damage; if the attack roll is greater 
        than or equal to the target's AC +10 or override = 1, attack is a 
        critical hit and deals double damage.
        '''
        self.actions -= 1
        print(self.name, "attacks", str(target.name) + "! Jaws strike!")
        print("They have made", self.attacks_made, "attacks so far this turn.")

        if self.attacks_made == 1:
            map_penalty = 5
        elif self.attacks_made >= 2:
            map_penalty = 10
        else:
            map_penalty = 0

        if override == 0:
            attack = dice.d20() + self.attack_bonus + self.status_bonus - self.status_penalty - map_penalty
        else: attack = 0

        damage = 8
        poison = 0
        for i in range(2):
            poison += dice.d4()
            damage += dice.d10()

        self.attacks_made += 1
        print(self.name, "rolls", attack, "for their attack roll.")

        if attack >= target.ac + 10 + target.circumstance_bonus - target.status_penalty - target.og_circumstance_penalty or override == 1:
            print("Critical hit!")
            damage *= 2
            poison *= 2
            print(target.name, "takes", damage, "piercing and", poison, "poison damage.")
            target.current_hp -= (damage + poison)
        
        elif attack >= target.ac + target.circumstance_bonus - target.status_penalty - target.og_circumstance_penalty or override == 2:
            print("Hit!")
            print(target.name, "takes", damage, "piercing and", poison, "poison damage.")
            target.current_hp -= (damage + poison)
        
        else:
            # access with override == 3
            print("Miss!")
            print(target.name, "takes 0 damage.")
        
        print(target.name, "has", target.current_hp, "HP.")

    def claw(self, target): 
        '''
        Method: claw
        Parameters: self, object - target of the attack
        Returns: none
        
        Functionality for the dragon's claw attack. Makes a strike using
        the dragon's claw.

        Function is handled by the strike() method of Creature using its 
        parameter options: target is target, weapon_name = "Claw", 
        damage_dice = 2, die_size = 8, damage_type = "slashing", damage_bonus
        = 8, finesse = False, agile = True, cleric, rogue, wizard = False, 
        action_cost = 1.

        Uses agile multiple attack penalty: -4 on the second attack, -8 on third +
        '''
        super().strike(target,"Claw",2,8,"slashing",8,False,True,False,False,False,1)

    def horn(self, target): 
        '''
        Method: horn
        Parameters: self, object - target of the attack
        Returns: none
        
        Functionality for the dragon's horn attack. Makes a strike using
        the dragon's horns.

        Function is handled by the strike() method of Creature using its 
        parameter options: target is target, weapon_name = "Horn", 
        damage_dice = 1, die_size = 12, damage_type = "piercing", damage_bonus
        = 7, finesse = True, agile, cleric, rogue, wizard = False, 
        action_cost = 1.

        Uses standard multiple attack penalty: -5 on the second attack, -10 on third +
        '''
        super().strike(target,"Horn",1,12,"piercing",7,True,False,False,False,False,1)

    def breath_weapon(self, target_list, override = 0): 
        '''
        Method: breath_weapon
        Parameters: self, list - list of all enemies; int - value to force a result
        Returns: none
        
        Functionality for the dragon's breath weapon. All PC's make a basic 
        Fortitude save, DC 25, or take 9d6 poison damage. The breath weapon is 
        then put on cooldown for 1d4 turns.

        Function first deducts the 2 action cost, sets breath_available to 
        False, and sets breath_timer between 1 and 4, then prints a message.

        If no override variable is passed or an override of 5 (bypass calls to
        time.sleep() but otherwise function as normal), rolls a Fortitude save for
        each target and appends it to a list to use later. If an override 
        variable other than 0 (default) or 5 is passed, each save is locked to 
        15 to force a failure on the save later on. The function then rolls 
        damage (9d6).

        Finally, the function determines which degree of success each save 
        gets, with values greater than or equal to spell_dc + 10 being a 
        critical success and taking no damage, values greater than or equal to
        spell_dc being a success and taking half damage, values less than 
        spell_dc being a failure and taking full damage, and values less than 
        spell_dc - 10 being a critical failure and taking double damage.

        Override values are used for testing purposes, with 0 being the default
        and not doing anything, 1 causing a crit success, 2 causing a success, 
        3 causing a crit fail, 4 causing a fail, and 5 running the function as 
        normal but bypassing calls to time.sleep().        
        '''
        self.actions -= 2
        print(self.name, "uses their Breath Weapon! A deluge of deadly poison!")
        self.breath_available = False
        timer = dice.d4()
        self.breath_timer = timer
        print("The Breath Weapon can't be used again for", timer, "rounds.")

        save_list = []
        if override == 0 or override == 5:
            for enemy in range(len(target_list)):
                save = dice.d20() + target_list[enemy].fortitude - target_list[enemy].status_penalty - target_list[enemy].rk_circumstance_penalty
                save_list.append(save)
        else:
            for i in range(len(target_list)):
                save_list.append(15)

        damage = 0
        for i in range(9):
            damage += dice.d6()

        for save in range(len(save_list)):
            if override == 0:
                time.sleep(1.5)
            print("")
            print(target_list[save].name, "makes a Fortitude save! They roll", str(save_list[save]) + ".")
            
            if save_list[save] >= self.spell_dc + 10 - self.status_penalty or override == 1:
                print(target_list[save].name, "got a critical success! They take no damage.")
                print(target_list[save].name, "has", target_list[save].current_hp, "HP.")
            
            elif save_list[save] >= self.spell_dc - self.status_penalty or override == 2:
                print(target_list[save].name, "got a success! They take half damage.")
                specific_damage =  damage // 2
                print(target_list[save].name, "takes", specific_damage, "poison damage.")
                target_list[save].current_hp -= specific_damage
                print(target_list[save].name, "has", target_list[save].current_hp, "HP.")
            
            elif save_list[save] < self.spell_dc - 10 - self.status_penalty or override == 3:
                print(target_list[save].name, "got a critical failure! They take double damage.")
                specific_damage = damage * 2
                print(target_list[save].name, "takes", specific_damage, "poison damage.")
                target_list[save].current_hp -= specific_damage
                print(target_list[save].name, "has", target_list[save].current_hp, "HP.")
            
            else:
                # access with override == 4
                print(target_list[save].name, "got a failure! They take full damage.")
                print(target_list[save].name, "takes", damage, "poison damage.")
                target_list[save].current_hp -= damage
                print(target_list[save].name, "has", target_list[save].current_hp, "HP.")

    def draconic_frenzy(self, target_list, override1 = -1, override2 = -1): 
        '''
        Method: draconic_frenzy
        Parameters: self, list - list of PC's; 2 ints - values to force targets
        Returns: none
        
        Selects two random targets from among the PC's. Makes a horn attack 
        against the first target and two claw attacks against the second. Makes
        new calls to strike() for these actions to change their action usage.

        Performs input sanitization on the output of random_target(); if the 
        selected target has 0 HP, they aren't a valid target, and a new roll is
        made. If all four PC's have 0 HP, ends the loop and the dragon attacks
        the lifeless bodies of whoever the last targets rolled were.

        Override values bypass random selection: override1 assigns first target, 
        override2 assigns second target
        '''
        stop = False
        fail_set = set([])
        while stop == False:
            t1 = hf.random_target(target_list, override1)
            if t1.current_hp > 0:
                stop = True
            else:
                fail_set.add(t1)
            if len(fail_set) == 4:
                stop = True
            
        stop = False
        while stop == False:
            t2 = hf.random_target(target_list, override2)
            if t2.current_hp > 0:
                stop = True
            else:
                fail_set.add(t2)
            if len(fail_set) == 4:
                stop = True

        print(self.name, "goes into a Draconic Frenzy! It makes a flurry of attacks!")
        super().strike(t1,"Horn",1,12,"piercing",7,True,False,False,False,False,0)
        print("")
        super().strike(t2,"Claw",2,8,"slashing",8,False,True,False,False,False,0)
        print("")
        super().strike(t2,"Claw",2,8,"slashing",8,False,True,False,False,False,0)
        self.actions -= 2

    def frightful_presence(self, target_list): 
        '''
        Method: frightful_presence
        Parameters: self, list - list of PC's
        Returns: none
        
        Attempts to demoralize all player characters. Resets the 
        been_demoralized attribute for each after, since frightful presence
        doesn't count as a demoralize attempt.
        '''
        for i in range(len(target_list)):
            self.demoralize(target_list[i])
            target_list[i].been_demoralized = False
            self.actions = 3
