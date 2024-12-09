# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Wizard
'''
Contains the Wizard class, a child class of Creature. Generates the attributes
and methods for the Wizard player character.
'''
# https://2e.aonprd.com/Classes.aspx?ID=39
import dice
from creature import Creature
import helper_functions as hf
import time

class Wizard(Creature):
    '''
    Class: Wizard
    Attributes:
        team: used to determine whether take_turn() or ai() is called on the object's turn
        spell_attack: used for spell attack rolls such as the Ignition spell
        dex_attack_bonus: used for the dagger's attack rolls
        spell_dc: the difficulty class of the wizard's spells
        action_list: used by take_turn(), lists the actions the Wizard player character can take
        query_list: used to detail what the above actions do
        spell_list: lists the spells the Wizard character can cast
        spell_query: used to detail what the above spells do
        invis_target: stores the current target of the Invisibility spell so it can be removed on the Wizard's turn.
        casts_gust_of_wind: uses remaining of the Gust of Wind spell
        casts_force_barrage: uses remaining of the Force Barrage spell
        casts_invisibility: uses remaining of the Invisiblity spell
        casts_thunderstrike: uses remaining of the Thunderstrike spell
        casts_fireball: uses remaining of the Fireball spell
        casts_haste: uses remaining of the Haste spell
    Methods:
        constructor: generates an object
        start_turn: inherits the start_turn method of Creature, adds functionality to reset Invisiblity spell
        take_turn: interface function to allow the player to select actions on the wizard's turn
        
        ### Cantrip Methods - cantrips are spells that can be used infinitely ###
            electric_arc: cantrip, deals 4d4 electricity damage to two targets on a basic Reflex save
            frostbite: cantrip, deals 4d4 cold damage to one target on a basic Fortitude save
            ignition: cantrip, deals 4d6 fire damage to one target on a spell attack roll
            shield: cantrip, grants user +1 circumstance bonus to AC until the start of their next turn
        
        ### Spell Methods - spells can be used a finite amount of times. All wizard spells can be used twice ###
            gust_of_wind: spell, two targets make Fortitude saves or be off-guard until the start of their next turns
            force_barrage: spell, 1-3 actions, selects the same number of targets to take 1d4+1 force damage with no chance to avoid
            invisiility: spell, target is automatically hidden until the start of the wizard's next turn
            thunderstrike: spell, target makes a basic Reflex save or takes 2d12 electricity + 2d4 sonic damage.
            fireball: spell, all enemies makes a basic Reflex save or takes 6d6 fire damage.
            haste: spell, target gains an extra action.
        
        ### Weapon Method ###
            dagger_strike: makes a Strike with the dagger.
    
    Class contains methods and attributes that are specific to the Wizard 
    player character. When called, generates an object of Creature to inherit
    using a prescribed set of arguments. Uses the attributes of Creature to 
    calculate spell_attack, dex_attack_bonus, and spell_dc; the rest of the 
    Wizard specific attributes are for specific use cases:

    The four list attributes (action_list, query_list, spell_list, and 
    spell_query) are used by the take_turn() method, allowing the user to
    respectively select an action, see what said action does, select a spell,
    and see what said spell does. 

    The invis_target attribute is used by the start_turn() and invisibility() 
    methods; invisibility() assigns it an object as a value as part of its 
    runtime, and start_turn() uses said object to remove the benefits of the 
    Invisiblity spell when the duration has expired.

    Finally the "casts" set of variables control how many uses the Wizard has
    of its six leveled spells. Each spell can be used two times per playthrough.
    '''
    def __init__(self, name):
        '''
        Method: Constructor
        Parameters: self, any - input that will be converted to a string if it is not already and stored as self.name
        Returns: none; creates objects of class Wizard

        Creates objects of the Wizard class. 
        '''
        super().__init__(str(name),0,3,3,4,2,0,"medium",5,48,21,1,2,2,1,0,2,0,0,0,1,0,"society",20)
        self.team = "ally"
        self.spell_attack = self.intelligence + self.level + 2
        self.dex_attack_bonus = self.dexterity + self.level + 2 + 1
        self.spell_dc = self.spell_attack + 10
        
        self.action_list = ["Spells", "Strike: Dagger", "Recall Knowledge", "Seek", "Pass", "Info"]
        self.query_list = ["Spells", "Strike: Dagger", "Recall Knowledge", "Seek", "Pass"]
        self.spell_list = ["Electric Arc", "Frostbite", "Ignition", "Shield", "Gust of Wind", "Force Barrage",
                           "Invisibility", "Thunderstrike", "Fireball", "Haste", "Info"]
        self.spell_query = ["Electric Arc", "Frostbite", "Ignition", "Shield", "Gust of Wind", "Force Barrage",
                           "Invisibility", "Thunderstrike", "Fireball", "Haste"]
        
        self.invis_target = None
        
        self.casts_gust_of_wind = 2
        self.casts_force_barrage = 2
        self.casts_invisibility = 2
        self.casts_thunderstrike = 2
        self.casts_fireball = 2
        self.casts_haste = 2

    def start_turn(self):
        '''
        Method: start_turn
        Parameters: self
        Returns: none
        
        Calls the parent start_turn() function and adds the wizard specific 
        functionality to remove the invisibility spell from a target.
        '''
        super().start_turn()
        if self.invis_target:
            print(self.invis_target.name, "is no longer invisible.")
            self.invis_target.not_hidden()
            self.invis_target = None

    def take_turn(self, ally_list, enemy_list, override1 = 0, override2 = 0, override3 = 0, override4 = 0, override5 = -1):
        '''
        Method: take_turn
        Parameters: self, 2 lists: list of all allies and enemies objects respectively; 5 int, values to bypass user input and force results
        Returns: none
        
        Interface function to allow the player to select actions on the 
        wizard's turn. 

        First sets the loop variable: as long as an action has not been taken, 
        the function will loop. Then proceeds to take user input via the 
        target_select() helper function which returns a string from the lists 
        of strings it is passed as parameters (action_list, query_list, 
        spell_list, spell_query). The result is compared against the set of 
        options to determine what action is taken. If the "Info" action/spell 
        is selected, the user is prompted for input again, and information 
        about their choice is printed.
        '''
        start = self.actions
        while start == self.actions:
            try:
                if override1 == 0:
                    act = hf.target_select(self.action_list, "option")
                else:
                    act = override1
                if act == "Info":
                    query = hf.target_select(self.query_list, "option")
                    if query == "Spells":
                        print("The list of spells", self.name, "has available.")
                    elif query == "Strike: Dagger":
                        print("1 action. Strike with", self.name + "'s dagger. +11 to hit, 2d4 piercing damage.")
                    elif query == "Recall Knowledge":
                        print("1 action. Attempt to recall information about a target to make their saving throws less effective.")
                    elif query == "Seek":
                        print("1 action. Search for a hidden target, or closely examine a visible target.")
                    elif query == "Pass":
                        print("1-3 actions. Ends the current turn.")

                elif act == "Spells" or act == 1:
                    if override2 == 0:
                        spell = hf.target_select(self.spell_list, "spell")
                    else: 
                        spell = override2

                    if spell == "Info":
                        query = hf.target_select(self.spell_query, "spell")
                        if query == "Electric Arc":
                            print("2 actions, Cantrip.")
                            print("Select two targets. Each target takes 4d4 electricity damage with a basic Reflex save.")
                        elif query == "Frostbite":
                            print("2 actions, Cantrip.")
                            print("Select one target to take 4d4 cold damage with a basic Fortitude save.")
                        elif query == "Ignition":
                            print("2 actions, Cantrip.")
                            print("Make a spell attack against one target, dealing 4d6 fire damage on a hit.")
                        elif query == "Shield":
                            print("1 action, Cantrip.")
                            print("A magical barrier grants the caster +1 to AC until the start of their next turn.")
                        elif query == "Gust of Wind":
                            print("2 actions, Rank 1:", self.casts_gust_of_wind, "uses remaining.")
                            print("Select 2 targets. Each target makes a Fortitude save, becoming off-guard on a failure.")
                        elif query == "Force Barrage": 
                            print("1-3 actions, Rank 1:", self.casts_force_barrage, "uses remaining.")
                            print("Choose 1-3 targets depending on how many actions are spent. Each target takes 1d4 + 1 force damage.")
                        elif query == "Invisibility": 
                            print("2 actions, Rank 2:", self.casts_invisibility, "uses remaining.")
                            print("Select an ally. They become invisible, and are hidden from all foes.")
                        elif query == "Thunderstrike": 
                            print("2 actions, Rank 2:", self.casts_thunderstrike, "uses remaining.")
                            print("Choose a target to make a basic Reflex save or take 2d12 electricity and 2d4 sonic damage.")
                        elif query == "Fireball": 
                            print("2 actions, Rank 3:", self.casts_fireball, "uses remaining.")
                            print("All enemies make a basic Reflex save or take 6d6 fire damage.")
                        elif query == "Haste": 
                            print("2 actions, Rank 3:", self.casts_haste, "uses remaining.")
                            print("Select an ally. They gain an extra action to use each turn for the remainder of the encounter.")

                    elif spell == "Electric Arc" or spell == 1: 
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
                        self.electric_arc(target_list, override3)  

                    elif spell == "Frostbite" or spell == 2: 
                        if self.actions < 2:
                            raise ValueError
                        target = hf.target_select(enemy_list, "target")
                        self.frostbite(target, override3)

                    elif spell == "Ignition" or spell == 3: 
                        if self.actions < 2:
                            raise ValueError
                        target = hf.target_select(enemy_list, "target")
                        self.ignition(target)

                    elif spell == "Shield" or spell == 4: 
                        self.shield()

                    elif spell == "Gust of Wind" or spell == 5: 
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
                        self.gust_of_wind(target_list, override3)

                    elif spell == "Force Barrage" or spell == 6: 
                        self.force_barrage(enemy_list, override4, override5)

                    elif spell == "Invisibility" or spell == 7: 
                        if self.actions < 2:
                            raise ValueError
                        target = hf.target_select(ally_list, "target")
                        self.invisibility(target)

                    elif spell == "Thunderstrike" or spell == 8: 
                        if self.actions < 2:
                            raise ValueError
                        target = hf.target_select(enemy_list, "target")
                        self.thunderstrike(target, override3)

                    elif spell == "Fireball" or spell == 9:
                        if self.actions < 2:
                            raise ValueError
                        self.fireball(enemy_list, override3)

                    elif spell == "Haste" or spell == 10: 
                        if self.actions < 2:
                            raise ValueError
                        target = hf.target_select(ally_list, "target")
                        self.haste(target)
                        
                elif act == "Strike: Dagger" or act == 2:
                    target = hf.target_select(enemy_list, "target")
                    self.dagger_strike(target)

                elif act == "Recall Knowledge" or act == 3:
                    target = hf.target_select(enemy_list, "target")
                    self.recall_knowledge(target)

                elif act == "Seek" or act == 4:
                    target = hf.target_select(enemy_list, "target")
                    self.seek(target)

                elif act == "Pass" or act == 5:
                    self.actions = 0

            except ValueError:
                print(self.name, "doesn't have enough actions left for that.")

    def electric_arc(self, target_list, override = 0): 
        # https://2e.aonprd.com/Spells.aspx?ID=1509
        '''
        Method: electric_arc
        Parameters: self, list - list of two targets to affect, int - override to force a result
        Returns: none
        
        Functionality for the electric arc spell. Each target takes 4d4 
        electricity damage on a basic Reflex save.

        Since Electric Arc is a cantrip and can be used an unlimited number of
        times, it doesn't have a usage limit to check. Function first deducts 
        the 2 action cost of the spell, then prints a message based on how many
        targets are passed to the function.
        
        If no override variable is passed or an override of 5 (bypass calls to
        time.sleep() but otherwise function as normal), rolls a Reflex save for
        each target and appends it to a list to use later. If an override 
        variable other than 0 (default) or 5 is passed, each save is locked to 
        15 to force a failure on the save later on. The function then rolls 
        damage (4d4).

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
        if len(target_list) == 1:
            print(self.name, "casts Electric Arc on", target_list[0].name + '!')
        elif len(target_list) == 2:
            print(self.name, "casts Electric Arc on", target_list[0].name, "and", str(target_list[1].name) + "!")
        
        save_list = []
        if override == 0 or override == 5:
            for i in range(len(target_list)):
                save = dice.d20() + target_list[i].reflex - target_list[i].status_penalty - target_list[i].rk_circumstance_penalty
                save_list.append(save)

        else:
            for i in range(len(target_list)):
                save = 15
                save_list.append(save)

        damage = 0
        for i in range(4):
            damage += dice.d4()

        for save in range(len(save_list)):
            if override == 0:
                time.sleep(1.5)
            print(target_list[save].name, "makes a Reflex save! They roll", str(save_list[save]) + ".")

            if save_list[save] >= self.spell_dc + 10 - self.status_penalty or override == 1:
                print(target_list[save].name, "got a critical success! They take no damage.")
                print(target_list[save].name, "has", target_list[save].current_hp, "HP.")

            elif save_list[save] >= self.spell_dc - self.status_penalty or override == 2:
                print(target_list[save].name, "got a success! They take half damage.")
                specific_damage = damage // 2
                print(target_list[save].name, "takes", specific_damage, "electricity damage.")
                target_list[save].current_hp -= specific_damage
                print(target_list[save].name, "has", target_list[save].current_hp, "HP.")

            elif save_list[save] < self.spell_dc - 10 - self.status_penalty or override == 3:
                print(target_list[save].name, "got a critical failure! They take double damage.")
                specific_damage = damage * 2
                print(target_list[save].name, "takes", damage, "electricity damage.")
                target_list[save].current_hp -= specific_damage
                print(target_list[save].name, "has", target_list[save].current_hp, "HP.")

            else:
                # access with override == 4
                print(target_list[save].name, "got a failure! They take full damage.")
                print(target_list[save].name, "takes", damage, "electricity damage.")
                target_list[save].current_hp -= damage
                print(target_list[save].name, "has", target_list[save].current_hp, "HP.")

    def frostbite(self, target, override = 0): 
        # https://2e.aonprd.com/Spells.aspx?ID=1539
        '''
        Method: frostbite
        Parameters: self, object - target of attack; int - value to force a result
        Returns: none
        
        Functionality for the Frostbite spell. Target makes a basic Fortitude 
        save, taking 4d4 cold damage on a failure.

        Since Frostbite is a cantrip and can be used an unlimited number of 
        times, it doesn't have a usage limit to check. Function first deducts 
        the 2 action cost of the spell, then prints a message.
        
        If no override variable is passed or an override of 5 (bypass calls to
        time.sleep() but otherwise function as normal), rolls a Fortitude save 
        for the target. If an override  variable other than 0 (default) or 5 is 
        passed, the save is locked to 15 to force a failure on the save later 
        on. The function then rolls damage (4d4).

        Finally, the function determines which degree of success the save 
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
        print(self.name, "casts Frostbite on", str(target.name) + "!")

        if override == 0 or override == 5:
            save = dice.d20() + target.fortitude - target.status_penalty - target.rk_circumstance_penalty
        else:
            save = 15
        
        damage = 0
        for i in range(4):
            damage += dice.d4()

        if override == 0:
            time.sleep(1.5)
        print(target.name, "makes a Fortitude save! They roll", str(save) + ".")

        if save >= self.spell_dc + 10 - self.status_penalty or override == 1:
            print(target.name, "got a critical success! They take no damage.")

        elif save >= self.spell_dc - self.status_penalty or override == 2:
            print(target.name, "got a success! They take half damage.")
            damage //= 2
            print(target.name, "takes", damage, "cold damage.")
            target.current_hp -= damage  

        elif save < self.spell_dc - 10 - self.status_penalty or override == 3:
            print(target.name, "got a critical failure! They take double damage.")
            damage *= 2
            print(target.name, "takes", damage, "cold damage.")
            target.current_hp -= damage

        else:
            # access with override == 4
            print(target.name, "got a failure! They take full damage.")
            print(target.name, "takes", damage, "cold damage.")
            target.current_hp -= damage

        print(target.name, "has", target.current_hp, "HP.")
   
    def ignition(self, target):
        # https://2e.aonprd.com/Spells.aspx?ID=1565
        '''
        # Method: ignition
        # Parameters: self, object - target of the attack; int, value to force a result
        # Returns: none

        # Functionality for the Ignition spell. User makes a spell attack against
        # the target, dealing 4d6 fire damage on a hit and double on a crit.

        Function is handled by the strike() function of Creature using its 
        parameter options: target is target, weapon_name is "Ignition", 
        damage_dice = 4, die_size = 6, damage_type = "fire", damage_bonus = 0,
        finesse, agile, cleric, and rogue = False, wizard = True, and 
        action_cost = 2.

        Since Ignition is a cantrip, doesn't check if uses are available.

        Uses normal multiple attack penalty: -5 on second attack, -10 on third +
        '''
        super().strike(target,"Ignition",4,6,"fire",0,False,False,False,False,True,2)
        time.sleep(1.5)

    def shield(self): 
        # https://2e.aonprd.com/Spells.aspx?ID=1671
        '''
        Method: shield
        Parameters: self
        Returns: none
        
        Functionality for the Shield spell. Gives the user a +1 circumstance
        bonus to AC until the start of its next turn for a cost of 1 action.

        Since Shield is a cantrip, doesn't check if uses are available.
        '''
        self.actions -= 1
        print(self.name, "casts Shield!")
        print("A magical barrier grants them +1 AC until the start of their next turn.")
        self.circumstance_bonus = 1
        time.sleep(1)

    def gust_of_wind(self, target_list, override = 0): 
        # https://2e.aonprd.com/Spells.aspx?ID=1550
        '''
        Method: gust_of_wind
        Parameters: self, list - list of targets; int - value to force a result
        Returns: none

        Functionality for the Gust of Wind spell. Each target makes a Fortitude
        save, becoming off guard on a failure and taking 2d6 bludgeoning damage
        on a critical fail.

        Function first checks if the user has uses of Gust of Wind remaining.
        If yes, deducts a use of casts_gust_of_wind and the 2 action cost of the 
        spell, then prints a message.
        
        If no override variable is passed or an override of 5 (bypass calls to
        time.sleep() but otherwise function as normal), rolls a Fortitude save for
        the target and appends it to a list to use later. If an override 
        variable other than 0 (default) or 5 is passed, the save is locked to 
        15 to force a failure on the save later on. 

        Finally, the function determines which degree of success the save 
        gets, with values greater than or equal to spell_dc being a success 
        and having no effect, values less than spell_dc being a failure and 
        leaving the target off-guard, and values less than spell_dc - 10 being 
        a critical failure, leaving the target off-guard and dealing 2d6 damage.

        Override values are used for testing purposes, with 0 being the default
        and not doing anything, 1 causing a success, 2 causing a crit fail, 3
        causing a fail, and 5 running the function as normal but bypassing calls
        to time.sleep().
        '''
        if self.casts_gust_of_wind <= 0:
            print(self.name, "is out of uses for Gust of Wind.")
        else:
            self.casts_gust_of_wind -= 1
            self.actions -= 2

            if len(target_list) == 1:
                print(self.name, "casts Gust of Wind on", target_list[0].name + "!")
            elif len(target_list) == 2:
                print(self.name, "casts Gust of Wind on", target_list[0].name, "and", str(target_list[1].name + "!"))

            save_list = []
            if override == 0 or override == 5:
                for i in range(len(target_list)):
                    save = dice.d20() + target_list[i].fortitude - target_list[i].status_penalty - target_list[i].rk_circumstance_penalty
                    save_list.append(save)
                    
            else:
                for i in range(len(target_list)):
                    save = 15
                    save_list.append(save)

            for save in range(len(save_list)):
                if override == 0:
                    time.sleep(1.5)
                print(target_list[save].name, "makes a Fortitude save! They roll", str(save_list[save]) + ".")

                if save_list[save] >= self.spell_dc - self.status_penalty or override == 1:
                    print(target_list[save].name, "got a success! The spell has no effect.")

                elif save_list[save] < self.spell_dc - 10 - self.status_penalty or override == 2:
                    print(target_list[save].name, "got a critical failure!")
                    target_list[save].be_off_guard_all()
                    print(target_list[save].name, "is off-guard and damaged from the wind!")
                    damage = 0
                    for i in range(2):
                        damage += dice.d6()
                    print(target_list[save].name, "takes", damage, "bludgeoning damage.")
                    target_list[save].current_hp -= damage
                    print(target_list[save].name, "has", target_list[save].current_hp, "HP.")
                    
                else:
                    # access with override == 3
                    print(target_list[save].name, "got a failure!")
                    target_list[save].be_off_guard_all()
                    print(target_list[save].name, "is off-guard from the wind!")

    def force_barrage(self, target_list, override = 0, override2 = -1): 
        # https://2e.aonprd.com/Spells.aspx?ID=1536
        '''
        Method: force_barrage
        Parameters: self, dict- dictof all possible targets; 2 ints - input bypass
        Returns: none

        Functionality for the Force Barrage spell. Prompts the user for how 
        many actions they want to spend, then uses that value as the range for
        a for loop which repeats the spell that many times, selecting a target
        and dealing damage to it separately each time.

        Function first checks if there are uses of Force Barrage remaining. If
        so, deducts a usage of casts_force_barrage and begins a loop to collect
        user input for how many actions will be spent on the spell, 1, 2, or 
        3, which can't be greater than the number of actions the user has 
        remaining. Once valid input is collected, exits the loop. If value is
        passed to override, bypasses user input and sets the value of override 
        as the number of actions used instead. 

        Function then deducts the selected action cost and begins another loop
        which takes user input to select a target if no value is entered for
        override2; if there is an argument, uses that to select the target
        instead. The target takes 1d4 + 1 damage, and the iteration of the loop 
        ends. If an invalid target is selected, raises a TypeError until a 
        valid target is chosen; this shouldn't be reachable with the 
        target_select() function in use, but was left in just in case.

        override bypasses user input for selecting the number of actions spent.
        override2 bypasses user input for target selection.
        '''
        if self.casts_force_barrage <= 0:
            print(self.name, "is out of uses of Force Barrage.")
        else:
            self.casts_force_barrage -= 1
            print(self.name, "casts Force Barrage!")

            stop = False
            if override == 0:
                while stop == False:
                    try:
                        action_choice = int(input("How many actions will they use: 1, 2, or 3?\n"))
                        valid = [1, 2, 3]
                        if action_choice not in valid:
                            raise TypeError("Enter 1, 2, or 3.")
                        elif action_choice > self.actions:
                            raise TypeError("Can't spend that many actions.\n" + str(self.name) + " has " + str(self.actions) + " actions remaining.")
                        else:
                            stop = True
                    except TypeError as err:
                        print(err)
                    except ValueError:
                        print("Enter a number.")
            else:
                action_choice = override

            self.actions -= action_choice
            for i in range(action_choice):
                valid = False
                while valid == False:
                    try:
                        if override2 == -1:
                            target = hf.target_select(target_list, "target")
                        else: target = target_list[override2]
                        if target:
                            damage = dice.d4() + 1
                            print(target.name, "takes", damage, "force damage.")
                            target.current_hp -= damage
                            print(target.name, "has", target.current_hp, "HP.")
                            valid = True
                            time.sleep(1)
                        else:
                            raise TypeError("Select a target in the encounter.")
                    except TypeError as err:
                        print(err)
            
    def invisibility(self, target): 
        # https://2e.aonprd.com/Spells.aspx?ID=1577
        '''
        Method: invisibility
        Parameters: self, object - target of the spell
        Returns: none
        
        Functionality for the Invisibility spell. Target is made hidden with no
        check. Target is stored so the condition can be removed at the start
        of the user's next turn. Unlike tabletop, invisibility lasts until the
        start of the user's next turn even if a hostile action is taken, but 
        only ever lasts one turn.

        Checks if the user has uses of Invisibility remaining. If yes, deducts
        a use of casts_invisibility and the 2 action cost, then applies the
        hidden condition to the target and stores its object to invis_target 
        for later use.
        '''
        if self.casts_invisibility <= 0:
            print(self.name, "is out of uses of Invisibility.")
        else:
            self.casts_invisibility -= 1
            self.actions -= 2
            print(self.name, "casts Invisibility on", target.name + "!")
            self.invis_target = target
            target.be_hidden()
            print(target.name, "vanishes from sight!")
            time.sleep(1.5)

    def thunderstrike(self, target, override = 0): 
        # https://2e.aonprd.com/Spells.aspx?ID=1721
        '''
        Method: thunderstrike
        Parameters: self, object - target of the spell; int - value to force a result
        Returns: none
        
        Functionality for the Thunderstrike spell upcast to Rank 2. Target
        makes a basic Reflex save or takes 2d12 electricity and 2d4 sonic 
        damage.

        Function first checks if there are uses of Thunderstike remaining. If
        so, deducts a use of casts_thunderstrike and the 2 action cost of the 
        spell, then prints a message.
        
        If no override variable is passed or an override of 5 (bypass calls to
        time.sleep() but otherwise function as normal), rolls a Reflex save 
        for the target. If an override variable other than 0 (default) or 5 is 
        passed, the save is locked to 15 to force a failure on the save later 
        on. The function then rolls damage (2d12 + 2d4).

        Finally, the function determines which degree of success the save 
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
        if self.casts_thunderstrike <= 0:
            print(self.name, "is out of uses of Thunderstrike.")
        else:
            self.casts_thunderstrike -= 1
            self.actions -= 2
            print(self.name, "casts Thunderstrike on", target.name + "!")

            if override == 0 or override == 5:
                save = dice.d20() + target.reflex - target.status_penalty - target.rk_circumstance_penalty
            else:
                save = 15

            damage1 = 0
            damage2 = 0
            for i in range(2):
                damage1 += dice.d12()
                damage2 += dice.d4()

            if override == 0:
                time.sleep(1.5)
            print(target.name, "makes a Reflex save! They roll", str(save) + ".")

            if save >= self.spell_dc + 10 - self.status_penalty or override == 1:
                print(target.name, "got a critical success! They take no damage.")

            elif save >= self.spell_dc - self.status_penalty or override == 2:
                print(target.name, "got a success! They take half damage.")
                damage1 //= 2
                damage2 //= 2
                print(target.name, "takes", damage1, "electricity and", damage2, "sonic damage.")
                target.current_hp -= (damage1 + damage2)

            elif save < self.spell_dc - 10 - self.status_penalty or override == 3:
                print(target.name, "got a critical failure! They take double damage.")
                damage1 *= 2
                damage2 *= 2
                print(target.name, "takes", damage1, "electricity and", damage2, "sonic damage.")
                target.current_hp -= (damage1 + damage2)

            else:
                # access with override == 4
                print(target.name, "got a failure! They take full damage.")
                print(target.name, "takes", damage1, "electricity and", damage2, "sonic damage.")
                target.current_hp -= (damage1 + damage2)

            print(target.name, "has", target.current_hp, "HP.")

    def fireball(self, target_list, override = 0): 
        # https://2e.aonprd.com/Spells.aspx?ID=1530
        '''
        Method: fireball
        Parameters: self, list - list of all enemies in encounter; int, value to force a result
        Returns: none
        
        Functionality for the Fireball spell. All enemies make a basic Reflex
        save or take 6d6 fire damage.

        Function first checks if there are uses of Fireball, then deducts a use
        of casts_fireball and the 2 action cost of the spell, then prints a 
        message.
        
        If no override variable is passed or an override of 5 (bypass calls to
        time.sleep() but otherwise function as normal), rolls a Reflex save for
        each target and appends it to a list to use later. If an override 
        variable other than 0 (default) or 5 is passed, each save is locked to 
        15 to force a failure on the save later on. The function then rolls 
        damage (6d6).

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
        if self.casts_fireball <= 0:
            print(self.name, "is out of uses of Fireball.")
        else:
            self.casts_fireball -= 1
            self.actions -= 2
            print(self.name, "casts Fireball!")

            save_list = []
            if override == 0 or override == 5:
                for enemy in range(len(target_list)):
                    save = dice.d20() + target_list[enemy].reflex - target_list[enemy].status_penalty - target_list[enemy].rk_circumstance_penalty
                    save_list.append(save)
            else:
                for i in range(len(target_list)):
                    save_list.append(15)

            damage = 0
            for i in range(6):
                damage += dice.d6()

            for save in range(len(save_list)):
                if override == 0:
                    time.sleep(1.5)
                print(target_list[save].name, "makes a Reflex save! They roll", str(save_list[save]) + ".")

                if save_list[save] >= self.spell_dc + 10 - self.status_penalty or override == 1:
                    print(target_list[save].name, "got a critical success! They take no damage.")
                    print(target_list[save].name, "has", target_list[save].current_hp, "HP.")

                elif save_list[save] >= self.spell_dc - self.status_penalty or override == 2:
                    print(target_list[save].name, "got a success! They take half damage.")
                    specific_damage = damage // 2
                    print(target_list[save].name, "takes", specific_damage, "fire damage.")
                    target_list[save].current_hp -= specific_damage
                    print(target_list[save].name, "has", target_list[save].current_hp, "HP.")

                elif save_list[save] < self.spell_dc - 10 - self.status_penalty or override == 3:
                    print(target_list[save].name, "got a critical failure! They take double damage.")
                    specific_damage = damage * 2
                    print(target_list[save].name, "takes", specific_damage, "fire damage.")
                    target_list[save].current_hp -= specific_damage
                    print(target_list[save].name, "has", target_list[save].current_hp, "HP.")

                else:
                    # access with override == 4
                    print(target_list[save].name, "got a failure! They take full damage.")
                    print(target_list[save].name, "takes", damage, "fire damage.")
                    target_list[save].current_hp -= damage
                    print(target_list[save].name, "has", target_list[save].current_hp, "HP.")
        
    def haste(self, target): 
        # https://2e.aonprd.com/Spells.aspx?ID=1553
        '''
        Method: haste
        Parameters: self, object - target of the spell
        Returns: none

        Functionality for the Haste spell. Gives the recipient an extra action.
        Should only be usable for Strike and Stride actions, but we're going to 
        try the Baldur's Gate route and see what broken things can be done if 
        there are no restrictions. 

        First checks if there are uses of Haste remaining. If yes, deducts a 
        use of casts_haste and the 2 action cost of the spell, then sets the
        extra_actions attribute of the target to 1.
        '''
        if self.casts_haste <= 0:
            print(self.name, "is out of uses of Haste.")
        else:
            self.casts_haste -= 1
            self.actions -= 2
            print(self.name, "casts Haste on", target.name + "!")
            target.extra_actions = 1
            print(target.name + "'s movements speed up! They gain an extra action each turn.")
            time.sleep(1)

    def dagger_strike(self, target): 
        # https://2e.aonprd.com/Weapons.aspx?ID=358
        '''
        Method: dagger_strike
        Parameters: self, object - target of the attack
        Returns: none
        
        Makes a Strike action using the wizard's +1 striking dagger.

        Function is handled by the strike() function of Creature using its 
        parameter options: target is target, weapon_name is "Dagger", 
        damage_dice = 2, die_size = 4, damage_type = "piercing", damage_bonus
        = 0, finesse, agile = True, cleric, rogue, wizard = False, and 
        action_cost = 1.

        Uses agile multiple attack penalty: -4 on the second attack, -8 on third +
        '''
        super().strike(target,"Dagger",2,4,"piercing",0,True,True,False,False,False,1)
        time.sleep(1.5)
