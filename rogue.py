# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Rogue
'''
Contains the Rogue class, a child class of Creature. Generates the attributes
and methods for the Rogue player character.
'''
# https://2e.aonprd.com/Classes.aspx?ID=37
import dice
from creature import Creature
import helper_functions as hf
import time

class Rogue(Creature):
    '''
    Class: Rogue
    Attributes:
        team: used to determine whether take_turn() or ai() is called on the object's turn
        dex_attack_bonus: used for the shortsword's attack rolls
        action_list: used by take_turn(), lists the actions the Rogue player character can take
        query_list: used to detail what the above actions do
    Methods:
        constructor: generates an object
        take_turn: interface function to allow the player to select actions on the rogue's turn
        twin_feint: 2 actions. Makes two attacks against one target; the target is automatically off-guard against the second attack.
        shortsword_strike: makes a Strike with the shortsword.

    Class contains methods and attributes that are specific to the Rogue 
    player character. When called, generates an object of Creature to inherit
    using a prescribed set of arguments. Uses the attributes of Creature to 
    calculate dex_attack_bonus.

    The two list attributes (action_list and query_list) are used by the 
    take_turn() method, allowing the user to respectively select an action and
    see what it does.
    '''
    def __init__(self, name):
        '''
        Method: constructor
        Parameters: self, any - input that will be converted to a string if it is not already and stored as self.name
        Returns: none; creates objects of class Rogue

        Creates objects of the Rogue class.
        '''
        super().__init__(name,0,4,3,0,2,3,"medium",5,68,23,1,2,2,2,2,0,0,2,0,0,2,"society",20)
        self.team = "ally"
        self.dex_attack_bonus = self.dexterity + self.level + 4 + 1
        self.action_list = ["Twin Feint", "Strike: Shortsword", "Hide", "Tumble Through", "Seek", "Pass", "Info"]
        self.query_list = ["Twin Feint", "Strike: Shortsword", "Hide", "Tumble Through", "Seek", "Pass"]

    def take_turn(self, ally_list, enemy_list):
        '''
        Method: take_turn
        Parameters: self, 2 lists: list of all allies and enemies objects respectively
            Note: ally_list is not used by any Rogue methods, but needs to be accepted
            as an argument so that calls to take_turn() can be compatible with all four
            player classes.
        Returns: none

        Interface function to allow the player to select actions on the 
        rogue's turn.

        First sets the loop variable: as long as an action has not been taken, 
        the function will loop. Then proceeds to take user input via the 
        target_select() helper function which returns a string from the lists 
        of strings it is passed as parameters (action_list, query_list). 
        The result is compared against the set of options to determine what 
        action is taken. If the "Info" action/attack is selected, the user is 
        prompted for input again, and information about their choice is printed.
        '''
        start = self.actions
        while start == self.actions:
            try:
                act = hf.target_select(self.action_list, "option")
                if act == "Info": 
                    query = hf.target_select(self.query_list, "option")
                    if query == "Twin Feint": 
                        print("2 actions, 2 attacks. Makes two shortsword Strikes against one target.")
                        print("The target is automatically off-guard against the second attack.")
                    elif query == "Strike: Shortsword": 
                        print("1 action. Strike with", self.name + "'s shortsword. + 14 to hit, 2d6 + 4 piercing damage.")
                        print("If the target of", self.name + "'s attacks is off guard, they take an additional 2d6 damage.")
                    elif query == "Hide": 
                        print("1 action. Attempts to hide from all enemies in the encounter, making them off-guard to", self.name + ".")
                    elif query == "Tumble Through": 
                        print("1 action. Tumbles behind a target, making them off-guard to", self.name + "'s attacks.")
                    elif query == "Seek":
                        print("1 action. Search for a hidden target, or closely examine a visible target.")
                    elif query == "Pass":
                        print("1-3 actions. Ends the current turn.")

                elif act == "Twin Feint": 
                        if self.actions < 2:
                            raise ValueError
                        target = hf.target_select(enemy_list, "target")
                        self.twin_feint(target)

                elif act == "Strike: Shortsword": 
                    target = hf.target_select(enemy_list, "target")
                    self.shortsword_strike(target)

                elif act == "Hide": 
                    self.hide(enemy_list)

                elif act == "Tumble Through": 
                    target = hf.target_select(enemy_list, "target")
                    self.tumble_through(target)

                elif act == "Seek":
                    target = hf.target_select(enemy_list, "target")
                    self.seek(target)

                elif act == "Pass":
                    self.actions = 0

            except ValueError:
                print(self.name, "doesn't have enough actions left for that.")

    def twin_feint(self, target): 
        # https://2e.aonprd.com/Feats.aspx?ID=4921
        '''
        Method: twin_feint
        Parameters: self, object - target of the attacks
        Returns: none
        
        Functionality for the Twin Feint feat. Makes two attacks, with the 
        target automatically off-guard against the second.

        Doesn't need a separate action cost step since the shortsword_strike()
        calls both cost one action, totaling the correct amount.
        '''
        print(self.name, "performs a Twin Feint!")
        self.shortsword_strike(target)
        if target.off_guard_specific == False:
            target.be_off_guard_specific()
            self.shortsword_strike(target)
            target.not_off_guard_specific()
        else:
            self.shortsword_strike(target)

    def shortsword_strike(self, target): 
        # https://2e.aonprd.com/Weapons.aspx?ID=398
        # https://2e.aonprd.com/Feats.aspx?ID=4930
        '''
        Method: shortsword_strike
        Parameters: self, object - target of the attack
        Returns: none
        
        Makes a Strike with the rogue's +1 striking shortsword. Incorporates
        functionality of the Dread Striker feat: if the target is Frightened,
        they are also off-guard to the rogue.

        The attack portion of the function is handled by the strike() method of
        Creature using its parameter options: weapon name is "Shortsword", 
        damage_dice = 2, die_size = 6, damage_type = "piercing", damage_bonus
        = 4, finesse, agile = True, cleric = False, rogue = True, wizard = False,
        and action_cost = 1.
        '''
        if target.status_penalty > 0 and target.off_guard_specific == False:
            print(target.name + "'s fear makes them off-guard to", self.name + "!")
            target.be_off_guard_specific()
        super().strike(target, "Shortsword",2,6,"piercing",4,True,True,False,True,False,1)
        time.sleep(1.5)

