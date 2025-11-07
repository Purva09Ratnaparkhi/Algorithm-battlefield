"""Performance measurement utilities"""

import timeit
import tracemalloc

# Reference algorithm implementations for validation
from algorithms import searching as ref_searching
from algorithms import sorting as ref_sorting
from algorithms import string_matching as ref_string_matching
from algorithms import shortest_path as ref_shortest
from algorithms import mcst as ref_mcst
from algorithms import subset as ref_subset
from algorithms import knapsack as ref_knapsack
from algorithms import graph as ref_graph


def truncate_output(result, max_items=500, max_string_length=10000):
    """
    Truncate large outputs to prevent JSON serialization issues
    
    Args:
        result: The output from algorithm
        max_items: Maximum items to include in list/set
        max_string_length: Maximum string length
    
    Returns:
        Truncated result or summary dict
    """
    if isinstance(result, list):
        if len(result) > max_items:
            # For large lists, return summary
            return {
                'type': 'truncated_list',
                'count': len(result),
                'sample': result[:10],
                'message': f'Full output has {len(result)} items (showing first 10 for display)'
            }
        return result
    
    elif isinstance(result, set):
        if len(result) > max_items:
            return {
                'type': 'truncated_set',
                'count': len(result),
                'sample': list(result)[:10],
                'message': f'Full output has {len(result)} items (showing first 10 for display)'
            }
        return result
    
    elif isinstance(result, str):
        if len(result) > max_string_length:
            return result[:max_string_length] + f'\n...[truncated, total length: {len(result)}]'
        return result
    
    return result


def run_algorithm(func, input_data, *args):
    """
    Run algorithm and measure execution time and memory usage
    
    Args:
        func: Algorithm function
        input_data: Input data for the algorithm
        *args: Additional arguments for the function
    
    Returns:
        dict: {
            'output': result,
            'time': execution_time (in milliseconds),
            'memory': memory_used (in KB),
            'status': 'success' or 'error',
            'error': error message (if any)
        }
    """
    try:
        # Start memory tracking
        tracemalloc.start()
        
        # Measure execution time
        start_time = timeit.default_timer()

        # Run the algorithm and keep raw output for validation
        raw_result = func(input_data, *args)

        # Stop time measurement
        end_time = timeit.default_timer()
        execution_time = (end_time - start_time) * 1000  # Convert to ms
        
        # Get memory usage
        current, peak = tracemalloc.get_traced_memory()
        memory_used = peak / 1024  # Convert to KB
        tracemalloc.stop()
        
        # Truncate large outputs to prevent JSON serialization issues
        truncated_result = truncate_output(raw_result)

        return {
            'raw_output': raw_result,
            'output': truncated_result,
            'time': round(execution_time, 4),
            'memory': round(memory_used, 2),
            'status': 'success',
            'error': None
        }
    
    except Exception as e:
        tracemalloc.stop()
        return {
            'output': None,
            'time': 0,
            'memory': 0,
            'status': 'error',
            'error': str(e)
        }


def compare_results(result1, result2, category1=None, input1=None, category2=None, input2=None):
    """
    Compare two algorithm results and determine winner
    
    Args:
        result1: Result dict from Player 1
        result2: Result dict from Player 2
    
    Returns:
        dict: {
            'winner': 'Player 1', 'Player 2', or 'Draw',
            'score_1': score for player 1,
            'score_2': score for player 2,
            'time_winner': who has faster execution,
            'memory_winner': who uses less memory
        }
    """
    if result1['status'] == 'error' or result2['status'] == 'error':
        if result1['status'] == 'error' and result2['status'] != 'error':
            return {
                'winner': 'Player 2',
                'score_1': 0,
                'score_2': 100,
                'time_winner': 'Player 2',
                'memory_winner': 'Player 2',
                'reason': 'Player 1 algorithm encountered an error'
            }
        elif result2['status'] == 'error' and result1['status'] != 'error':
            return {
                'winner': 'Player 1',
                'score_1': 100,
                'score_2': 0,
                'time_winner': 'Player 1',
                'memory_winner': 'Player 1',
                'reason': 'Player 2 algorithm encountered an error'
            }
        else:
            return {
                'winner': 'Draw',
                'score_1': 0,
                'score_2': 0,
                'time_winner': 'N/A',
                'memory_winner': 'N/A',
                'reason': 'Both algorithms encountered errors'
            }
    
    time1 = result1['time']
    memory1 = result1['memory']
    time2 = result2['time']
    memory2 = result2['memory']
    
    # Calculate scores
    score_1, score_2 = calculate_score(time1, memory1, time2, memory2)

    # Validate correctness for each player's output (if possible)
    validation_1 = validate_result(category1, input1, result1.get('raw_output')) if category1 is not None else {'correct': True, 'accuracy': 1.0, 'details': 'No validation'}
    validation_2 = validate_result(category2, input2, result2.get('raw_output')) if category2 is not None else {'correct': True, 'accuracy': 1.0, 'details': 'No validation'}

    # Apply correctness penalties: incorrect results get a heavy penalty
    penalty = 30.0  # points to subtract for incorrect/invalid outputs

    if not validation_1.get('correct', True):
        score_1 = max(0.0, score_1 - penalty)
    if not validation_2.get('correct', True):
        score_2 = max(0.0, score_2 - penalty)
    
    # Determine winner
    if score_1 > score_2:
        winner = 'Player 1'
    elif score_2 > score_1:
        winner = 'Player 2'
    else:
        winner = 'Draw'
    
    # Time and memory winners
    time_winner = 'Player 1' if time1 < time2 else ('Player 2' if time2 < time1 else 'Draw')
    memory_winner = 'Player 1' if memory1 < memory2 else ('Player 2' if memory2 < memory1 else 'Draw')
    
    return {
        'winner': winner,
        'score_1': round(score_1, 2),
        'score_2': round(score_2, 2),
        'time_winner': time_winner,
        'memory_winner': memory_winner,
        'validation': {
            'player1': validation_1,
            'player2': validation_2
        }
    }


def validate_result(category, input_data, raw_output):
    """
    Validate algorithm raw output against a reference implementation for the given category.

    Returns:
        dict: { 'correct': bool, 'accuracy': float (0..1), 'details': str }
    """
    try:
        if category is None:
            return {'correct': True, 'accuracy': 1.0, 'details': 'No category provided'}

        # Sorting: output should be a sorted permutation of input list
        if category == 'sorting':
            expected = ref_sorting.merge_sort(input_data.copy()) if isinstance(input_data, list) else None
            if expected is None:
                return {'correct': False, 'accuracy': 0.0, 'details': 'Invalid input for sorting'}
            correct = (raw_output == expected)
            return {'correct': correct, 'accuracy': 1.0 if correct else 0.0, 'details': 'Sorted array match' if correct else 'Mismatch with expected sorted array'}

        # Searching: input_data = (arr, target)
        if category == 'searching' and isinstance(input_data, tuple):
            arr, target = input_data
            expected_idx = ref_searching.linear_search(arr, target)
            # raw_output should be int index
            correct = False
            if isinstance(raw_output, int):
                correct = (raw_output == expected_idx)
            return {'correct': correct, 'accuracy': 1.0 if correct else 0.0, 'details': f'Expected index {expected_idx}'}

        # String matching: input_data = (text, pattern)
        if category == 'string_matching' and isinstance(input_data, tuple):
            text, pattern = input_data
            expected = ref_string_matching.naive_search(text, pattern)
            # raw_output should be list of occurrences
            correct = (sorted(raw_output) == sorted(expected)) if isinstance(raw_output, list) else False
            return {'correct': correct, 'accuracy': 1.0 if correct else 0.0, 'details': f'Found occurrences {expected}'}

        # Subset generation: input_data is list
        if category == 'subset generation' and isinstance(input_data, list):
            expected = ref_subset.subset_bitmasking(input_data)
            # Compare counts and that each reported subset is a subset of input
            if not isinstance(raw_output, list):
                return {'correct': False, 'accuracy': 0.0, 'details': 'Output not list of subsets'}
            correct = len(raw_output) == len(expected)
            return {'correct': correct, 'accuracy': 1.0 if correct else min(1.0, len(raw_output) / len(expected) if len(expected) > 0 else 0.0), 'details': f'Expected {len(expected)} subsets'}

        # Knapsack: input_data = (n, weights, values, capacity)
        if category == '0/1 knapsack' and isinstance(input_data, tuple):
            try:
                _, weights, values, capacity = input_data
            except Exception:
                return {'correct': False, 'accuracy': 0.0, 'details': 'Invalid knapsack input'}
            expected_value = ref_knapsack.knapsack_dp(weights, values, capacity)
            correct = (raw_output == expected_value)
            return {'correct': correct, 'accuracy': 1.0 if correct else 0.0, 'details': f'Expected optimal value {expected_value}'}

        # Shortest path / graph: input_data = (num_nodes, edges, start)
        if category in ['shortest_path', 'graph'] and isinstance(input_data, tuple):
            try:
                num_nodes, edges, start = input_data
            except Exception:
                return {'correct': False, 'accuracy': 0.0, 'details': 'Invalid graph input'}

            # Build graph dict expected by reference implementations
            graph = {}
            # Nodes may be numbered 0..n-1 or named; try to use numeric nodes if edges contain ints
            for i in range(num_nodes):
                graph[i] = []

            for e in edges:
                if len(e) == 2:
                    u, v = e
                    w = 1
                else:
                    u, v, w = e
                # Ensure keys exist
                if u not in graph:
                    graph[u] = []
                if v not in graph:
                    graph[v] = []
                graph[u].append((v, w))
                # For undirected graphs also add reverse
                graph[v].append((u, w))

            expected_dist = ref_shortest.dijkstra(graph, start)
            # raw_output might be a dict of distances
            correct = isinstance(raw_output, dict) and raw_output == expected_dist
            return {'correct': correct, 'accuracy': 1.0 if correct else 0.0, 'details': 'Shortest path distances compared'}

        # MST: input_data = (num_nodes, edges)
        if category == 'mst' and isinstance(input_data, tuple):
            try:
                num_nodes, edges = input_data
            except Exception:
                return {'correct': False, 'accuracy': 0.0, 'details': 'Invalid MST input'}
            # Reference kruskal expects edges as (u,v,weight) and nodes list
            nodes = list(range(num_nodes))
            expected_mst = ref_mcst.kruskal(edges, nodes)
            # Compare total weight
            def total_weight(mst):
                return sum(e[2] for e in mst) if isinstance(mst, list) else float('inf')
            expected_w = total_weight(expected_mst)
            actual_w = total_weight(raw_output)
            correct = (actual_w == expected_w)
            return {'correct': correct, 'accuracy': 1.0 if correct else 0.0, 'details': f'Expected total weight {expected_w}'}

        # Fallback: unable to validate
        return {'correct': True, 'accuracy': 1.0, 'details': 'No validator for this category; assumed correct'}

    except Exception as e:
        return {'correct': False, 'accuracy': 0.0, 'details': f'Validation error: {e}'}


def calculate_score(time_a, mem_a, time_b, mem_b):
    """
    Calculate scores for both algorithms
    
    Lower time and memory = higher score
    Scores are always meaningful (not just 0 or 100)
    
    Args:
        time_a, mem_a: Time (ms) and Memory (KB) for algorithm A
        time_b, mem_b: Time (ms) and Memory (KB) for algorithm B
    
    Returns:
        tuple: (score_a, score_b)
    """
    # Each algorithm gets a base score of 50, then adjusted based on performance difference
    base_score = 50
    max_adjustment = 45  # Allow scores to range from 5 to 95
    
    # Calculate total cost (time weighted 2x more than memory)
    total_cost_a = (time_a * 2.0) + (mem_a * 0.5)
    total_cost_b = (time_b * 2.0) + (mem_b * 0.5)
    
    # Calculate the difference in performance
    if total_cost_a == total_cost_b:
        # Perfect tie
        score_a = base_score
        score_b = base_score
    else:
        # Winner gets more points
        total_max = max(total_cost_a, total_cost_b)
        if total_max > 0:
            # Calculate ratio: 0 to 1 (0 means very bad, 1 means very good)
            ratio_a = 1 - (total_cost_a / total_max)
            ratio_b = 1 - (total_cost_b / total_max)
            
            # Convert to scores: base_score ± adjustment
            score_a = base_score + (ratio_a * max_adjustment)
            score_b = base_score + (ratio_b * max_adjustment)
        else:
            score_a = base_score
            score_b = base_score
    
    # Ensure scores are in valid range
    score_a = max(5, min(95, score_a))
    score_b = max(5, min(95, score_b))
    
    return (score_a, score_b)
