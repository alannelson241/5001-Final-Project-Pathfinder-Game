# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Test Hobgoblin General
'''
Suite of test functions for the Hobgoblin General class.
'''
import unittest
from hobgoblin_general import Hobgoblin_General

class Test_Hobgoblin_General(unittest.TestCase):
    '''
    Class: Test_Hobgoblin_General
    Attributes: none
    Methods: test_constructor, test_ai, test_raise_a_shield

    Class of test functions for the Hobgoblin General class.

    Note: the following methods are not tested:
        warhammer_strike: just a call to Creature's strike() method, testing covered in that class
    '''
    def test_constructor(self):
        '''
        Method: test_constructor
        Parameters: self
        Returns: none
        
        Tests the constructor method of Hobgoblin General. Verifies that all Hobgoblin 
        General-specific attributes are assigned correctly (attributes inherited
        from Creature are checked in the testing for that class).

        Generates an object of the Hobgoblin General class.
        '''
        t = Hobgoblin_General()

        # expected value: "enemy"
        self.assertEqual(t.team, "enemy")

        # expected value: 15
        self.assertEqual(t.attack_bonus, 15)

        # expected value: True
        self.assertTrue(t.first_turn)

    def test_raise_a_shield(self): 
        '''
        Method: test_raise_a_shield
        Parameters: self
        Returns: none
        
        Tests the raise_a_shield method of Hobgoblin_General. Generates an object of
        Hobgoblin_General and calls raise_a_shield() on it, then checks that the action
        cost and circumstance_bonus are applied correctly.
        '''
        u = Hobgoblin_General()

        # expected value: 2 for each
        u.raise_a_shield()
        self.assertEqual(u.circumstance_bonus, 2)
        self.assertEqual(u.actions, 2)

    def test_ai(self):
        '''
        Method: test_ai
        Parameters: self
        Returns: none
        
        Tests the ai method of Hobgoblin_General using override arguments to 
        bypass RNG. Generates three objects, a user and two targets. Target's
        ac, will_dc, reflex_dc, and HP are modified to control results.

        Calls ai() 9 times:
            -3 actions, first_turn = True, rand = 1, - demoralize with General's Cry then Strike
            -3 actions, rand = 1, been_demoralized = False - demoralize
            -3 actions, rand = 1, been_demoralized = True - Strike
            -3 actions, rand = 2, off_guard = False - tumble through
            -3 actions, rand = 2, off_guard = True - Strike
            -3 actions, rand = 3, off_guard = False - trip
            -3 actions, rand = 3, off_guard = True - strike
            -3 actions, rand = 4 - strike
            -2 actions - strike
            -1 action - raise a shield
        '''
        u = Hobgoblin_General()
        t1 = Hobgoblin_General()
        t2 = Hobgoblin_General()
        t1.ac = -100
        t1.will_dc = -100
        t1.reflex_dc = -100

        # expected value: 2 - General's Cry into Strike
        u.ai([t1,t1,t1,t1],[],1)
        self.assertEqual(t1.status_penalty, 2)
        self.assertEqual(u.actions, 2)

        # expected value: 2 - demoralize
        u.actions = 3
        t1.been_demoralized = False
        t1.status_penalty = 0
        u.ai([t1,t1,t1,t1],[],1)
        self.assertEqual(t1.status_penalty, 2)

        # expected value: < 70 - been_demoralized = True; Strike
        t1.current_hp = 70
        u.actions = 3
        u.ai([t1,t1,t1,t1],[],1)
        self.assertLess(t1.current_hp, 70)

        # expected value: True - tumble through
        u.actions = 3
        u.ai([t1,t1,t1,t1],[],2)
        self.assertTrue(t1.off_guard_specific)

        # expected value < 70 - off_guard = True; Strike
        t1.off_guard = True
        t1.current_hp = 70
        u.actions = 3
        u.ai([t1,t1,t1,t1],[],2)
        self.assertLess(t1.current_hp, 70)

        # expected value: True - trip
        t1.off_guard = False
        u.actions = 3
        u.ai([t1,t1,t1,t1],[],3)
        self.assertTrue(t1.off_guard)

        # expected value: < 70 - off_guard = True; Strike
        t1.current_hp = 70
        u.actions = 3
        u.ai([t1,t1,t1,t1],[],3)
        self.assertLess(t1.current_hp, 70)

        # expected value: < 70 - Strike
        t1.current_hp = 70
        u.actions = 3
        u.ai([t1,t1,t1,t1],[],4)
        self.assertLess(t1.current_hp, 70)
        
        # expected value: < 60; should go for weaker target
        # override value is just to bypass time.sleep()
        t1.current_hp = 60
        u.actions = 2
        u.ai([t2,t1,t2,t2],[],5)
        self.assertLess(t1.current_hp, 60)

        # expected value: 2 - raise a shield
        u.ai([t1,t1,t2,t2],[],5)
        self.assertEqual(u.circumstance_bonus, 2)

if __name__ == "__main__":
    unittest.main()