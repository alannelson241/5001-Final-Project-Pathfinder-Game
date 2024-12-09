# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Test Hobgoblin_Soldier
'''
Suite of test functions for the Hobgoblin_Soldier class.
'''
import unittest
from hobgoblin_soldier import Hobgoblin_Soldier

class Test_Hobgoblin_Soldier(unittest.TestCase):
    '''
    Class: Test_Hobgoblin_Soldier
    Attributes: none
    Methods: test_constructor, test_start_turn, test_raise_a_shield, test_ai

    Class of test functions for the Hobgoblin_Soldier class.

    Note: the following methods are not tested:
        longsword_strike: just a call to Creature's strike() method, testing covered in that class
    '''
    def test_constructor(self):
        '''
        Method: test_constructor
        Parameters: self
        Returns: none
        
        Tests the constructor method of Hobgoblin_Soldier. Verifies that all 
        Hobgoblin_Soldier-specific attributes are assigned correctly (attributes inherited
        from Creature are checked in the testing for that class).

        Generates an object of the Hobgoblin_Soldier class.
        '''
        t = Hobgoblin_Soldier()

        #expected value: "enemy"
        self.assertEqual(t.team, "enemy")

        # expected value: 10
        self.assertEqual(t.attack_bonus, 10)

        # expected value: None
        self.assertIsNone(t.focus)

    def test_start_turn(self):
        '''
        Method: test_start_turn
        Parameters: self
        Returns: none
        
        Checks that the Hobgoblin_Soldier specific functionality of start_turn()
        to reset the value of focus to None works correctly.
        '''
        u = Hobgoblin_Soldier()
        u.focus = u

        # expected value: None
        u.start_turn()
        self.assertIsNone(u.focus)

    def test_ai(self):
        '''
        Method: test_ai
        Parameters: self
        Returns: none

        Tests the ai method of Hobgoblin_Soldier. Generates two objects of 
        Hobgoblin_Soldier, a user and a target. Target's ac and reflex_dc 
        are modified to control results.

        ai() is called 5 times:
            - 3 actions, target not off-guard - trip
            - 3 actions, target off-guard - Strike against off-guard target
            - 2 actions, target not off-guard - Strike against random target
                verify random vs deliberate using focus attribute
            - 2 actions, target off-guard - Strike against off-guard target
            - 1 action - raise a shield
        '''
        u = Hobgoblin_Soldier()
        t = Hobgoblin_Soldier()
        t.ac = -100
        t.reflex_dc = -100

        # expected value: True - trip
        u.ai([t,t,t,t],[])
        self.assertTrue(t.off_guard)
        
        # expected value: 2
        self.assertEqual(u.actions, 2)

        # expected value: < 30 - strike off-guard target
        u.actions = 3
        u.ai([t,t,t,t],[])
        self.assertLess(t.current_hp, 30)

        # expected value: t
        self.assertEqual(u.focus, t)

        # expected value: < 30 - strike random target
        u.actions = 2
        u.focus = None
        t.current_hp = 30
        u.ai([t,t,t,t],[])
        self.assertLess(t.current_hp, 30)

        # expected value: None
        u.start_turn()
        self.assertIsNone(u.focus)

        # expected value: < 30 - strike off-guard target
        u.actions = 2
        u.focus = None
        t.current_hp = 30
        u.ai([t,t,t,t],[])
        self.assertLess(t.current_hp, 30)

        # expected value: t
        self.assertEqual(u.focus, t)

        # expected value: 2 - raise a shield
        u.actions = 1
        u.ai([t,t,t,t],[])
        self.assertEqual(u.circumstance_bonus, 2)

    def test_raise_a_shield(self): 
        '''
        Method: test_raise_a_shield
        Parameters: self
        Returns: none
        
        Tests the raise_a_shield method of Hobgoblin_Soldier. Generates an object of
        Hobgoblin_Soldier and calls raise_a_shield() on it, then checks that the action
        cost and circumstance_bonus are applied correctly.
        '''
        u = Hobgoblin_Soldier()

        # expected value: 2 for each
        u.raise_a_shield()
        self.assertEqual(u.circumstance_bonus, 2)
        self.assertEqual(u.actions, 2)
        
if __name__ == "__main__":
    unittest.main()
