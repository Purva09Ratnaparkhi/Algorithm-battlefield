# Algorithm Battlefield Arena

A gamified Flask web application where two players compete by running algorithms from different categories and comparing their performance (execution time and memory usage).

## 🎮 Features

- **34+ Algorithms** across 8 categories (Sorting, Searching, Graph, String Matching, etc.)
- **Real-time Performance Metrics** - Measures execution time and memory usage
- **Gamified Battle Interface** - Engaging UI with animations and effects
- **Responsive Design** - Works perfectly on mobile, tablet, and desktop
- **Session Management** - Track game state without a database
- **Visual Comparison** - Side-by-side results with charts and statistics

## 🚀 Quick Start

### Installation

1. **Clone or extract the project**
```bash
cd "d:\SEM 5\NEW CA CP"
```

2. **Create virtual environment**
```powershell
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

### Running the Application

```powershell
python app.py
```

Then open your browser and go to: `http://localhost:5000`

## 📁 Project Structure

```
algorithm-battlefield-arena/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
│
├── algorithms/                 # Algorithm implementations
│   ├── sorting.py             # 6 sorting algorithms
│   ├── searching.py           # 3 searching algorithms
│   ├── shortest_path.py       # 3 shortest path algorithms
│   ├── mcst.py               # 2 MST algorithms
│   ├── graph.py              # 2 graph traversal algorithms
│   ├── string_matching.py    # 4 string matching algorithms
│   ├── subset.py             # 5 subset generation algorithms
│   └── knapsack.py           # 3 knapsack algorithms
│
├── utils/                      # Utility functions
│   ├── performance.py         # Performance measurement
│   ├── input_generator.py     # Random input generation
│   └── validators.py          # Input validation
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── select_category.html   # Category selection
│   ├── select_algorithm.html  # Algorithm selection
│   ├── input.html             # Input entry
│   ├── battle.html            # Battle execution
│   └── result.html            # Results display
│
└── static/                     # Static files
    ├── css/
    │   ├── style.css          # Main stylesheet
    │   ├── animations.css     # Animations
    │   └── responsive.css     # Responsive design
    └── js/
        ├── main.js            # Main JavaScript
        ├── battle.js          # Battle logic
        ├── animations.js      # Animation effects
        └── api.js             # API utilities
```

## 🎯 Gameplay Flow

1. **Home Page** - Welcome screen with "Start Battle" button
2. **Category Selection** - Both players choose different algorithm categories
3. **Algorithm Selection** - Players choose specific algorithms
4. **Input Entry** - Provide input data (manual or random)
5. **Battle** - Algorithms execute and compete
6. **Results** - View detailed performance comparison

## 🧠 Supported Algorithms

### Sorting (6)
- Bubble Sort
- Insertion Sort
- Merge Sort
- Quick Sort
- Selection Sort
- Heap Sort

### Searching (3)
- Linear Search
- Binary Search
- Fibonacci Search

### Shortest Path (3)
- Dijkstra's Algorithm
- Bellman-Ford Algorithm
- Floyd-Warshall Algorithm

### MST (2)
- Prim's Algorithm
- Kruskal's Algorithm

### Graph Traversal (2)
- BFS (Breadth-First Search)
- DFS (Depth-First Search)

### String Matching (4)
- Naive Search
- KMP Search
- Rabin-Karp
- Boyer-Moore

### Subset Generation (5)
- Bitmasking
- Backtracking
- Recursive
- Iterative
- Python Built-in

### 0/1 Knapsack (3)
- Dynamic Programming
- Backtracking
- Branch & Bound

## 💡 How It Works

### Performance Measurement

The application uses:
- **`timeit.default_timer()`** - Precise execution time measurement
- **`tracemalloc`** - Memory usage profiling
- **Session management** - Stores game state temporarily

### Scoring System

Winner is determined by lowest combined score:
```
Score = 100 - (execution_time * 100 + memory_usage * 0.1)
```

### Features

- **Real-time Execution** - Algorithms run sequentially with timing
- **Error Handling** - Graceful error messages for invalid inputs
- **Input Validation** - Ensures data is compatible with algorithms
- **Responsive UI** - Adapts to all screen sizes
- **Animations** - Smooth transitions and visual feedback

## 🎨 UI/UX Highlights

- **Dark Gaming Theme** - Navy blue + Neon red/green
- **Responsive Design** - Mobile-first approach
- **Smooth Animations** - Fade, slide, and glow effects
- **Modern Typography** - Orbitron, Poppins, Montserrat fonts
- **Interactive Elements** - Hover effects, ripple animations
- **Progress Visualization** - Animated bars during execution

## ⚙️ Configuration

Edit `config.py` to customize:
- Session timeout
- Default input sizes
- Algorithm-specific settings
- Logging levels

## 🔧 Requirements

- Python 3.8+
- Flask 2.3.3
- Flask-Session 0.5.0
- Werkzeug 2.3.7
- python-dotenv 1.0.0

## 📊 Performance Considerations

- Input size limits prevent long-running algorithms
- Timeout protection for execution
- Memory-efficient implementations
- Optimized for competitive testing

## 🐛 Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed
- Verify all dependencies: `pip install -r requirements.txt`
- Check port 5000 is available

### Algorithms running slowly
- Reduce input size in settings
- Check system resources
- Monitor memory usage

### UI looks broken
- Clear browser cache
- Update to latest browser version
- Ensure JavaScript is enabled

## 📝 Example Scenarios

### Scenario 1: Sorting Competition
- Player 1: Bubble Sort with 100 numbers
- Player 2: Merge Sort with 100 numbers
- Result: Merge Sort wins with faster execution

### Scenario 2: String Matching
- Player 1: Naive Search in 1000 character text
- Player 2: Boyer-Moore in same text
- Result: Boyer-Moore wins with optimal algorithm

### Scenario 3: Graph Traversal
- Player 1: BFS on graph with 50 nodes
- Player 2: DFS on same graph
- Result: Compare traversal performance

## 🎓 Educational Value

- Learn algorithm performance characteristics
- Compare different implementations
- Understand time vs. space tradeoffs
- Practice competitive programming

## 🔐 Security Notes

- Session data stored locally (no persistence)
- Input validation prevents injection attacks
- No sensitive data stored
- Safe for educational use

## 📄 License

Free for educational and personal use.

## 🤝 Contributing

Feel free to add:
- More algorithms
- Additional categories
- Enhanced UI features
- Performance optimizations

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review algorithm implementations
3. Verify input data format
4. Check browser console for errors

---

**Enjoy the Algorithm Battlefield Arena!** ⚔️🎮

Made with ❤️ for algorithm enthusiasts
