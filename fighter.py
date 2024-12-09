# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Fighter
'''
Contains the Fighter class, a child class of Creature. Generates the attributes
and methods for the Fighter player character.
'''
# https://2e.aonprd.com/Classes.aspx?ID=35
import dice
from creature import Creature
import helper_functions as hf
import time

class Fighter(Creature):
    '''
    Class: Fighter
    Attributes:
        team: used to determine whether take_turn() or ai() is called on the object's turn
        attack_bonus: used for the greatsword's attack rolls
        action_list: used by take_turn(), lists the actions the Fighter player character can take
        query_list: used to detail what the above actions do
        special_attack_list: lists the special attacks the Fighter can use
        attack_query: used to detail what the above attacks do
        flourish: tracks if the user has made an attack with the flourish trait (Vicious Swing) this turn.
    Methods:
        constructor: generates an object
        start_turn: inherits the start_turn method of creature, adds functionality to reset the Boolean for flourish
        take_turn: interface function to allow the player to select actions on the fighter's turn

        ### Special Attacks - weapon attacks that have extra effects ###
            vicious_swing: deals an extra die of damage on a hit
            intimidating_strike: frightens the target on a hit
            swipe: uses one attack roll against two targets
        
        ### Weapon Method ###
        greatsword_strike: makes a strike with the greatsword. Used by the special attack methods

        
    Class contains methods and attributes that are specific to the Fighter
    player character. When called, generates an object of Creature to inherit
    using a preset set of arguments. Uses the attributes of Creatuer to 
    calculate attack_bonus.

    The four list attributes (action_list, query_list, special_attack_list, and
    attack_query) are used by the take_turn() method, allowing the user to 
    respectively select an action, see what action does, select a special 
    attack, and see what said attack does.

    The flourish method is used by the start_turn() and vicious_swing() methods;
    vicious_swing() sets it to True as part of its operation, preventing that
    attack from being used more than once per turn; start_turn() resets it at 
    the start of the Fighter's turn.
    '''
    def __init__(self, name):
        '''
        Method: constructor
        Parameters: self, any - value that is converted to a string if it is not already one
        Returns: none; creates objects of class Fighter

        Creates objects of the Fighter class.
        '''
        super().__init__(str(name),4,0,3,0,2,3,"medium",5,78,24,2,2,2,2,0,0,2,2,0,0,0,"society",20)
        self.team = "ally"
        self.attack_bonus = self.strength + self.level + 6 + 1
        
        self.action_list = ["Special Attacks", "Strike: Greatsword", "Demoralize", "Trip", "Seek", "Pass", "Info"]
        self.query_list = ["Special Attacks", "Strike: Greatsword", "Demoralize", "Trip", "Seek", "Pass"]
        self.special_attack_list = ["Vicious Swing", "Intimidating Strike", "Swipe", "Info"]
        self.attack_query = ["Vicious Swing", "Intimidating Strike", "Swipe"]
        
        self.flourish = False

    def start_turn(self):
        '''
        Method: start_turn
        Parameters: self
        Returns: none
        
        Calls the parent start_turn() method and adds the fighter specific
        functionality to reset the flourish attribute.
        '''
        super().start_turn()
        self.flourish = False

    def take_turn(self, ally_list, enemy_list):
        '''
        Method: take_turn
        Parameters: self, 2 lists: list of all allies and enemies objects respectively
            Note: ally_list is not used by any Fighter methods, but needs to be accepted
            as an argument so that calls to take_turn() can be compatible with all four
            player classes.
        Returns: none

        Interface function to allow the player to select actions on the 
        fighter's turn.

        FIrst sets the loop variable: as long as an action has not been taken, 
        the function will loop. Then proceeds to take user input via the 
        target_select() helper function which returns a string from the lists 
        of strings it is passed as parameters (action_list, query_list, 
        special_attack_list, attack_query). The result is compared against the 
        set of options to determine what action is taken. If the "Info" 
        action/attack is selected, the user is prompted for input again, and 
        information about their choice is printed.
        '''
        start = self.actions
        while start == self.actions:
            try:
                act = hf.target_select(self.action_list, "option")
                if act == "Info":
                    query = hf.target_select(self.query_list, "option")
                    if query == "Special Attacks":
                        print("The list of special attacks", self.name, "can perform.")
                    elif query == "Strike: Greatsword":
                        print("1 action. Strike with", self.name + "'s greatsword. + 16 to hit, 2d12 + 4 slashing damage.")
                    elif query == "Demoralize":
                        print("1 action. Attempt to demoralize an opponent to inflict the frightened condition, a penalty to all rolls.")
                        print("Each creature can be targeted once per encounter.")
                    elif query == "Trip":
                        print("1 action. Trip attack, success inflicts the off-guard condition, a penalty to the target's AC.")
                    elif query == "Seek":
                        print("1 action. Search for a hidden target, or closely examine a visible target.")
                    elif query == "Pass":
                        print("1-3 actions. Ends the current turn.")

                elif act == "Special Attacks":
                    special = hf.target_select(self.special_attack_list, "attack")
                    if special == "Info":
                        query = hf.target_select(self.attack_query, "attack")
                        if query == "Vicious Swing":
                            print("2 actions, Flourish, 2 attacks. Makes a greatsword Strike, dealing an extra d12 of damage on a hit.")
                        elif query == "Intimidating Strike":
                            print("2 actions, 1 attack. Makes a greatsword Strike, inflicting the frightened condition on a hit.")
                        elif query == "Swipe":
                            print("2 actions, 2 attacks. Makes a greatsword Strike against the AC of two targets.")
                    
                    elif special == "Vicious Swing":
                        if self.actions < 2:
                            raise ValueError
                        target = hf.target_select(enemy_list, "target")
                        self.vicious_swing(target)
                    
                    elif special == "Intimidating Strike":
                        if self.actions < 2:
                            raise ValueError
                        target = hf.target_select(enemy_list, "target")
                        self.intimidating_strike(target)
                    
                    elif special == "Swipe":
                        if self.actions < 2:
                            raise ValueError
                        target_list = []
                        target1 = hf.target_select(enemy_list, "target")
                        target_list.append(target1)
                        if len(enemy_list) > 1:
                            while len(target_list) == 1:
                                target2 = hf.target_select(enemy_list, "target")
                                if target1 == target2:
                                    print("The two targets must be different.")
                                else:
                                    target_list.append(target2) 
                        self.swipe(target_list)
                
                elif act == "Strike: Greatsword":
                    target = hf.target_select(enemy_list, "target")
                    self.greatsword_strike([target])
                
                elif act == "Demoralize":
                    target = hf.target_select(enemy_list, "target")
                    self.demoralize(target)
                
                elif act == "Trip":
                    target = hf.target_select(enemy_list, "target")
                    self.trip(target)
                
                elif act == "Seek":
                    target = hf.target_select(enemy_list, "target")
                    self.seek(target)
                
                elif act == "Pass":
                    self.actions = 0
            
            except ValueError:
                print(self.name, "doesn't have enough actions left for that.")

    def vicious_swing(self, target): 
        # https://2e.aonprd.com/Feats.aspx?ID=4775
        '''
        Method: vicious_swing
        Parameters: self, object - target of the attack
        Returns: none
        
        Functionality for the Vicious Swing feat. If the user hasn't made a 
        flourish action this turn, makes an attack against the target that
        deals an extra die of damage. Attack is otherwise functionally 
        identical to the greatsword_strike() method.
        '''
        if self.flourish == False:
            print(self.name, "winds up for a Vicious Swing against", target.name +"!")
            self.greatsword_strike([target], 3,2,2)
            self.flourish = True
        else:
            print(self.name, "can't make another attack like that this turn.")

    def intimidating_strike(self, target, override = 0): 
        # https://2e.aonprd.com/Feats.aspx?ID=4782
        '''
        Method: intimidating_strike
        Parameters: self, object - target of the attack; int, value to force a result
        Returns: none
        
        Functionality for the Intimidating Strike feat. Makes a greatsword 
        Strike against the target, who is Frightened 1 on a hit or 2 on a crit.

        Uses the return value of greatsword_strike to determine the degree of 
        success for the frightened effect.
        '''
        print(self.name, "attacks with terrifying skill! Intimidating Strike against", target.name + "!")
        result = self.greatsword_strike([target],2,2,1, override)
        if result == 2:
            print(target.name, "is Frightened 2!")
            target.be_frightened(2)
        elif result == 1:
            print(target.name, "is Frightened 1!")
            target.be_frightened(1)

    def swipe(self, target_list): 
        # https://2e.aonprd.com/Feats.aspx?ID=4795
        '''
        Method: swipe
        Parameters: self, list - list of two targets to attack
        Returns: none

        Functionality for the Swipe feat. Makes one greatsword strike against 
        two targets, rolling a single attack and damage roll for the attack.
        '''
        print(self.name, "attacks two foes at once with a mighty Swipe!")
        self.greatsword_strike(target_list,2,2,2)

    def greatsword_strike(self, target_list, damage_dice = 2, action_cost = 1, attack_cost = 1, override = 0): 
        # https://2e.aonprd.com/Weapons.aspx?ID=379
        '''
        Method: greatsword_strike
        Parameters: self, list - list of targets of the attack
        Returns: int - 0,1,2; miss, hit, crit respectively
        
        Makes a Strike action using the fighter's +1 striking greatsword. Needs
        to be bespoke to accommodate the on-crit effect from the fighter's 
        weapon mastery. Has extra parameters for compatibility with 
        other fighter methods. 
        
        Note that all targets, even for a single target Strike, must be input 
        as a list.
        
        Return value is used by intimidating_strike() to determine degrees of
        success.

        First deducts the action cost - 1 by default, but can be changed with 
        arguments to the action_cost parameter - then prints typical messages
        for an attack. Function then determines the level of multiple attack
        penalty (MAP): -0 for the first attack on a turn, -5 for the second,
        and -10 for the third and subsequent.

        Next, if no override parameter is passed, makes an attack roll. The 
        formula is:
            1d20 + attack bonus (16 for Fighter) + highest status bonus = highest status penalty - MAP penalty

        Damage is then calculated: for a typical attack, damage = 2d12 + 4, with
        the Vicious Swing attack dealing 3d12 + 4 instead.

        The function then prints a message and determines the degree of success.
        If the attack roll is greater than or equal to the target's AC with any relevant 
        modifiers applied (AC + highest circumstance bonus, - highest status 
        bonus and circumstance penalty) then the attack is a hit and deals full
        damage. If the attack roll is greater than or equal to the target's AC
        + 10 then the attack is a critical hit and deals double damage. Finally, 
        if the attack roll is less than the target's AC the attack misses and 
        deals no damage.
        '''
        self.actions -= action_cost
        print(self.name, "attacks! Greatsword strike!")
        print("They have made", self.attacks_made, "attacks so far this turn.")

        if self.attacks_made == 1:
            map_penalty = 5
        elif self.attacks_made >= 2:
            map_penalty = 10
        else:
            map_penalty = 0

        if override == 0:
            attack = dice.d20() + self.attack_bonus + self.status_bonus - self.status_penalty - map_penalty
        else: 
            attack = 0

        self.attacks_made += attack_cost
        damage = 0
        for i in range(damage_dice):
            damage += dice.d12()
        damage += self.strength

        print(self.name, "rolls", attack, "for their attack roll.")
        for enemy in range(len(target_list)):
            if attack >= target_list[enemy].ac + 10 + target_list[enemy].circumstance_bonus - target_list[enemy].status_penalty - target_list[enemy].og_circumstance_penalty or override == 1:
                print("Critical hit!", self.name + "'s might leaves", target_list[enemy].name, "off-guard!")
                specific_damage = damage * 2
                print(target_list[enemy].name, "takes", specific_damage, "slashing damage.")
                target_list[enemy].current_hp -= (specific_damage)
                print(target_list[enemy].name, "has", target_list[enemy].current_hp, "HP.")
                target_list[enemy].be_off_guard_all()
                degree = 2
            
            elif attack >= target_list[enemy].ac + target_list[enemy].circumstance_bonus - target_list[enemy].status_penalty - target_list[enemy].og_circumstance_penalty or override == 2:
                print("Hit!")           
                print(target_list[enemy].name, "takes", damage, "slashing damage.")
                target_list[enemy].current_hp -= (damage)
                print(target_list[enemy].name, "has", target_list[enemy].current_hp, "HP.")
                degree = 1
            
            else:
                # access with override == 3
                print("Miss!")
                print(target_list[enemy].name, "takes 0 damage.")
                print(target_list[enemy].name, "has", target_list[enemy].current_hp, "HP.")
                degree = 0
                
        return degree
