# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Test Orc_Commander
'''
Suite of test functions for the Orc_Commander class.
'''
import unittest
from orc_commander import Orc_Commander

class Test_Orc_Commander(unittest.TestCase):
    '''
    Class: Test_Orc_Commander
    Attributes: none
    Methods: test_constructor, test_battle_cry, test_ai

    Class of test functions for the Orc_Commander class.

    Note: the following methods are not tested:
        maul_strike: just a call to Creature's strike() method, testing covered in that class
    '''
    def test_constructor(self):
        '''
        Method: test_constructor
        Parameters: self
        Returns: none
        
        Tests the constructor method of Orc_Commander. Verifies that all 
        Orc_Commander-specific attributes are assigned correctly (attributes inherited
        from Creature are checked in the testing for that class).

        Generates an object of the Orc_Commander class.
        '''
        t = Orc_Commander()

        # expected value: "enemy"
        self.assertEqual(t.team, "enemy")

        # expected value: 12
        self.assertEqual(t.attack_bonus, 12)

        # expected value: False
        self.assertFalse(t.battle_cry_used)

    def test_battle_cry(self): 
        '''
        Method: test_battle_cry
        Parameters: self
        Returns: none
        
        Tests the battle_cry method of Orc_Commander. Generates two objects of 
        Orc_Commander, a user and an ally, then calls battle_cry() targeting 
        both. Checks that the user's actions are reduced by 1  and that both 
        targets have the status bonus applied correctly. 
        '''
        u = Orc_Commander()
        t = Orc_Commander()

        # expected value: 1
        u.battle_cry([u,t])
        self.assertEqual(u.status_bonus, 1)
        self.assertEqual(t.status_bonus, 1)

        # expected value: 2
        self.assertEqual(u.actions, 2)

    def test_ai(self):
        '''
        Method: test_ai
        Parameters: self
        Returns: none
        
        Tests the ai method of Orc_Commander using override arguments to bypass
        RNG. Generates three objects of Orc_Commander, a user and two targets.
        Target's ac, will_dc, reflex_dc, and hp are modified to control results.
        Commander should prioritize the target with lower HP for all actions.

        ai() is called 6 times:
            - 3 actions, battle_cry_used = False - battle cry
            - 3 actions, debuff = 0, been_demoralized = False - demoralize
            - 3 actions, debuff = 0, been_demoralized = True - trip
            - 3 actions, debuff = 1 - strike
            - 2 actions - strike
            - 1 action - strike
        '''
        u = Orc_Commander()
        t1 = Orc_Commander()
        t2 = Orc_Commander()
        t1.ac = -100
        t1.will_dc = -100
        t1.reflex_dc = -100
        t1.current_hp = 40

        # expected value: 1 - battle cry
        # non-debuff tests have override 5 to bypass time.sleep()
        u.ai([t2,t2,t1,t2], [u], 5)
        self.assertEqual(u.status_bonus, 1)

        # expected value: 2 - demoralize
        u.actions = 3
        u.ai([t2,t2,t1,t2], [u],0)
        self.assertEqual(t1.status_penalty, 2)

        # expected value: 2 - trip
        u.actions = 3
        u.ai([t2,t2,t1,t2], [u],0)
        self.assertEqual(t1.og_circumstance_penalty, 2)

        # expected value: < 40 - strike
        u.actions = 3
        u.ai([t2,t2,t1,t2], [u],1)
        self.assertLess(t1.current_hp, 40)

        # expected value: < 40 - strike
        t1.current_hp = 40
        u.actions = 2
        u.ai([t2,t2,t1,t2], [u],5)
        self.assertLess(t1.current_hp, 40)

        # expected value: < 40 - strike
        t1.current_hp = 40
        u.actions = 1
        u.ai([t2,t2,t1,t2], [u],5)
        self.assertLess(t1.current_hp, 40)

if __name__ == "__main__":
    unittest.main()
