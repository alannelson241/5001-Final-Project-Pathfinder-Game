# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Test Cleric
'''
Suite of test functions for the Cleric class.
'''
import unittest
from cleric import Cleric

class Test_Cleric(unittest.TestCase):
    '''
    Class: Test_Cleric
    Attributes: none
    Methods: test_constuctor, test_bless, test_sudden_blight, test_fear, 
    test_heal, test_raise_a_shield
    
    Class of test functions for the Cleric class.

    Note: the following methods are not tested:
        - take_turn(): we discussed this in office hours, refactoring to sequester user inputs would be a major undertaking
        - divine_lance(): is just a call to Creature's strike() method, testing covered in that class
        - mace_strike(): just a call to Creature's strike() method
    '''
    def test_constructor(self):
        '''
        Method: test_constructor
        Parameters: self
        Returns: none
        
        Tests the constructor method of Cleric. Verifies that all 
        Cleric-specific attributes are assigned correctly (attributes inherited
        from Creature are checked in the testing for that class).

        Generates an object of the Cleric class. Since the attributes of a 
        Cleric object are prescribed except for name, only need to use one
        object to fully test.
        ''' 
        t = Cleric('t')

        # expected value: "ally"
        self.assertEqual(t.team, "ally")

        # expected value: 11
        self.assertEqual(t.spell_attack, 11)
        self.assertEqual(t.attack_bonus, 11)

        # expected value: 21
        self.assertEqual(t.spell_dc, 21)

        # expected value: ["Spells", "Strike: Mace", "Raise a Shield", "Battle Medicine", "Trip", "Seek", "Pass", "Info"]
        self.assertEqual(t.action_list, ["Spells", "Strike: Mace", "Raise a Shield", "Battle Medicine", "Trip", "Seek", "Pass", "Info"])

        # expected value: ["Spells", "Strike: Mace", "Raise a Shield", "Battle Medicine", "Trip", "Seek", "Pass"]
        self.assertEqual(t.query_list, ["Spells", "Strike: Mace", "Raise a Shield", "Battle Medicine", "Trip", "Seek", "Pass"])

        # expected value: ["Divine Lance", "Bless", "Sudden Blight", "Fear", "Heal", "Info"]
        self.assertEqual(t.spell_list, ["Divine Lance", "Bless", "Sudden Blight", "Fear", "Heal", "Info"])

        # expected value: ["Divine Lance", "Bless", "Sudden Blight", "Fear", "Heal"]
        self.assertEqual(t.spell_query, ["Divine Lance", "Bless", "Sudden Blight", "Fear", "Heal"])

        # expected value: 3
        self.assertEqual(t.casts_bless, 3)
        self.assertEqual(t.casts_sudden_blight, 3)
        self.assertEqual(t.casts_fear, 3)

        # expected value: 5
        self.assertEqual(t.casts_heal, 5)

    def test_bless(self): 
        '''
        Method: test_bless
        Parameters: self
        Returns: none
        
        Tests the bless method of Cleric. Generates two objects of Cleric, a 
        user and an ally, then calls bless() targeting both. Checks that the 
        user's actions are reduced by 2 and casts by 1 and that both targets
        have the status bonus applied correctly. 
        '''
        u = Cleric('u')
        t = Cleric('t')

        # expected value: 1
        u.bless([u,t])
        self.assertEqual(u.actions, 1)
        self.assertEqual(u.status_bonus, 1)
        self.assertEqual(t.status_bonus, 1)

        # expected value: 2
        self.assertEqual(u.casts_bless, 2)

    def test_sudden_blight(self): 
        '''
        Method: test_sudden_blight
        Parameters: self
        Returns: none
        
        Tests the sudden_blight method of Cleric. Generates three objects of 
        Cleric, one user and two targets. sudden_blight() is called 5 times:
        once each for each degree of success (crit fail, fail, success, crit
        success) using override values to bypass RNG and once with RNG enabled
        and the user's spell_dc modified to force an expected result.
        '''
        u = Cleric('u')
        t1 = Cleric('t1')
        t2 = Cleric('t2')
        u.casts_sudden_blight = 5

        # expected value: 63 - crit success
        u.sudden_blight([t1,t2], 1)
        self.assertEqual(t1.current_hp, 63)
        self.assertEqual(t2.current_hp, 63)

        # expected value: 1
        self.assertEqual(u.actions, 1)

        # expected value: 4
        self.assertEqual(u.casts_sudden_blight, 4)

        # expected value: 53-62 - success
        u.sudden_blight([t1,t2], 2)
        self.assertIn(t1.current_hp, range(53,63))
        self.assertIn(t2.current_hp, range(53,63))

        # expected value: 23-59 - crit fail
        t1.current_hp = 63
        t2.current_hp = 63
        u.sudden_blight([t1,t2], 3)
        self.assertIn(t1.current_hp, range(23,60))
        self.assertIn(t2.current_hp, range(23,60))

        # expected value: 43-61 - fail
        t1.current_hp = 63
        t2.current_hp = 63
        u.sudden_blight([t1,t2], 4)
        self.assertIn(t1.current_hp, range(43,62))
        self.assertIn(t2.current_hp, range(43,62))

        # expected value: 23-59 - crit fail, rng
        u.spell_dc = 100
        t1.current_hp = 63
        t2.current_hp = 63
        u.sudden_blight([t1,t2], 5)
        self.assertIn(t1.current_hp, range(23,60))
        self.assertIn(t2.current_hp, range(23,60))        

    def test_fear(self): 
        '''
        Method: test_fear
        Parameters: self
        Returns: none
        
        Tests the fear method of Cleric. Generates two objects of Cleric, a 
        user and a target.
        
        fear() is called five times: once to check each degree of success using
        override values, and once with RNG enabled.
        '''
        u = Cleric("u")
        t = Cleric("t")
        u.casts_fear = 5

        # expected value: 0 - crit success
        u.fear([t], 1)
        self.assertEqual(t.status_penalty, 0)

        # expected value: 1
        self.assertEqual(u.actions, 1)

        # expected value: 4
        self.assertEqual(u.casts_fear, 4)

        # expected value: 1 - success
        u.fear([t], 2)
        self.assertEqual(t.status_penalty, 1)

        # expected calue: 3 - crit fail
        u.fear([t], 3)
        self.assertEqual(t.status_penalty, 3)

        # expected value: 2 - fail
        t.status_penalty = 0
        u.fear([t], 4)
        self.assertEqual(t.status_penalty, 2)

        # expected calue: 3 - crit fail, rng
        u.spell_dc = 100
        u.fear([t], 5)
        self.assertEqual(t.status_penalty, 3)

    def test_heal(self): 
        '''
        Method: test_heal
        Parameters: self
        Returns: none
        
        Tests the heal method of Cleric. Generates two objects of Cleric, a 
        user and an ally.
        
        heal() is called three times, using override arguments to bypass user 
        input. Each action cost use case is tested.
        '''
        u = Cleric("u")
        a = Cleric('a')
        a.current_hp = 0
        u.current_hp = 0
        u.actions = 6

        # expected value: 3-30 - 1 action
        u.heal([a,u],1)
        self.assertIn(a.current_hp, range(3,31)) 

        # expected value: 0 - single action is single target, override targets index 0
        self.assertEqual(u.current_hp, 0)

        # expected value: 5
        self.assertEqual(u.actions, 5)

        # expected value: 4
        self.assertEqual(u.casts_heal, 4)

        # expected value: 27-54 - 2 action
        a.current_hp = 0
        u.heal([a,u], 2)
        self.assertIn(a.current_hp, range(27,55))

        # expected value: 0 - two actions is single target, override targets index 0
        self.assertEqual(u.current_hp, 0)

        # expected value: 3-30 - 3 actions
        a.current_hp = 0
        u.heal([a,u], 3)
        self.assertIn(a.current_hp, range(3,31))
        self.assertIn(u.current_hp, range(3,31))

    def test_raise_a_shield(self): 
        '''
        Method: test_raise_a_shield
        Parameters: self
        Returns: none
        
        Tests the raise_a_shield method of Cleric. Generates an object of
        Cleric and calls raise_a_shield() on it, then checks that the action
        cost and circumstance_bonus are applied correctly.
        '''
        u = Cleric("u")

        # expected value: 2 for each
        u.raise_a_shield()
        self.assertEqual(u.circumstance_bonus, 2)
        self.assertEqual(u.actions, 2)
        
if __name__ == "__main__":
    unittest.main()
