"""Input generation and validation utilities"""

import random
import string


def generate_random_input(algorithm_type, size=5):
    """
    Generate random input based on algorithm type in human-readable format
    """
    import random
    import string

    if algorithm_type == 'sorting':
        return [random.randint(1, 1000) for _ in range(size)]

    elif algorithm_type == 'searching':
        arr = [random.randint(1, 1000) for _ in range(size)]
        return arr

    elif algorithm_type == 'string matching':
        # Generate text exactly based on user-provided size
        text = ''.join(random.choices(string.ascii_lowercase, k=size))
        formatted = f"Generated Text ({size} chars): {text}"
        return text, formatted


    elif algorithm_type in ['graph', 'shortest path']:
        # Generate nodes as letters A, B, C, ...
        nodes = [chr(65 + i) for i in range(min(size, 10))]
        edges = []

        # Generate random weighted edges (40% probability)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if random.random() < 0.4:  # ~40% chance of edge
                    weight = random.randint(1, 20)
                    edges.append((nodes[i], nodes[j], weight))

        # Ensure every node appears in at least one edge
        connected = set([n for edge in edges for n in edge[:2]])
        missing = [n for n in nodes if n not in connected]
        for m in missing:
            other = random.choice([n for n in nodes if n != m])
            weight = random.randint(1, 20)
            edges.append((m, other, weight))

        # Choose a random start node for shortest path
        start_node = random.choice(nodes)

        # Format edges as strings (A,B,10);(B,C,5)
        edges_str = '; '.join([f"({u},{v},{w})" for u, v, w in edges])

        # ✅ Include full node list at the top
        formatted = f"{','.join(nodes)}\n{edges_str}\n{start_node}"
        return (len(nodes), edges, start_node), formatted


    elif algorithm_type == 'mst':
        # Generate nodes as letters A, B, C, ...
        nodes = [chr(65 + i) for i in range(min(size, 10))]
        edges = []

        # Generate random weighted edges (40% probability)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if random.random() < 0.4:
                    weight = random.randint(1, 20)
                    edges.append((nodes[i], nodes[j], weight))

        # Ensure all nodes appear in at least one edge
        connected = set([n for edge in edges for n in edge[:2]])
        missing = [n for n in nodes if n not in connected]
        for m in missing:
            other = random.choice([n for n in nodes if n != m])
            weight = random.randint(1, 20)
            edges.append((m, other, weight))

        # Format output
        edges_str = '; '.join([f"({u},{v},{w})" for u, v, w in edges])
        formatted = f"{','.join(nodes)}\n{edges_str}"

        return (len(nodes), edges), formatted


    elif algorithm_type in ['0/1 knapsack', '0/1_knapsack']:

        n = min(size, 10)
        values = [random.randint(10, 100) for _ in range(n)]
        weights = [random.randint(5, 50) for _ in range(n)]
        capacity = random.randint(sum(weights)//3, sum(weights)//2)
        formatted = (
            f"{n}\n"
            f"Values: {', '.join(map(str, values))}\n"
            f"Weights: {', '.join(map(str, weights))}\n"
            f"Capacity: {capacity}"
        )
        return (n, weights, values, capacity), formatted

    elif algorithm_type == 'subset generation':
        num_elements = min(size, 15)
        arr = [random.randint(1, 100) for _ in range(num_elements)]
        return arr

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
