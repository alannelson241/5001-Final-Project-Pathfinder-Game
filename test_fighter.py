# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Test Fighter
'''
Suite of test functions for the Fighter class.
'''
import unittest
from fighter import Fighter

class Test_Fighter(unittest.TestCase):
    '''
    Class: Test_Fighter
    Attributes: none
    Methods: test_constructor, test_start_turn, test_greatsword_strike,
     test_vicious_swing, test_intimidating_strike, test_swipe, 

    Class of test functions for the Fighter class.

    Note: the following methods are not tested:
        - take_turn(): as we discussed in office hours, refactoring to sequester user input would be a major undertaking
        - swipe(): functionality is fully covered by greatsword_strike() testing.
    '''
    
    def test_constructor(self):
        '''
        Method: test_constructor
        Parameters: self
        Returns: none
        
        Tests the constructor method of Fighter. Verifies that all Fighter
        specific attributes are assigned correctly (attributes inherited from
        Creature are checked in the testing for that class).
        
        Generates an objects of the Fighter class.
        '''
        t = Fighter("test")

        # expected value: "ally"
        self.assertEqual(t.team, "ally")

        # expected value: 16
        self.assertEqual(t.attack_bonus, 16)

        # expected value: ["Special Attacks", "Strike: Greatsword", "Demoralize", "Trip", "Seek", "Pass", "Info"]
        self.assertEqual(t.action_list, ["Special Attacks", "Strike: Greatsword", "Demoralize", "Trip", "Seek", "Pass", "Info"])

        # expected value: ["Special Attacks", "Strike: Greatsword", "Demoralize", "Trip", "Seek", "Pass"]
        self.assertEqual(t.query_list, ["Special Attacks", "Strike: Greatsword", "Demoralize", "Trip", "Seek", "Pass"])

        # expected value: ["Vicious Swing", "Intimidating Strike", "Swipe", "Info"]
        self.assertEqual(t.special_attack_list, ["Vicious Swing", "Intimidating Strike", "Swipe", "Info"])

        # expected value: ["Vicious Swing", "Intimidating Strike", "Swipe"]
        self.assertEqual(t.attack_query, ["Vicious Swing", "Intimidating Strike", "Swipe"])

        # expected value: False
        self.assertFalse(t.flourish)

    def test_start_turn(self):
        '''
        Method: test_start_turn
        Parameters: self
        Returns: none
        
        Tests the fighter specific functionality added to the start_turn() 
        method. Specifically, that the value of the flourish attribute is 
        reset when start_turn() is called.
        
        Generates an object of Fighter and sets its flourish attribute to True,
        then calls start_turn().
        '''
        t = Fighter("test")
        t.flourish = True

        # expected value: False
        t.start_turn()
        self.assertFalse(t.flourish)

    def test_greatsword_strike(self):
        '''
        Method: test_greatsword_strike
        Parameters: self
        Returns: none
        
        Tests the greatsword_strike method of Fighter. Generates four objects 
        of Fighter, one user and three targets. Two targets have their AC set
        low enough to ensure that attacks against them are critical hits for 
        consistency purposes.
        
        greatsword_strike() is called 9 times:
            - single target
            - two targets
            - 3 damage dice
            - 1 action
            - 2 actions
            - 1 attack for MAP
            - 2 attacks for MAP
            - default values; override to force crit, hit, and miss
        '''
        u = Fighter("user")
        t1 = Fighter("t1")
        t2 = Fighter('t2')
        t3 = Fighter("t3")
        t1.ac = -20
        t2.ac = -20

        # expected value: 22-66 - single target, 1 action, crit, rng
        u.greatsword_strike([t1])
        self.assertIn(t1.current_hp, range(22,66))

        # expected value: 22-66 - 2 targets, 1 action, crit, rng
        t1.current_hp = 78
        u.greatsword_strike([t1, t2])
        self.assertIn(t1.current_hp, range(22,66))
        self.assertIn(t2.current_hp, range(22,66))

        # expected value: 10-65 - 3 damage dice
        t1.current_hp = 78
        u.greatsword_strike([t1],3)
        self.assertIn(t1.current_hp, range(10,65))

        # expected value: 2 - 1 action
        u.actions = 3
        u.greatsword_strike([t1],2,1)
        self.assertEqual(u.actions, 2)

        # expected value: 0 - 2 actions
        u.greatsword_strike([t1],2,2)
        self.assertEqual(u.actions, 0)

        # expected value: 1 - 1 attack worth
        u.attacks_made = 0
        u.greatsword_strike([t1],2,1,1)
        self.assertEqual(u.attacks_made, 1)

        # expected value: 3 - 2 attacks worth
        u.greatsword_strike([t1],2,1,2)
        self.assertEqual(u.attacks_made, 3)

        # expected value: 22-66 - crit
        x = u.greatsword_strike([t3],2,1,1,1)
        self.assertIn(t3.current_hp, range(22,66))

        # expected value: true
        self.assertTrue(t3.off_guard)

        # expected value: 2
        self.assertEqual(x, 2)

        # expected value: 50-72 - hit
        t3.current_hp = 78
        x = u.greatsword_strike([t3],2,1,1,2)
        self.assertIn(t3.current_hp, range(50,73))

        # expected value: 1
        self.assertEqual(x, 1)

        # expected value: 78 - miss
        t3.current_hp = 78
        x = u.greatsword_strike([t3],2,1,1,3)
        self.assertEqual(t3.current_hp, 78)

        # expected value: 0
        self.assertEqual(x, 0)

    def test_vicious_swing(self):
        '''
        Method: test_vicious_swing
        Parameters: self
        Returns: none
        
        Tests the vicious_swing method of Fighter. Generates two objects of Fighter,
        a user and a target. Calls vicious_swing() on the target.
        
        The damage dealing functionality of vicious_swing() is tested under 
        greatsword_strike(); this test confirms that the flourish attribute is 
        updated to True correctly.
        '''
        u = Fighter('u')
        t = Fighter('t')

        # expected value: True
        u.vicious_swing(t)
        self.assertTrue(u.flourish)

    def test_intimidating_strike(self):
        '''
        Method: test_intimidating_strike
        Parameters: self
        Returns: none
        
        Tests the intimidating_strike method of Fighter. Generates two objects 
        of Fighter: a user and a target. 
        
        Calls intimidating_strike() four times: three times using the override
        parameter to check each degree of success, and once with no override to
        check that random number generation works to apply the desired condition 
        correctly. Intimidating Strike should apply a status penalty (due to 
        frightened) of 2 on a crit, 1 on a hit, and 0 on a miss.
        '''
        u = Fighter("user")
        t = Fighter("t")

        # expected value: 2 - crit
        u.intimidating_strike(t, 1)
        self.assertEqual(t.status_penalty, 2)

        # expected value: 1 - hit
        t.status_penalty = 0
        u.intimidating_strike(t, 2)
        self.assertEqual(t.status_penalty, 1)

        # expected value: 0 - miss
        t.status_penalty = 0
        u.intimidating_strike(t, 3)
        self.assertEqual(t.status_penalty, 0)

        # expected value: 2 - crit, rng
        t.ac = -20
        u.intimidating_strike(t)
        self.assertEqual(t.status_penalty, 2)

if __name__ == "__main__":
    unittest.main()
