def longest_substring_with_k_repetitions(string, k):
    # Initialize variables to store the start and end indices of the longest substring
    start = 0
    end = 0
    max_length = 0
    longest_substring = ""

    # Dictionary to keep track of character counts in the current window
    char_count = {}

    while end < len(string):
        # Add the character at the end index to the char_count dictionary
        char_count[string[end]] = char_count.get(string[end], 0) + 1

        # Move the end pointer forward
        end += 1

        # Check if all characters in the current window have counts equal to k
        if all(count == k for count in char_count.values()):
            # Check if the current window is longer than the previously found longest substring
            if end - start > max_length:
                max_length = end - start
                longest_substring = string[start:end]

        # If any character count exceeds k, move the start pointer forward
        # until all characters have counts less than or equal to k
        while any(count > k for count in char_count.values()):
            char_count[string[start]] -= 1
            if char_count[string[start]] == 0:
                del char_count[string[start]]
            start += 1

    return longest_substring

# Test the function
given_string = 'AABACDE'
k = 1
print(longest_substring_with_k_repetitions(given_string, k))
