"""Algorithm Battlefield Arena - Main Flask Application"""

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import threading
import json
import os
from datetime import datetime

# Import algorithms
from algorithms.sorting import bubble_sort, insertion_sort, merge_sort, quick_sort, selection_sort, heap_sort
from algorithms.searching import linear_search, binary_search, fibonacci_search
from algorithms.shortest_path import dijkstra, bellman_ford, floyd_warshall
from algorithms.mcst import prim, kruskal
from algorithms.graph import bfs, dfs
from algorithms.string_matching import naive_search, kmp_search, rabin_karp, boyer_moore
from algorithms.subset import subset_bitmasking, subset_backtracking, subset_recursive, subset_iterative, subset_builtin
from algorithms.knapsack import knapsack_dp, knapsack_backtracking, knapsack_branch_bound

# Import utilities
from utils.performance import run_algorithm, compare_results, calculate_score
from utils.input_generator import generate_random_input, validate_array_input, validate_text_input
from utils.validators import validate_input

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'algorithm-battlefield-arena-secret-key-2024'

# Add cache-busting headers to prevent browser caching issues
@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Algorithm registry
algorithms = {
    "string matching": [
        {"key": "naive_search", "name": "Naive Search", "func": naive_search},
        {"key": "kmp_search", "name": "KMP Search", "func": kmp_search},
        {"key": "rabin_karp", "name": "Rabin-Karp", "func": rabin_karp},
        {"key": "boyer_moore", "name": "Boyer-Moore", "func": boyer_moore},
    ],
    "sorting": [
        {"key": "bubble_sort", "name": "Bubble Sort", "func": bubble_sort},
        {"key": "insertion_sort", "name": "Insertion Sort", "func": insertion_sort},
        {"key": "merge_sort", "name": "Merge Sort", "func": merge_sort},
        {"key": "quick_sort", "name": "Quick Sort", "func": quick_sort},
        {"key": "selection_sort", "name": "Selection Sort", "func": selection_sort},
        {"key": "heap_sort", "name": "Heap Sort", "func": heap_sort},
    ],
    "searching": [
        {"key": "linear_search", "name": "Linear Search", "func": linear_search},
        {"key": "binary_search", "name": "Binary Search", "func": binary_search},
        {"key": "fibonacci_search", "name": "Fibonacci Search", "func": fibonacci_search},
    ],
    "shortest path": [
        {"key": "dijkstra", "name": "Dijkstra's Algorithm", "func": dijkstra},
        {"key": "bellman_ford", "name": "Bellman-Ford Algorithm", "func": bellman_ford},
        {"key": "floyd_warshall", "name": "Floyd-Warshall Algorithm", "func": floyd_warshall},
    ],
    "mst": [
        {"key": "prim", "name": "Prim's Algorithm", "func": prim},
        {"key": "kruskal", "name": "Kruskal's Algorithm", "func": kruskal},
    ],
    "graph": [
        {"key": "bfs", "name": "Breadth-First Search (BFS)", "func": bfs},
        {"key": "dfs", "name": "Depth-First Search (DFS)", "func": dfs},
    ],
    "subset generation": [
        {"key": "subset_bitmasking", "name": "Bitmasking", "func": subset_bitmasking},
        {"key": "subset_backtracking", "name": "Backtracking", "func": subset_backtracking},
        {"key": "subset_recursive", "name": "Recursive", "func": subset_recursive},
        {"key": "subset_iterative", "name": "Iterative", "func": subset_iterative},
        {"key": "subset_builtin", "name": "Python Built-in", "func": subset_builtin},
    ],
    "0/1 knapsack": [
        {"key": "knapsack_dp", "name": "Dynamic Programming", "func": knapsack_dp},
        {"key": "knapsack_backtracking", "name": "Backtracking", "func": knapsack_backtracking},
        {"key": "knapsack_branch_bound", "name": "Branch & Bound", "func": knapsack_branch_bound},
    ],
}

# Store results temporarily
battle_results = {}


# ==================== Routes ====================

@app.route('/')
def index():
    """Home Page"""
    session.clear()
    return render_template('index.html')


@app.route('/select_category', methods=['GET', 'POST'])
def select_category():
    """Category Selection - Player 1 chooses, Player 2 must use same category"""
    if request.method == 'POST':
        data = request.get_json()
        player = data.get('player')
        category = data.get('category')
        
        if player == 1:
            # Player 1 can select any category
            session['category_p1'] = category
            session.modified = True
            return jsonify({'success': True, 'message': 'Category selected for Player 1'})
        
        elif player == 2:
            # Player 2 can ONLY select Player 1's category
            p1_category = session.get('category_p1')
            
            if not p1_category:
                return jsonify({'success': False, 'message': 'Player 1 must select a category first'})
            
            if category != p1_category:
                return jsonify({'success': False, 'message': f'Player 2 must use Player 1\'s category: {p1_category}'})
            
            session['category_p2'] = category
            session.modified = True
            return jsonify({'success': True, 'message': 'Category confirmed for Player 2'})
        
        return jsonify({'success': False, 'message': 'Invalid player'})
    
    categories = list(algorithms.keys())
    p1_category = session.get('category_p1')
    p2_category = session.get('category_p2')
    
    return render_template('select_category.html', 
                          categories=categories,
                          p1_category=p1_category,
                          p2_category=p2_category)


@app.route('/select_algorithm', methods=['GET', 'POST'])
def select_algorithm():
    """Algorithm Selection"""
    if request.method == 'POST':
        data = request.get_json()
        player = data.get('player')
        algorithm = data.get('algorithm')
        
        if player == 1:
            session['algorithm_p1'] = algorithm
            session.modified = True
        elif player == 2:
            session['algorithm_p2'] = algorithm
            session.modified = True
        
        return jsonify({'success': True})
    
    p1_category = session.get('category_p1')
    p2_category = session.get('category_p2')
    
    p1_algorithms = algorithms.get(p1_category, []) if p1_category else []
    p2_algorithms = algorithms.get(p2_category, []) if p2_category else []
    
    p1_selected = session.get('algorithm_p1')
    p2_selected = session.get('algorithm_p2')
    
    return render_template('select_algorithm.html',
                          p1_algorithms=p1_algorithms,
                          p2_algorithms=p2_algorithms,
                          p1_selected=p1_selected,
                          p2_selected=p2_selected)


@app.route('/input', methods=['GET', 'POST'])
def input_page():
    """Input Entry Page - Each player provides their own input"""
    
    def parse_edges(edge_string):
        """Parse edge string format: (A,B,4);(B,C,2) or (A,B);(B,C)"""
        edges = []
        try:
            # Split by semicolon
            edge_items = [e.strip() for e in edge_string.split(';')]
            for item in edge_items:
                if item:
                    # Remove parentheses
                    item = item.strip('()')
                    parts = [p.strip() for p in item.split(',')]
                    if len(parts) == 2:
                        # Unweighted edge (A,B)
                        edges.append((parts[0], parts[1]))
                    elif len(parts) == 3:
                        # Weighted edge (A,B,4)
                        edges.append((parts[0], parts[1], int(parts[2])))
            return edges
        except Exception as e:
            raise ValueError(f"Invalid edge format: {e}")
    
    def parse_manual_input(input_text, category, pattern=None):
        """Parse manual input based on category format"""
        input_text = input_text.strip()
        
        if category == 'sorting' or category == 'subset generation':
            # Format: 5, 3, 8, 1, 9
            return [int(x.strip()) for x in input_text.split(',')]
        
        elif category == 'searching':
            # Format: 5, 3, 8, 1, 9 (will get target from searching)
            return [int(x.strip()) for x in input_text.split(',')]
        
        elif category == 'string matching':
            if action == 'generate':
                # Generate only the random text
                text = generate_random_input('string_matching', size)
                session[f'p{player}_input'] = text  # temporarily store text only
                return jsonify(success=True, input=text, preview=text)
            
            elif action == 'submit_pattern':
                # Accept pattern from frontend and combine it with text
                pattern = data.get('pattern')
                text = session.get(f'p{player}_input')
                if not text or not pattern:
                    return jsonify(success=False, error="Missing text or pattern")
                
                session[f'p{player}_input'] = [text, pattern]
                return jsonify(success=True, input=[text, pattern])
        
        elif category in ['shortest_path', 'graph']:
            # Format: nodes\nedges\nstart_node
            lines = [line.strip() for line in input_text.split('\n') if line.strip()]
            if len(lines) < 3:
                raise ValueError("Format should be: nodes\\nedges\\nstart_node (each on new line)")
            
            num_nodes = int(lines[0])
            edges = parse_edges(lines[1])
            start_node = int(lines[2])
            
            return (num_nodes, edges, start_node)
        
        elif category == 'mst':
            # Format: nodes\nedges
            lines = [line.strip() for line in input_text.split('\n') if line.strip()]
            if len(lines) < 2:
                raise ValueError("Format should be: nodes\\nedges (each on new line)")
            
            num_nodes = int(lines[0])
            edges = parse_edges(lines[1])
            
            return (num_nodes, edges)
        
        elif category == '0/1 knapsack':
            # Format: n\nweights\nvalues\ncapacity
            lines = [line.strip() for line in input_text.split('\n') if line.strip()]
            if len(lines) < 4:
                raise ValueError("Format should be: n\\nweights\\nvalues\\ncapacity")
            
            n = int(lines[0])
            weights = [int(x.strip()) for x in lines[1].split(',')]
            values = [int(x.strip()) for x in lines[2].split(',')]
            capacity = int(lines[3])
            
            return (n, weights, values, capacity)
        
        else:
            raise ValueError(f"Unknown category: {category}")
    
    if request.method == 'POST':
        data = request.get_json()
        player = data.get('player')
        action = data.get('action')
        category = data.get('category')
        # Normalize category name (handle both 'string matching' and 'string_matching')
        category_normalized = category.replace(' ', '_').lower() if category else ''
        
        if action == 'generate':
            size = int(data.get('size', 5))
            pattern = data.get('pattern')  # For string matching, user-provided pattern
            
            try:
                input_data = generate_random_input(category_normalized, size)
                
                # For string matching, if user provided a pattern, override the generated one
                if category_normalized == 'string_matching' and pattern and isinstance(input_data, tuple) and len(input_data) == 2:
                    text, _ = input_data
                    input_data = (text, pattern)
                
                if player == 1:
                    session['input_p1'] = input_data
                else:
                    session['input_p2'] = input_data
                
                session.modified = True
                
                # For searching, extract and display the target
                response_data = {
                    'success': True,
                    'input': str(input_data),
                    'input_complete': False,  # Flag to indicate if input is ready for battle
                }
                
                if category_normalized == 'searching' and isinstance(input_data, tuple) and len(input_data) == 2:
                    arr, target = input_data
                    response_data['preview'] = f"Array: {str(arr)[:100]}... Target: {target}"
                    response_data['search_key'] = target  # Return the auto-generated search key
                    response_data['input_complete'] = True  # Searching input is complete
                elif category_normalized == 'string_matching' and isinstance(input_data, tuple) and len(input_data) == 2:
                    text, pat = input_data
                    preview_text = text[:50] if len(text) > 50 else text
                    response_data['preview'] = f"Text: {preview_text}... Pattern: {pat}"
                    response_data['pattern'] = pat  # Send the generated/provided pattern to frontend
                    response_data['input_complete'] = True  # String matching now has both text and pattern
                else:
                    preview_str = str(input_data)[:150]
                    if len(str(input_data)) > 150:
                        preview_str += '...'
                    response_data['preview'] = preview_str
                    response_data['input_complete'] = True  # Other categories are complete
                
                return jsonify(response_data)
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        elif action == 'manual':
            input_text = data.get('input_text')
            search_key = data.get('search_key')
            pattern = data.get('pattern')  # For string matching with separate pattern field
            
            try:
                # For string matching with separate pattern field, pass pattern to parser
                if category_normalized == 'string_matching' and '\n' in input_text:
                    # Pattern was passed as separate field in format "text\npattern"
                    lines = input_text.split('\n', 1)
                    text = lines[0].strip()
                    pattern_from_input = lines[1].strip() if len(lines) > 1 else ''
                    parsed_input = parse_manual_input(text, category_normalized, pattern_from_input)
                else:
                    parsed_input = parse_manual_input(input_text, category_normalized, pattern)
                
                # For searching, create tuple with search key
                if category_normalized == 'searching' and search_key is not None:
                    parsed_input = (parsed_input, int(search_key))
                
                if player == 1:
                    session['input_p1'] = parsed_input
                else:
                    session['input_p2'] = parsed_input
                
                session.modified = True
                return jsonify({'success': True, 'input': str(parsed_input)})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
    
    p1_category = session.get('category_p1', 'sorting')
    p2_category = session.get('category_p2', 'sorting')
    
    return render_template('input.html', 
                          p1_category=p1_category,
                          p2_category=p2_category)


@app.route('/battle', methods=['GET', 'POST'])
def battle():
    """Battle Execution Page - Each player uses their own input"""
    if request.method == 'POST':
        # Execute algorithms
        p1_category = session.get('category_p1')
        p2_category = session.get('category_p2')
        p1_algo_key = session.get('algorithm_p1')
        p2_algo_key = session.get('algorithm_p2')
        input_p1 = session.get('input_p1')
        input_p2 = session.get('input_p2')
        
        # Get algorithm functions
        p1_algo = next((a['func'] for a in algorithms.get(p1_category, []) 
                       if a['key'] == p1_algo_key), None)
        p2_algo = next((a['func'] for a in algorithms.get(p2_category, []) 
                       if a['key'] == p2_algo_key), None)
        
        if not p1_algo or not p2_algo or input_p1 is None or input_p2 is None:
            return jsonify({'success': False, 'error': 'Missing algorithm or input data'})
        
        def run_algo_with_input(algo, category, input_data):
            """Run algorithm with proper input format unpacking"""
            try:
                # Normalize category name
                category_norm = category.replace(' ', '_').lower()
                
                if category_norm == 'searching' and (isinstance(input_data, tuple) or isinstance(input_data, list)):
                    # searching: (array, target)
                    return run_algorithm(algo, input_data[0], input_data[1])
                
                elif category_norm == 'string_matching' and (isinstance(input_data, tuple) or isinstance(input_data, list)):
                    # Combine text and pattern, then handle inside run_algorithm()
                    return run_algorithm(algo, (input_data[0], input_data[1]))
                
                elif category_norm in ['shortest_path', 'graph'] and (isinstance(input_data, tuple) or isinstance(input_data, list)):
                    # shortest_path/graph: (num_nodes, edges, start_node)
                    return run_algorithm(algo, input_data[0], input_data[1], input_data[2])
                
                elif category_norm == 'mst' and (isinstance(input_data, tuple) or isinstance(input_data, list)):
                    # mst: (num_nodes, edges)
                    return run_algorithm(algo, input_data[0], input_data[1])
                
                elif category_norm == '0/1 knapsack' and (isinstance(input_data, tuple) or isinstance(input_data, list)):
                    # knapsack: (n, weights, values, capacity)
                    return run_algorithm(algo, input_data[0], input_data[1], input_data[2], input_data[3])
                
                else:
                    # sorting, subset generation: just array/list
                    return run_algorithm(algo, input_data)
            except Exception as e:
                raise Exception(f"Error running {category} algorithm: {str(e)}")
        
        try:
            result1 = run_algo_with_input(p1_algo, p1_category, input_p1)
            result2 = run_algo_with_input(p2_algo, p2_category, input_p2)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
        
        # Compare results (include categories and original inputs so we can validate correctness)
        comparison = compare_results(result1, result2, p1_category, input_p1, p2_category, input_p2)

        # Helper function to truncate large results for JSON serialization
        def truncate_result(result, category, max_items=500):
            """Truncate large results to avoid response header size issues"""
            if isinstance(result, list):
                if len(result) > max_items:
                    # For subset generation, show summary instead of full list
                    if category == 'subset generation':
                        return {
                            'type': 'truncated_subset',
                            'total_subsets': len(result),
                            'message': f'Generated {len(result)} subsets',
                            'sample': result[:10]  # Show first 10 subsets
                        }
                    else:
                        return {
                            'type': 'truncated',
                            'total_items': len(result),
                            'preview': str(result[:50])[:500],  # Limit string length too
                            'message': f'Result contains {len(result)} items (showing first 50)'
                        }
            elif isinstance(result, dict):
                # Already a result dict, don't truncate
                return result
            return result

        # Truncate results if needed
        result1_display = truncate_result(result1, p1_category)
        result2_display = truncate_result(result2, p2_category)

        # Store original results in session (not truncated)
        session['result1'] = result1
        session['result2'] = result2
        session['comparison'] = comparison
        session.modified = True

        return jsonify({
            'success': True,
            'result1': result1_display,
            'result2': result2_display,
            'comparison': comparison
        })
    
    p1_algo_name = session.get('algorithm_p1', 'Algorithm 1')
    p2_algo_name = session.get('algorithm_p2', 'Algorithm 2')
    
    return render_template('battle.html',
                          p1_algo=p1_algo_name,
                          p2_algo=p2_algo_name)


@app.route('/result')
def result():
    """Result Page"""
    result1 = session.get('result1')
    result2 = session.get('result2')
    comparison = session.get('comparison')
    
    if not result1 or not result2 or not comparison:
        return redirect(url_for('select_category'))
    
    p1_algo_name = session.get('algorithm_p1', 'Algorithm 1')
    p2_algo_name = session.get('algorithm_p2', 'Algorithm 2')
    p1_category = session.get('category_p1', 'Unknown')
    p2_category = session.get('category_p2', 'Unknown')
    
    return render_template('result.html',
                          result1=result1,
                          result2=result2,
                          comparison=comparison,
                          p1_algo_name=p1_algo_name,
                          p2_algo_name=p2_algo_name,
                          p1_category=p1_category,
                          p2_category=p2_category)


@app.route('/play_again')
def play_again():
    """Reset and go to category selection"""
    session.clear()
    return redirect(url_for('select_category'))


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """404 Error Handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """500 Error Handler"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
