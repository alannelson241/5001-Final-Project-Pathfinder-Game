# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Test Creature
'''
Suite of test functions for the Creature class.
'''
import unittest
from creature import Creature

class Test_Creature(unittest.TestCase):
    '''
    Class: Test_Creature
    Attributes: none
    Methods: test_constructor, test_be_frightened, test_decrement_frightened, 
        test_be_off_guard_all, test_not_off_guard, test_be_off_guard_specific,
        test_not_off_guard_specific, test_be_hidden, test_not_hidden, test_end_encounter,
        test_roll_initiative, test_seek, test_battle_medicine, test_demoralize, test_hide,
        test_recall_knowledge, test_trip, test_tumble_through
        
    Class of test functions for the Creature class.
    '''
    def test_constructor(self): 
        '''
        Method: test_constructor
        Parameters: self
        Returns: none
        
        Tests the constructor function of Creature. Verifies that all attributes
        are assigned correctly and checks all conditional assignment paths for 
        specific attributes.

        Generates and tests two objects: one with all possible default values
        (test 1) and one with assigned values for each argument (test 2). Test 1
        should check all "else" cases for skill assignment; Test 2 should check
        all "if" cases for skill assignment. Attributes that are not assigned
        from arguments are only checked for Test 1 since they should be the 
        same for both test cases.
        '''
        test_1 = Creature("Test 1")
        
        # expected value: "Test 1"
        self.assertEqual(test_1.name, "Test 1")

        # expected value: 0 for each
        self.assertEqual(test_1.strength, 0)
        self.assertEqual(test_1.dexterity, 0)
        self.assertEqual(test_1.constitution, 0)
        self.assertEqual(test_1.intelligence, 0)
        self.assertEqual(test_1.wisdom, 0)
        self.assertEqual(test_1.charisma, 0)

        # expected value: 1
        self.assertEqual(test_1.level, 1)

        # expected value: 10 for each
        self.assertEqual(test_1.max_hp, 10)
        self.assertEqual(test_1.current_hp, 10)
        self.assertEqual(test_1.ac, 10)

        # expected value: "medium"
        self.assertEqual(test_1.size, "medium")

        # expected value: 3 for each; since the values for each ability score
        # and proficiency are equal, they should all have the same value
        self.assertEqual(test_1.fortitude, 3)
        self.assertEqual(test_1.will, 3)
        self.assertEqual(test_1.reflex, 3)
        self.assertEqual(test_1.perception, 3)

        # expected value: 13 for each; same reason as above
        self.assertEqual(test_1.fort_dc, 13)
        self.assertEqual(test_1.will_dc, 13)
        self.assertEqual(test_1.reflex_dc, 13)
        self.assertEqual(test_1.perception_dc, 13)

        # expected value: 0 for each; since each skill has a proficiency of 0,
        # they are assigned the value of the ability score, also 0.
        self.assertEqual(test_1.acrobatics, 0)
        self.assertEqual(test_1.arcana, 0)
        self.assertEqual(test_1.athletics, 0)
        self.assertEqual(test_1.intimidation, 0)
        self.assertEqual(test_1.medicine, 0)
        self.assertEqual(test_1.society, 0)
        self.assertEqual(test_1.stealth, 0)

        # expected value: False; since each skill has a proficiency of 0, the
        # gates for all skill actions are set to False
        self.assertFalse(test_1.has_tumble_through)
        self.assertFalse(test_1.has_recall_knowledge)
        self.assertFalse(test_1.has_trip)
        self.assertFalse(test_1.has_demoralize)
        self.assertFalse(test_1.has_battle_medicine)
        self.assertFalse(test_1.has_hide)

        # expected value: 10
        self.assertEqual(test_1.rk_dc, 10)
        
        # expected value: "society"
        self.assertEqual(test_1.rk_skill, "society")

        # expected value: 0 for each; internal attributes which always default
        # to 0 as a starting value
        self.assertEqual(test_1.extra_actions, 0)
        self.assertEqual(test_1.attacks_made, 0)
        self.assertEqual(test_1.circumstance_bonus, 0)
        self.assertEqual(test_1.rk_circumstance_penalty, 0)
        self.assertEqual(test_1.og_circumstance_penalty, 0)
        self.assertEqual(test_1.status_bonus, 0)
        self.assertEqual(test_1.status_penalty, 0)

        # expected value: False for each; internal attributes which always 
        # default to False as a starting value
        self.assertFalse(test_1.off_guard)
        self.assertFalse(test_1.off_guard_specific)
        self.assertFalse(test_1.hidden)
        self.assertFalse(test_1.had_battle_medicine)
        self.assertFalse(test_1.been_demoralized)
        self.assertFalse(test_1.been_rk)

        # expected value: 0 for each
        self.assertEqual(test_1.spell_attack, 0)
        self.assertEqual(test_1.dex_attack_bonus, 0)
        self.assertEqual(test_1.attack_bonus, 0)

        # object 2 has arguments for each parameter that are different from default values
        test_2 = Creature("Test 2",1,1,1,1,1,1,"small",2,20,11,2,2,2,2,1,1,1,1,1,1,1,"arcana",11)

        # expected value: "Test 2"
        self.assertEqual(test_2.name, "Test 2")

        # expected value: 1 for each
        self.assertEqual(test_2.strength, 1)
        self.assertEqual(test_2.dexterity, 1)
        self.assertEqual(test_2.constitution, 1)
        self.assertEqual(test_2.intelligence, 1)
        self.assertEqual(test_2.wisdom, 1)
        self.assertEqual(test_2.charisma, 1)

        # expected value: 1
        self.assertEqual(test_2.level, 2)

        # expected value: 10 for each
        self.assertEqual(test_2.max_hp, 20)
        self.assertEqual(test_2.current_hp, 20)

        # expected value: 11
        self.assertEqual(test_2.ac, 11)

        # expected value: "small"
        self.assertEqual(test_2.size, "small")

        # expected value: 7 for each; since the values for each ability score
        # and proficiency are equal, they should all have the same value
        self.assertEqual(test_2.fortitude, 7)
        self.assertEqual(test_2.will, 7)
        self.assertEqual(test_2.reflex, 7)
        self.assertEqual(test_2.perception, 7)

        # expected value: 17 for each; same reason as above
        self.assertEqual(test_2.fort_dc, 17)
        self.assertEqual(test_2.will_dc, 17)
        self.assertEqual(test_2.reflex_dc, 17)
        self.assertEqual(test_2.perception_dc, 17)

        # expected value: 5 for each; since each skill has proficiency, they
        # are calculated with the same formula as saves 
        self.assertEqual(test_2.acrobatics, 5)
        self.assertEqual(test_2.arcana, 5)
        self.assertEqual(test_2.athletics, 5)
        self.assertEqual(test_2.intimidation, 5)
        self.assertEqual(test_2.medicine, 5)
        self.assertEqual(test_2.society, 5)
        self.assertEqual(test_2.stealth, 5)

        # expected value: True; since each skill has a proficiency of 2, the
        # gates for all skill actions are set to True
        self.assertTrue(test_2.has_tumble_through)
        self.assertTrue(test_2.has_recall_knowledge)
        self.assertTrue(test_2.has_trip)
        self.assertTrue(test_2.has_demoralize)
        self.assertTrue(test_2.has_battle_medicine)
        self.assertTrue(test_2.has_hide)

        # expected value: 11
        self.assertEqual(test_2.rk_dc, 11)
        
        # expected value: "arcana"
        self.assertEqual(test_2.rk_skill, "arcana")

    def test_be_frightened(self): 
        '''
        Method: test_be_frightened
        Parameters: self
        Returns: none
        
        Tests the be_frightened function. Generates an object of the Creature
        class and checks the value of its status_penalty attribute before and
        after running this method.
        '''
        test = Creature("Test")
        # expected value: 0
        self.assertEqual(test.status_penalty, 0)

        # expected value: 1
        test.be_frightened(1)
        self.assertEqual(test.status_penalty, 1)

    def test_decrement_frightened(self):
        '''
        Method: test_decrement_frightened
        Parameters: self
        Returns: none
        
        Tests the decrement_frightened function of the Creature class. 
        Generates a Creature object and sets its status_penaly attribute to 1,
        then runs decrement_frightened() on the object twice. The first instance
        should reduce the status_penalty to 0, and the second shouldn't do 
        anything.
        '''
        test = Creature("test")
        test.status_penalty = 1
        # expected value: 1
        self.assertEqual(test.status_penalty, 1)

        # expected value: 0
        test.decrement_frightened()
        self.assertEqual(test.status_penalty, 0)

        # expected value: 0
        test.decrement_frightened()
        self.assertEqual(test.status_penalty, 0)

    def test_be_off_guard_all(self): 
        '''
        Method: test_be_off_guard_all
        Parameters: self
        Returns: none

        Tests the be_off_guard_all function. Generates an object of the 
        Creature class and calls be_off_guard_all() on it twice. The first
        instance should toggle the off_guard condition to True and set the 
        og_circumstance_penalty to 2; the second instance shouldn't do anything.
        '''
        test = Creature('Test')
        # expected value: True
        test.be_off_guard_all()
        self.assertTrue(test.off_guard)
        # expected value: 2
        self.assertEqual(test.og_circumstance_penalty, 2)

        # expected value: True
        test.be_off_guard_all()
        self.assertTrue(test.off_guard)
        # expected value: 2
        self.assertEqual(test.og_circumstance_penalty, 2)

    def test_not_off_guard(self): 
        '''
        Method: test_not_off_guard
        Parameters: self
        Returns: none

        Tests the not_off_guard function. Generates an object of the Creature
        class and calls not_off_guard() on it once, then calls 
        be_off_guard_all() once and not_off_guard() a second time. The first 
        call to not_off_guard() should do nothing; the second should undo the 
        effect of calling be_off_guard_all().
        '''
        test = Creature("Test")
        # expected value: False
        test.not_off_guard()
        self.assertFalse(test.off_guard)
        # expected value: 0
        self.assertEqual(test.og_circumstance_penalty, 0)

        # expected value: True
        test.be_off_guard_all()
        self.assertTrue(test.off_guard)
        # expected value: 2
        self.assertEqual(test.og_circumstance_penalty, 2)

        # expected value: False
        test.not_off_guard()
        self.assertFalse(test.off_guard)
        # expected value: 0
        self.assertEqual(test.og_circumstance_penalty, 0)

    def test_be_off_guard_specific(self): 
        '''
        Method: test_be_off_guard_specific
        Parameters: self
        Returns: none
        
        Tests the be_off_guard_specific function of the Creature class. 
        Generates two objects of Creature for testing. The first has the
        be_off_guard_specific() function called on it twice; the first call 
        should apply the condition and the second should do nothing. 

        The second object has be_off_guard_all() called first before 
        be_off_guard_specific() is called twice; the off_guard_specific Boolean
        should be changed but the value of og_circumstance_penalty unaffected.
        The not_off_guard() function is then called; since the general 
        off-guard condition is only removed at the start of the subject's turn
        while the specific off-guard condition is removed at the end of the
        source's turn, the og_circumstance_penalty attribute is reset even if
        off_guard_specific is still True since it should already have been 
        reset.
        '''
        test1 = Creature("Test1")
        # expected value: True - apply off_guard_specific
        test1.be_off_guard_specific()
        self.assertTrue(test1.off_guard_specific)
        # expected value: 2
        self.assertEqual(test1.og_circumstance_penalty, 2)

        # expected value: True - off_guard_specific already applied
        test1.be_off_guard_specific()
        self.assertTrue(test1.off_guard_specific)
        # expected value: 2
        self.assertEqual(test1.og_circumstance_penalty, 2)

        test2 = Creature("Test2")
        # expected value: False - general on, specific off
        test2.be_off_guard_all()
        self.assertFalse(test2.off_guard_specific)
        # expected value: 2
        self.assertEqual(test2.og_circumstance_penalty, 2)

        # expected value: True - general on, specific on
        test2.be_off_guard_specific()
        self.assertTrue(test2.off_guard_specific)
        # expected value: 2
        self.assertEqual(test2.og_circumstance_penalty, 2)

        # expected value: True - general on, specific already on
        test2.be_off_guard_specific()
        self.assertTrue(test2.off_guard_specific)
        # expected value: 2
        self.assertEqual(test2.og_circumstance_penalty, 2)

        # expected value: True - general off, specific on:
        # general og_circumstance_penalty supercedes specific and removes penalty
        test2.not_off_guard()
        self.assertTrue(test2.off_guard_specific)
        # expected value: 0
        self.assertEqual(test2.og_circumstance_penalty, 0)

    def test_not_off_guard_specific(self):
        '''
        Method: test_not_off_guard_specific
        Parameters: self
        Returns: none
        
        Tests the not_off_guard_specific function of the Creature class. 
        Generates three Creature objects. The first object has 
        not_off_guard_specific() called three times: once right away, and twice 
        after be_off_guard_specific() has been called. The first and third 
        calls shouldn't do anything, while the second should undo the call to
        be_off_guard_specific().

        The second object has be_off_guard_all() called on it, then 
        not_off_guard_specific() is called, which shouldn't do anything. 
        be_off_guard_specific() is then called, followed by another two calls 
        to not_off_guard_specific(); the first should change the 
        off_guard_specific Boolean to False without affecting the 
        og_circumstance_penalty attribute, and the second shouldn't do anything.

        The third object has be_off_guard_specific() called, then 
        be_off_guard_all(), followed finally by not_off_guard_specific() twice,
        which should first change only the off_guard_specific Boolean and 
        nothing the second time.

        The order of precedence for og_circumstance_penalty should prioritize 
        the general condition, which is active across multiple turns, over the 
        specific condition which is only active on a single creature's turn.
        '''
        test1 = Creature("Test1")
        # expected value: False - specific already off
        test1.not_off_guard_specific()
        self.assertFalse(test1.off_guard_specific)
        # expected value: 0
        self.assertEqual(test1.og_circumstance_penalty, 0)

        # expected value: True - put specific on
        test1.be_off_guard_specific()
        self.assertTrue(test1.off_guard_specific)
        # expected value: 2
        self.assertEqual(test1.og_circumstance_penalty, 2)

        # expected value: False - remove specific
        test1.not_off_guard_specific()
        self.assertFalse(test1.off_guard_specific)
        # expected value: 0
        self.assertEqual(test1.og_circumstance_penalty, 0)

        test2 = Creature("Test2")
        test2.be_off_guard_all()
        # expected value: False - general on, specific off; removing specific does nothing
        test2.not_off_guard_specific()
        self.assertFalse(test2.off_guard_specific)
        # expected value: True
        self.assertTrue(test2.off_guard)
        # expected value: 2
        self.assertEqual(test2.og_circumstance_penalty, 2)

        # expected value: True - put specific on
        test2.be_off_guard_specific()
        self.assertTrue(test2.off_guard_specific)
        # expected value: True
        self.assertTrue(test2.off_guard)
        # expected value: 2
        self.assertEqual(test2.og_circumstance_penalty, 2)

        # expected value: False - remove specific; general takes precedence so og_circumstance_penalty is still applied
        test2.not_off_guard_specific()
        self.assertFalse(test2.off_guard_specific)
        # expected value: True
        self.assertTrue(test2.off_guard)
        # expected value: 2
        self.assertEqual(test2.og_circumstance_penalty, 2)

        test3 = Creature("Test3")
        # expected value: True - specific on first, general on second
        test3.be_off_guard_specific()
        self.assertTrue(test3.off_guard_specific)
        # expected value: 2
        self.assertEqual(test3.og_circumstance_penalty, 2)
        # expected value: True
        test3.be_off_guard_all()
        self.assertTrue(test3.off_guard)
        self.assertEqual(test3.og_circumstance_penalty, 2)

        # expected value: False - remove specific; general supercedes 
        test3.not_off_guard_specific()
        self.assertFalse(test3.off_guard_specific)
        # expected value: True
        self.assertTrue(test3.off_guard)
        # expected value: 2
        self.assertEqual(test3.og_circumstance_penalty, 2)

        # expected value: False - specific already off, no change
        test3.not_off_guard_specific()
        self.assertFalse(test3.off_guard_specific)
        # expected value: True
        self.assertTrue(test3.off_guard)
        # expected value: 2
        self.assertEqual(test3.og_circumstance_penalty, 2)

    def test_be_hidden(self): 
        '''
        Method: test_be_hidden
        Parameters: self
        Returns: none
        
        Tests the be_hidden function of the Creature class. Generates an object
        of Creature and calls be_hidden() twice; the first set the hidden 
        Boolean to True, and the second shouldn't do anything.
        '''
        test = Creature("Test")
        # expected value: False
        self.assertFalse(test.hidden)

        # expected value: True
        test.be_hidden()
        self.assertTrue(test.hidden)

        # expected value: True
        test.be_hidden()
        self.assertTrue(test.hidden)

    def test_not_hidden(self): 
        '''
        Method: test_not_hidden
        Parameters: self
        Returns: none
        
        Tests the not_hidden function of the Creature class. Generates an 
        object of Creature and calls not_hidden() once, then calls be_hidden()
        followed by not_hidden() a second time. The first call shouldn't do
        anything, while the second should undo the call to be_hidden().
        '''
        test = Creature("Test")
        # expected value: False
        test.not_hidden()
        self.assertFalse(test.hidden)

        # expected value: True
        test.be_hidden()
        self.assertTrue(test.hidden)

        # expected value: False
        test.not_hidden()
        self.assertFalse(test.hidden)

    def test_end_encounter(self): 
        '''
        Method: test_end_encounter
        Parameters: self
        Returns: none
        
        Tests the end_encounter function of the Creature class. Generates an 
        object of creature and manually sets the values of the extra_actions,
        circumstance_bonus, rk_circumstance_penalty, og_circumstance_penalty, 
        status_bonus, status_penalty, off_guard, off_guard_specific, hidden,
        had_battle_medicine, been_demoralized, been_rk, and current_hp
        attributes to non-default values.
        
        Once this has been done, calls end_encounter() which resets the values
        of all the above attributes back to their defaults.
        '''
        test = Creature("Test")
        # expected value: 1 for each
        test.extra_actions = 1
        test.circumstance_bonus = 1
        test.rk_circumstance_penalty = 1
        test.og_circumstance_penalty = 1
        test.status_bonus = 1
        test.status_penalty = 1
        test.current_hp = 1
        self.assertEqual(test.extra_actions, 1)
        self.assertEqual(test.circumstance_bonus, 1)
        self.assertEqual(test.rk_circumstance_penalty, 1)
        self.assertEqual(test.og_circumstance_penalty, 1)
        self.assertEqual(test.status_bonus, 1)
        self.assertEqual(test.status_penalty, 1)
        self.assertEqual(test.current_hp, 1)

        # expected value: True for each
        test.off_guard = True
        test.off_guard_specific = True
        test.hidden = True
        test.had_battle_medicine = True
        test.been_demoralized = True
        test.been_rk = True
        self.assertTrue(test.off_guard)
        self.assertTrue(test.off_guard_specific)
        self.assertTrue(test.hidden)
        self.assertTrue(test.had_battle_medicine)
        self.assertTrue(test.been_demoralized)
        self.assertTrue(test.been_rk)

        # expected value: 0 for each
        test.end_encounter()
        self.assertEqual(test.extra_actions, 0)
        self.assertEqual(test.circumstance_bonus, 0)
        self.assertEqual(test.rk_circumstance_penalty, 0)
        self.assertEqual(test.og_circumstance_penalty, 0)
        self.assertEqual(test.status_bonus, 0)
        self.assertEqual(test.status_penalty, 0)

        # expected value: False for each
        self.assertFalse(test.off_guard)
        self.assertFalse(test.off_guard_specific)
        self.assertFalse(test.hidden)
        self.assertFalse(test.had_battle_medicine)
        self.assertFalse(test.been_demoralized)
        self.assertFalse(test.been_rk)

        # expected value: 10
        self.assertEqual(test.current_hp, 10)
        
    def test_start_turn(self):
        '''
        Method: test_start_turn
        Parameters: self
        Returns: none
        
        Tests the start_turn function of the Creature class. Generates an 
        object of Creature.
        
        First, modifies the values that start_turn() resets, specifically:
        rk_circumstance_penalty, hidden, off_guard, circumstance_bonus, and
        actions.
        
        Then calls start_turn() and checks that the above values are reset to 
        default as expected.
        '''
        test = Creature("test")
        test.rk_circumstance_penalty = 1
        test.hidden = True
        test.off_guard = True
        test.circumstance_bonus = 1
        test.actions = 0

        test.start_turn()

        # expected value: 0
        self.assertEqual(test.rk_circumstance_penalty, 0)
        self.assertEqual(test.circumstance_bonus, 0)

        # expected value: False
        self.assertFalse(test.hidden)
        self.assertFalse(test.off_guard)

        # expected value: 3
        self.assertEqual(test.actions, 3)

    def test_end_turn(self):
        '''
        Method: test_end_turn
        Parameters: self
        Returns: none
        
        Tests the end_turn method of the Creature class. Generates two objects 
        of Creature, a user and a recipient.
        
        First, modifies the values that are reset by end_turn(): the 
        recipient's off_guard_specific attribute and the user's attacks_made 
        and status_penalty attributes.

        Then calls end_turn and checks that the affected values are reset.
        '''
        test1 = Creature("test1")
        test2 = Creature("test2")
        test1.attacks_made = 1
        test1.status_penalty = 2
        test2.off_guard_specific = True
        test2.current_hp = -5

        # expected value: 0
        test1.end_turn([test2])
        self.assertEqual(test1.attacks_made, 0)

        # expected value: 1
        self.assertEqual(test1.status_penalty, 1)

        # expected value: False
        self.assertFalse(test2.off_guard_specific)

        # expected value: 0
        self.assertEqual(test2.current_hp, 0)



    def test_roll_initiative(self):
        '''
        Method: test_roll_initiative
        Parameters: self
        Returns: none
        
        Tests the roll_initiative function of the Creature class. Generates an
        object of Creature.
        
        First, calls roll_initiative() on the object and checks that the return
        value is an instance of a list.
        
        Second, calls roll_initiative() 100 times. For each, checks that the 
        first element of the returned list is in the range between 1 and 20 and
        that the second element is "Test", the value for the name attribute of 
        the object.
        '''
        test = Creature("Test")
        # expected value:
        self.assertIsInstance(test.roll_initiative(), list)

        for i in range(100):
            check = test.roll_initiative()
            self.assertIn(check[0], range(3, 24))
            self.assertEqual(check[1], test)

    def test_seek(self): 
        '''
        Method: test_seek
        Parameters: self
        Returns: none
        
        Tests the seek function of the Creature class. Generates three Creature
        objects: one to use seek and two to be the target. The targets
        recieve arguments on creation to ensure that their Stealth DC is set
        such that the function either always succeeds or never succeeds 
        respectively. The seeker recieves default arguments. Test checks for 
        action deduction in both cases.

        The seek() function has two trees that must be tested separately:
        
        In the first case, the target object has be_hidden() called on them, 
        allowing the if case of seek() to be tested. The seeker calls seek()
        targeting both options. The value of each target's hidden attribute is
        used to check if the function works or not; the successful seek should
        set hidden to False, while the unsuccessful seek should leave it as 
        True.

        The second case does not reference the hidden state, so the target to 
        be checked has not_hidden() called on them. The else case of seek() 
        references the max and current HP and the AC of the target. The target
        is checked with full HP, below half HP, and below 1/4 HP to see each.

        Note that the second case is not checked with unittest! Since it only
        prints and doesn't return or modify anything, the only option is to 
        check that the print statements are correct.
        '''
        seeker = Creature("Seeker")
        strong_target = Creature("Strong", 0, 50)
        weak_target = Creature("Weak", 0, -50)
        strong_target.be_hidden()
        weak_target.be_hidden()
        
        # expected value: 3
        self.assertEqual(seeker.actions, 3)
        # expected value: True
        seeker.seek(strong_target)
        self.assertTrue(strong_target.hidden)
        # expected value: 2
        self.assertEqual(seeker.actions, 2)
        # expected value: False
        seeker.seek(weak_target)
        self.assertFalse(weak_target.hidden)
        # expected value: 1
        self.assertEqual(seeker.actions, 1)

        weak_target.not_hidden()
        # expected: "Weak is still going strong."
        # expected: "Based on their armor, weak has 10 AC."
        seeker.seek(weak_target)
        # expected value: 0
        self.assertEqual(seeker.actions, 0)

        weak_target.current_hp = 4
        # expected: "Weak is bloodied! Keep going!"
        # expected: "Based on their armor, weak has 10 AC."
        seeker.seek(weak_target)
        # expected value: -1
        self.assertEqual(seeker.actions, -1)

        weak_target.current_hp = 1
        # expected: "Weak is barely hanging in there!"
        # expected: "Based on their armor, weak has 10 AC."
        seeker.seek(weak_target)
        # expected value: -2
        self.assertEqual(seeker.actions, -2)

    def test_battle_medicine(self): 
        '''
        Method: test_battle_medicine
        Parameters: self
        Returns: none
        
        Tests the battle_medicine method of the Creature class. Generates four
        Creature objects, one to use battle medicine on four targets including
        itself. Also attempts to call battle_medicine() again on itself, which
        should fail; verified by actions not decrementing and current_hp not
        changing. Actions are tracked on each call. Each object has its
        max_hp attribute increased to 100; current_hp should be unmodified, 
        allowing the healing to occur. 
        
        Uses the override argument for battle_medicine() to force each of the 
        four possible results, as well as running once with RNG enabled.
        '''
        first = Creature("First")
        second = Creature("Second")
        third = Creature("Third")
        fourth = Creature("Fourth")
        fifth = Creature("Fifth")
        first.max_hp = 100
        second.max_hp = 100
        third.max_hp = 100
        fourth.max_hp = 100
        fifth.max_hp = 100
        
        # expected value: between 24 and 52, crit success
        first.battle_medicine(first, 1)
        unchanged = first.current_hp
        self.assertIn(first.current_hp, range(24, 53))
        # expected value: 2
        self.assertEqual(first.actions, 2)
        # expected value: same as before
        first.battle_medicine(first)
        self.assertEqual(first.current_hp, unchanged)
        # expected value: 2
        self.assertEqual(first.actions, 2)

        # expected value: between 22 and 36, success
        first.battle_medicine(second, 2)
        self.assertIn(second.current_hp, range(22, 37))
        # expected value: 1
        self.assertEqual(first.actions, 1)

        # expected value: between 2 and 9, crit fail
        first.battle_medicine(third, 3)
        self.assertIn(third.current_hp, range(2, 10))
        # expected value: 0
        self.assertEqual(first.actions, 0)

        # expected value: 10, fail
        first.battle_medicine(fourth, 4)
        self.assertEqual(fourth.current_hp, 10)
        # expected value: -1
        self.assertEqual(first.actions, -1)

        # expected value: between 24 and 52, crit success, rng
        first.medicine = 100
        first.battle_medicine(fifth)
        self.assertIn(fifth.current_hp, range(24, 53))

    def test_demoralize(self): 
        '''
        Method: test_demoralize
        Parameters: self
        Returns: none
        
        Tests the demoralize function of the Creature class. Generates four 
        objects of Creature, a user and three targets. Tests each of the 
        outcome options of demoralize() using the override parameter, as well
        as attempting to use it a second time on a specific target.
        '''
        user = Creature("User")
        t1 = Creature("Target1")
        t2 = Creature("Target2")
        t3 = Creature("Target3")

        # expected value: 2 - crit fail
        user.demoralize(t1, 1)
        self.assertEqual(t1.status_penalty, 2)

        # expected value: 2 - target already been_demoralized
        user.demoralize(t1)
        self.assertEqual(t1.status_penalty, 2)

        # expected value: 1 - fail
        user.demoralize(t2, 2)
        self.assertEqual(t2.status_penalty, 1)

        # expected value: 0 - success
        user.demoralize(t3, 3)
        self.assertEqual(t3.status_penalty, 0)

        # expected value: 0
        self.assertEqual(user.actions, 0)

        # expected value: 2 - crit fail, rng
        user.intimidation = 100
        t3.been_demoralized = False
        user.demoralize(t3)
        self.assertEqual(t3.status_penalty, 2)


    def test_hide(self): 
        '''
        Method: test_hide
        Parameters: self
        Returns: none
        
        Tests the hide function of the Creature class. Generates four objects 
        of Creature: two to hide and two to hide from. One hider object has its
        check to guarantee success, the other set to guarantee failure. Both 
        hider objects call hide() with the last two objects as the contents of
        the target_list arguement.
        '''
        hide1 = Creature("hide fail",0,-50)
        hide2 = Creature("hide success",0,50)
        hide3 = Creature("avo 1")
        hide4 = Creature("avo 2")

        # expected value: False
        hide1.hide([hide3, hide4])
        self.assertFalse(hide1.hidden)
        self.assertFalse(hide3.off_guard_specific)
        self.assertFalse(hide4.off_guard_specific)

        # expected value: True
        hide2.hide([hide3, hide4])
        print(hide2.hidden)
        self.assertTrue(hide2.hidden)
        self.assertTrue(hide3.off_guard_specific)
        self.assertTrue(hide4.off_guard_specific)

    def test_recall_knowledge(self): 
        '''
        Method: test_recall_knowledge
        Parameters: self
        Returns: none
        
        Tests the recall_knowledge function of the Creature class. Generates 
        three objects of creature: one user and three targets. Uses the 
        override parameter to force one of the three outcomes. Also checks that
        using recall_knowledge() on a target a second time has no effect.
        '''
        user = Creature("User")
        t1 = Creature("T1")
        t2 = Creature("T2")
        t3 = Creature("T3")

        # expected value: 2 - crit success
        user.recall_knowledge(t1, 1)
        self.assertEqual(t1.rk_circumstance_penalty, 2)

        # expeced value: 2 - no change, target been_rk True
        user.recall_knowledge(t1, 1)
        self.assertEqual(t1.rk_circumstance_penalty, 2)

        # expected value: 1 - success
        user.recall_knowledge(t2, 2)
        self.assertEqual(t2.rk_circumstance_penalty, 1)

        # expected value: 0 - fail
        user.recall_knowledge(t3, 3)
        self.assertEqual(t3.rk_circumstance_penalty, 0)

        # expected value: 0
        self.assertEqual(user.actions, 0)

        # expected value: 2 - crit success, rng
        user.society = 100
        t3.been_rk = False
        user.recall_knowledge(t3)
        self.assertEqual(t3.rk_circumstance_penalty, 2)

    def test_trip(self): 
        '''
        Method: test_trip
        Parameters: self
        Returns: none
        
        Tests the trip function of the Creature class. Generates five objects 
        of Creature: one attacker and four targets. Uses the override parameter
        of trip() to force each of the four possible results as well as running 
        once with RNG enabled.
        '''
        atk = Creature("Attacker")
        t1 = Creature("t1")
        t2 = Creature("t2")
        t3 = Creature("t3")
        t4 = Creature("t4")

        # expected value: True - crit success
        atk.trip(t1, 1)
        self.assertTrue(t1.off_guard)
        self.assertIn(t1.current_hp, range(4, 10))

        # expected value: True - success
        atk.trip(t2, 2)
        self.assertTrue(t2.off_guard)

        # expected value: False - crit fail
        atk.trip(t3, 3)
        self.assertFalse(t3.off_guard)
        # expected value: True
        self.assertTrue(atk.off_guard)

        # expected value: False - fail
        atk.trip(t4, 4)
        self.assertFalse(t4.off_guard)

        # expected value: -1
        self.assertEqual(atk.actions, -1)

        # expected value: 4
        self.assertEqual(atk.attacks_made, 4)

        # expected value: True - crit success, rng
        atk.athletics = 100
        atk.trip(t4)
        self.assertTrue(t4.off_guard)
        self.assertIn(t4.current_hp, range(4, 10))

    def test_tumble_through(self): 
        '''
        Method: test_tumble_through
        Parameters: Self
        Returns: none
        
        Tests the tumble_through function of the Creature class. Generates 
        three objects of Creature: one user and two targets. Uses the override
        parameter of tumble_through() to force both possible results, as well 
        as running once with rng enabled.
        '''
        user = Creature("user")
        t1 = Creature("t1")
        t2 = Creature("t2")

        # expected value: True - success
        user.tumble_through(t1, 1)
        self.assertTrue(t1.off_guard_specific)

        # expected value: False - failure
        user.tumble_through(t2, 2)
        self.assertFalse(t2.off_guard_specific)

        # expected value: 1
        self.assertEqual(user.actions, 1)

        # expected value: True - success
        user.acrobatics = 100
        user.tumble_through(t2)
        self.assertTrue(t2.off_guard_specific)

    def test_strike(self):
        '''
        Method: test_strike
        Parameters: self
        Returns: none
        
        Tests the strike function of the Creature class. Generates three objects
        of Creature: an attacker and two targets, one with default stats and a 
        second with -50 AC to always guarantee a crit without using the override,
        for checking arguments that the override bypasses.

        Calls strike() several times to check all argument options:
            - weapon: str, doesn't need specific testing; either the prints 
            work or they don't
            - damage_dice: 2 runs, for 1 dice and 2 dice
            - die_size: 10 runs, all five die options with both results
            - damage_type: str, doesn't need specific testing
            - damage_bonus: 2 runs, +1 bonus each hit and crit; no bonus 
            checked with damage_type
            - finesse: 1 run with on
            - agile: 3 runs with on, can't check if map is good but can make 
            sure it doesn't break anything
            - cleric: 1 run with on
            - rogue: 4 runs with on, one each with/without sneak attack for
            both results
            - wizard: 1 run with on
            - action_cost: 2 run, at 1 and 2 actions; 1 action is default and never 
            use more than 2 on a single attack
            +1 for miss
        '''
        atk = Creature("atk")
        tar = Creature("def")
        tar2 = Creature("def2",0,0,0,0,0,0,"medium",0,100,-50)
        tar.current_hp = 100
        
        # damage_dice tests:
        # expected value: 96-99 - 1 die
        atk.strike(tar,"test",1,4,"test",0,False,False,False,False,False,1,2)
        self.assertIn(tar.current_hp, range(96, 100))
        # expected value: 2
        self.assertEqual(atk.actions, 2)
        # expected value: 1
        self.assertEqual(atk.attacks_made, 1)
        # expected value: 92-98 - 2 dice
        tar.current_hp = 100
        atk.strike(tar,"test",2,4,"test",0,False,False,False,False,False,1,2)
        self.assertIn(tar.current_hp, range(92, 99))
        # expected value: 1
        self.assertEqual(atk.actions, 1)
        # expected value: 2
        self.assertEqual(atk.attacks_made, 2)

        # die_size tests:
        # 1d4 hit checked above
        # expected value: 92-98; d4 crit
        tar.current_hp = 100
        atk.strike(tar,"test",1,4,"test",0,False,False,False,False,False,1,1)
        self.assertIn(tar.current_hp, range(92, 99))
        # expected value: 94-99; d6 hit
        tar.current_hp = 100
        atk.strike(tar,"test",1,6,"test",0,False,False,False,False,False,1,2)
        self.assertIn(tar.current_hp, range(94, 100))
        # expected value: 88-98; d6 crit
        tar.current_hp = 100
        atk.strike(tar,"test",1,6,"test",0,False,False,False,False,False,1,1)
        self.assertIn(tar.current_hp, range(88, 99))
        # expected value: 92-99; d8 hit
        tar.current_hp = 100
        atk.strike(tar,"test",1,8,"test",0,False,False,False,False,False,1,2)
        self.assertIn(tar.current_hp, range(92, 100))
        # expected value: 84-98; d8 crit
        tar.current_hp = 100
        atk.strike(tar,"test",1,8,"test",0,False,False,False,False,False,1,1)
        self.assertIn(tar.current_hp, range(84, 99))
        # expected value: 90-99; d10 hit
        tar.current_hp = 100
        atk.strike(tar,"test",1,10,"test",0,False,False,False,False,False,1,2)
        self.assertIn(tar.current_hp, range(90, 100))
        # expected value: 80-98; d10 hit
        tar.current_hp = 100
        atk.strike(tar,"test",1,10,"test",0,False,False,False,False,False,1,1)
        self.assertIn(tar.current_hp, range(80, 99))
        # expected value: 88-99; d12 hit
        tar.current_hp = 100
        atk.strike(tar,"test",1,12,"test",0,False,False,False,False,False,1,2)
        self.assertIn(tar.current_hp, range(88, 100))
        # expected value: 76-98; d12 crit
        tar.current_hp = 100
        atk.strike(tar,"test",1,12,"test",0,False,False,False,False,False,1,1)
        self.assertIn(tar.current_hp, range(76, 99))
        
        # damage_bonus tests:
        # expected value: 95-98
        tar.current_hp = 100
        atk.strike(tar,"test",1,4,"test",1,False,False,False,False,False,1,2)
        self.assertIn(tar.current_hp, range(95, 99))
        # expected value: 90-96
        tar.current_hp = 100
        atk.strike(tar,"test",1,4,"test",1,False,False,False,False,False,1,1)
        self.assertIn(tar.current_hp, range(90, 97))

        # finesse test:
        # expected value: 92-98
        tar2.current_hp = 100
        atk.strike(tar2,"test",1,4,"test",0,True)
        self.assertIn(tar2.current_hp, range(92, 99))

        # agile tests:
        # expected value: 92-98
        tar2.current_hp = 100
        atk.attacks_made = 0
        atk.strike(tar2,"test",1,4,"test",0,False,True)
        self.assertIn(tar2.current_hp, range(92, 99))
        tar2.current_hp = 100
        atk.strike(tar2,"test",1,4,"test",0,False,True)
        self.assertIn(tar2.current_hp, range(92, 99))
        tar2.current_hp = 100
        atk.strike(tar2,"test",1,4,"test",0,False,True)
        self.assertIn(tar2.current_hp, range(92, 99))

        # regular map tests:
        # expected value: 92-98
        tar2.current_hp = 100
        atk.attacks_made = 0
        atk.strike(tar2,"test",1,4,"test",0)
        self.assertIn(tar2.current_hp, range(92, 99))
        tar2.current_hp = 100
        atk.strike(tar2,"test",1,4,"test",0)
        self.assertIn(tar2.current_hp, range(92, 99))
        tar2.current_hp = 100
        atk.strike(tar2,"test",1,4,"test",0)
        self.assertIn(tar2.current_hp, range(92, 99))

        # cleric test:
        # expected value: 92-98
        tar2.current_hp = 100
        atk.strike(tar2,"test",1,4,"test",0,False,False,True)
        self.assertIn(tar2.current_hp, range(92, 99))

        # rogue tests: 
        # without sneak attack
        # expected value: 92-98
        tar.current_hp = 100
        atk.strike(tar,"test",1,4,"test",0,False,False,False,True,False,1,1)
        self.assertIn(tar.current_hp, range(92, 99))
        # expected value: 96-99
        tar.current_hp = 100
        atk.strike(tar,"test",1,4,"test",0,False,False,False,True,False,1,2)
        self.assertIn(tar.current_hp, range(96, 100))
        # with sneak attack
        tar.og_circumstance_penalty = 2
        # expected value: 68-94
        tar.current_hp = 100
        atk.strike(tar,"test",1,4,"test",0,False,False,False,True,False,1,1)
        self.assertIn(tar.current_hp, range(68, 95))
        # expected value: 84-97
        tar.current_hp = 100
        atk.strike(tar,"test",1,4,"test",0,False,False,False,True,False,1,2)
        self.assertIn(tar.current_hp, range(84, 98))        

        # wizard tests:
        # expected value: 92-98
        tar2.current_hp = 100
        atk.strike(tar2,"test",1,4,"test",0,False,False,False,False,True)
        self.assertIn(tar2.current_hp, range(92, 99))

        # action_cost tests:
        # expected value: 2
        atk.actions = 3
        atk.strike(tar2,"test",1,4,"test",0,False,False,False,False,False,1)
        self.assertEqual(atk.actions, 2)
        # expected value: 0
        atk.strike(tar2,"test",1,4,"test",0,False,False,False,False,False,2)
        self.assertEqual(atk.actions, 0)

        # miss test:
        # expected value: 100
        tar.current_hp = 100
        atk.strike(tar,"test",1,4,"test",0,False,False,False,False,False,1,3)
        self.assertEqual(tar.current_hp, 100)

        # w/ rng test: 
        # expected value: 92-98
        tar.current_hp = 100
        atk.attack_bonus = 100
        atk.strike(tar,"test",1,4,"test",0,False,False,False,False,False,1)
        self.assertIn(tar.current_hp, range(92, 99))
        

if __name__ == "__main__":
    unittest.main()
