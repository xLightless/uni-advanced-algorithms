"""
This module contains Task 1.3 "Search with parallelism".

You need to design a frequency-counting program with parallelism programming.
Your task is to count the frequency of each name in the text.

You are given two files:
- One is the file with a long text.
- The other is a file including a set of names.

The Result:
- The result is like “Harry” 102, “Ron” 54 and so on.
- The result should be saved in a new file.
- Compound words including these names should be counted too.

For example, the word like “Harry's talk ...” should be counted
even if “Harry” is not an independent word.
"""

import time
import os
import multiprocessing as mp


class FrequencyCounter:
    """
    Using parallelism programming count the frequency
    of strings.

    Predicate: ∀x∀y(S(x)∧N(y)∧F(x,y)=count(x,y))
    """

    def get_stringfile(self, file_name: str) -> str:
        """
        This function gets the ASCII characters from a text file
        and reads it into an array of characters.
        :return: str
        """

        with open(file_name, "r", encoding="utf-8") as file:
            file_string = file.read()
        return file_string

    def