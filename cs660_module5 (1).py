
# CS-660 Module Five Activity
# Student: Justice Williamson
# Part One: Programming Paradigm Comparison


# --------------------------------------------------
# 1. Imperative Programming Approach
# --------------------------------------------------

def imperative_approach(numbers):
    # Create an empty list to store the results.
    result = []

    # Use a loop to process each number step by step.
    for number in numbers:

        # Check whether the number is odd.
        # Even numbers are excluded from the result.
        if number % 2 != 0:

            # Square the odd number and add it to the list.
            result.append(number ** 2)

    # Return the completed list of squared odd numbers.
    return result


# Test the imperative approach.
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print("Original List:", numbers)
print("Imperative Result:", imperative_approach(numbers))

# --------------------------------------------------
# 2. Object-Oriented Programming Approach
# --------------------------------------------------

class OddNumberProcessor:
    # The constructor initializes the object's data.
    # Encapsulation keeps the number list inside the object.
    def __init__(self, numbers):
        self.numbers = list(numbers)

    # This method defines the behavior of the object.
    def process_numbers(self):
        # Create a new list to store squared odd numbers.
        result = []

        # Iterate through the numbers stored in the object.
        for number in self.numbers:

            # Exclude even numbers using a conditional statement.
            if number % 2 != 0:

                # Square each odd number and add it to the result.
                result.append(number ** 2)

        return result


# Create an object (instance) of the OddNumberProcessor class.
processor = OddNumberProcessor(numbers)

# Call the object's method to process the list.
print("Object-Oriented Result:", processor.process_numbers())

# --------------------------------------------------
# 3. Functional Programming Approach
# --------------------------------------------------

def functional_approach(numbers):
    # Use filter() to select only odd numbers.
    # A lambda function determines whether each number is odd.
    odd_numbers = filter(lambda number: number % 2 != 0, numbers)

    # Use map() to square each remaining odd number.
    # This transforms the data without modifying the original list.
    squared_numbers = map(lambda number: number ** 2, odd_numbers)

    # Convert the mapped values into a new list.
    return list(squared_numbers)


# Test the functional approach using the original list.
print("Functional Result:", functional_approach(numbers))
