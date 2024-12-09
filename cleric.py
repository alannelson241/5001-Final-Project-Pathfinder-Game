# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Cleric
'''
Contains the Cleric class, a child class of Creature. Generates the attributes
and methods for the Cleric player character.
'''
# https://2e.aonprd.com/Classes.aspx?ID=33
import dice
from creature import Creature
import helper_functions as hf
import time

class Cleric(Creature):
    '''
    Class: Cleric
    Attributes:
        team: used to determine whether take_turn() or ai() is called on the object's turn
        spell_attack: used for spell attack rolls such as the Divine Lance spell
        attack_bonus: used for the mace's attack rolls
        spell_dc: the difficulty class of the cleric's spells
        action_list: used by take_turn(), lists the actions the Cleric player character can take
        query_list: used to detail what the above actions do
        spell_list: lists the spells the Cleric character can cast
        spell_query: used to detail what the above spells do
        casts_bless: uses remaining of the Bless spell
        casts_sudden_blight: uses remaining of the Sudden Blight spell
        casts_fear: uses remaining of the Fear spell
        casts_heal: uses remaining of the Heal spell
    Methods:
        constructor: generates an object
        take_turn: interface function to allow the player to select actions on the cleric's turn

    ### Cantrip Methods - cantrips are spells that can be used infinitely ###
        divine_lance: cantrip, deals 4d4 spirit damage on a spell attack roll

    ### Spell Methods - spells can be used a finite amount of times. Bless, Sudden Blight, and Fear can be used three times; Heal can be used 5 times
        bless: spell, all allies gain a +1 status bonus to attack rolls for the rest of the encounter.
        sudden_blight: spell, all enemies make a basic Fortitude save or take 2d10 void damage.
        fear: spell, all enemies make a Will save, becoming Frightened 1 on a success, 2 on a fail, or 3 on a crit fail.
        heal: spell, 1-3 actions:
            1 action: heals one ally 3d10
            2 actions: heals one ally 3d10 + 24
            3 actions: heals all allies 3d10

    ### Weapon/Other Methods ###
        mace_strike: makes a Strike with the mace.
        raise_a_shield: grants the user +2 circumstance bonus to AC until the start of their next turn.

    Class contains methods and attributes that are specific to the Cleric 
    player character. When called, generates an object of Creature to inherit
    using a prescribed set of arguments. Uses the attributes of Creature to 
    calculate spell_attack, attack_bonus, and spell_dc; the rest of the 
    Cleric specific attributes are for specific use cases:

    The four list attributes (action_list, query_list, spell_list, and 
    spell_query) are used by the take_turn() method, allowing the user to
    respectively select an action, see what said action does, select a spell,
    and see what said spell does. 

    Finally the "casts" set of variables control how many uses the Cleric has
    of its four leveled spells. Each spell can be used three times per 
    playthrough, except Heal which can be used five times.
    '''
    def __init__(self, name):
        '''
        Method: constructor
        Parameters: self, any - input that will be converted to a string if it is not already and stored as self.name
        Returns: none; creates objects of class Cleric
        
        Creates objects of the Cleric class.
        '''
        super().__init__(str(name),3,0,2,0,4,3,"medium",5,63,24,2,1,2,2,0,0,2,0,2,0,0,"society",20)
        self.team = "ally"
        self.spell_attack = self.wisdom + self.level + 2
        self.attack_bonus = self.strength + self.level + 2 + 1
        self.spell_dc = self.spell_attack + 10

        self.action_list = ["Spells", "Strike: Mace", "Raise a Shield", "Battle Medicine", "Trip", "Seek", "Pass", "Info"]
        self.query_list = ["Spells", "Strike: Mace", "Raise a Shield", "Battle Medicine", "Trip", "Seek", "Pass"]
        self.spell_list = ["Divine Lance", "Bless", "Sudden Blight", "Fear", "Heal", "Info"]
        self.spell_query = ["Divine Lance", "Bless", "Sudden Blight", "Fear", "Heal"]
        
        self.casts_bless = 3
        self.casts_sudden_blight = 3
        self.casts_fear = 3
        self.casts_heal = 5

    def take_turn(self, ally_list, enemy_list):
        '''
        Method: take_turn
        Parameters: self, 2 lists: list of all allies and enemies objects respectively
        Returns: none
        
        Interface function to allow the player to select actions on the 
        cleric's turn. 

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
                act = hf.target_select(self.action_list, "option")
                if act == "Info":
                    query = hf.target_select(self.action_list, "option")
                    if query == "Spells": 
                        print("The list of spells", self.name, "has available.")
                    elif query == "Strike: Mace": 
                        print("1 action. Strike with", self.name + "'s mace. + 11 to hit, 2d6 + 3 bludgeoning damage.")
                    elif query == "Raise a Shield": 
                        print("1 action.", self.name, "raises their shield, granting +2 to AC until the start of their next turn.")
                    elif query == "Battle Medicine": 
                        print("1 action. Makes a medicine check to attempt to perform non-magical healing, restoring 2d8 + 10 hp on a success.")
                    elif query == "Trip": 
                        print("1 action. Trip attack, success inflicts the off-guard condition, a penalty to the target's AC.")
                    elif query == "Seek":
                        print("1 action. Search for a hidden target, or closely examine a visible target.")
                    elif query == "Pass":
                        print("1-3 actions. Ends the current turn.")

                elif act == "Spells":
                    spell = hf.target_select(self.spell_list, "spell")
                    if spell == "Info":
                        query = hf.target_select(self.spell_query, "spell")
                        if query == "Divine Lance": 
                            print("2 actions, Cantrip.")
                            print("Make a spell attack against one target, dealing 4d4 spirit damage on a hit.")
                        elif query == "Bless": 
                            print("2 actions, Rank 1:", self.casts_bless, "uses remaining.")
                            print("Provides all allies  +1 bonus to attack rolls for the rest of the encounter.")
                        elif query == "Sudden Blight": 
                            print("2 actions, Rank 2:", self.casts_sudden_blight, "uses remaining.")
                            print("All enemies make a basic Fortitude save or take 2d10 void damage.")
                        elif query == "Fear": 
                            print("2 actions, Rank 3:", self.casts_fear, "uses remaining.")
                            print("All enemies make a Will save, becoming frightened 1 on a success, 2 on a failure, or 3 on a critical fail.")
                        elif query == "Heal": 
                            print("1-3 actions, Rank 3:", self.casts_heal, "uses remaining.")
                            print("1 action: one ally regains 3d10 HP.")
                            print("2 actions: one ally regains 3d10 + 24 HP.")
                            print("3 actions: all allies regain 3d10 HP.")

                    elif spell == "Divine Lance": 
                        if self.actions < 2:
                            raise ValueError
                        target = hf.target_select(enemy_list, "target")
                        self.divine_lance(target)

                    elif spell == "Bless":
                        if self.actions < 2:
                            raise ValueError
                        self.bless(ally_list)

                    elif spell == "Sudden Blight":
                        if self.actions < 2:
                            raise ValueError
                        self.sudden_blight(enemy_list)

                    elif spell == "Fear":
                        if self.actions < 2:
                            raise ValueError
                        self.fear(enemy_list)

                    elif spell == "Heal":
                        self.heal(ally_list)

                elif act == "Strike: Mace": 
                    target = hf.target_select(enemy_list, "target")
                    self.mace_strike(target)

                elif act == "Raise a Shield": 
                    self.raise_a_shield()

                elif act == "Battle Medicine": 
                    target = hf.target_select(ally_list, "target")
                    self.battle_medicine(target)

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
                
    def divine_lance(self, target): 
        # https://2e.aonprd.com/Spells.aspx?ID=1498
        '''
        Method: divine_lance
        Parameters: self, object - target of the attack
        Returns: none
        
        Functionality for the Divine Lance spell. Makes a spell attack roll
        against the target, dealing 4d4 spirit damage on a hit and double on a
        crit.

        Function is handled by the strike() function of Creature using its
        parameter options: target is target, weapon_name is "Divine Lance", 
        damage_dice = 4, die_size = 4, damage_type = "spirit", damage_bonus = 0,
        finesse, agile = False, cleric = True, rogue, wizard = False, and
        action_cost = 2.

        Since Divine Lance is a cantrip, doesn't check if uses are available.

        Uses normal multiple attack penalty: -5 on second attack, -10 on third +
        '''
        super().strike(target,"Divine Lance",4,4,"spirit",0,False,False,True,False,False,2)

    def bless(self, target_list): 
        # https://2e.aonprd.com/Spells.aspx?ID=1451
        '''
        Method: bless
        Parameters: self, list - list of all ally objects
        Returns: none
        
        Functionality for the Bless spell. First checks if the user has uses of
        Bless remaining. If yes, deducts a use of cast_bless and the 2 action 
        cost of the spell, then prints a message.
        
        Finally, loops through target_list and grants each ally a +1 status 
        bonus to attack rolls.
        '''
        if self.casts_bless <= 0:
            print(self.name, "is out of uses for Bless.")
        else:
            self.casts_bless -= 1
            self.actions -= 2
            print(self.name, "casts Bless! Their allies gain a +1 bonus to attack rolls!")
            for ally in range(len(target_list)):
                target_list[ally].status_bonus = 1

    def sudden_blight(self, target_list, override = 0): 
        # https://2e.aonprd.com/Spells.aspx?ID=2033
        '''
        Method: sudden_blight
        Parameters: self, list - list of all enemy objects; int - value to force a result
        Returns: none
        
        Functionality for the Sudden Blight spell. Deals 2d10 void damage on a 
        basic Fortitude save to all enemies. 

        Function first checks if there are uses of Sudden Blight, then deducts
        a use of casts_sudden_blight and the 2 action cost of the spell, then 
        prints a message.
        
        If no override variable is passed or an override of 5 (bypass calls to
        time.sleep() but otherwise function as normal), rolls a Fortitude save for
        each target and appends it to a list to use later. If an override 
        variable other than 0 (default) or 5 is passed, each save is locked to 
        15 to force a failure on the save later on. The function then rolls 
        damage (2d10).

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
        if self.casts_sudden_blight <= 0:
            print(self.name, "is out of uses for Sudden Blight.")
        else:
            self.casts_sudden_blight -= 1
            self.actions -= 2
            print(self.name, "casts Sudden Blight!")

            save_list = []
            if override == 0 or override == 5:
                for enemy in range(len(target_list)):
                    save = dice.d20() + target_list[enemy].fortitude - target_list[enemy].status_penalty - target_list[enemy].rk_circumstance_penalty
                    save_list.append(save)
            else:
                for i in range(len(target_list)):
                    save_list.append(15)

            damage = 0
            for i in range(2):
                damage += dice.d10()

            for save in range(len(save_list)):
                if override == 0:
                    time.sleep(1.5)
                print(target_list[save].name, "makes a Fortitude save! They roll", str(save_list[save]) + ".")
              
                if save_list[save] >= self.spell_dc + 10 - self.status_penalty or override == 1:
                    print(target_list[save].name, "got a critical success! They take no damage.")
                    print(target_list[save].name, "has", target_list[save].current_hp, "HP.")
                
                elif save_list[save] >= self.spell_dc - self.status_penalty or override == 2:
                    print(target_list[save].name, "got a success! They take half damage.")
                    specific_damage = damage // 2
                    print(target_list[save].name, "takes", specific_damage, "void damage.")
                    target_list[save].current_hp -= specific_damage
                    print(target_list[save].name, "has", target_list[save].current_hp, "HP.")
                
                elif save_list[save] < self.spell_dc - 10 - self.status_penalty or override == 3:
                    print(target_list[save].name, "got a critical failure! They take double damage.")
                    specific_damage = damage * 2
                    print(target_list[save].name, "takes", specific_damage, "void damage.")
                    target_list[save].current_hp -= specific_damage
                    print(target_list[save].name, "has", target_list[save].current_hp, "HP.")
                
                else:
                    # access with override == 4
                    print(target_list[save].name, "got a failure! They take full damage.")
                    print(target_list[save].name, "takes", damage, "void damage.")
                    target_list[save].current_hp -= damage
                    print(target_list[save].name, "has", target_list[save].current_hp, "HP.")

    def fear(self, target_list, override = 0): 
        # https://2e.aonprd.com/Spells.aspx?ID=1524
        '''
        Method: fear
        Parameters: self, list - list of all enemy objects; int - value to force a result
        Returns: none
        
        Functionality for the Fear spell upcast to Rank 3. All enemies make a 
        Will save, becoming Frightened 1 on a success, 2 on a failure, and 3 on
        a critical failure.

        Function first checks if the user has uses of Fear remaining. If yes,
        deducts a use of casts_fear and the 2 action cost of the spell, then 
        prints a message.

        If no override variable is passed or an override of 5 (bypass calls to
        time.sleep() but otherwise function as normal), rolls a Will save for
        the target and appends it to a list to use later. If an override 
        variable other than 0 (default) or 5 is passed, the save is locked to 
        15 to force a failure on the save later on. 

        Finally, the function determines which degree of success the save gets,
        with values greater than or equal to spell_dc + 10 being a critical 
        success and having no effect, values greater than or equal to spell_dc 
        being a success and leaving the target Frightened 1, values less than
        spell_dc being a failure and leaving the target Frightened 2, and 
        values less than spell_dc -10 being a critical failure and leaving the
        target Frightened 3. Frightened values are applied as a status_penalty.

        Override values are used for testing purposes, with 0 being the default
        and not doing anything, 1 causing a crit success, 2 causing a success, 3
        causing a crit fail, 4 causing a fail, and 5 running the function as 
        normal but bypassing calls to time.sleep().
        '''
        if self.casts_fear <= 0:
            print(self.name, "is out of uses for Fear.")
        else:
            self.casts_fear -= 1
            self.actions -= 2
            print(self.name, "casts Fear!")
            save_list = []
            
            if override == 0 or override == 5:
                for enemy in range(len(target_list)):
                    save = dice.d20() + target_list[enemy].will - target_list[enemy].status_penalty - target_list[enemy].rk_circumstance_penalty
                    save_list.append(save)
            else:
                for i in range(len(target_list)):
                    save_list.append(15)
            
            for save in range(len(save_list)):
                if override == 0:
                    time.sleep(1.5)
                print(target_list[save].name, "makes a Will save! They roll", str(save_list[save]) + ".")
                
                if save_list[save] >= self.spell_dc + 10 - self.status_penalty or override == 1:
                    print(target_list[save].name, "got a critical success! The spell has no effect.")
                
                elif save_list[save] >= self.spell_dc - self.status_penalty or override == 2:
                    if target_list[save].status_penalty == 0:
                        print(target_list[save].name, "got a success! They become Frightened 1.")
                        target_list[save].status_penalty = 1
                    else:
                        print(target_list[save].name, "got a success! They were already Frightened", str(target_list[save].status_penalty) + ".")
                
                elif save_list[save] < self.spell_dc - 10 - self.status_penalty or override == 3:
                    if target_list[save].status_penalty < 3:
                        print(target_list[save].name, "got a critical failure! They become Frightened 3.")
                        target_list[save].status_penalty = 3
                    else:
                        print(target_list[save].name, "got a critical failure! They were already Frightened", str(target_list[save].status_penalty) + ".")
                
                else:
                    # access with override == 4
                    if target_list[save].status_penalty < 2:
                        print(target_list[save].name, "got a failure! They become Frightened 2.")
                        target_list[save].status_penalty = 2
                    else:
                        print(target_list[save].name, "got a failure! They were already Frightened", str(target_list[save].status_penalty) + ".")
                
    def heal(self, target_list, override = 0): 
        # https://2e.aonprd.com/Spells.aspx?ID=1554
        # https://2e.aonprd.com/Feats.aspx?ID=4646
        '''
        Method: heal
        Parameters: self, list - list of all ally objects; int, value to bypass user input
        Returns: none
        
        Functionality for the Heal spell upcast to Rank 3. Takes 1, 2, or 3 as 
        user input to determine how many actions to spend on the spell.

        Function first checks if there are uses of Heal remaining. If so, 
        deducts a usage of casts_heal and begins a loop to collect user input
        for how many actions will be spent on the spell: 1, 2, or 3, which
        can't be greater than the number of actions the user has remaining. 
        Once valid input is collected, exits the loop. If value is passed to
        override, bypasses user input and sets the value of override as the
        number of actions used instead.

        Function then deducts the selected action cost and executes based on 
        the number selected:        
            1 action: heals the target 3d10 HP.
            2 actions: heals the target 3d10 + 24 HP.
            3 actions: heals all allies 3d10 HP.
        If 1 or 2 are selected, prompts the user for input to determine the 
        target (This block has a try/except block, but the except condition
        shouldn't be accessible as bad input should be caught in 
        hf.target_select()).
        
        Modified by the Healing Hands feat (heals d10's instead of d8's)
        '''
        if self.casts_heal <= 0:
            print(self.name, "is out of uses for Heal.")
        else:
            self.casts_heal -= 1
            print(self.name, "casts Heal!")

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
            if action_choice == 1 or action_choice == 2:
                try:
                    if override == 0:
                        target = hf.target_select(target_list, "target")
                    else: 
                        target = target_list[0]
                    if target:
                        print(self.name, "heals", target.name + "!")
                        healing = 0
                        for i in range(3):
                            healing += dice.d10()
                        if action_choice == 2:
                            healing += 24
                        print(target.name, "regains", healing, "HP.")
                        target.current_hp += healing
                        if target.current_hp > target.max_hp:
                            target.current_hp = target.max_hp
                        print(target.name, "has", target.current_hp, "HP.")
                    else:
                        raise TypeError("Select an ally in the encounter.")
                except TypeError as err:
                    print(err)

            elif action_choice == 3:
                print(self.name, "heals all allies!")
                healing = 0
                for i in range(3):
                    healing += dice.d10()
                for ally in range(len(target_list)):
                    if override == 0:
                        time.sleep(.5)
                    print(target_list[ally].name, "regains", healing, "HP.")
                    target_list[ally].current_hp += healing
                    if target_list[ally].current_hp > target_list[ally].max_hp:
                        target_list[ally].current_hp = target_list[ally].max_hp
                    print(target_list[ally].name, "has", target_list[ally].current_hp, "HP.")

    def raise_a_shield(self): 
        # https://2e.aonprd.com/Actions.aspx?ID=2316
        '''
        Method: raise_a_shield
        Parameters: self
        Returns: none
        
        The cleric raises their shield, gaining a +2 circumstance bonus to AC 
        until the start of their next turn.
        '''
        self.actions -= 1
        print(self.name, "raises their shield! They gain +2 AC until the start of their next turn.")
        self.circumstance_bonus = 2

    def mace_strike(self, target): 
        # https://2e.aonprd.com/Weapons.aspx?ID=362
        # https://2e.aonprd.com/Feats.aspx?ID=4642
        '''
        Method: mace_strike
        Parameters: self, object - the target of the attack
        Returns: none
        
        The cleric makes a Strike with their +1 striking mace. Modified by the
        Deadly Simplicity feat (increases damage die from d6 to d8).

        Function is handled by the strike() function of Creature using its 
        parameter options: target is target, weapon_name is "Mace", 
        damage_dice = 2, die_size = 8, damage_type = "bludgeoning", damage_bonus
        = 3, finesse, agile, cleric, rogue, wizard = False, and 
        action_cost = 1.

        Uses standard multiple attack penalty: -5 on the second attack, -10 on third +
        '''
        super().strike(target, "Mace",2,8,"bludgeoning",3,False,False,False,False,False,1)

