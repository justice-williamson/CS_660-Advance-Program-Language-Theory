
def example_1():
    x = "outer"  # Local variable belonging to example_1()

    def inner():
        # Python finds x in the enclosing example_1() scope.
        print(f"Inner sees: {x}")

    inner()
    # This accesses x directly in example_1()'s local scope.
    print(f"Outer has: {x}")


def example_2():
    x = 10  # Local variable in example_2()

    def middle():
        x = 20  # Shadows the x = 10 variable in the outer function

        def inner():
            # Python finds x = 20 in the enclosing middle() function.
            print(f"Inner sees: {x}")

        inner()
        # This uses middle()'s local x, which is 20.
        print(f"Middle has: {x}")

    middle()
    # This uses example_2()'s original x, which remains 10.
    print(f"Outer has: {x}")

def example_3():
    count = 0  # Local variable belonging to example_3()

    def increment():
        nonlocal count  # Refers to count in the enclosing example_3() scope
        count += 1  # Updates the enclosing variable instead of creating a new one
        return count

    def get_counter():
        def counter():
            # Calls increment(), which updates the shared count variable
            return increment()
        return counter

    my_counter = get_counter()
    print(my_counter())  # First call: count becomes 1
    print(my_counter())  # Second call: count becomes 2
    print(count)  # The enclosing variable now holds 2


def example_4():
    name = "global"  # Local variable in example_4(), not a true global variable

    def outer():
        name = "outer"  # Shadows the name defined in example_4()

        def inner():
            name = "inner"  # Creates a separate local variable
            print(f"Inner: {name}")  # Uses inner()'s local name

        inner()
        print(f"Outer: {name}")  # Uses outer()'s local name

    outer()
    print(f"Global: {name}")  # Uses example_4()'s local name


# Simulated dynamic scoping example
def dynamic_scope_example():
    # Simulates the variable environment of the calling function.
    def inner(caller_scope):
        # Under simulated dynamic scoping, x comes from the caller.
        print(f"Dynamic inner sees: {caller_scope['x']}")

    def outer():
        x = 10  # Variable belonging to outer()

        def middle():
            x = 20  # Variable in the active calling function

            # Pass the active caller's variable to simulate dynamic lookup.
            inner({"x": x})

        middle()
        print(f"Dynamic outer has: {x}")

    outer()
    
def compare_scoping():
    x = "lexical environment"

    def inner(caller_scope=None):
        # Lexical lookup uses the scope where inner() was defined.
        print(f"Lexical lookup: {x}")

        # Simulated dynamic lookup uses the active caller's environment.
        if caller_scope is not None:
            print(f"Simulated dynamic lookup: {caller_scope['x']}")

    def caller():
        x = "calling environment"
        inner({"x": x})

    caller()

if __name__ == "__main__":
    print("Example 1:")
    example_1()
    
    print("\nExample 2:")
    example_2()
    
    print("\nExample 3:")
    example_3()
    
    print("\nExample 4:")
    example_4()

    
    print("\nExample 5: Simulated Dynamic Scoping")
    dynamic_scope_example()

    print("\nExample 6: Lexical vs. Dynamic Scoping")
    compare_scoping()
