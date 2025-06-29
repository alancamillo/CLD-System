# Causal Loop Diagrams (CLDs) System

This project implements a lightweight notation for creating and visualizing professional **Causal Loop Diagrams** from simple text files using **Graphviz**.

## 1. Notation

Use a simple text file with the following format:

```
# syntax: source  sign  destination
# sign: +  (same direction)   –  (opposite directions)

PressureDue          + ExtraHours
ExtraHours           - Productivity
Productivity         - ScheduleDelay
ScheduleDelay        + PressureDue
```

### 1.1. Detailed Notation Rules

| Item              | Rules and Specifications                                                                      |
| ----------------- | -------------------------------------------------------------------------------------------- |
| **Comments**      | Begin with `#` and continue to end of line. Can be anywhere.                                |
| **Variables**     | Only letters (A-Z, a-z), numbers (0-9) and underscore (_). **Do not use spaces**.          |
| **Separators**    | Minimum **one space** or tab between source, sign and destination.                          |
| **Sign (+)**      | Indicates influence in **same direction**: ↑source → ↑destination or ↓source → ↓destination |
| **Sign (-)**      | Indicates **opposite** influence: ↑source → ↓destination or ↓source → ↑destination          |
| **Empty lines**   | Automatically ignored.                                                                       |
| **Loops**         | **Automatically detected** - no need to declare explicitly.                                 |

### 1.2. Notation Examples

#### ✅ **Correct:**
```
# Example: Population Growth System
BirthRate       + TotalPopulation
TotalPopulation + ResourcePressure  
ResourcePressure - QualityOfLife
QualityOfLife   - BirthRate
```

#### ❌ **Incorrect:**
```
# Common problems:
Total Population + Births    # ❌ Space in variable name
ResourcePressure-QualityOfLife   # ❌ No proper spacing
Births ++ TotalPopulation   # ❌ Double sign
```

### 1.3. Sign Interpretation

| Relation      | Meaning                                           | Example                                  |
| ------------- | ------------------------------------------------- | ---------------------------------------- |
| A **+** B     | When A increases, B increases. When A decreases, B decreases | `Sales + Profit`                        |
| A **-** B     | When A increases, B decreases. When A decreases, B increases | `Price - Demand`                       |

## 2. Requirements and Installation

### 2.1. System Prerequisites

**⚠️ IMPORTANT: Install Graphviz on the system BEFORE installing Python dependencies:**

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install graphviz graphviz-dev
```

#### macOS:
```bash
brew install graphviz
```

#### Windows:
1. Download installer from: https://graphviz.org/download/
2. Install and add to system PATH
3. Restart terminal/prompt

### 2.2. Python Installation

```bash
# 1) Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2) Install Python dependencies
pip install -r requirements.txt

# 3) Test installation
python -c "import pydot; print('✅ Graphviz OK')"
```

### 2.3. Dependencies

```txt
networkx>=3.0       # Graph analysis and loops
pydot>=3.0.0        # Graphviz interface
graphviz>=0.20.0    # Python bindings for Graphviz
```

## 3. Usage

### 3.1. Basic Commands
```bash
# Generate professional diagram with multiple layouts
python cld_graphviz.py example.txt

# Specific optimized layout (RECOMMENDED)
python cld_graphviz.py example.txt system.svg sfdp

# Disable anti-crossing optimizations
python cld_graphviz.py example.txt system.svg circo --no-crossings
```

### 3.2. Layout Guide

| Layout  | Best For                             | Characteristics                                    |
| ------- | ------------------------------------ | -------------------------------------------------- |
| **sfdp** | Complex systems (>15 nodes)        | ⭐ **Best anti-crossing**, scalable force         |
| **fdp**  | Medium systems (5-15 nodes)        | Force-directed with optimizations                 |
| **circo** | Traditional CLDs                   | Circular layout, good for presentations           |
| **neato** | Small systems (<10 nodes)         | Spring model, fast and efficient                  |
| **dot**   | Hierarchical systems               | Level structure, great for processes              |
| **twopi** | Systems with clear central node    | Radial, highlights main element                    |

## 4. Practical Example

### 4.1. Creating a Simple CLD

1. **Create a file `example.txt`:**
```
# Organizational Feedback System
EmployeeStress  + Absenteeism
Absenteeism     - Productivity
Productivity    - Quality
Quality         + CustomerComplaints
CustomerComplaints + ManagementPressure
ManagementPressure + EmployeeStress
```

2. **Run the professional generator:**
```bash
python cld_graphviz.py example.txt professional_example.svg
```

3. **Expected result:**
```
📊 System with 6 variables and 6 relations
🚀 Generating professional CLD with Graphviz...

============================================================
DETAILED SYSTEM ANALYSIS
============================================================

🔄 IDENTIFIED LOOPS (1):
   Loop 1: EmployeeStress → Absenteeism → Productivity → Quality → CustomerComplaints → ManagementPressure → EmployeeStress
   📍 Type: Reinforcing (0 negative signs)
   📈 Behavior: Amplifies changes (exponential growth)
   ⚠️  Warning: May lead to uncontrolled growth
```

## 5. Professional Features

### ✨ Advanced Features:

#### 🎯 **Anti-Crossing Optimization:**
- **Specialized algorithms** to minimize arrow intersections
- **Multiple optimized layouts**: sfdp, fdp, circo, neato
- **Automatic configuration** based on system size
- **Advanced parameters**: splines, separation, repulsive force

#### 📊 **Automatic Analysis:**
- **Node classification**: Central, Intermediate, Peripheral
- **Loop detection**: Automatic identification with DFS algorithm
- **Behavioral analysis**: Reinforcing vs Balancing
- **System metrics**: Centrality, connectivity, complexity

#### 🎨 **Professional Visualization:**
- **Hierarchical styles**: Colors and sizes based on importance
- **Multiple formats**: SVG, PNG, PDF, DOT
- **Specialized layouts**: Each optimized for different cases
- **Professional quality**: Suitable for presentations and publications

### 🎯 Complete Command:
```bash
# Generate all layouts for comparison
python cld_graphviz.py complex_system.txt

# Specific optimized layout (RECOMMENDED)
python cld_graphviz.py complex_system.txt result.svg sfdp

# Multiple formats
python cld_graphviz.py complex_system.txt result.png fdp
python cld_graphviz.py complex_system.txt result.pdf circo

# Analysis without optimizations (for comparison)
python cld_graphviz.py complex_system.txt basic.svg circo --no-crossings
```

### 📊 Professional Output Example:
```
🎯 Anti-crossing mode ACTIVE
🚀 Generating professional CLD with Graphviz...

============================================================
DETAILED SYSTEM ANALYSIS
============================================================

🎯 NODE CLASSIFICATION:
   Central (3): WillingnessToAdopt, NumberOfUsers, AdoptionRate
   Intermediate (7): CumulativeProduction, CostAndPerformance...
   Peripheral (4): MarketSaturation, PotentialUsers...

🔄 IDENTIFIED LOOPS (6):
   Loop 1: QuantityAndQualityOfInfo → WillingnessToAdopt → AdoptionRate → NumberOfUsers → QuantityAndQualityOfInfo
   📍 Type: Reinforcing (0 negative signs)
   📈 Behavior: Amplifies changes (exponential growth)
   ⚠️  Warning: May lead to uncontrolled growth

   Loop 6: MarketSaturation → AdoptionRate → NumberOfUsers → MarketSaturation
   📍 Type: Balancing (1 negative signs)
   ⚖️  Behavior: Seeks equilibrium (self-regulation)
   ✅ Effect: Stabilizes the system

📈 SYSTEM METRICS:
   • Total variables: 14
   • Total relations: 20
   • Positive relations: 15
   • Negative relations: 5
   • Layout used: sfdp

🎯 RECOMMENDATIONS TO MINIMIZE CROSSINGS:
   🥇 Best option: 'sfdp' (scalable force)
   🥈 Second option: 'fdp' (force-directed)
   🥉 For smaller CLDs: optimized 'circo'
```

## 6. Project Structure

```
.
├── examples/
│   ├── cld.txt                     # Basic CLD example
│   ├── exemplo.txt                 # Simple additional example
│   ├── exemplo_complexo.txt        # Complex example (technology adoption)
│   ├── exemplo_empresa.txt         # Business example
│   └── nuclear.txt                 # Nuclear system example
├── cld_graphviz.py                 # Main script ⭐
├── requirements.txt                # Essential dependencies
├── venv/                           # Virtual environment
├── *.svg, *.png                    # Generated diagrams
└── README.md                       # This file
```

## 7. Graphviz Implementation Advantages

### 🏆 Professional Characteristics:
- **✅ Anti-crossing optimization**: Specialized algorithms to minimize intersections
- **✅ Professional quality**: Used worldwide by industry and academia
- **✅ Multiple specialized layouts**: 6+ algorithms optimized for different cases
- **✅ Scalability**: Works well with systems from 5 to 100+ nodes
- **✅ Advanced analysis**: Automatic classification and centrality metrics
- **✅ Multiple formats**: SVG, PNG, PDF, DOT for different uses

## 8. Troubleshooting

### 8.1. Common Problems

#### ❌ **Error: "graphviz executables not found"**
```bash
# Solution: Install Graphviz on system
sudo apt install graphviz      # Linux
brew install graphviz          # macOS
# Windows: Download from graphviz.org and add to PATH
```

#### ❌ **Error: "No module named 'pydot'"**
```bash
# Solution: Install Python dependencies
pip install -r requirements.txt
```

#### ❌ **Input file not found**
```bash
# Solution: Check if file exists
ls -la examples/
# Or use absolute path
python cld_graphviz.py /complete/path/to/file.txt
```

#### ❌ **Too many crossings in diagram**
```bash
# Solution: Use optimized layout
python cld_graphviz.py file.txt output.svg sfdp
# Or test different layouts
python cld_graphviz.py file.txt  # Generates all for comparison
```

### 8.2. Performance Optimization

For **very large systems** (>50 nodes):
```bash
# Use sfdp for better performance
python cld_graphviz.py large_system.txt result.svg sfdp

# Or disable optimizations if needed
python cld_graphviz.py large_system.txt result.svg sfdp --no-crossings
```

## 9. Use Cases

- **Business Analysis**: Organizational process modeling
- **Academic Research**: Systems dynamics studies
- **Strategic Planning**: Interdependency visualization
- **Education**: Systems thinking teaching
- **Consulting**: Complex analysis presentations

## 10. License

MIT License - see LICENSE file for details.

## 11. Contributing

Contributions are welcome! Please open issues or submit pull requests.

---

## 🚀 **Get Started Now!**

1. **Install Graphviz on system:**
   ```bash
   sudo apt install graphviz  # Linux
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create your first CLD:**
   ```bash
   python cld_graphviz.py examples/exemplo.txt my_first_cld.svg sfdp
   ```

4. **Open the generated SVG file** in your browser or editor of choice.

**Enjoy professional CLD generation with Graphviz!** 🎉 