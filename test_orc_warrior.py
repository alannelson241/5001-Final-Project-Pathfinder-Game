# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Test Orc_Warrior
'''
Suite of test functions for the Orc_Warrior class.
'''
import unittest
from orc_warrior import Orc_Warrior

class Test_Orc_Warrior(unittest.TestCase):
    '''
    Class: Test_Orc_Warrior
    Attributes: none
    Methods: test_constructor, test_ai

    Class of test functions for the Orc_Warrior class.

    Note: the following methods are not tested:
        battleaxe_strike: just a call to Creature's strike() method, testing covered in that class
        shortsword_strike: just a call to Creature's strike() method
    '''
    def test_constructor(self):
        '''
        Method: test_constructor
        Parameters: self
        Returns: none
        
        Tests the constructor method of Orc_Warrior. Verifies that all 
        Orc_Warrior-specific attributes are assigned correctly (attributes inherited
        from Creature are checked in the testing for that class).

        Generates an object of the Orc_Warrior class.
        '''
        t = Orc_Warrior('t')

        # expected value: "t the Orc Warrior"
        self.assertEqual(t.name, "t the Orc Warrior")

        # expected value: "enemy"
        self.assertEqual(t.team, "enemy")

        # expected value: 9 for each
        self.assertEqual(t.attack_bonus, 9)
        self.assertEqual(t.dex_attack_bonus, 9)

    def test_ai(self):
        '''
        Method: test_ai
        Parameters: self
        Returns: none
        
        Tests the ai method of Orc_Warrior using override arguments to bypass
        RNG. Generates three objects of Orc_Warrior, a user and two targets.
        Target's ac, will_dc, reflex_dc, and hp are modified to control results.
        Warrior should prioritize the target with higher HP for all actions.

        ai() is called 6 times:
            - 3 actions, debuff = 0, been_demoralized = False - demoralize
            - 3 actions, debuff = 0, been_demoralized = True - trip
            - 3 actions, debuff = 1 - strike
            - 2 actions, 0 attacks - battleaxe Strike
            - 2 actions, 1 attack - shortsword Strike
            - 1 action - shortsword Strike
        '''
        u = Orc_Warrior('u')
        t1 = Orc_Warrior('t1')
        t2 = Orc_Warrior('t2')
        t1.ac = -100
        t1.will_dc = -100
        t1.reflex_dc = -100
        t2.current_hp = -1000

        # expected value: 2 - demoralize
        u.actions = 3
        u.ai([t2,t2,t1,t2], [u],0)
        self.assertEqual(t1.status_penalty, 2)

        # expected value: 2 - trip
        u.actions = 3
        u.ai([t2,t2,t1,t2],[],0)
        self.assertEqual(t1.og_circumstance_penalty, 2)

        # expected value: < 33 - strike
        u.actions = 3
        u.ai([t2,t2,t1,t2],[],1)
        self.assertLess(t1.current_hp, 33)

        # expected value: < 33 - battleaxe strike
        t1.current_hp = 33
        u.attacks_made = 0
        u.actions = 2
        u.ai([t2,t2,t1,t2],[],5)
        self.assertLess(t1.current_hp, 33)

        # expected value: < 33 - shortsword strike
        t1.current_hp = 33
        u.actions = 2
        u.ai([t2,t2,t1,t2],[],5)
        self.assertLess(t1.current_hp, 33)

        # expected value: < 33 - shortsword strike
        t1.current_hp = 33
        u.actions = 1
        u.ai([t2,t2,t1,t2],[],5)
        self.assertLess(t1.current_hp, 33)

if __name__ == "__main__":
    unittest.main()
