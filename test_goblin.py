# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Test Goblin
'''
Suite of test functions for the Goblin class.
'''
import unittest
from goblin import Goblin

class Test_Goblin(unittest.TestCase):
    '''
    Class: Test_Goblin
    Attributes: none
    Methods: test_constructor, test_start_turn, test_ai

    Class of test functions for the Goblin class.

    Note: the following methods are not tested:
        spear_strike: just a call to Creature's strike() method, testing covered in that class
    '''
    def test_constructor(self):
        '''
        Method: test_constructor
        Parameters: self
        Returns: none
        
        Tests the constructor method of Goblin. Verifies that all 
        Goblin-specific attributes are assigned correctly (attributes inherited
        from Creature are checked in the testing for that class).

        Generates an object of the Goblin class.
        '''
        t = Goblin('t')

        # expected value: "t the Goblin"
        self.assertEqual(t.name, "t the Goblin")

        # expected value: "enemy"
        self.assertEqual(t.team, "enemy")

        # expected value: 8
        self.assertEqual(t.attack_bonus, 8)

        # expected value: False
        self.assertFalse(t.hide_attempt)

    def test_start_turn(self):
        '''
        Method: test_start_turn
        Parameters: self
        Returns: none
        
        Tests that hide_attempt is reset correctly when start_turn() is called.
        '''
        t = Goblin("t")
        t.hide_attempt = True

        # expected value: False
        t.start_turn()
        self.assertFalse(t.hide_attempt)

    def test_ai(self):
        '''
        Method: test_ai
        Parameters: self
        Returns: none
        
        Tests the ai method of Goblin using override arguments to bypass RNG.
        Generates two objects of Goblin, a user and a target. Target's AC, 
        perception_dc, and reflex_dc are modified to control results.
        
        ai() is called 5 times:
            - rand = 0, hide_attempt = False: attempts to hide
            - rand = 0, hide_attempt = True: makes a Strike
            - rand = 1, off_guard = False: attempts to trip
            - rand = 1, off_guard = True: makes a Strike
            - rand = 2: makes a Strike
        '''
        u = Goblin('u')
        t = Goblin('t')
        t.ac = -100
        t.perception_dc = -100
        t.reflex_dc = -100

        # expected value: True - attempt to hide
        u.ai([t,t,t,t],[],0)
        self.assertTrue(u.hidden)
        self.assertTrue(u.hide_attempt)

        # expected value: 2
        self.assertEqual(u.actions, 2)

        # expected value: < 18 - can't hide, strikes
        u.ai([t,t,t,t],[],0)
        self.assertLess(t.current_hp, 18)

        # expected value: True - attempt to trip
        u.ai([t,t,t,t],[],1)
        self.assertTrue(t.off_guard)

        # expected value: < 18 - target off-guard, strikes
        t.current_hp = 18
        u.ai([t,t,t,t],[],1)
        self.assertLess(t.current_hp, 18)

        # expected value: < 18 - strikes
        t.current_hp = 18
        u.ai([t,t,t,t],[],2)
        self.assertLess(t.current_hp, 18)

if __name__ == "__main__":
    unittest.main()
