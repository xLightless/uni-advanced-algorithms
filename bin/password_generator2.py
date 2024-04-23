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
from typing import List


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
        self.categories = self.capitals + self.lowercase \
            + self.numericals + self.symbols

        self.int_categories = self.convert_categories(
            self.capitals + self.lowercase + self.numericals + self.symbols
        )

        # print(self.categories, self.int_categories)

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

    # def has_partial_rules(self, password) -> bool:
    #     """
    #     Checks if the partial password meets the rule bounds.
    #     """

    #     # - must include at least one element from each category
    #     # - must start with letter
    #     # - must not include more than two capital letters
    #     # - must not include more than two special symbols

    #     is_first_letter = False
    #     max_capital_letters = False
    #     max_special_letters = False
    #     starting_index = password[0]

    #     # Must start with a letter (lower or upper case)
    #     if starting_index <= 9:
    #         is_first_letter = True

    #     if not (is_first_letter):
    #         return False

    #     return True

    def has_starting_letter(self, password) -> bool:
        """
        Must start with a letter (lower or upper case).
        """

        starting_index = password[0]
        if not starting_index <= len(self.lowercase) + len(self.capitals) - 1:
            return False
        return True

    def has_each_category_item(self, password) -> bool:
        """
        Must include at least one element from each category.
        """

        has_capital = 0
        has_lower = 0
        has_numerical = False
        has_symbol = 0

        for i in password:
            if i < 5:
                has_capital += 1

            if i >= 5 and i < 10:
                has_lower += 1

            if (i >= 10 and i < 15) and has_numerical is False:
                has_numerical = True

            if i >= 15:
                has_symbol += 1

        if not (
            self.has_starting_letter(password) and
            self.has_bicapitalization(capitals=has_capital) and
            self.has_symbols(symbols=has_symbol)
        ):
            return False

        if not has_numerical:
            return False

        return True

    def has_bicapitalization(self, capitals: int):
        """
        Must not include more than two capital letters.
        Bicapitalization is where the first letter is capital
        and somewhere else in the word.
        """

        if capitals > 2 or capitals == 0:
            return False
        return True

    def has_symbols(self, symbols: int):
        """
        Must not include more than two special symbols.
        """
        if symbols > 2 or symbols == 0:
            return False
        return True

    def has_partial_rules(self, password):
        """
        Checks the partial password rule boundaries.
        :returns: true if has_partial_rules, otherwise false.
        """

        if len(password) != self.password_length:
            return False

        has_capital = 0
        has_lower = 0
        has_numerical = 0
        has_symbol = 0

        for i in password:
            if i < 5:
                has_capital += 1

            if i >= 5 and i < 10:
                has_lower += 1

            if i >= 10 and i < 15:
                has_numerical += 1

            if i >= 15:
                has_symbol += 1

        if not self.has_each_category_item(password):
            return False

        return True

        # current_password = [
        #     self.has_each_category_item(password),
        #     self.has_starting_letter(password),
        #     self.has_bicapitalization(password),
        #     self.has_limited_repeated_symbols(password)
        # ]

        # if not (  # If passed we can assume its true
        #     self.has_each_category_item(password) and
        #     self.has_starting_letter(password)
        # ):
        #     return False

        # if not (
        #     self.has_bicapitalization(password) and
        #     self.has_limited_repeated_symbols(password)
        # ):
        #     return False

        # if current_password != [True] * 4:
        #     return False
        # return True

    def custom_product2(self, *iterables, password_length):
        """
        Tail Recursive Optimization (TCO) implementation of
        product with characters from multiple sets. TCO is a
        memory technique for recursive depth handling.

        Parameters:
        *iterables (list): Input variable of n sets
        length (int): password/string length expected.

        Returns:
        list of strings: All possible passwords of the given length.
        """

        def tail_recursive_product(password, current_index):

            if current_index == password_length:
                if (
                    self.has_starting_letter(password)
                ):
                    return [tuple(password)]
                return []

            accumulated_passwords = []
            for char_set in iterables:
                for char in char_set:
                    print(password)
                    password.append(char)
                    print(password)
                    accumulated_passwords.extend(
                        tail_recursive_product(
                            password, current_index + 1
                        )
                    )

                    # print(password)
                    password.pop()
            return accumulated_passwords

        return tail_recursive_product([], 0)

    def custom_product(self, password_length) -> List[str]:
        """
        Tail Recursive Optimization (TCO) implementation of
        product with characters from multiple sets. TCO is a
        memory technique for recursive depth handling.

        Parameters:
        password_length (int): password/string length expected.

        Returns:
        list of strings: All possible passwords of the given length.
        """

        def tail_recursive_product(
            password,
            current_index: int,
            capitals_used: bool,
            lowercase_used: bool,
            numericals_used: bool,
            symbols_used: bool
        ):
            if current_index == password_length:
                # Check if all categories have been used at least once
                if capitals_used and lowercase_used and numericals_used and symbols_used:
                    return ["".join(password)]
                return []

            accumulated_passwords = []
            for char in self.categories:
                new_password = password + [char]
                new_capitals_used = capitals_used or (char in self.capitals)
                new_lowercase_used = lowercase_used or (char in self.lowercase)
                new_numericals_used = numericals_used or (char in self.numericals)
                new_symbols_used = symbols_used or (char in self.symbols)

                if current_index == 0 and char not in (self.capitals + self.lowercase):
                    continue

                accumulated_passwords.extend(
                    tail_recursive_product(
                        new_password,
                        current_index + 1,
                        new_capitals_used,
                        new_lowercase_used,
                        new_numericals_used,
                        new_symbols_used
                    )
                )
            # print(new_capitals_used, new_lowercase_used, new_numericals_used, new_symbols_used)
            return accumulated_passwords

        # Initialize variables to track whether each category has been used at least once
        capitals_used = False
        lowercase_used = False
        numericals_used = False
        symbols_used = False

        return tail_recursive_product(
            [], 0, capitals_used, lowercase_used, numericals_used, symbols_used
        )

    def generate_passwords(self):
        """
        Generate all possible passwords within the rule bounds.
        """

        start_time = time.time()
        passwords = self.custom_product(self.password_length)
        end_time = time.time()
        f = open("log.txt", "w", encoding="utf-8")
        for password in passwords:
            f.write(f"{password} \n")
        elapsed_time = end_time - start_time
        print(f"Found {len(passwords)} passwords.")
        print(f"The algorithm took {elapsed_time} seconds to complete.")


password_length_input = int(input("Enter a password length: "))

password_generator = PasswordGenerator(password_length=password_length_input)
password_generator.generate_passwords()
