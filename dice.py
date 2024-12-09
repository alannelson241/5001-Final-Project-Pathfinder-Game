# Alan Nelson
# 12/8/2024
# CS5001
# Final Project: Dice
'''
Contains functions to represent a set of dice.
'''
import random

def d4():
    '''
    Function: d4
    Parameters: none
    Returns: int, the value of the "die" 

    Simulates rolling a 4-sided die.
    '''
    return random.randint(1, 4)

def d6():
    '''
    Function: d6
    Parameters: none
    Returns: int, the value of the "die"

    Simulates rolling a 6-sided die.
    '''
    return random.randint(1, 6)

def d8():
    '''
    Function: d8
    Parameters: none
    Returns: int, the value of the "die"
    
    Simulates rolling an 8-sided die.
    '''
    return random.randint(1, 8)

def d10():
    '''
    Function: d10
    Parameters: none
    Returns: int, the value of the "die"
    
    Simulates rolling a 10-sided die.
    '''
    return random.randint(1, 10)

def d12():
    '''
    Function: d12
    Parameters: none
    Returns: int, the value of the "die"
    
    Simulates rolling a 12-sided die.
    '''
    return random.randint(1, 12)

def d20():
    '''
    function: d20
    Parameters: none
    Returns: int, the value of the "die"
    
    Simulates rolling a 20-sided die.
    '''
    return random.randint(1, 20)

def d100():
    '''
    function: d100
    Parameters: none
    Returns: int, the value of the "die"
    
    Simulates rolling a 100-sided die.
    '''
    return random.randint(1, 100)