# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Test Dragon
'''
Suite of test functions for the Dragon class.
'''
import unittest
from dragon import Dragon

class Test_Dragon(unittest.TestCase):
    '''
    Class: Test_Dragon
    Attributes: none
    Methods: test_constructor, test_start_turn, test_ai, test_jaws, 
        test_breath_weapon, test_draconic_frenzy, test_frightful_presence

    Class of test functions for the Dragon class.

    Note: the following methods are not tested:
        claw: just a call to Creature's strike() method, testing covered in that class
        horn: just a call to Creature's strike() method, testing covered in that class
    '''
    def test_constructor(self):
        '''
        Method: test_constructor
        Parameters: self
        Returns: none
        
        Tests the constructor method of Dragon. Verifies that all Dragon
        specific attributes are assigned correctly (attributes inherited from
        Creature are checked in the testing for that class).
        
        Generates an objects of the Dragon class.
        '''
        t = Dragon()

        # expected value: "enemy"
        self.assertEqual(t.team, "enemy")

        # expected value: 25
        self.assertEqual(t.spell_dc, 25)

        # expected value: 18
        self.assertEqual(t.attack_bonus, 18)

        # expected value: 16
        self.assertEqual(t.dex_attack_bonus, 16)

        # expected value: True
        self.assertTrue(t.breath_available)
        self.assertTrue(t.first_turn)

        # expected value: 0
        self.assertEqual(t.breath_timer, 0)

    def test_start_turn(self):
        '''
        Method: test_start_turn
        Parameters: self
        Returns: none
        
        Tests the Dragon specific functionality added to start_turn(). Sets
        breath_timer to 2 and breath_available to False, then calls start_turn()
        twice, checking that values update correctly.
        '''
        t = Dragon()
        t.breath_available = False
        t.breath_timer = 2

        # expected value: 1
        t.start_turn()
        self.assertEqual(t.breath_timer, 1)

        # expected value: False
        self.assertFalse(t.breath_available)

        # expected value: 0
        t.start_turn()
        self.assertEqual(t.breath_timer, 0)

        # expected value: True
        self.assertTrue(t.breath_available)

    def test_jaws(self):
        '''
        method: test_jaws
        Parameters: self
        Returns: none
        
        Tests the jaws method of Dragon. Generates two objects of Dragon, a 
        user and a target. 
        
        jaws() is called 4 times: once for each degree of success accessed via
        override values, and once with RNG enabled, modifying target's AC to 
        control the result. 
        '''
        u = Dragon()
        t = Dragon()

        # expected value: 63-119 - crit
        u.jaws(t,1)
        self.assertIn(t.current_hp, range(63,120))

        # expected value: 2
        self.assertEqual(u.actions, 2)

        # expected value: 1
        self.assertEqual(u.attacks_made, 1)

        # expected value: 101-123 - hit
        t.current_hp = 135
        u.jaws(t, 2)
        self.assertIn(t.current_hp, range(101,124))

        # expected value: 135 - miss
        t.current_hp = 135
        u.jaws(t, 3)
        self.assertEqual(t.current_hp, 135)

        # expected value: 63-119 - crit, rng
        t.ac = -100
        u.jaws(t,5)
        self.assertIn(t.current_hp, range(63,120))

    def test_breath_weapon(self):
        '''
        Method: test_breath_weapon
        Parameters: self
        Returns: none
        
        Tests the breath_weapon method of Dragon. Generates two objects of 
        Dragon, a user and a target. 
        
        breath_weapon() is called 5 times: once for each degree of success, 
        accessed via override arguments, and once with RNG enabled, modifying
        the DC of breath_weapon() to control the result.
        '''
        u = Dragon()
        t = Dragon()

        # expected value: 135 - crit success
        u.breath_weapon([t],1)
        self.assertEqual(t.current_hp, 135)

        # expected value: 1
        self.assertEqual(u.actions, 1)

        # expected value: 1-4
        self.assertIn(u.breath_timer, range(1, 5))

        # expected value: False
        self.assertFalse(u.breath_available)

        # expected value: 108-131 - success
        u.breath_weapon([t], 2)
        self.assertIn(t.current_hp, range(108,132))

        # expected value: 27-117 - crit fail
        t.current_hp = 135
        u.breath_weapon([t], 3)
        self.assertIn(t.current_hp, range(27,118))

        # expected value: 81-126 - fail
        t.current_hp = 135
        u.breath_weapon([t], 4)
        self.assertIn(t.current_hp, range(81,127))

        # expected value: 27-117 - crit fail, rng
        u.spell_dc = 100
        t.current_hp = 135
        u.breath_weapon([t], 5)
        self.assertIn(t.current_hp, range(27,118))

    def test_draconic_frenzy(self):
        '''
        Method: test_draconic_frenzy
        Parameters: self
        Returns: none
        
        Tests the draconic_frenzy method of Dragon. Generates three objects of 
        Dragon: a user and two targets.
        
        Modifies the AC of targets to control result and uses override arguments
        for draconic_frenzy to force each target to be selected once. Verifies 
        that both targets have their HP reduced and that the action cost is 
        deducted from the user.
        '''
        u = Dragon()
        t1 = Dragon()
        t2 = Dragon()
        t1.ac = -100
        t2.ac = -100

        # expected value: less than 135
        u.draconic_frenzy([t1,t1,t2,t2], 0, 2)
        self.assertLess(t1.current_hp, 135)
        self.assertLess(t2.current_hp, 135)

        # expected value: 1
        self.assertEqual(u.actions, 1)

    def test_frightful_presence(self):
        '''
        Method: test_frightful_presence
        Parameters: self
        Returns: none
        
        Tests the frightful_presence method of Dragon. Generates two objects of
        Dragon, a user and a target. The target's Will save is modified to 
        control the result.
        
        Calls frightful_presence(), then verifies that the expected 
        status_penalty is applied and that been_demoralized is still False.
        '''
        u = Dragon()
        t = Dragon()
        t.will_dc = -100

        # expected value: 2
        u.frightful_presence([t])
        self.assertEqual(t.status_penalty, 2)

        # expected value: False
        self.assertFalse(t.been_demoralized)

### Needs to come after other tests since it depends on everything else ###
    def test_ai(self):
        '''
        Method: test_ai
        Parameters: self
        Returns: none

        Tests the ai method of Dragon. Generates two objects of Dragon, a user 
        and a target. Target's AC, Will save, Fortitude save, and recall 
        knowledge DC are modified to control results.

        Calls ai() 7 times with different numbers of actions and different 
        relevant Boolean values:
            -3: first_turn, breath_available = True, been_rk = False. Should 
                demoralize and use Recall Knowledge, 2 actions remaining
            -3: breath_available, been_rk = True. Should use the Breath Weapon,
                1 action remaining.
            -3: breath_available, been_demoralized = False. Should demoralize, 
                2 action remaining.
            -3: breath_available = False, been_demoralized = True. Should use
                Draconic Frenzy, 1 action remaining.
            -2: breath_available = True: Should use the Breath Weapon, 0 
                actions remaining.
            -2: breath_available = False: Should use Draconic Frenzy, 0 actions
                remaining.
            -1: Should use Jaws, 0 actions remaining.
        '''
        u = Dragon()
        t = Dragon()
        t.ac = -100
        t.will_dc = -100
        t.fort_dc = -100
        t.rk_dc = -100

        # expected value: 2 - Frightful Presence, Recall Knowledge
        u.actions = 3
        u.ai([t,t,t,t],[])
        self.assertEqual(t.status_penalty, 2)
        self.assertEqual(t.rk_circumstance_penalty, 2)
        self.assertEqual(u.actions, 2)

        # expected value: 135
        self.assertEqual(t.current_hp, 135)

        # expected value: < 135 - invalid RK target, Breath Weapon
        u.actions = 3
        u.ai([t,t,t,t],[])
        self.assertLess(t.current_hp, 135)

        # expected value: 1
        self.assertEqual(u.actions, 1)

        # expected value: 2 - no Breath Weapon, valid Demoralize target
        t.status_penalty = 0
        u.actions = 3
        u.ai([t,t,t,t],[])
        self.assertEqual(t.status_penalty, 2)
        self.assertEqual(u.actions, 2)

        # expected value: < 135 - invalid Demoralize target, Draconic Frenzy
        t.current_hp = 135
        u.actions = 3
        u.ai([t,t,t,t],[])
        self.assertLess(t.current_hp, 135)

        # expected value: 1
        self.assertEqual(u.actions, 1)

        # expected value: < 135 - Breath Weapon only
        t.current_hp = 135
        u.actions = 2
        u.breath_available = True
        u.ai([t,t,t,t],[])
        self.assertLess(t.current_hp, 135)

        # expected value: 0
        self.assertEqual(u.actions, 0)

        # expected value: < 135 - Draconic Frenzy only
        t.current_hp = 135
        u.actions = 2
        u.ai([t,t,t,t],[])
        self.assertLess(t.current_hp, 135)

        # expected value: 0
        self.assertEqual(u.actions, 0)

        # expected value: < 135 - Jaws only
        t.current_hp = 135
        u.actions = 1
        u.ai([t,t,t,t],[])
        self.assertLess(t.current_hp, 135)

        # expected value: 0
        self.assertEqual(u.actions, 0)        

if __name__ == "__main__":
    unittest.main()
