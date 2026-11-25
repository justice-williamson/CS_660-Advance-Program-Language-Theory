
# CS-660 Module Three Activity
# Part One: Typing Behavior
# Demonstrating Python's dynamic typing

def demonstrate_dynamic_typing():
    value = 100
    print(f"Original value: {value}")
    print(f"Original type: {type(value).__name__}")

    # Reassign the same variable to a string.
    value = "One hundred"
    print(f"Updated value: {value}")
    print(f"Updated type: {type(value).__name__}")

def demonstrate_type_mismatch():
    number = 100
    text = "50"

    # This operation causes a TypeError because an integer
    # cannot be added directly to a string.
    try:
        result = number + text
        print(f"Result: {result}")
    except TypeError as error:
        print(f"Type mismatch detected: {error}")

def demonstrate_type_correction():
    number = 100
    text = "50"

    # Convert the string to an integer before adding.
    converted_number = int(text)
    result = number + converted_number

    print(f"Corrected result: {result}")
    print(f"Result type: {type(result).__name__}")

def demonstrate_type_annotations():
    # The annotation suggests that age should be an integer.
    age: int = 25
    print(f"Original age: {age}")
    print(f"Original type: {type(age).__name__}")

    # Python permits this reassignment at runtime,
    # even though it conflicts with the annotation.
    age = "twenty-five"
    print(f"Updated age: {age}")
    print(f"Updated type: {type(age).__name__}")

def demonstrate_type_safe_code() -> None:
    # Use separate variables for different data types.
    number: int = 100
    text: str = "One hundred"

    print(f"Integer value: {number}")
    print(f"String value: {text}")

    # Convert the numeric string before performing addition.
    additional_amount: str = "50"
    total: int = number + int(additional_amount)

    print(f"Type-safe total: {total}")

    # Keep the annotated variable consistent with its type.
    age: int = 25
    age = 26

    print(f"Updated age: {age}")

if __name__ == "__main__":
    print("Part One: Dynamic Typing")
    demonstrate_dynamic_typing()

    print("\nPart One: Type Mismatch")
    demonstrate_type_mismatch()

    print("\nPart One: Type Correction")
    demonstrate_type_correction()

    print("\nPart One: Type Annotations")
    demonstrate_type_annotations()

    print("\nPart One: Type-Safe Code")
    demonstrate_type_safe_code()
