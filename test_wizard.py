# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Test Wizard
'''
Suite of test functions for the Wizard class.
'''
import unittest
from wizard import Wizard

class Test_Wizard(unittest.TestCase):
    '''
    Class: Test_Wizard
    Attributes: none
    Methods: test_constructor, test_start_turn, test_electric_arc, test_frostbite,
        test_shield, test_gust_of_wind, test_force_barrage, test_invisibility,
        test_thunderstrike, test_fireball, test_haste, test_dagger_strike

    Class of test functions for the Wizard class.

    Note: the following methods are not tested:
        - take_turn(): we discussed this in office hours, refactoring to sequester user inputs would be a major undertaking
        - ignition(): is just a call to Creature's strike() method, testing covered in that class
        - dagger_strike(): just a call to Creature's strike() method
    '''
    def test_constructor(self):
        '''
        Method: test_constructor
        Parameters: self
        Returns: none
        
        Tests the constructor method of Wizard. Verifies that all 
        Wizard-specific attributes are assigned correctly (attributes inherited
        from Creature are checked in the testing for that class).

        Generates an object of the Wizard class. Since the attributes of a 
        Wizard object are prescribed except for name, only need to use one
        object to fully test.
        '''
        test = Wizard("test")

        # expected value: "ally"
        self.assertEqual(test.team, "ally")

        # expected value: 11
        self.assertEqual(test.spell_attack, 11)
        self.assertEqual(test.dex_attack_bonus, 11)

        # expected value: 21
        self.assertEqual(test.spell_dc, 21)

        # expected value: ["Spells", "Strike: Dagger", "Recall Knowledge", "Seek", "Pass", "Info"]
        self.assertEqual(test.action_list, ["Spells", "Strike: Dagger", "Recall Knowledge", "Seek", "Pass", "Info"])

        # expected value: ["Spells", "Strike: Dagger", "Recall Knowledge", "Seek", "Pass"]
        self.assertEqual(test.query_list, ["Spells", "Strike: Dagger", "Recall Knowledge", "Seek", "Pass"])

        # expected value: ["Electric Arc", "Frostbite", "Ignition", "Shield", "Gust of Wind", "Force Barrage","Invisibility", "Thunderstrike", "Fireball", "Haste", "Info"]
        self.assertEqual(test.spell_list, ["Electric Arc", "Frostbite", "Ignition", "Shield", "Gust of Wind", "Force Barrage","Invisibility", "Thunderstrike", "Fireball", "Haste", "Info"])

        # expected value: ["Electric Arc", "Frostbite", "Ignition", "Shield", "Gust of Wind", "Force Barrage","Invisibility", "Thunderstrike", "Fireball", "Haste"]
        self.assertEqual(test.spell_query, ["Electric Arc", "Frostbite", "Ignition", "Shield", "Gust of Wind", "Force Barrage","Invisibility", "Thunderstrike", "Fireball", "Haste"])

        # expected value: None
        self.assertIsNone(test.invis_target)

        # expected value: 2 for each
        self.assertEqual(test.casts_gust_of_wind, 2)
        self.assertEqual(test.casts_force_barrage, 2)
        self.assertEqual(test.casts_invisibility, 2)
        self.assertEqual(test.casts_thunderstrike, 2)
        self.assertEqual(test.casts_fireball, 2)
        self.assertEqual(test.casts_haste, 2)

    def test_start_turn(self):
        '''
        Method: test_start_turn
        Parameters: self
        Returns: none
        
        Tests the start_turn method of the Wizard class. Doesn't test the 
        functionality inherited from the call to start_turn() from Creature,
        which is instead checked in the testing for that class.
        
        Generates two objects of Wizard, a user and a target. The invis_target 
        attribute of the user is set to the target, then start_turn() is 
        called, which should reset the value of that attribute.
        '''
        user = Wizard("user")
        target = Wizard("target")
        user.invis_target = target

        # expected value: target
        self.assertEqual(user.invis_target, target)

        # expected value: None
        user.start_turn()
        self.assertIsNone(user.invis_target)

    def test_electric_arc(self):
        '''
        Method: test_electric_arc
        Parameters: self
        Returns: none
        
        Tests the electric_arc method of the Wizard class. Generates three 
        objects of Wizard: one user and two targets.
        
        Calls electric_arc() 6 times: once for each degree of success, once
        with a single target, and once with no override and user.spell_dc 
        modified to ensure a critical failure for both targets to test that the
        random number generation functions. Note that override is set to 5 for 
        the "no override" execution so that time.sleep() is suppressed.
        '''
        u = Wizard("user")
        t1 = Wizard("t1")
        t2 = Wizard("t2")

        # expected value: 48 - crit success
        u.electric_arc([t1, t2], 1)
        self.assertEqual(t1.current_hp, 48)
        self.assertEqual(t2.current_hp, 48)

        # expected value: 1
        self.assertEqual(u.actions, 1)

        # expected value: 40-46 - success
        t1.current_hp = 48
        t2.current_hp = 48
        u.electric_arc([t1, t2], 2)
        self.assertIn(t1.current_hp, range(40,47))
        self.assertIn(t1.current_hp, range(40,47))

        # expected value: 16-40 - crit fail
        t1.current_hp = 48
        t2.current_hp = 48
        u.electric_arc([t1, t2], 3)
        self.assertIn(t1.current_hp, range(16,41))
        self.assertIn(t1.current_hp, range(16,41))

        # expected value: 32-44 - fail
        t1.current_hp = 48
        t2.current_hp = 48
        u.electric_arc([t1, t2], 4)
        self.assertIn(t1.current_hp, range(32,45))
        self.assertIn(t1.current_hp, range(32,45))

        # expected value: 48 - single target
        t1.current_hp = 48
        u.electric_arc([t1], 1)
        self.assertEqual(t1.current_hp, 48)

        # expected value: 16-40 - success, rng
        t1.current_hp = 48
        t2.current_hp = 48
        u.spell_dc = 100
        u.electric_arc([t1, t2], 5)
        self.assertIn(t1.current_hp, range(16,41))
        self.assertIn(t1.current_hp, range(16,41))

    def test_frostbite(self):
        '''
        Method: test_frostbite
        Parameters: self
        Returns: none
        
        Tests the frostbite method of the Wizard class. Generates two objects 
        of Wizard: a user and a target.
        
        Calls frostbite() 5 times: one for each degree of success, and one with
        no forced result to confirm the random number generation functions.
        '''
        u = Wizard("user")
        t = Wizard("target")

        # expected value: 48 - crit success
        u.frostbite(t, 1)
        self.assertEqual(t.current_hp, 48)

        # expected value: 1
        self.assertEqual(u.actions, 1)

        # expected value: 40-46 - success
        t.current_hp = 48
        u.frostbite(t, 2)
        self.assertIn(t.current_hp, range(40,47))

        # expected value: 16-40 - crit fail
        t.current_hp = 48
        u.frostbite(t, 3)
        self.assertIn(t.current_hp, range(16,41))

        # expected value: 32-44 - fail
        t.current_hp = 48
        u.frostbite(t, 4)
        self.assertIn(t.current_hp, range(32, 45))

        # expected value: 16-40 - crit fail, rng
        t.current_hp = 48
        u.spell_dc = 100
        u.frostbite(t, 5)
        self.assertIn(t.current_hp, range(16,41))

    def test_shield(self):
        '''
        Method: test_shield
        Parameters: self
        Returns: none
        
        Tests the shield method of the Wizard class. Generates an object of 
        Wizard and calls shield() on it, then checks that the object's 
        circumstance_bonus attribute is modified.
        '''
        u = Wizard("user")
        
        # expected value: 1
        u.shield()
        self.assertEqual(u.circumstance_bonus, 1)

        # expected value: 2
        self.assertEqual(u.actions, 2)

    def test_gust_of_wind(self):
        '''
        Method: test_gust_of_wind
        Parameters: self
        Returns: none
        
        Tests the gust_of_wind method of the Wizard class. Generates three
        objects of Wizard: one user and two targets.
        
        gust_of_wind() is called 5 times: once for each degree of success, 
        once with a single target, and once with randomness enabled to confirm
        random number generation functions correctly.

        The conditional that checks if casts_gust_of_wind > 0 is not checked, 
        since it only prints and has no code to check.
        '''
        u = Wizard("user")
        t1 = Wizard("t1")
        t2 = Wizard("t2")
        u.casts_gust_of_wind = 5

        # expected value: False - success
        u.gust_of_wind([t1, t2], 1)
        self.assertFalse(t1.off_guard)
        self.assertFalse(t2.off_guard)

        # expected value: 1
        self.assertEqual(u.actions, 1)

        # expected value: 4
        self.assertEqual(u.casts_gust_of_wind, 4)

        # expected value: True - crit fail
        u.gust_of_wind([t1, t2], 2)
        self.assertTrue(t1.off_guard)
        self.assertTrue(t2.off_guard)

        # expected value: 36-46
        self.assertIn(t1.current_hp, range(36, 47))
        self.assertIn(t2.current_hp, range(36, 47))

        # expected value: True - fail
        t1.not_off_guard()
        t2.not_off_guard()
        u.gust_of_wind([t1, t2], 3)
        self.assertTrue(t1.off_guard)
        self.assertTrue(t2.off_guard)

        # expected value: True
        t1.not_off_guard()
        u.gust_of_wind([t1], 3)
        self.assertTrue(t1.off_guard)

        # expected value: True - crit fail, rng
        t1.not_off_guard()
        t2.not_off_guard()
        u.spell_dc = 100
        u.gust_of_wind([t1, t2], 5)
        self.assertTrue(t1.off_guard)
        self.assertTrue(t2.off_guard)

    def test_force_barrage(self):
        '''
        Method: test_force_barrage
        Parameters: self
        Returns: none
        
        Tests the force_barrage method of the Wizard class. Generates two
        objects of Wizard, a user and a target.
        
        force_barrage() is called three times, one for each action amount.
        Override arguments are used to bypass user input for both action cost
        and target selection.

        The conditional that checks if self.casts_force_barrage > 0 is not
        checked since it only prints.
        '''
        u = Wizard("user")
        t = Wizard("t")
        u.casts_force_barrage = 3

        # expected value: 43-46 - 1 action
        u.force_barrage([t],1,0)
        self.assertIn(t.current_hp, range(43,47))

        # expected value: 2
        self.assertEqual(u.actions, 2)
        self.assertEqual(u.casts_force_barrage, 2)

        # expected value: 38-44 - 2 actions
        t.current_hp = 48
        u.force_barrage([t],2,0)
        self.assertIn(t.current_hp, range(38,45))

        # expected value: 0
        self.assertEqual(u.actions, 0)

        # expected value: 33-42 - 3 actions
        t.current_hp = 48
        u.actions = 3
        u.force_barrage([t],3,0)
        self.assertIn(t.current_hp, range(33,43))

        # expected value: 0
        self.assertEqual(u.actions, 0)

    def test_invisiblity(self):
        '''
        Method: test_invisiblity
        Parameters: self
        Returns: none
        
        Tests the invisibility method of Wizard. Generates 1 object of Wizard
        and calls invisiblity(), targeting itself. Checks that the invis_target
        attribute is assigned the object and that the object's hidden attribute
        is set to True.
        '''
        u = Wizard("user")

        # expected value: u
        u.invisibility(u)
        self.assertEqual(u.invis_target, u)

        # expected value: True
        self.assertTrue(u.hidden)

        # expected value: 1
        self.assertEqual(u.actions, 1)
        self.assertEqual(u.casts_invisibility, 1)

    def test_thunderstrike(self):
        '''
        Method: test_thunderstrike
        Parameters: self
        Returns: none
        
        Tests the thunderstrike method of Wizard. Generates two objects of 
        Wizard, a user and a target.
        
        thunderstrike() is called 5 times: once for each degree of success as 
        well as once with random number generation enabled to verify it 
        functions.
        '''
        u = Wizard("user")
        t = Wizard("target")
        u.casts_thunderstrike = 5

        # expected value: 48 - crit success
        u.thunderstrike(t,1)
        self.assertEqual(t.current_hp, 48)

        # expected value: 1
        self.assertEqual(u.actions, 1)

        # expected value: 4
        self.assertEqual(u.casts_thunderstrike, 4)

        # expected value: 32-46 - success
        u.thunderstrike(t,2)
        self.assertIn(t.current_hp, range(32,47))

        # expected value: -16 - 40 - crit fail
        t.current_hp = 48
        u.thunderstrike(t,3)
        self.assertIn(t.current_hp, range(-16, 41))

        # expected value: 16-44 - fail
        t.current_hp = 48
        u.thunderstrike(t,4)
        self.assertIn(t.current_hp, range(16, 45))

        # expected value: -16 - 40 - crit fail, rng
        t.current_hp = 48
        u.spell_dc = 100
        u.thunderstrike(t,5)
        self.assertIn(t.current_hp, range(-16, 41))

    def test_fireball(self):
        '''
        Method: test_fireball
        Parameters: self
        Returns: none
        
        Tests the fireball method of Wizard. Generates two objects of Wizard, a
        user and a target.
        
        Calls fireball() 5 times: once for each degree of success, and one with
        random number generation enabled to check that it functions.
        '''
        u = Wizard("user")
        t = Wizard("target")
        u.casts_fireball = 5

        # expected value: 48 - crit success
        u.fireball([t], 1)
        self.assertEqual(t.current_hp, 48)

        # expected value: 4
        self.assertEqual(u.casts_fireball, 4)

        # expected value: 1
        self.assertEqual(u.actions, 1)

        # expected value: 30-45 - success
        u.fireball([t],2)
        self.assertIn(t.current_hp, range(30,46))

        # expected value: -24 - 36 - crit fail
        t.current_hp = 48
        u.fireball([t],3)
        self.assertIn(t.current_hp, range(-24, 37))

        # expected value: 12-42 - fail
        t.current_hp = 48
        u.fireball([t],4)
        self.assertIn(t.current_hp, range(12,43))

        # expected value: -24 - 36 - crit fail, rng
        t.current_hp = 48
        u.spell_dc = 100
        u.fireball([t],5)
        self.assertIn(t.current_hp, range(-24, 37))        
                      
    def test_haste(self):
        '''
        Method: test_haste
        Parameters: self
        Returns: none
        
        Tests the haste method of Wizard. Generates one object of Wizard which 
        calls haste() on itself, then ckecks that the values of casts_haste, 
        actions, and extra_actions attributes are updated correctly.
        '''
        u = Wizard("user")

        # expected value: 1 for each
        u.haste(u)
        self.assertEqual(u.casts_haste, 1)
        self.assertEqual(u.extra_actions, 1)
        self.assertEqual(u.actions, 1)

### Out of order, but take_turn needs to come last since it depends on everything else ###
    # def test_take_turn(self):
        # '''
        # Method: test_take_turn
        # Parameters: self
        # Returns: none

        # tests the take_turn method of Wizard. Generates two objects of Wizard, 
        # one user and one target.

        # Uses the override parameters for take_turn() to check all non-query
        # selection options. override1 is used to select each action in turn;
        # override2 likewise selects each spell. override3 is set to 5, bypassing
        # all calls to time.sleep() to allow testing to be more efficient but 
        # otherwise running each method unmodified. overrides 4 and 5 are used to 
        # check that take_turn() can call all variations of force_barrage() 
        # correctly. Attributes are modified to control which result is produced.

        # Query selections are not tested since they consist solely of print 
        # statements.
        # '''
        # u = Wizard("user")
        # t = Wizard("target")
        # u.spell_dc = 100
        # u.actions = 100

        # # expected value: 16-41
        # u.take_turn([u],[t],1,1,5)
        # self.assertIn(t.current_hp, range(16,41))


if __name__ == "__main__":
    unittest.main()
