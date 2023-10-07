#!/usr/bin/env python3
"""
created:10-03-2023 15:31:06 
author:seraph★776
email:seraph776@gmail.com
project:PROJECTNAME
"""

import string

VOWELS = 'aeiou'
CONSONANTS = ''.join([a for a in string.ascii_lowercase if a not in VOWELS])

NUMERIC_LETTER_VALUES = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
                         'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9,
                         's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8, }

PLANES_OF_EXPRESSION = {
    'mental': 0,
    'physical': 0,
    'emotional': 0,
    'intuitive': 0
}

SCORE = {
    'vowels': 0,
    'consonants': 0
}


def reduce_to_single_digit(number):
    """This function reduces number to single digit unless the number is a Master Number (e.g., 11, 22, 33, 44)"""
    master_numbers = (11, 22, 33, 44)
    while True:
        # Check if number is a master number or single digit, if so return it:
        if number in master_numbers or len(str(number)) == 1:
            break
        # else, cast number to list and attempt to reduce to single digit:
        number = sum([int(n) for n in str(number)])
    return number


def inspector_y(name):
    """This function determines if the letter y in name is either a VOWEL or CONSONANT
    RULES:
        Y is a VOWEL when:
            (1) There are no other vowels in a word, "y" takes on a vowel sound.
            (2) When Y Follows the Last Consonant of a Word
            (3) When Y Follows the Last Vowel of a Word
            (4) hen Y Is in the Middle of a Syllable
            (5) When Y Is in the Middle of a Syllable
        Y is a CONSTANT when:
            (1) when Y Is the First Letter in a Word
            (2) When Y is the First Letter in a Syllable
     """
    global SCORE
    # If name starts with Y mark as CONSONANT:
    if name[0] == 'y':
        SCORE['consonants'] += NUMERIC_LETTER_VALUES.get('y')

    # If there are no other vowels mark as VOWEL
    vowel_check = len([a for a in name if a in VOWELS]) == 0
    if vowel_check and 'y' in name:
        SCORE['vowels'] += NUMERIC_LETTER_VALUES.get('y')

    # If Y follows last CONSONANT in name, mark as VOWEL
    if name[-1] == 'y' and name[-2] in CONSONANTS:
        SCORE['vowels'] += NUMERIC_LETTER_VALUES.get('y')

    # If Y follows last VOWEL in name, mark as VOWEL
    if name[-1] == 'y' and name[-2] in VOWELS:
        SCORE['vowels'] += NUMERIC_LETTER_VALUES.get('y')

    # If Y is in the Middle of the syllable, mark as VOWEL
    for i in range(1, len(name) - 1):
        # If letter is Y:
        if name[i] == 'y':
            # If the letter to teh left, and the letter to the right are CONSTANTS then mark as
            if name[i - 1] in CONSONANTS or name[i + 1] in CONSONANTS:
                SCORE['vowels'] += NUMERIC_LETTER_VALUES.get('y')
            else:
                SCORE['consonants'] += NUMERIC_LETTER_VALUES.get('y')
    # Removing letter Y from name
    name = name.replace('y', '')
    return name


def parse_name(name):
    """This is the main parsing function,that evaluates each letter of the name"""
    global SCORE

    if name == '':
        pass
    else:
        # (!) Integrity check: Because name gets modify in the inspector_y function, Therefore, name gets
        # checked for integrity first.
        name = name.lower()
        if integrity_check(name):
            # First determine if each occurrence of the letter Y is ether is VOWEL or CONSONANT:
            name = inspector_y(name)
            # Then evaluate all other letters
            for i, letter in enumerate(name):
                if letter in VOWELS:
                    SCORE['vowels'] += NUMERIC_LETTER_VALUES.get(letter)
                if letter in CONSONANTS:
                    SCORE['consonants'] += NUMERIC_LETTER_VALUES.get(letter)
            return name


def integrity_check(name):
    """
    Ths function checks that the total occurrences of each number in the inclusion table
    is the same as the total length of name.

    For example:
        seraph = [1, 5, 9, 1, 7, 8]                 # Value of each letter in the name
        result = {1: 2, 5: 1, 9: 1, 7: 1, 8: 1}     # Count occurrence of each number in the list
        values = [2, 1, 1, 1, 1]                    # Sum the total of the results
        total = 6
        len(seraph)  == 6                           # The total sum must always be the same length of name
    """
    # name = name.replace(' ', '').lower()
    c1 = all([l.isalpha() for l in name])
    if not c1:
        raise Exception('Error >> Name must contain all letters!')

    inclusion_table = [NUMERIC_LETTER_VALUES.get(i) for i in name]
    # Count the number of occurrences of each digit in inclusion table:
    count_values = {k: inclusion_table.count(k) for k in inclusion_table}

     # Cast to a list, and sum the letter values:
    result = sum(list(count_values.values()))
    # The value should be equal to the length of the name
    if result != len(name):
        raise Exception('Name failed integrity check!')
    else:
        return True


def evaluate_name(first_name: str, last_name: str, middle_name: str):
    full_name = [first_name, middle_name, last_name]
    for name in full_name:
        parse_name(name)
    return full_name


def calculate_final_results(full_name: list):
    planes_of_expression = {
        'mental': 0,
        'physical': 0,
        'emotional': 0,
        'intuitive': 0
    }
    life_direction = {'desire': reduce_to_single_digit(SCORE['vowels']),
                      'personality': reduce_to_single_digit(SCORE['consonants']),
                      'destiny': reduce_to_single_digit(SCORE['vowels'] + SCORE['consonants'])}

    for name in full_name:
        inclusion_table = [NUMERIC_LETTER_VALUES.get(i) for i in name]
        # Count the number of occurrences of each digit in inclusion table:
        count_values = {k: inclusion_table.count(k) for k in inclusion_table}

        mental = sum([count_values.get(i) for i in count_values if i in [1, 8]])
        physical = sum([count_values.get(i) for i in count_values if i in [4, 5]])
        emotional = sum([count_values.get(i) for i in count_values if i in [2, 3, 6]])
        intuitive = sum([count_values.get(i) for i in count_values if i in [7, 9]])

        planes_of_expression['mental'] = reduce_to_single_digit(mental)
        planes_of_expression['physical'] = reduce_to_single_digit(physical)
        planes_of_expression['emotional'] = reduce_to_single_digit(emotional)
        planes_of_expression['intuitive'] = reduce_to_single_digit(intuitive)

    return {'Life Direction': life_direction, 'Planes of Existence': planes_of_expression}


def main():
    result = evaluate_name(first_name='amelia', last_name='earhart', middle_name='mary')
    print(calculate_final_results(result))


if __name__ == '__main__':
    main()
