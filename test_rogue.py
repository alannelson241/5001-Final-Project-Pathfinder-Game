# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Test Rogue
'''
Suite of test functions for the Rogue class.
'''
import unittest
from rogue import Rogue

class Test_Rogue(unittest.TestCase):
    '''
    Class: Test_Rogue
    Attributes: none
    Methods: test_constructor, test_shortsword_strike

    Class of test functions for the Rogue class.

    Note: the following methods are not tested:
        - take_turn(): we discussed this in office hours, refactoring to sequester user inputs would be a major undertaking
        - twin_feint: the majority of this method's functionality is covered under testing shortsword_strike;
            the remaining functionality is self contained and doesn't have anything that is testable - the only 
            change is that off_guard_specific is toggled on and off for the second attack if it wasn't already on.
            Nothing but HP is changed, and the change in HP is tested as part of strike() which shortsword_strike() calls.
    '''
    def test_constructor(self):
        '''
        Method: test_constructor
        Parameters: self
        Returns: none
        
        Tests the constructor method of Rogue. Verifies that all 
        Rogue-specific attributes are assigned correctly (attributes inherited
        from Creature are checked in the testing for that class).

        Generates an object of the Rogue class. Since the attributes of a 
        Rogue object are prescribed except for name, only need to use one
        object to fully test.
        '''
        t = Rogue('t')

        # expected value: "ally"
        self.assertEqual(t.team, "ally")

        # expected value: "14"
        self.assertEqual(t.dex_attack_bonus, 14)

        # expected value: ["Twin Feint", "Strike: Shortsword", "Hide", "Tumble Through", "Seek", "Pass", "Info"]
        self.assertEqual(t.action_list, ["Twin Feint", "Strike: Shortsword", "Hide", "Tumble Through", "Seek", "Pass", "Info"])

        # expected value: ["Twin Feint", "Strike: Shortsword", "Hide", "Tumble Through", "Seek", "Pass"]
        self.assertEqual(t.query_list, ["Twin Feint", "Strike: Shortsword", "Hide", "Tumble Through", "Seek", "Pass"])

    def test_shortsword_strike(self): 
        '''
        Method: test_shortsword_strike
        Parameters: self
        Returns: none
        
        Tests the shortsword_strike method of Rogue. Generates two objects of 
        Rogue, a user and a target. Sets the target's status_penalty to 1 and
        calls shortsword_strike(), then checks that off_guard_specific changed
        correctly.
        
        The strike functionality is tested under Creature's strike method which
        is called as part of this method. 
        '''
        u = Rogue("u")
        t = Rogue('t')
        t.status_penalty = 1
        
        # expected value: True
        u.shortsword_strike(t)
        self.assertTrue(t.off_guard_specific)

if __name__ == "__main__":
    unittest.main()
