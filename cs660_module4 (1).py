# 4-2 Activity: Recursive and Functional Problem Solving with Exception Handling
# Justice Williamson
# CS-660: Advance Program Language Theory
# Southern New Hampshire University
# October 18, 2026

"""CS 660 Module Four: recursion, exception handling, and functional tools."""
import json
from pathlib import Path


def load_catalog(filename):
    """Load the astronomical catalog with clear file and JSON errors."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if not isinstance(data, dict) or not isinstance(data.get('astronomical_catalog'), dict):
            raise ValueError('Expected an astronomical_catalog object.')
        return data['astronomical_catalog']
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(f'Unable to load catalog: {error}') from error


def find_leaves(node, path='root'):
    """Recursively yield (path, value) for every innermost value."""
    try:
        if isinstance(node, dict):
            for key, value in node.items():
                yield from find_leaves(value, f'{path}.{key}')
        elif isinstance(node, list):
            for index, value in enumerate(node):
                yield from find_leaves(value, f'{path}[{index}]')
        elif node is None or isinstance(node, (str, int, float, bool)):
            yield path, node
        else:
            raise TypeError(f'Unsupported data type at {path}: {type(node).__name__}')
    except (TypeError, RecursionError) as error:
        raise ValueError(f'Cannot traverse {path}: {error}') from error


def count_leaves(node):
    """Recursively count leaf values; reject invalid input types."""
    try:
        if isinstance(node, dict):
            return sum(count_leaves(value) for value in node.values())
        if isinstance(node, list):
            return sum(count_leaves(value) for value in node)
        if node is None or isinstance(node, (str, int, float, bool)):
            return 1
        raise TypeError(f'Unsupported input: {type(node).__name__}')
    except (TypeError, RecursionError) as error:
        raise ValueError(f'Invalid recursive input: {error}') from error


def apply_operation(items, operation):
    """Accept a function as an argument and apply it to each item."""
    if not callable(operation):
        raise TypeError('operation must be a function')
    return list(map(operation, items))


def main():
    try:
        catalog = load_catalog(Path(__file__).with_name('catalog.json'))
        print('Catalog:', catalog['catalog_name'])
        print('\nPART ONE: RECURSION AND EXCEPTION HANDLING')
        leaves = list(find_leaves(catalog))
        print('Total leaf values:', count_leaves(catalog))
        print('Leaf values found:', len(leaves))
        print('\nInnermost leaf data (path = value):')
        for path, value in leaves:
            print(f'{path} = {value!r}')

        print('\nException-handling demonstration:')
        for invalid in ({'bad': {1, 2}}, object()):
            try:
                count_leaves(invalid)
            except ValueError as error:
                print('Handled invalid input:', error)
        try:
            list(find_leaves({'invalid_nested_data': {1, 2}}))
        except ValueError as error:
            print('Handled nested-data error:', error)

        print('\nPART TWO: FUNCTIONAL CONSTRUCTS')
        galaxies = catalog['galaxies']
        # Anonymous function: transform galaxy distances into millions of light-years.
        distances = list(map(lambda galaxy: (galaxy['name'], round(galaxy['distance_ly'] / 1_000_000, 2)), galaxies))
        print('Galaxy distances (millions of light-years):', distances)
        # Higher-order filter(): retain spiral galaxies.
        spiral_galaxies = list(filter(lambda galaxy: galaxy['type'] == 'spiral', galaxies))
        print('Spiral galaxies:', [galaxy['name'] for galaxy in spiral_galaxies])
        # User-defined higher-order function accepts another function.
        labels = apply_operation(catalog['nebulae'], lambda nebula: f"{nebula['name']} ({nebula['type']})")
        print('Nebula labels:', labels)
    except (ValueError, KeyError, TypeError) as error:
        print('Program error:', error)


if __name__ == '__main__':
    main()
