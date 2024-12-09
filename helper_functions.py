# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Helper Functions
'''
Helper functions involving user input or randomness.
'''
import dice

def target_select(target_list, option_name):
    # https://stackoverflow.com/questions/37565793/how-to-let-the-user-select-an-input-from-a-finite-list
    '''
    Function: target_select
    Parameters: self, list - list of options; str - name of said list
    Returns: object, the selected object

    Function to allow the player to select a target. Converts the target list
    to a dict with the key and value being the same, then generates a list of 
    the dict keys and prints messages along the lines of 
        1. option
        2. option2
        3. option3
    for the user to select from in the next step.

    The function then enters an input validation loop, collecting input in the
    form of an integer from the user; 1 is subtracted from the int to convert
    it to the corresponding index value. If incorrect input is submitted, 
    raises either a TypeError for a number that does not correspond to any 
    index or a ValueError if a non-integer is entered. When valid input is
    submitted, returns the corresponding list value.
    '''
    option_dict = {}
    for item in target_list:
        option_dict[item] = item
    index = 0
    option_list = []
    if option_name[0] in "aeiou":
        print("Select an", option_name + ":")
    else:
        print('Select a', option_name + ':')
    for key in option_dict:
        index = index + 1
        option_list.extend([option_dict[key]])
        print(str(index) + '. ' + str(key))
    valid = False
    while not valid:
        try:
            pick = int(input(option_name + ': ')) - 1
            if pick > -1 and pick < len(option_list):
                selected = option_list[pick]
                print('Selected ' +  option_name + ': ' + str(selected))
                valid = True
            else:
                raise TypeError("Enter a valid number.")
        except TypeError as err:
            print(err)
        except ValueError:
            print("Enter a number.")
    return selected

def random_target(target_list, override = -1):
    '''
    Function: random_target
    Parameters: list - list of 4 objects; int, value to force a result
    Returns: object, target of the effect

    Function for randomly selecting a player character to target. Chooses one
    of the four pc's at random to return. 

    Note that random_target() must take a target_list of exactly four items.
    '''
    if override == -1:
        target = target_list[dice.d4() - 1]
    else:
        target = target_list[override]
    return target
