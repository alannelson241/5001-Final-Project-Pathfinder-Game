# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Creature
'''
Contains the Creature class, a parent class inherited by all other classes.
Creature generates standard attributes and methods common to all classes in the
game, which will be supplemented by the specific features of the other classes.
'''
import dice

class Creature():
    '''
    Class: Creature
    Attributes: 
        strength, dexterity, constitution, intelligence, wisdom, charisma - ability scores
        level, max_hp, current_hp, ac, size - direct values
        fortitude, fort_dc, will, will_dc, reflex, reflex_dc, perception, perception_dc - calculated saves
        acrobatics, arcana, athletics, intimidation, medicine, society, stealth - calculated skill values
        has_tumble_through, has_recall_knowledge, has_trip, has_demoralize, has_battle_medicine, has_hide - skill action access gates
        extra_actions, actions, attacks_made - turn-specific variables
        circumstance_bonus, rk_circumstance_penalty, og_circumstance_penalty, status_bonus, status_penalty - bonuses and penalties
        rk_skill, rk_dc - recall knowledge specific variables
        off_guard, ogg_guard_specific - control the off-guard condition, either general, applied to all enemies, or specific, only applied to one
        hidden - controls the hidden condition
        had_battle_medicine, been_demoralized, been_rk - track if a creature has been affected by a 1/encounter effect
    Methods:
        constructor - used by child classes to generate attributes and methods
        str - sets the string returned when the object is printed

        ### Condition Manipulation Methods ###
            be_frightened - applies the frightened status penalty if there is not already a greater one
            decrement_frightened - decrements the frightened status penalty
            be_off_guard_all - applies the general version of the off-guard condition 
            not_off_guard - removes the general off-guard condition
            be_off_guard_specific - applies the specific version of the off-guard condition
            not_off_guard_specific = removes the specific off-guard condition. Penalty is only reset if target is not also generally off-guard
            be_hidden - applies the hidden trait
            not_hidden - removes the hidden trait
            end_encounter - resets encounter-specific attributes to their default values.
            start_turn - resets values and effects that end on the start of a creature's turn.
            end_turn - resets values and effects that end at the end of a creature's turn.

        ### Univeral Utility Methods ###
            roll_initiative - rolls an initiative check, returning a multidimensional list of the result and the user's name
            seek - attempts to find a hidden foe or provides basic info on a non-hidden foe

        ### Skill Action Methods ###
            battle_medicine - non-magical 1/encounter healing
            demoralize - 1/encounter frightened condition
            hide - repeatable source of user-specific off-guard for all enemies
            recall_knowledge - 1/encounter circumstance penalty to saves
            trip - attack, repeatable source of general off-guard
            tumble_through - repeatable source of user-specific off-guard for one enemy

    Class contains the universal attributes and methods that are common to all
    creatures in the game. Collects as parameters information needed to 
    determine a creature's ability scores, size, level, max hit points, defenses 
    (armor class, fortitude save/dc, will save/dc, reflex save/dc), perception
    bonus/dc,  skill bonuses and skill action access, and details used by the 
    recall knowledge function. 

    Ability scores, size, level, max HP, and AC are translated directly from 
    the argument values. Ability scores and level are used to calculate 
    subsequent values.

    Save and skill bonuses are calculated using the following formula:
        ability_score + level + 2 * proficiency_rank
    Each skill is associated with a skill action. Proficiency in the skill gives 
    access to the corresponding skill action.

    Last set of variables are for specific use cases: 
        - extra_actions is affected by the Wizard's haste spell, gives an extra
        action each turn.
        - actions controls how many actions the creature can take per turn. Once 
        reduced to zero, creature's turn ends.
        - attacks_made determines the multiple attack penalty for the creature 
        this turn. Resets at the end of a creature's turn.
        - circumstance_bonus as inplemented is an AC bonus from the shield 
        spell or raise a shield action.
        - rk_circumstance_penalty - penalty to saving throws from recall knowledge
        - og_circumstance_penalty - penalty to AC from off-guard
        - status_bonus - bonus to attack rolls from bless spell or orc 
        commander's battle cry ability
        - status_penalty - penalty to all checks (including attacks) and saves
        from the frightened condition
        - rk_skill - the skill used by the recall knowledge action, either 
        arcana or society
        - rk_dc - the DC the user of recall knowledge needs to beat.
        - off_guard - tracks if the subject has the general off-guard condition, off-guard to all foes
        - off_guard_specific - tracks if the subject has the specific off-guard condition, off-guard to one foe
        - hidden - tracks if the subject has the hidden condition
        - had_battle_medicine - tracks if the subject has been targeted by the battle medicine action this encounter
        - been_demoralized - tracks if the subject has been targeted by the demoralize action this encounter
        - been_rk - tracks if the subject has been targeted by the recall knowledge action this encounter
    '''
    def __init__(self, name,  
        strn = 0, dex = 0, con = 0, intl = 0, wis = 0, cha = 0, 
        size = "medium", lvl = 1, max_hp = 10, ac = 10,
        fort_prof = 1, will_prof = 1, ref_prof = 1, perception_prof = 1,
        acrobatics = 0, arcana = 0, athletics = 0, intimidation = 0,  
        medicine = 0, society = 0, stealth = 0,
        rk_skill = "society", rk_dc = 10
        ):
        '''
        Method: constructor
        Parameters: strength, dexterity, constitution, intelligence, wisdom, charisma - core ASI values
            size, lvl, max_hp, ac - other key values, either used in calcs or otherwise universal
            fort_prof, will_prof, ref_prof, perception_prof - save proficiencies for calcs
            acrobatics, arcana, athletics, diplomacy, intimidation, medicine, society, stealth - skill proficiencies
            rk_skill, rk_dc - defaults for recall knowledge to use; changed by each child class
        Returns: none; creates an object

        Generates an object of the Creature class.
        '''
        self.name = str(name)
        # raw ASI and values from parameters
        self.strength = strn
        self.dexterity = dex
        self.constitution = con
        self.intelligence = intl
        self.wisdom = wis
        self.charisma = cha
        self.level = lvl
        self.max_hp = max_hp
        self.current_hp = self.max_hp
        self.ac = ac
        self.size = size

        # calculated saves
        self.fortitude = self.constitution + self.level + 2 * fort_prof
        self.fort_dc = self.fortitude + 10
        self.will = self.wisdom + self.level + 2 * will_prof
        self.will_dc = self.will + 10
        self.reflex = self.dexterity + self.level + 2 * ref_prof
        self.reflex_dc = self.reflex + 10
        self.perception = self.wisdom + self.level + 2 * perception_prof
        self.perception_dc = self.perception + 10

        # optional skills; value determined conditionally, trained in skill grants skill action access
        if acrobatics > 0:
            self.acrobatics = self.dexterity + self.level + 2 * acrobatics
            self.has_tumble_through = True
        else:
            self.acrobatics = self.dexterity
            self.has_tumble_through = False
        if arcana > 0:
            self.arcana = self.intelligence + self.level + 2 * arcana
            self.has_recall_knowledge = True
        else:
            self.arcana = self.intelligence
            if society > 0:
                self.has_recall_knowledge = True
            else: 
                self.has_recall_knowledge = False
        if athletics > 0:
            self.athletics = self.strength + self.level + 2 * athletics
            self.has_trip = True
        else: 
            self.athletics = self.strength
            self.has_trip = False
        if intimidation > 0:
            self.intimidation = self.charisma + self.level + 2 * intimidation
            self.has_demoralize = True
        else:
            self.intimidation = self.charisma
            self.has_demoralize = False
        if medicine > 0:
            self.medicine = self.wisdom + self.level + 2 * medicine
            self.has_battle_medicine = True
        else:
            self.medicine = self.wisdom
            self.has_battle_medicine = False
        if society > 0:
            self.society = self.intelligence + self.level + 2 * society
            self.has_recall_knowledge = True
        else: 
            self.society = self.intelligence
            if arcana > 0:
                self.has_recall_knowledge = True
            else: 
                self.has_recall_knowledge = False
        if stealth > 0:
            self.stealth = self.dexterity + self.level + 2 * stealth
            self.has_hide = True
        else: 
            self.stealth = self.dexterity
            self.has_hide = False

        # other universal values
        # extra actions sources: haste spell
        self.extra_actions = 0
        self.actions = 3 + self.extra_actions
        self.attacks_made = 0
        # circumstance bonuses: shield spell to ac, raise shield
        self.circumstance_bonus = 0
        # circumstance penalties: recall knowledge, off-guard
        self.rk_circumstance_penalty = 0
        self.og_circumstance_penalty = 0
        # status bonuses: bless spell
        self.status_bonus = 0
        # status penalties: frightened
        self.status_penalty = 0
        # default value for testing rk_skill and rk_dc, overwritten by each child class
        self.rk_skill = rk_skill
        self.rk_dc = rk_dc
        # off guard sources: trip, fighter crit, gust of wind spell, twin feint 2nd hit, 
        # hide, tumble through, rogue dread striker if frightened
        # basic off-guard applies for all creatures on the other team
        self.off_guard = False
        # specific is for when one creature is off-guard to another, 
        # gets reset at the end of the current turn.
        self.off_guard_specific = False
        self.hidden = False
        self.had_battle_medicine = False
        self.been_demoralized = False
        self.been_rk = False

        # dummy values that are replaced in child classes, needed for strike method
        self.dex_attack_bonus = 0
        self.spell_attack = 0
        self.attack_bonus = 0  
        
    def __str__(self):
        return f'{self.name}'
    
    def be_frightened(self, value):
        # https://2e.aonprd.com/Conditions.aspx?ID=19 
        '''
        Method: be_frightened
        Parameters: self, int - frightened value
        Returns: none
        
        Applies the frightened condition to a creature and increases the status
        penalty by the same amount if it is not greater.

        Since frightened is the only source of a status penalty implemented, 
        can use the status penalty as a tracker for frightened level.
        '''
        if self.status_penalty < value:
            self.status_penalty = value

    def decrement_frightened(self): 
        '''
        Method: decrement_frightened
        Parameters: self
        returns: none
        
        Function to decrement the frightened condition at the end of a 
        creature's turn.
        '''
        if self.status_penalty > 0:
            self.status_penalty -= 1

    def be_off_guard_all(self): 
        # https://2e.aonprd.com/Conditions.aspx?ID=58
        '''
        Method: be_off_guard_all
        Parameters: self
        Returns: none
        
        Function toggles on the off-guard condition. Also applies the value for
        the off-guard circumstance penalty.
        '''
        if self.off_guard == False:
            self.off_guard = True
            self.og_circumstance_penalty = 2

    def not_off_guard(self):
        '''
        Method: not_off_guard
        Parameters: self
        Returns: none
        
        Function toggles off the off-guard condition. Also resets the value for
        the off-guard circumstance penalty.
        '''
        if self.off_guard == True:
            self.off_guard = False
            self.og_circumstance_penalty = 0

    def be_off_guard_specific(self):
        '''
        Method: be_off_guard_specific
        Parameters: self
        Returns: none

        Function toggles the specific version of the off-guard condition. If 
        the target is not already off-guard (general), applies the value for
        the off-guard circumstance penalty.
        '''
        if self.off_guard == False:
            if self.off_guard_specific == False:
                self.off_guard_specific = True
                self.og_circumstance_penalty = 2
        elif self.off_guard == True:
            if self.off_guard_specific == False:
                self.off_guard_specific = True
    
    def not_off_guard_specific(self):
        '''
        Method: not_off_guard_specific
        Parameters: self
        Returns: none
        
        Function toggles off the specific version of the off-guard condition. 
        If the target is not already off-guard (general), removes the value for
        the off-guard circumstance penalty.
        '''
        if self.off_guard == False:
            if self.off_guard_specific == True:
                self.off_guard_specific = False
                self.og_circumstance_penalty = 0
        elif self.off_guard == True:
            if self.off_guard_specific == True:
                self.off_guard_specific = False

    def be_hidden(self):
        # https://2e.aonprd.com/Rules.aspx?ID=2416 
        # https://2e.aonprd.com/Conditions.aspx?ID=79 
        '''
        Method: be_hidden
        Parameters: self
        Returns: none
        
        Toggles the hidden state on.
        '''
        if self.hidden == False:
            self.hidden = True

    def not_hidden(self): 
        '''
        Method: not_hidden
        Parameters: self
        Returns: none
        
        Toggles the hidden state off.
        '''
        if self.hidden == True:
            self.hidden = False

    def end_encounter(self):
        '''
        Method: end_encounter
        Parameters: self
        Returns: none
        
        Resets per-encounter values to their default states.
        '''
        self.extra_actions = 0
        self.circumstance_bonus = 0
        self.rk_circumstance_penalty = 0
        self.og_circumstance_penalty = 0
        self.status_bonus = 0
        self.status_penalty = 0
        self.current_hp = self.max_hp
        self.off_guard = False
        self.off_guard_specific = False
        self.hidden = False
        self.had_battle_medicine = False
        self.been_demoralized = False
        self.been_rk = False

    def start_turn(self):
        '''
        Method: start_turn
        Parameters: self
        Returns: none
        
        Resets rk_circumstance_penalty, hidden, off_guard, circumstance_bonus, 
        and actions at the start of a creature's turn. Corresponding messages 
        are printed if the value is changed.
        '''
        if self.rk_circumstance_penalty > 0:
            print(self.name, "is no longer vulnerable from Recall Knowledge.")
        self.rk_circumstance_penalty = 0
        if self.hidden == True:
            print(self.name, "is no longer hidden.")
        self.not_hidden()
        if self.off_guard == True:
            print(self.name, "is no longer off-guard.")
        self.not_off_guard()
        if self.circumstance_bonus == 1:
            print(self.name + "'s Shield spell fades.")
        elif self.circumstance_bonus == 2:
            print(self.name, "lowers their shield.")
        self.circumstance_bonus = 0
        self.actions = 3 + self.extra_actions
        if self.current_hp < 0:
            self.current_hp = 0

    def end_turn(self, encounter_list):
        '''
        Method: end_turn
        Parameters: self, list - list of all objects in the encounter
        Returns: none
        
        Resets any instances of off_guard_specific in the encounter, sets any 
        HP value less than 0 to 0, resets the value of attacks_made, and
        decrements the frightened condition.
        '''
        for char in encounter_list:
            if char.off_guard_specific == True:
                print(char.name, "is no longer off-guard to", self.name + ".")
                char.not_off_guard_specific()
            if char.current_hp < 0:
                char.current_hp = 0
        self.attacks_made = 0
        if self.status_penalty > 0:
            self.decrement_frightened()
            print(self.name, "is now frightened", str(self.status_penalty) + ".")

    def roll_initiative(self): 
        # https://2e.aonprd.com/Rules.aspx?ID=2539
        '''
        Method: roll_initiative
        Parameters: self
        Returns: list: [initiative value, object]
        
        Rolls an initiative check for the creature. Returns a multidimensional
        list containing the initiative value and the creature's name to be 
        sorted into an initiative order.
        '''
        check = dice.d20() + self.perception - self.status_penalty
        print(self.name, "Rolls", check, "for initiative.")
        return [check, self]

    def seek(self, target): 
        # https://2e.aonprd.com/Actions.aspx?ID=2301
        '''
        Method: seek
        Parameters: self, object - the target to seek
        Returns: none
        
        Does two things. If used on a hidden target, attempts a perception 
        check against target's stealth dc, ending hidden condition on success.
        If used on a visible target, gives some basic info: a message is 
        printed depending on how far the target's current HP is from its max,
        as well as the target's AC. 
        '''
        self.actions -= 1
        if target.hidden == True:
            print(self.name, "searches for", target.name + ".")
            check = dice.d20() + self.perception - self.status_penalty
            print(self.name, "rolls", check, "for Perception.")

            if (check) >= (target.stealth + 10 - target.status_penalty):
                print(target.name, "was spotted! They're no longer hidden!")
                target.hidden = False
            else:
                print(self.name, "couldn't find", target.name, "this time.")

        else:
            print(self.name, "examines", target.name +".")
            message = ''
            if target.current_hp > target.max_hp / 2:
                message += target.name + " is still going strong.\n"
                
            elif target.current_hp <= target.max_hp / 2 and target.current_hp > target.max_hp / 4:
                message += target.name + " is bloodied! Keep going!\n"

            elif target.current_hp < target.max_hp / 4:
                message += target.name + " is barely hanging in there!\n"

            message += "Based on their armor, " + target.name + " has " + str(target.ac) + " AC."
            print(message)

    def battle_medicine(self, target, override = 0):
        # https://2e.aonprd.com/Feats.aspx?ID=5125
        # https://2e.aonprd.com/Actions.aspx?ID=2399
        '''
        Method: battle_medicine
        Parameters: self, object - the target to heal, int - a value to force a result
        Returns: none
        
        Rolls a medicine check against the Expert DC and heals the target based 
        on the result. If the check succeeds, sets the flag that the target 
        can't be targeted by battle medicine again this encounter.

        Function first checks if the target has already been targeted by 
        battle_medicine() in the current encounter, ending the function if so.
        If the target is valid, sets its had_battle_medicine attribute to True 
        and prints a message.

        If no override value is provided, a medicine check is rolled, followed
        by healing being rolled depending on the anticipated degree of success:
        checks greater than or equal to 30 heal 4d8 + 10; checks greater than or 
        equal to 20 heal 2d8 + 10; checks less than 20 heal nothing, and checks
        less than 10 deal 1d8 damage.

        Override arguments can be used to get a specific degree of success for
        testing purposes: 1 gives a critical success, 2 a success, 3 a critical
        failure, and 4 a failure.
        '''
        if target.had_battle_medicine == True:
            print(target.name, "has already recieved battle medicine this encounter.")

        else:
            self.actions -= 1
            target.had_battle_medicine = True
            print(self.name, "attempts battle medicine on", target.name + ".")
            if override == 0:
                check = dice.d20() + self.medicine - self.status_penalty
            else: 
                check = 10
            print(self.name, "rolls", check, "for Medicine.")

            healing = 0
            if check >= 30 or override == 1:
                for i in range(4):
                    healing += dice.d8()
                healing += 10
                print("Critical success!")

            elif check >= 20 or override == 2:
                for i in range (2):
                    healing += dice.d8()
                healing += 10 
                print("Success!")

            elif check < 10 + self.medicine or override == 3:
                healing = -1 * dice.d8()
                print("Critical failure!")

            else:
                # accessed with override == 4
                healing = 0
                print("Failure!")

            if healing > 0:
                print(target.name, "heals", healing, "HP.")
                target.current_hp += healing
                if target.current_hp > target.max_hp:
                    target.current_hp = target.max_hp
                print(target.name, "has", target.current_hp, "HP.")

            elif healing == 0:
                print("Nothing happens.")

            elif healing < 0:
                print(target.name, "takes", healing, "damage.")
                target.current_hp += healing
                print(target.name, "has", target.current_hp, "HP.")

    def demoralize(self, target, override = 0): 
        # https://2e.aonprd.com/Actions.aspx?ID=2395
        '''
        Method: demoralize
        Parameters: self, object - the target enemy to affect, int - value to force a result
        returns: none
        
        Attempts an intimidation check using the user's intimidation score and
        the target's Will DC. If successful, calls be_frightened() to apply the
        penalty, with a penalty of 1 on success or 2 on critical success. A 
        creature can only have an attempt to demoralize once per combat. 

        Function first checks if the target has been targeted by demoralize 
        this encounter already. If so, ends the function; if not, prints a 
        message.

        If no value is given for an override argument, rolls a check and 
        determines the degree of success. Checks greater than or equal to 10 + 
        the target's Will DC are a critical success and inflict Frightened 2,
        checks greater than the Will DC are a success and inflict Frightened 1,
        and checks less than the DC are a failure and do nothing.

        Override arguments can be used to force a specific result for testing
        purposes. 1 yields a critical success, 2 a success, and 3 a failure.
        '''
        if target.been_demoralized == True:
            print(target.name, "has already been demoralized this encounter.")
        else:
            self.actions -= 1
            target.been_demoralized = True
            print(self.name, "attempts to demoralize", target.name + ".")

            if override == 0:
                check = dice.d20() + self.intimidation - self.status_penalty
            else: 
                check = 0                
            print(self.name, "rolls", check, "for Intimidation.")

            if check >= target.will_dc + 10 - target.status_penalty or override == 1:
                print("Critical success!")
                level = 2

            elif check >= target.will_dc - target.status_penalty or override == 2:
                print("Success!")
                level = 1

            else:
                # accessed with override == 3
                print("Failure!")
                level = 0

            target.be_frightened(level)
            if level > 0:
                print(target.name, "is frightened", str(target.status_penalty) + ".")
            else:
                print(target.name + "'s frightened level is unchanged.")
    
    def hide(self, target_list):
        # https://2e.aonprd.com/Actions.aspx?ID=2404
        '''
        Method: hide
        Parameters: self, list of objects - list of all targets to hide from
        Returns: none
        
        Attempts a stealth check against the perception DCs of all enemy 
        combatants. If the check beats all DC's, user is hidden.
        
        High risk, high reward option for causing enemies to be off-guard to 
        the user; high risk because the user needs to beat the Perception DCs
        of all enemies, high reward because if successful all enemies are left
        off-guard for the rest of the turn.
        '''
        self.actions -= 1
        print(self.name, "attempts to hide.")
        check = dice.d20() + self.stealth - self.status_penalty
        print(self.name, "rolls", check, "for stealth.")
        success = True

        for char in target_list:
            if char.perception_dc - char.status_penalty > check:
                success = False

        if success == True:
            print(self.name, "hid successfully! Their enemies can't find them.")
            for char in target_list:
                char.be_off_guard_specific()
                self.hidden = True

        else:
            print(self.name, "wasn't able to hide!")
        
    def recall_knowledge(self, target, override = 0):
        # https://2e.aonprd.com/Skills.aspx?ID=24&General=true
        # reference included even though this program essentially just does its own thing
        '''
        Method: recall_knowledge
        Parameters: self, object, the target to affect; int, value to force a result
        Returns: none
        
        Attempts a knowledge check using the target's recall knowledge DC and
        skill. On a success, applies an rk circumstance penalty based on the 
        result: 1 for success, 2 for critical success.

        Never more than one creature on a side that can use the recall knowledge
        skill action at a time, so can modify the value directly. A creature can
        only have recall knowledge used against it once per encounter.

        Function first checks if the target is valid. If no, ends the function.
        If yes, makes a check using the target's rk_skill, either Society or 
        Arcana (Society for all (including the player characters) but the 
        dragon, who uses Arcana). If an override argument is provided, bypasses
        the check and forces a result.

        Next determines degree of success: checks greater than or equal to the
        DC + 10 are a critical success and impose a circumstance penalty of 2,
        checks greater than or equal to the DC are a success and impose a 
        penalty of 1, and checks less than the DC are a failure and do nothing.

        Override arguments can be used to force a result for testing purposes.
        Override = 1 forces a critical success, 2 forces a success, and 3 
        forces a failure.
        '''
        if target.been_rk == True:
            print(target.name, "has already had knowledge recalled this encounter.")
        else:
            self.actions -= 1
            target.been_rk = True
            print(self.name, "attempts to recall knowledge about", target.name + '.')

            if override == 0:
                if target.rk_skill == 'society':
                    check = dice.d20() + self.society - self.status_penalty
                elif target.rk_skill == 'arcana':
                    check = dice.d20() + self.arcana - self.status_penalty
            else:
                check = 0

            print(self.name, "rolls", check, "for", target.rk_skill + '.')
            if check >= target.rk_dc - target.status_penalty + 10 or override == 1:
                print("Critical success!")
                value = 2

            elif check >= target.rk_dc - target.status_penalty or override == 2:
                print("Success!")
                value = 1

            else: 
                # accessed with override == 3
                print("Failure!")
                value = 0

            if value > 0:
                print(self.name, "remembered a weakness!", target.name, "is vulnerable!")
            else:
                print("No effect.")
            target.rk_circumstance_penalty = value

    def trip(self, target, override = 0): 
        # https://2e.aonprd.com/Actions.aspx?ID=2382
        '''
        Method: trip
        Parameters: self, object - the target to affect; int - value to force a result
        Returns: none
        
        User attempts to trip the target, attempting an Athletics check agains 
        the target's Reflex DC. On a critical success, target is off-guard and 
        takes damage. On a success, target is off-guard. On a critical failure,
        user is off-guard.

        Function first deducts the action cost and prints a message, then 
        determines multiple attack penalty (MAP) since trip counts as an attack.
        If no override argument is provided, makes an attack roll using 
        athletics and determines degrees of success.

        A roll greater than or equal to the target's Reflex DC + 10 is a 
        critical success, making the target off-guard and dealing 1d6 damage;
        greater than or equal to the DC are a success, making the target
        off-guard; less than the DC are a failure, doing nothing; and less than
        the DC - 10 is a critical failure, causing the user to be off-guard 
        instead.

        Override parameters can be used to force a result for testing purposes.
        1 is a critical success, 2 a success, 3 a critical failure, and 4 a 
        failure.
        '''
        self.actions -= 1
        print(self.name, "attempts a trip attack on", target.name +".")
        print("They have made", self.attacks_made, "attacks so far this turn.")

        if self.attacks_made == 1:
            map_penalty = 5
        elif self.attacks_made >= 2:
            map_penalty = 10
        else:
            map_penalty = 0

        if override == 0:
            attack = dice.d20() + self.athletics - self.status_penalty + self.status_bonus - map_penalty
        else:
            attack = 10

        self.attacks_made += 1
        print(self.name, "rolls", attack, "for Athletics.")

        if attack >= target.reflex_dc - target.status_penalty + 10 or override == 1:
            print("Critical success!")
            damage = dice.d6()
            print(target.name, "takes", damage, "bludgeoning damage.")
            target.current_hp -= damage
            print(target.name, "has", target.current_hp, "HP.")
            result = 1

        elif attack >= target.reflex_dc - target.status_penalty or override == 2:
            print("Success!")
            result = 1

        elif attack < target.reflex_dc - target.status_penalty - 10 or override == 3:
            print("Critical failure!")
            result = 0
            print("The trip attempt backfired!", self.name, "is off-guard!")
            self.be_off_guard_all()

        else:
            # access with override == 4
            print("Failure!")
            print("The trip attempt was unsuccessful.")
            result = 0

        if result == 1:
            print(target.name, "was tripped and is off-guard!")
            target.be_off_guard_all()

    def tumble_through(self, target, override = 0):
        # https://2e.aonprd.com/Actions.aspx?ID=2370
        # https://2e.aonprd.com/Feats.aspx?ID=4920 
        '''
        Method: tumble_through
        Parameters: self, object - the target to affect; int, value to force a result
        Returns: none
        
        User attempts to tumble through the target. User attempts an Acrobatics 
        check against the target's Reflex DC. Target is off-guard against the 
        user on a success (incorporates the Tumble Behind rogue feat).

        Low-risk, low-reward option for getting an opponent off-guard.

        Override arguments can be used to force a specific result for testing
        purposes. 1 is a success, 2 a failure.
        '''
        self.actions -= 1
        print(self.name, "attempts to tumble behind", target.name + '.')

        if override == 0:
            check = dice.d20() + self.acrobatics - self.status_penalty
        else: 
            check = 0

        print(self.name, "rolls", check, "for Acrobatics.")
        if check >= target.reflex_dc - target.status_penalty or override == 1:
            print("Success!")
            target.be_off_guard_specific()
            print(self.name, "rolled past them!", target.name, "is off-guard!")

        else:
            # accessed with override == 2
            print("Failure!")
            print(self.name, "couldn't get past them!")

    def strike(self, target, weapon, damage_dice, die_size, damage_type, damage_bonus, finesse = False, agile = False, cleric = False, rogue = False, wizard = False, action_cost = 1, override = 0): 
        # https://2e.aonprd.com/Actions.aspx?ID=2306
        '''
        Method: strike
        Parameters: self, object - target of the attack; str - name of the weapon; int - how many dice of damage; 
            int - size of dice; str - type of damage; int, bonus to damage rolls; bool, if attack has finesse trait; 
            bool, if attack has agile trait; bool, if attacker is a cleric; bool, if attacker is a rogue; 
            bool, if attacker is a wizard; int - number of actions for strike; int, value to force a result
        Returns: none

        Functionality for the strike action. User makes an attack roll against
        the target, dealing damage on a hit and double on a crit.

        Function first deducts action_cost from actions and prints a message.
        It then determines multiple attack penalty (MAP): if the strike does 
        not have the agile flag, MAP is -5 to the second attack a turn and -10
        to the third onward. With the agile flag, MAP is -4 and -8 respectively.

        If no override argument is provided, then makes an attack roll. The 
        roll is determined in one of four ways: if the finesse or rogue flags
        are True, uses the dex_attack_bonus for calculating the roll, derived
        from Dexerity; if the cleric or wizard flags are True, uses 
        spell_attack, calculated using Wisdom or Intelligence respectively; and
        if none of the above are true uses attack_bonus, calculated using 
        Strength.

        Next rolls damage: rolls damage_dice number of dice of die_size size, ie
        2d4 rolls 2 four sided dice. If the rogue flag is True, also adds 2d6
        sneak attack damage if the target is off-guard.

        Finally, determines degree of success. Rolls greater than or equal to 
        target AC + 10 are a critical hit and deal double damage, greater than
        or equal to AC are a hit and deal normal damage, and rolls less than AC
        are a miss and deal no damage.

        Override arguments can be used to force a result for testing purposes.
        Override = 1 yields a critical hit, 2 a hit, and 3 a miss.
        '''
        self.actions -= action_cost
        print(self.name, "attacks", str(target.name) + "!", weapon, "strike!")
        print("They have made", self.attacks_made, "attacks so far this turn.")

        if agile == False:
            if self.attacks_made == 1:
                map_penalty = 5
            elif self.attacks_made >= 2:
                map_penalty = 10
            else:
                map_penalty = 0

        elif agile == True:
            if self.attacks_made == 1:
                map_penalty = 4
            elif self.attacks_made >= 2:
                map_penalty = 8
            else: 
                map_penalty = 0

        if override == 0:
            if finesse == True or rogue == True:
                attack = dice.d20() + self.dex_attack_bonus + self.status_bonus - self.status_penalty - map_penalty
            elif cleric == True or wizard == True:
                attack = dice.d20() + self.spell_attack + self.status_bonus - self.status_penalty - map_penalty
            else:
                attack = dice.d20() + self.attack_bonus + self.status_bonus - self.status_penalty - map_penalty
        else: attack = 0

        damage = damage_bonus
        for i in range(damage_dice):
            if die_size == 4:
                damage += dice.d4()
            elif die_size == 6:
                damage += dice.d6()
            elif die_size == 8:
                damage += dice.d8()
            elif die_size == 10:
                damage += dice.d10()
            elif die_size == 12:
                damage += dice.d12()
        if rogue == True and target.og_circumstance_penalty > 0:
            print("Sneak attack!", target.name, "takes extra damage!")
            for i in range(2):
                damage += dice.d6()

        self.attacks_made += 1
        print(self.name, "rolls", attack, "for their attack roll.")

        if attack >= target.ac + 10 + target.circumstance_bonus - target.status_penalty - target.og_circumstance_penalty or override == 1:
            print("Critical hit!")
            damage *= 2
            print(target.name, "takes", damage, damage_type, "damage.")
            target.current_hp -= (damage)

        elif attack >= target.ac + target.circumstance_bonus - target.status_penalty - target.og_circumstance_penalty or override == 2:
            print("Hit!")
            print(target.name, "takes", damage, damage_type, "damage.")
            target.current_hp -= (damage)

        else:
            # access with override == 3
            print("Miss!")
            print(target.name, "takes 0 damage.")
        print(target.name, "has", target.current_hp, "HP.")

