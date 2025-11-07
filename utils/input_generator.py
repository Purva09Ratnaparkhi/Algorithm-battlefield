"""Input generation and validation utilities"""

import random
import string


def generate_random_input(algorithm_type, size=50):
    """
    Generate random input based on algorithm type
    
    Args:
        algorithm_type: Type of algorithm
        size: Size of input data
    
    Returns:
        Generated input suitable for the algorithm
    """
    if algorithm_type == 'sorting':
        return [random.randint(1, 1000) for _ in range(size)]
    
    elif algorithm_type == 'searching':
        arr = [random.randint(1, 1000) for _ in range(size)]
        # Generate a completely random search key (may or may not exist in array)
        target = random.randint(1, 1000)
        return (arr, target)
    
    elif algorithm_type == 'string_matching':
        # Generate only random text; pattern will be added manually by user later
        text = ''.join(random.choices(string.ascii_lowercase, k=size))
        return text
    
    elif algorithm_type == 'shortest_path':
        # Return tuple: (nodes, edges, start_node)
        nodes = min(size, 10)  # Limit nodes for performance
        edges = []
        for i in range(nodes):
            for j in range(i + 1, nodes):
                if random.random() < 0.4:
                    weight = random.randint(1, 100)
                    edges.append((i, j, weight))
        start_node = random.randint(0, nodes - 1)
        return (nodes, edges, start_node)
    
    elif algorithm_type == 'mst':
        # Return tuple: (nodes, edges)
        nodes = min(size, 10)
        edges = []
        for i in range(nodes):
            for j in range(i + 1, nodes):
                if random.random() < 0.4:
                    weight = random.randint(1, 100)
                    edges.append((i, j, weight))
        return (nodes, edges)
    
    elif algorithm_type == 'graph':
        # Return tuple: (nodes, edges, start_node)
        nodes = min(size, 10)
        edges = []
        for i in range(nodes):
            for j in range(nodes):
                if i != j and random.random() < 0.2:
                    edges.append((i, j))
        start_node = random.randint(0, nodes - 1)
        return (nodes, edges, start_node)
    
    elif algorithm_type == 'subset generation':
        # Generate random numbers for subset generation
        # IMPORTANT: Keep size small! 2^n grows exponentially
        # 15 elements = 32,768 subsets (manageable)
        # 16 elements = 65,536 subsets (large)
        # 17+ elements = too many subsets
        num_elements = min(size, 15)  # Cap at 15 to avoid 2^n explosion
        arr = [random.randint(1, 100) for _ in range(num_elements)]
        return arr
    
    elif algorithm_type == '0/1 knapsack':
        # Return tuple: (items, weights, values, capacity)
        n = min(size, 10)
        weights = [random.randint(1, 50) for _ in range(n)]
        values = [random.randint(1, 100) for _ in range(n)]
        capacity = sum(weights) // 2
        return (n, weights, values, capacity)
    
    else:
        return [random.randint(1, 1000) for _ in range(size)]


def validate_array_input(input_str):
    """Validate and parse array input from user"""
    try:
        input_str = input_str.strip()
        
        # Try to parse as JSON array
        if input_str.startswith('[') and input_str.endswith(']'):
            import json
            arr = json.loads(input_str)
        else:
            # Try parsing as comma-separated values
            arr = [int(x.strip()) for x in input_str.split(',')]
        
        if not arr or len(arr) > 1000:
            raise ValueError("Array must have between 1 and 1000 elements")
        
        return arr
    
    except Exception as e:
        raise ValueError(f"Invalid array input: {str(e)}")


def validate_text_input(input_str, max_length=10000):
    """Validate text input for string matching algorithms"""
    input_str = input_str.strip()
    
    if not input_str:
        raise ValueError("Input cannot be empty")
    
    if len(input_str) > max_length:
        raise ValueError(f"Input too long (max {max_length} characters)")
    
    return input_str


def validate_graph_input(input_str):
    """Validate graph input"""
    try:
        import json
        graph = json.loads(input_str)
        
        if not isinstance(graph, dict):
            raise ValueError("Graph must be a dictionary")
        
        return graph
    
    except Exception as e:
        raise ValueError(f"Invalid graph input: {str(e)}")
