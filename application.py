# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Application

import time
import sys

from cleric import Cleric
from fighter import Fighter
from rogue import Rogue
from wizard import Wizard
from goblin import Goblin
from hobgoblin_soldier import Hobgoblin_Soldier
from orc_warrior import Orc_Warrior
from orc_commander import Orc_Commander
from hobgoblin_general import Hobgoblin_General
from dragon import Dragon

def initiative(player_list, enemy_list):
    '''
    Method: initiative
    Parameters: 2 lists - list of PC's and of NPC's
    Returns: list - list of characters in initiative order
    
    Updates encounter_list and creates an init_list to determine turn order.

    First, combines the player and enemy lists into an encounter list, then 
    calls roll_initiative() on each object in said list, saving the result in
    a separate multidimensional list containing the result and the object. 
    Finally, sorts the second list and returns it.
    '''
    encounter_list = player_list + enemy_list
    raw_init_list = []
    for char in encounter_list:
        raw_init_list.append(char.roll_initiative())
        time.sleep(.5)
    init_list = sorted(raw_init_list, key = lambda x: x[0], reverse = True)
    print('')
    time.sleep(1)
    return init_list


def encounter(player_list, enemy_list, init_list):
    '''
    Function: encounter
    Parameters: 3 lists - list of PC's, NPC's, and of characters in initiative order
    Returns: none
    
    Generates the loop structure that conducts an encounter.

    First, creates a list of all objects in the encounter for later use. Then 
    begins a loop that will continue until the encounter ends. Inside that loop,
    a second loop iterates through the initiative list, prompting each character
    in order to take their turns using the object's take_turn() method if a 
    player character or ai() method if a nonplayer character. On a character's
    turn, begins one final loop that continues until that character uses all of 
    their actions. At the start and end of a creature's turn, calls the 
    start_turn() and end_turn() methods respectively to reset relevant values.

    The innermost loop ends when the turn player runs out of actions; the 
    middle loop either ends once all characters in initiative have taken their
    turns and is restarted by the outer loop or is broken out of if either team
    has 0 remaining HP. This latter condition also ends the outer loop by 
    updating its loop variable.
    '''
    encounter_list = player_list + enemy_list
    stop = False
    while stop == False:
        for char in init_list:
            time.sleep(1)
            if char[1].current_hp > 0:
                char[1].start_turn()
                print(char[1].name + "'s turn!")
                while char[1].actions > 0:
                    if char[1].team == "ally":
                        char[1].take_turn(player_list, enemy_list)
                    elif char[1].team == "enemy":
                        char[1].ai(player_list, enemy_list)
                    print('')
                char[1].end_turn(encounter_list)
                print("")
                time.sleep(1)
                
            else:
                print(char[1].name, "has 0 HP! They can't fight!")
            a = 0
            for i in range(len(player_list)):
                a += player_list[i].current_hp
            b = 0
            for i in range(len(enemy_list)):
                b += enemy_list[i].current_hp
            if (a <= 0) or (b <= 0):
                stop = True
                # talked about this break statement in office hours; no other effective way to stop the for loop
                break

def main():
    '''
    Function: main
    Parameters: none
    Returns: none
    
    Executes the application.

    If a number is passed to the terminal as an argument, is converted to an 
    int and used as an override parameter to skip to a specific fight.

    Takes user input for the names of the four player characters and creates
    objects for each which are then stored in a list of player characters. The
    function then executes four encounters:

        1. 4 goblins and 1 hobgoblin soldier
        2. 2 orc warriors and 1 orc commander
        3. 4 goblins and 1 hobgoblin general
        4. 1 young green dragon
    
    After an encounter is completed, checks to see if it ended because the 
    player ran out of HP, also calling end_encounter() on each PC at the same
    time. If the player lost the last encounter, ends the game.
    '''
    if len(sys.argv) > 1:
        if sys.argv[1].isnumeric():
            override = int(sys.argv[1])
        else:
            override == 0
    else:
        override = 0
    print("Gather your adventuring party!")
    fig_name = input("What is the fighter's name? ")
    wiz_name = input("What is the wizard's name? ")
    rog_name = input("What is the rogue's name? ")
    cle_name = input("What is the cleric's name? ")
    fig = Fighter(fig_name)
    wiz = Wizard(wiz_name)
    rog = Rogue(rog_name)
    cle = Cleric(cle_name)
    player_list = [wiz,fig,cle,rog]

    print("")
    print("The party of", fig.name + ",", wiz.name + ",", rog.name + ", and", cle.name, "venture forth!")
    print("The party decends into the dungeon.")
    print("A gang of goblins appears! They ready for battle!")
    time.sleep(1)

    if override == 0 or override == 1:
        enemy_list = [Goblin("Gakk"), Goblin("Margo"), Goblin("Ludo"), Goblin("Cronch"), Hobgoblin_Soldier()]
        init_list = initiative(player_list, enemy_list)
        encounter(player_list, enemy_list, init_list)
        a = 0
        for i in range(len(player_list)):
            a += player_list[i].current_hp
            player_list[i].end_encounter()
        if a > 0:
            print("The party are victorious!")
        else:
            print("Alas, the party were vanquished!")
            return
    
    print("")
    print("The party continues their decent into the depths.")
    print("A party of orcs appear! They charge to attack!")
    time.sleep(1)

    if override == 0 or override == 2:
        enemy_list = [Orc_Warrior("Kabor"), Orc_Warrior("Avak"), Orc_Commander()]
        init_list = initiative(player_list, enemy_list)
        encounter(player_list, enemy_list, init_list)
        a = 0
        for i in range(len(player_list)):
            a += player_list[i].current_hp
            player_list[i].end_encounter()
        if a > 0:
            print("The party are victorious!")
        else:
            print("Alas, the party were vanquished!")
            return

    print("")
    print("The party decend into the darkest corners of the dungeons.")
    print("A hobgoblin general appears and barks orders to his troops!")
    time.sleep(1)

    if override == 0 or override == 3:
        enemy_list = [Goblin("Baboo"), Goblin("Jenkins"), Goblin("Boblin"), Goblin("Makka"), Hobgoblin_General()]
        init_list = initiative(player_list, enemy_list)
        encounter(player_list, enemy_list, init_list)
        a = 0
        for i in range(len(player_list)):
            player_list[i].end_encounter()
            a += player_list[i].current_hp
        if a > 0:
            print("The party are victorious!")
        else:
            print("Alas, the party were vanquished!")
            return

    print("")
    print("The party enters into a dragon's lair!")
    print("A mighty dragon attacks!")
    time.sleep(1)

    if override == 0 or override == 4:
        enemy_list = [Dragon()]
        init_list = initiative(player_list, enemy_list)
        encounter(player_list, enemy_list, init_list)
        a = 0
        for i in range(len(player_list)):
            a += player_list[i].current_hp
            player_list[i].end_encounter()
        if a > 0:
            print("The party are victorious!")
            print("Congratulations! You won!")
        else:
            print("Alas, the party were vanquished!")
            return

if __name__ == "__main__":
    main()            
