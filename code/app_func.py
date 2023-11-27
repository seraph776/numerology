#!/usr/bin/env python3
"""
created:11-25-2023 04:48:50
author:seraph★776
email:seraph776@gmail.com
project:PROJECTNAME
"""
import re
import string
import pyphen
from cipher import CIPHER

VOWELS = 'aeiou'
CONSONANTS = ''.join([a for a in string.ascii_lowercase if a not in VOWELS])
MASTER_NUMBERS = (11, 22, 33)

NUMERIC_LETTER_VALUES = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
                         'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9,
                         's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6, 'z': 8, }  # Y == 7


def reduce_digit(number):
    while True:
        if number in MASTER_NUMBERS:
            break
        if len(str(number)) == 1:
            break
        else:
            number = sum([int(n) for n in str(number)])
    return number


def life_path_number(birthday: str) -> int:
    pattern = r'/|-|\.| '
    month, day, year = [int(n) for n in re.split(pattern, birthday)]
    return reduce_digit(sum([month, day, year]))


def split_name(name):
    n = pyphen.Pyphen(lang='en')
    return n.inserted(name).split('-')


def calculate_numerology(first_name='', last_name='', middle_name='', birthday=''):
    score = {

        'life_path': 0,
        'soul_urge': 0,
        'personality': 0,
        'destiny': 0,

    }

    if middle_name:
        full_name = [first_name, last_name, middle_name]
    else:
        full_name = [first_name, last_name]

    full_name = [name.lower().replace(' ', '') for name in full_name]
    for name in full_name:

        # (1) If there are no other vowels in a word, "y" = VOWEL
        available_vowels = len([a for a in name if a in VOWELS])
        if available_vowels == 0 and 'y' in name:
            for letter in name:
                if letter == 'y':
                    score['soul_urge'] += 7
            return score

        # (2) If Y Is in the Middle of a Syllable marks as VOWEL
        syllable_name: list = split_name(name)
        new_syllables = []
        for i, syllable in enumerate(syllable_name):
            idx = len(syllable) // 2
            middle_syllable = syllable[idx]
            if middle_syllable == 'y':
                score['soul_urge'] += 7
            new_syllables.append(syllable.replace(middle_syllable, '', 1))
        # (3) If Y is the last letter mark as VOWEL
        for i, syllable in enumerate(new_syllables):
            if syllable[0] == 'y':
                score['personality'] += 7
            if syllable[-1] == 'y':
                score['soul_urge'] += 7

            # (4) If Y is anything else mark as CONSONANT
            for i, letter in enumerate(syllable[1:-1]):
                if letter == 'y':
                    score['soul_urge'] += 7

        # Now that Y has been calculated, remove Y, and determine the value of the remaining letters
        name = name.replace('y', '')

        for letter in name:
            if letter in VOWELS:
                score['soul_urge'] += NUMERIC_LETTER_VALUES.get(letter)
            if letter in CONSONANTS:
                score['personality'] += NUMERIC_LETTER_VALUES.get(letter)

        # Reduce digits to single digits
        score['life_path'] = reduce_digit(life_path_number(birthday))
        score['soul_urge'] = reduce_digit(score.get('soul_urge'))
        score['personality'] = reduce_digit(score.get('personality'))
        score['destiny'] = reduce_digit(score['soul_urge'] + score['personality'])

    for quality in score:
        print(f'{quality.upper()} ({score.get(quality)}): >>>  {CIPHER[score.get(quality)]}')
    print()

    return score


print(calculate_numerology(first_name='rebekka', last_name='williams', middle_name='karoline', birthday='3/7/1955'))
