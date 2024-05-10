"""
This module contains "Task 1.1 Password Generator".

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

Originally created by Reece Turner, 22036698.

"""

import time
import typing
import matplotlib.pyplot as plt


class PasswordGenerator:
    """
    Generate passwords via partial knowledge of the
    composition and password length.

    You can obtain these passwords externally via #passwords
    after generation.
    """

    def __init__(self, password_length: int = 4):
        self.password_length = password_length
        self.capitals = ['A', 'B', 'C', 'D', 'E']
        self.lowercase = ['a', 'b', 'c', 'd', 'e']
        self.numericals = ['1', '2', '3', '4', '5']
        self.symbols = ['$', '&', '%']
        self.categories = self.capitals + self.lowercase \
            + self.numericals + self.symbols

        self.passwords = []

    def generate_passwords(self) -> typing.List[str]:
        """
        Tail Recursive Optimization (TCO) implementation of
        product with characters from multiple sets. TCO is a
        memory technique for recursive depth handling.

        Returns:
        list of strings: All possible passwords of the given length.
        """

        def tail_recursive_product(
            password,
            current_index: int,
            capitals_used: bool,
            lowercase_used: bool,
            numericals_used: bool,
            symbols_used: bool,
            num_capitals: int,
            num_symbols: int
        ):

            # Guard clause return statement to check if theres
            # a need to perform recursion
            if current_index == self.password_length:
                if (
                    capitals_used and
                    lowercase_used and
                    numericals_used and
                    symbols_used
                ):
                    return ["".join(password)]
                return []

            # Create an array and passwords to store
            accumulated_passwords = []
            for char in self.categories:
                new_password = password + [char]
                new_capitals_used = capitals_used or (char in self.capitals)
                new_lowercase_used = lowercase_used or (char in self.lowercase)
                new_numericals_used = numericals_used or (
                    char in self.numericals
                )
                new_symbols_used = symbols_used or (char in self.symbols)

                if current_index == 0 and char not in (
                    self.capitals + self.lowercase
                ):
                    continue

                if char in self.capitals:
                    new_num_capitals = num_capitals + 1
                    if new_num_capitals > 2:
                        continue
                else:
                    new_num_capitals = num_capitals

                if char in self.symbols:
                    new_num_symbols = num_symbols + 1
                    if new_num_symbols > 2:
                        continue
                else:
                    new_num_symbols = num_symbols

                accumulated_passwords.extend(
                    tail_recursive_product(
                        new_password,
                        current_index + 1,
                        new_capitals_used,
                        new_lowercase_used,
                        new_numericals_used,
                        new_symbols_used,
                        new_num_capitals,
                        new_num_symbols
                    )
                )
            return accumulated_passwords

        # Update rules to false for the next recursion
        capitals_used = False
        lowercase_used = False
        numericals_used = False
        symbols_used = False

        # Prevents excessive recursion of adding a new capital or symbol since
        # we need to account for different types
        num_capitals = 0
        num_symbols = 0

        return tail_recursive_product(
            [], 0,
            capitals_used,
            lowercase_used,
            numericals_used,
            symbols_used,
            num_capitals,
            num_symbols
        )

    def _generate_passwords(self) -> float:
        """
        Internal function to handle display output of passwords.
        """

        start_time = time.time()
        pwrds = self.generate_passwords()
        end_time = time.time()
        self.passwords = pwrds
        elapsed_time = end_time - start_time
        counter = 0
        for password in self.passwords:
            counter += 1
            print(f"{counter}. {password}")
        return elapsed_time

    def __str__(self):
        elapsed_time = self._generate_passwords()
        results = f"\nFound {len(self.passwords)} passwords." + \
            f"\nTook {elapsed_time} seconds."
        return results


if __name__ == '__main__':
    user_input = int(input("Enter a password length: "))
    password_generator = PasswordGenerator(user_input)
    print(password_generator)
    password_time = {}
    passwords = {}

    GRAPH = True
    RUNS = 5
    average_time = 0

    # Create a graph of the user input over multiple runs.
    # We use a seperate elapsed time as this loops over
    # multiple instances whereas __str__ is designed for a
    # a single ran instance.
    if GRAPH:
        for i in range(RUNS):
            i_start_time = time.time()
            passwords[i] = password_generator.generate_passwords()
            i_end_time = time.time()
            elapsed_time_frame = i_end_time - i_start_time
            password_time[i] = elapsed_time_frame
            average_time += password_time[i]

        print(f"Average time over {RUNS} runs: {average_time / RUNS} seconds.")

        x = list(password_time.keys())
        y = list(password_time.values())
        plt.bar(x, y)
        plt.xlabel(f"Execution runs of password length {user_input}")
        plt.ylabel("Algorithm time taken")
        plt.title("Comparison of Run Times")
        plt.show()
