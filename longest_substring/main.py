"""
Retrieve the longest substrings but with k repeated elements.

Originally created by Reece Turner, 22036698.
"""

import os
import time
import typing


class LongestSubstrings:
    """
    Retrieve the longest substrings from a given
    set with k repeated elements.
    """

    def __init__(
        self,
        k: int = 1
    ):
        self.k = k
        current_directory = os.path.dirname(os.path.abspath(__name__))
        self.current_directory = current_directory + "\\"
        self.task_directory = self.current_directory + "\\tasks\\Task 1_2\\"

        self.string = self.get_stringfile(
            self.task_directory +
            "string.txt"
        )

    def get_stringfile(self, file_name: str) -> str:
        """
        This function gets the ASCII characters from a text file
        and reads it into an array of characters.
        :return: str
        """

        with open(file_name, "r", encoding="utf-8") as file:
            file_string = file.read()
        return file_string

    def is_valid_string(self, string: str) -> bool:
        """
        Check the algorithm against this rule boundary
        for violating k repeated.
        :return: bool
        """

        char_freq = {}
        for char in string:
            char_freq[char] = char_freq.get(char, 0) + 1

        repeats = [char for char, freq in char_freq.items() if freq > 1]

        if len(repeats) > self.k:
            return False
        return True

    def get_longest_substring(self) -> typing.List[str]:
        """
        Return the longest substring of k elements
        using dynamic programming + sliding window.
        :return: List[str].
        """

        max_length = 0
        max_substrings = []
        current_start = 0
        current_length = 0

        for i in range(len(self.string)):
            current_length += 1

            while not self.is_valid_string(self.string[current_start:i+1]):
                current_start += 1
                current_length -= 1

            if current_length > max_length:
                max_length = current_length
                max_substrings = [self.string[current_start:i+1]]

            elif current_length == max_length:
                # We use append as its O(1) where as
                # max_substring += [item] is O(n)
                max_substrings.append(self.string[current_start:i+1])

        return max_substrings

    def __str__(self):
        start_time = time.time()
        substrings = self.get_longest_substring()
        end_time = time.time()
        elapsed_time = end_time - start_time

        if len(substrings) == 0:
            return "[WARNING] No valid substrings were found!"
        return f"{substrings}.\nTook {elapsed_time} seconds."


if __name__ == "__main__":
    k_input = input("Enter substring, k, length: ")
    longest_substring = LongestSubstrings(k=int(k_input))
    print(longest_substring)
