"""
This module contains Task 1.1 Password Generator.

# Valid password elements:
# - {A, B, C, D, E},
# - {a, b, c, d, e},
# - {1, 2, 3, 4, 5},
# - {$, &, %}

# Rules:
# - must include at least one element from each category
# - must start with letter
# - must not include more than two capital letters
# - must not include more than two special symbols

"""

import time
from itertools import product


class PasswordGenerator:
    """
    Generate passwords via partial knowledge of the
    composition and password length.
    """

    def __init__(self, password_length: int = 4):
        self.password_length = password_length
        self.capitals = ['A', 'B', 'C', 'D', 'E']
        self.lowercase = ['a', 'b', 'c', 'd', 'e']
        self.numericals = ['1', '2', '3', '4', '5']
        self.symbols = ['$', '&', '%']
        self.int_categories = self.capitals + self.lowercase \
            + self.numericals + self.symbols
        self.categories = self.capitals + self.lowercase \
            + self.numericals + self.symbols

    def convert_categories(self, categories):
        """
        Convert the categories in each array to an integer to improve
        memory efficiency.
        """

        for i, _ in enumerate(categories):
            categories[i] = i
        return categories

    def has_rules(self, password) -> bool:
        """
        Checks if the password follows the rule bounds.
        """

        max_capitals = 2
        max_symbols = 2

        capitals_count = 0
        letter_count = 0
        symbols_count = 0
        numerical_count = 0

        starting_index = password[0]
        letters = (len(self.capitals) + len(self.lowercase)) - 1
        capitals = len(self.capitals) - 1
        symbols = len(self.symbols) - 1

        # Must start with letter (capital or lower-case)
        if starting_index > letters:
            return False

        # Can also start with a capital (capital or lower-case)
        if starting_index <= capitals:
            capitals_count += 1
        else:
            letter_count += 1

        for _, i in enumerate(password[1::]):
            if i <= capitals:  # Capitals
                capitals_count += 1

            if i >= (len(self.int_categories) - 1 - symbols):  # Symbols
                symbols_count += 1

            # Numerical values
            if i < (len(self.int_categories) - 1 - symbols) and i > letters:
                numerical_count += 1

            if i > capitals and i <= letters:
                letter_count += 1

        # Must not include more than two special symbols/capital letters
        if symbols_count > max_symbols or capitals_count > max_capitals:
            return False

        # Must include at least one element from each category
        if (
            not symbols_count or
            not capitals_count or
            not numerical_count or
            not letter_count
        ):
            return False
        return True

    def custom_product(self, *iterables, password_length):
        """
        Tail Recursive Optimization (TCO) implementation of
        product with characters from multiple sets.

        Parameters:
        *iterables (list): Input variable of n sets
        length (int): password/string length expected.

        Returns:
        list of strings: All possible passwords of the given length.
        """
        def tail_recursive_product(password, current_index):
            if current_index == password_length:
                return [tuple(password)]

            accumulated_passwords = []
            for char_set in iterables:
                for char in char_set:
                    password.append(char)
                    accumulated_passwords.extend(
                        tail_recursive_product(
                            password, current_index + 1
                        )
                    )
                    password.pop()
            return accumulated_passwords

        return tail_recursive_product([], 0)

    # def generate_passwords(self):
    #     """
    #     Generate all possible passwords within the rule bounds.
    #     """

    #     self.convert_categories(self.int_categories)
    #     counter = 0
    #     passwords = product(self.int_categories, repeat=self.password_length)
    #     for password in passwords:
    #         if self.has_rules(password) is True:
    #             counter += 1

    #     print(f"A total of {counter} password(s) have been generated.")


    def generate_passwords(self):
        """
        Generate all possible passwords within the rule bounds.
        """

        self.convert_categories(self.int_categories)
        counter = 0
        passwords = self.custom_product(self.int_categories, password_length=self.password_length)
        for password in passwords:
            if self.has_rules(password):
                counter += 1

        print(f"Found {counter} passwords.")


password_length_input = int(input("Enter a password length: "))
password_generator = PasswordGenerator(password_length=password_length_input)
start_time = time.time()
password_generator.generate_passwords()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"The algorithm took {elapsed_time} seconds to complete.")
