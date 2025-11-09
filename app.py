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
            return jsonify({'success': True, 'message': 'Algorithm selected for Player 1'})

        elif player == 2:
            algo_p1 = session.get('algorithm_p1')
            if algorithm == algo_p1:
                return jsonify({
                    'success': False,
                    'message': f"Player 2 cannot select the same algorithm as Player 1 ({algo_p1}). Please choose a different one."
                })
            session['algorithm_p2'] = algorithm
            session.modified = True
            return jsonify({'success': True, 'message': 'Algorithm selected for Player 2'})

        
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
        """
        Parse edge string format: (A,B,4);(B,C,2) or (A,B);(B,C)
        Supports flexible spacing and meaningful error messages.
        """
        edges = []
        try:
            if not edge_string.strip():
                raise ValueError("Edge input cannot be empty.")
            
            # Split by semicolon (each represents an edge)
            edge_items = [e.strip() for e in edge_string.split(';') if e.strip()]
            
            for item in edge_items:
                # Must start and end with parentheses
                if not (item.startswith('(') and item.endswith(')')):
                    raise ValueError(f"Edge '{item}' must be enclosed in parentheses, e.g. (A,B,10)")
                
                # Clean and split
                item = item.strip('()')
                parts = [p.strip() for p in item.split(',') if p.strip()]
                
                # Handle 2 or 3 parts
                if len(parts) == 2:
                    # Unweighted edge
                    edges.append((parts[0], parts[1]))
                elif len(parts) == 3:
                    # Weighted edge
                    try:
                        weight = int(parts[2])
                    except ValueError:
                        raise ValueError(f"Invalid weight '{parts[2]}' in edge {item}. Must be an integer.")
                    edges.append((parts[0], parts[1], weight))
                else:
                    raise ValueError(f"Edge '{item}' must have 2 or 3 parts, e.g. (A,B) or (A,B,10).")
            
            if not edges:
                raise ValueError("No valid edges found. Please check your input format.")
            
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
            # Expect input in format: text\npattern
            lines = [line.strip() for line in input_text.split('\n') if line.strip()]
            if len(lines) < 2:
                raise ValueError("Please enter both text and pattern (each on new line).")
            text, pattern = lines[0], lines[1]
            return (text, pattern)

            
        elif action == 'submit_pattern':
                # Accept pattern from frontend and combine it with text
                pattern = data.get('pattern')
                text = session.get(f'p{player}_input')
                if not text or not pattern:
                    return jsonify(success=False, error="Missing text or pattern")
                
                session[f'p{player}_input'] = [text, pattern]
                return jsonify(success=True, input=[text, pattern])
        
        elif category in ['shortest_path', 'graph']:
            lines = [line.strip() for line in input_text.split('\n') if line.strip()]
            if len(lines) < 3:
                raise ValueError("Format should be: nodes\\nedges\\nstart_node (each on new line)")

            nodes = [n.strip() for n in lines[0].split(',')]
            edges = parse_edges(lines[1])
            start_node = lines[2].strip()

            num_nodes = len(nodes)
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
            pattern = data.get('pattern')
            
            try:
                
                category_normalized = category_normalized.replace('_', ' ')
                generated = generate_random_input(category_normalized, size)

                # Handle (data, formatted_preview) or simple data
                if isinstance(generated, tuple) and len(generated) == 2 and isinstance(generated[1], str):
                    input_data, formatted_preview = generated
                else:
                    input_data, formatted_preview = generated, str(generated)

                # 🔹 Handle string matching case
                if category_normalized == 'string_matching':
                    # If user provided pattern, combine it with generated text
                    if pattern and isinstance(input_data, str):
                        input_data = (input_data, pattern)
                        formatted_preview = f"Text: {input_data[0][:50]}...\nPattern: {pattern}"
                    else:
                        # Pattern will be entered later
                        formatted_preview = f"Text: {input_data[:50]}...\nPattern: (Enter manually)"

                # 🔹 Save to session
                if player == 1:
                    session['input_p1'] = input_data
                else:
                    session['input_p2'] = input_data
                session.modified = True

                # 🔹 Build response (formatted nicely for frontend)
                response_data = {
                    'success': True,
                    'input': formatted_preview,      # show formatted text
                    'preview': formatted_preview,    # ensure same field for JS
                    'input_complete': False          # will become True for most categories
                }

                # ✅ Searching category: show array + target
                if category_normalized == 'searching':
                    # Only array generated — target entered manually later
                    response_data['preview'] = f"Array: {input_data}\nTarget: (Enter manually)"
                    response_data['input'] = input_data
                    response_data['input_complete'] = False  # Wait until user enters search key

                # ✅ String matching (with pattern entered)
                elif category_normalized == 'string_matching' and isinstance(input_data, tuple) and len(input_data) == 2:
                    text, pat = input_data
                    response_data['preview'] = f"Text: {text[:50]}...\nPattern: {pat}"
                    response_data['pattern'] = pat
                    response_data['input_complete'] = True

                # ✅ All other categories (graph, knapsack, etc.)
                else:
                    # For graph & knapsack, formatted_preview is already beautiful multiline text
                    response_data['preview'] = formatted_preview
                    response_data['input'] = formatted_preview
                    response_data['input_complete'] = True

                return jsonify(response_data)

            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        elif action == 'manual':
            input_text = data.get('input_text', '').strip()
            search_key = data.get('search_key')
            pattern = data.get('pattern')  # For string matching with separate pattern field
            num_elements = data.get('num_elements')  # ✅ New field from manual tab

            try:
                # Normalize category
                category_normalized = category_normalized.replace('_', ' ').lower()

                # ✅ For string matching (text + pattern)
                if category_normalized == 'string matching' and '\n' in input_text:
                    lines = input_text.split('\n', 1)
                    text = lines[0].strip()
                    pattern_from_input = lines[1].strip() if len(lines) > 1 else ''
                    parsed_input = parse_manual_input(text, category_normalized, pattern_from_input)

                # ✅ For searching, use num_elements and search_key if provided
                elif category_normalized == 'searching':
                    parsed_input = parse_manual_input(input_text, category_normalized)
                    if search_key is not None:
                        parsed_input = (parsed_input, int(search_key))
                    if num_elements:
                        print(f"[DEBUG] Player {player} specified {num_elements} elements for searching")

                # ✅ For sorting (include num_elements if needed)
                elif category_normalized == 'sorting':
                    parsed_input = parse_manual_input(input_text, category_normalized)
                    if num_elements:
                        print(f"[DEBUG] Player {player} specified {num_elements} elements for sorting")

                # ✅ All other categories
                else:
                    parsed_input = parse_manual_input(input_text, category_normalized, pattern)

                # ✅ Store in session
                if player == 1:
                    session['input_p1'] = parsed_input
                else:
                    session['input_p2'] = parsed_input

                session.modified = True

                return jsonify({
                    'success': True,
                    'input': str(parsed_input)
                })

            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                })

    
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
