"""Input validators"""


def validate_input(input_data, algorithm_type):
    """
    Validate input based on algorithm type
    
    Args:
        input_data: Input to validate
        algorithm_type: Type of algorithm
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if algorithm_type in ['sorting', 'searching', 'subset']:
        if not isinstance(input_data, (list, tuple)):
            return False, "Input must be a list"
        if len(input_data) == 0:
            return False, "Input cannot be empty"
        if len(input_data) > 1000:
            return False, "Input too large (max 1000 elements)"
        return True, ""
    
    elif algorithm_type == 'string_matching':
        if not isinstance(input_data, str):
            return False, "Input must be a string"
        if len(input_data) == 0:
            return False, "Input cannot be empty"
        if len(input_data) > 10000:
            return False, "Input too long (max 10000 characters)"
        return True, ""
    
    elif algorithm_type in ['shortest_path', 'mst', 'graph']:
        if not isinstance(input_data, (dict, list)):
            return False, "Input must be a graph (dict or list)"
        return True, ""
    
    elif algorithm_type == 'knapsack':
        if not isinstance(input_data, tuple) or len(input_data) != 3:
            return False, "Knapsack input must be (weights, values, capacity)"
        weights, values, capacity = input_data
        if len(weights) != len(values):
            return False, "Weights and values must have same length"
        if capacity < 0:
            return False, "Capacity must be non-negative"
        return True, ""
    
    return False, "Unknown algorithm type"
