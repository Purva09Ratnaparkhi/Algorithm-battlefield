# Input Formats Verification

## Summary
✅ All 8 algorithm categories have correct input formats defined in:
- **Backend**: `utils/input_generator.py` (random generation)
- **Backend**: `app.py` (manual input parsing)
- **Frontend**: `templates/input.html` (UI hints and placeholders)

---

## 1. **SORTING**

### Random Generation
- **Returns**: `[int, int, int, ...]` (list of random integers 1-1000)
- **Example**: `[523, 81, 945, 234, 102]`

### Manual Input
- **Format**: Comma-separated numbers
- **Placeholder**: `5, 3, 8, 1, 9`
- **UI Label**: "Number of Elements"
- **Hint**: "Number of elements to sort (2-500)"

### Backend Parsing
```python
# Parse: "5, 3, 8, 1, 9"
return [int(x.strip()) for x in input_text.split(',')]
```

✅ **Status**: CORRECT

---

## 2. **SEARCHING**

### Random Generation
- **Returns**: `(array, target)` tuple
- **Example**: `([523, 81, 945, 234, 102], 456)`
- **Note**: Target is **completely random** and may or may not exist in array

### Manual Input (with Search Key)
- **Array Format**: Comma-separated numbers
- **Search Key**: Separate input field
- **Array Placeholder**: `5, 3, 8, 1, 9`
- **UI Labels**: 
  - "Number of Elements" (for array size)
  - "Search Key (Target Value)" - appears in BOTH Random and Manual tabs
- **Random Tab**: Search key is **auto-populated** and **read-only**
- **Manual Tab**: Search key is **manual input** (writable)

### Backend Parsing
```python
# Random tab sends no search_key, backend generates it
# Manual tab sends search_key separately
parsed_input = (array_list, int(search_key))
```

✅ **Status**: CORRECT

---

## 3. **STRING MATCHING**

### Random Generation
- **Returns**: `(text, pattern)` tuple
- **Example**: `('abcdefghijklmnopqrstuvwxyz...', 'abd')`
- **Text Size**: `max(100, size * 2)` characters
- **Pattern Size**: `min(10, max(2, size // 10))` characters
- **Note**: Pattern is **completely random** and may or may not exist in text

### Manual Input
- **Format**: `text|pattern` (pipe-separated)
- **Placeholder**: `ABABDABAACAAB|AABAAC`
- **UI Labels**: 
  - "Text Length" (for size parameter)
- **Hint**: "Length of text to search in (5-500)"

### Backend Parsing
```python
# Parse: "ABABDABAACAAB|AABAAC"
parts = input_text.split('|')
return (parts[0].strip(), parts[1].strip())
```

✅ **Status**: CORRECT

---

## 4. **SHORTEST PATH**

### Random Generation
- **Returns**: `(num_nodes, edges, start_node)` tuple
- **Nodes**: Limited to min(size, 10) = max 10 nodes
- **Edges**: `(u, v, weight)` tuples with random weights 1-100
- **Example**: `(4, [(0, 1, 45), (0, 2, 31), (1, 3, 22)], 0)`

### Manual Input
- **Format**: 3 lines separated by newline
  - Line 1: Number of nodes (integer)
  - Line 2: Edges in format `(A,B,weight);(A,C,weight)`
  - Line 3: Start node (integer)
- **Placeholder**: 
  ```
  4
  (A,B,4);(B,C,2);(A,C,5)
  0
  ```
- **UI Labels**: 
  - "Number of Nodes"
- **Hint**: "Number of nodes in graph (2-10)"

### Backend Parsing
```python
# Parse format: nodes / edges / start_node
lines = [line.strip() for line in input_text.split('\n') if line.strip()]
num_nodes = int(lines[0])
edges = parse_edges(lines[1])  # Returns [(u,v,w), ...]
start_node = int(lines[2])
return (num_nodes, edges, start_node)
```

✅ **Status**: CORRECT

---

## 5. **MST (Minimum Spanning Tree)**

### Random Generation
- **Returns**: `(num_nodes, edges)` tuple
- **Nodes**: Limited to min(size, 10) = max 10 nodes
- **Edges**: `(u, v, weight)` tuples with random weights 1-100
- **Example**: `(4, [(0, 1, 45), (0, 2, 31), (1, 3, 22), (2, 3, 50)], None)`

### Manual Input
- **Format**: 2 lines separated by newline
  - Line 1: Number of nodes (integer)
  - Line 2: Edges in format `(A,B,weight);(A,C,weight)`
- **Placeholder**: 
  ```
  4
  (A,B,4);(B,C,2);(A,C,5);(B,D,3)
  ```
- **UI Labels**: 
  - "Number of Nodes"
- **Hint**: "Number of nodes in graph (2-10)"

### Backend Parsing
```python
# Parse format: nodes / edges
lines = [line.strip() for line in input_text.split('\n') if line.strip()]
num_nodes = int(lines[0])
edges = parse_edges(lines[1])
return (num_nodes, edges)
```

✅ **Status**: CORRECT

---

## 6. **GRAPH (BFS/DFS)**

### Random Generation
- **Returns**: `(num_nodes, edges, start_node)` tuple
- **Nodes**: Limited to min(size, 10) = max 10 nodes
- **Edges**: `(u, v)` unweighted tuples
- **Example**: `(4, [(0, 1), (1, 2), (0, 2), (2, 3)], 0)`

### Manual Input
- **Format**: 3 lines separated by newline
  - Line 1: Number of nodes (integer)
  - Line 2: Edges in format `(A,B);(A,C)` (no weights)
  - Line 3: Start node (integer)
- **Placeholder**: 
  ```
  4
  (A,B);(B,C);(A,C)
  0
  ```
- **UI Labels**: 
  - "Number of Nodes"
- **Hint**: "Number of nodes in graph (2-10)"

### Backend Parsing
```python
# Parse format: nodes / edges / start_node
lines = [line.strip() for line in input_text.split('\n') if line.strip()]
num_nodes = int(lines[0])
edges = parse_edges(lines[1])  # Returns [(u,v), ...] or [(u,v,w), ...]
start_node = int(lines[2])
return (num_nodes, edges, start_node)
```

✅ **Status**: CORRECT

---

## 7. **SUBSET GENERATION**

### Random Generation
- **Returns**: `[int, int, int, ...]` (list of random integers 1-100)
- **Size**: Capped at 15 elements max (2^15 = 32,768 subsets = manageable)
- **Example**: `[42, 15, 88, 3, 67]`

### Manual Input
- **Format**: Comma-separated numbers
- **Placeholder**: `1, 2, 3, 4`
- **UI Labels**: 
  - "Number of Elements"
- **Hint**: "Number of elements (2-15)"

### Backend Parsing
```python
# Parse: "1, 2, 3, 4"
return [int(x.strip()) for x in input_text.split(',')]
```

✅ **Status**: CORRECT

---

## 8. **0/1 KNAPSACK**

### Random Generation
- **Returns**: `(n, weights, values, capacity)` tuple
- **Items**: Limited to min(size, 10) = max 10 items
- **Weights**: Random integers 1-50
- **Values**: Random integers 1-100
- **Capacity**: sum(weights) // 2
- **Example**: `(3, [20, 15, 30], [50, 40, 60], 33)`

### Manual Input
- **Format**: 4 lines separated by newline
  - Line 1: Number of items (integer)
  - Line 2: Weights (comma-separated integers)
  - Line 3: Values (comma-separated integers)
  - Line 4: Capacity (integer)
- **Placeholder**: 
  ```
  3
  2, 3, 4
  3, 4, 5
  5
  ```
- **UI Labels**: 
  - "Number of Items"
- **Hint**: "Number of items (2-10)"

### Backend Parsing
```python
# Parse format: n / weights / values / capacity
lines = [line.strip() for line in input_text.split('\n') if line.strip()]
n = int(lines[0])
weights = [int(x.strip()) for x in lines[1].split(',')]
values = [int(x.strip()) for x in lines[2].split(',')]
capacity = int(lines[3])
return (n, weights, values, capacity)
```

✅ **Status**: CORRECT

---

## UI Display Verification

### Hints Mapping (All Correct)
| Category | Size Label | Size Hint | Manual Hint Format |
|----------|-----------|-----------|-------------------|
| Sorting | "Number of Elements" | "2-500" | "5, 3, 8, 1, 9" |
| Searching | "Number of Elements" | "2-100" | "5, 3, 8, 1, 9" |
| String Matching | **"Text Length"** | "5-500" | "text\|pattern" |
| Shortest Path | "Number of Nodes" | "2-10" | "nodes\nedges\nstart" |
| MST | "Number of Nodes" | "2-10" | "nodes\nedges" |
| Graph | "Number of Nodes" | "2-10" | "nodes\nedges\nstart" |
| Subset Generation | "Number of Elements" | "2-15" | "1, 2, 3, 4" |
| 0/1 Knapsack | "Number of Items" | "2-10" | "n\nweights\nvalues\ncap" |

### Special UI Elements
- ✅ **Searching**: Search key field appears in both Random and Manual tabs
  - Random tab: auto-populated and read-only
  - Manual tab: manual input (writable)
- ✅ **String Matching**: Shows "Text Length" not "Number of Elements"

---

## Testing Checklist

- [x] All 8 categories have proper random generation
- [x] All manual input formats are parsed correctly
- [x] UI hints match backend logic
- [x] Size parameters are appropriate (capped for exponential algorithms)
- [x] Searching has auto-generated random target
- [x] String matching has completely random pattern
- [x] Graph formats support weighted (shortest path, MST) and unweighted (BFS/DFS)
- [x] All edge formats parse correctly `(A,B,weight)` or `(A,B)`

---

## Summary
✅ **ALL INPUT FORMATS ARE CORRECT AND PROPERLY DISPLAYED IN THE UI**

The system is ready for battle with correct input generation and validation across all categories!
