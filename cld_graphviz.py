# cld_graphviz.py - Professional CLD Generator with Graphviz
import re
import networkx as nx
import pydot  # type: ignore
from pathlib import Path
import tempfile
import os

def load_edges(path: str):
    """
    Reads CLD notation file and returns list of tuples:
    [(source, destination, sign), ...]
    """
    edges = []
    pattern = re.compile(r"^\s*([A-Za-z0-9_]+)\s+([+-])\s+([A-Za-z0-9_]+)")
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.split("#", 1)[0]        # remove comments
            m = pattern.match(line)
            if m:
                edges.append((m.group(1), m.group(3), m.group(2)))
    return edges

def build_networkx_graph(edges):
    """Builds NetworkX graph for loop analysis"""
    G = nx.DiGraph()
    for src, dst, sign in edges:
        G.add_edge(src, dst, sign=sign)
    return G

def analyze_loops(G):
    """Analyzes graph loops and classifies as reinforcing or balancing"""
    loops = list(nx.simple_cycles(G))
    loop_analysis = []
    
    for loop in loops:
        negative_count = 0
        for i in range(len(loop)):
            src = loop[i]
            dst = loop[(i + 1) % len(loop)]
            if G.has_edge(src, dst):
                sign = G[src][dst]['sign']
                if sign == '-':
                    negative_count += 1
        
        loop_type = "Balancing" if negative_count % 2 == 1 else "Reinforcing"
        loop_analysis.append({
            'loop': loop,
            'type': loop_type,
            'negative_count': negative_count
        })
    
    return loop_analysis

def identify_central_nodes(G, edges):
    """Identifies central nodes based on connectivity degree"""
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    
    # Combines metrics to identify central nodes
    centrality_scores = {}
    for node in G.nodes():
        centrality_scores[node] = (
            degree_centrality[node] * 0.6 + 
            betweenness_centrality[node] * 0.4
        )
    
    # Sort by centrality
    sorted_nodes = sorted(centrality_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Classify nodes into categories
    total_nodes = len(sorted_nodes)
    central_nodes = [node for node, score in sorted_nodes[:max(1, total_nodes//4)]]
    intermediate_nodes = [node for node, score in sorted_nodes[total_nodes//4:3*total_nodes//4]]
    peripheral_nodes = [node for node, score in sorted_nodes[3*total_nodes//4:]]
    
    return {
        'central': central_nodes,
        'intermediate': intermediate_nodes,
        'peripheral': peripheral_nodes
    }

def create_professional_cld(edges, outfile="cld_professional.svg", layout="circo", minimize_crossings=True):
    """
    Creates a professional CLD using Graphviz with option to minimize crossings
    
    Available layouts:
    - circo: Circular layout (ideal for CLDs)  
    - fdp: Force-directed placement
    - neato: Spring model
    - dot: Hierarchical
    - twopi: Radial
    - sfdp: Scalable force-directed placement (better for large graphs)
    """
    
    # Graph analysis
    G_nx = build_networkx_graph(edges)
    loops = analyze_loops(G_nx)
    node_categories = identify_central_nodes(G_nx, edges)
    
    # Configure parameters based on graph size
    num_nodes = len(set([src for src, _, _ in edges] + [dst for _, dst, _ in edges]))
    num_edges = len(edges)
    
    # Basic graph configurations
    graph_attrs = {
        'graph_type': 'digraph',
        'layout': layout,
        'bgcolor': 'white',
        'fontname': 'Arial',
        'fontsize': '14'
        # Title removed as requested
    }
    
    # Add parameters to minimize crossings
    if minimize_crossings:
        if layout in ['circo', 'twopi']:
            # For circular layouts
            circular_attrs = {
                'overlap': 'false',
                'splines': 'curved',
                'concentrate': 'true',  # Groups parallel edges
                'mindist': '1.5',       # Minimum distance between nodes
                'sep': '+25,25',        # Extra separation between components
                'esep': '+10,10',       # Separation between edges
                'pack': 'true',         # Compacts the layout
                'packmode': 'graph',    # Compaction mode
            }
            if node_categories['central']:
                circular_attrs['root'] = str(node_categories['central'][0])
            graph_attrs.update(circular_attrs)
        elif layout in ['fdp', 'sfdp']:
            # For force-directed layouts
            graph_attrs.update({
                'overlap': 'prism',     # Advanced overlap algorithm
                'splines': 'spline',    # Smooth splines
                'concentrate': 'true',
                'K': str(0.9),          # Spring force (lower = fewer crossings)
                'maxiter': '1000',      # More iterations for better result
                'sep': '+15,15',
                'esep': '+8,8',
                'repulsiveforce': '2.0', # Repulsive force between nodes
                'smoothing': 'spring'    # Edge smoothing
            })
        elif layout == 'neato':
            # For spring model
            graph_attrs.update({
                'overlap': 'scale',
                'splines': 'spline',
                'concentrate': 'true',
                'epsilon': '0.01',      # Algorithm precision
                'maxiter': '500',
                'sep': '+20,20',
                'model': 'circuit'      # Circuit model for fewer crossings
            })
        elif layout == 'dot':
            # For hierarchical layout
            graph_attrs.update({
                'overlap': 'false',
                'splines': 'ortho',     # Orthogonal edges (right angles)
                'concentrate': 'true',
                'nodesep': '0.8',       # Separation between nodes at same level
                'ranksep': '1.2',       # Separation between levels
                'ordering': 'out',      # Order outputs to reduce crossings
                'compound': 'true'      # Allows compound edges
            })
    else:
        # Basic configurations without crossing optimization
        graph_attrs.update({
            'overlap': 'false',
            'splines': 'curved'
        })
    
    # Create the graph with optimized attributes
    graph = pydot.Dot(**graph_attrs)
    
    # Configure styles by node category
    node_styles = {
        'central': {
            'shape': 'ellipse',
            'style': 'filled',
            'fillcolor': '#FFE4B5',  # Moccasin - highlight for central nodes
            'color': '#8B4513',      # SaddleBrown
            'fontsize': '12',
            'fontcolor': '#8B4513',
            'penwidth': '2'
        },
        'intermediate': {
            'shape': 'ellipse',
            'style': 'filled',
            'fillcolor': '#E6F3FF',  # Alice Blue
            'color': '#4682B4',      # Steel Blue
            'fontsize': '10',
            'fontcolor': '#4682B4',
            'penwidth': '1.5'
        },
        'peripheral': {
            'shape': 'ellipse',
            'style': 'filled',
            'fillcolor': '#F0F8FF',  # Lighter AliceBlue
            'color': '#6495ED',      # Cornflower Blue
            'fontsize': '9',
            'fontcolor': '#6495ED',
            'penwidth': '1'
        }
    }
    
    # Add nodes with styles based on centrality
    all_nodes = set()
    for src, dst, sign in edges:
        all_nodes.add(src)
        all_nodes.add(dst)
    
    for node in all_nodes:
        # Determine node category
        if node in node_categories['central']:
            style = node_styles['central']
        elif node in node_categories['intermediate']:
            style = node_styles['intermediate']
        else:
            style = node_styles['peripheral']
        
        # Break line on long names
        label = node.replace('_', '\\n') if len(node) > 10 else node
        
        pydot_node = pydot.Node(node, label=label, **style)
        graph.add_node(pydot_node)
    
    # Add edges with styles based on sign and anti-crossing optimizations
    for src, dst, sign in edges:
        base_style = {
            'penwidth': '2',
            'arrowhead': 'normal',
            'arrowsize': '1.2'
        }
        
        # Add anti-crossing parameters if enabled
        if minimize_crossings:
            base_style.update({
                'constraint': 'true',    # Maintains hierarchical structure
                'weight': '2',           # Edge weight for positioning
                'minlen': '1'            # Minimum length
            })
        
        if sign == '+':
            edge_style = {
                **base_style,
                'color': '#228B22',      # Forest Green
            }
            label_style = {
                'label': '+',
                'fontcolor': '#228B22',
                'fontsize': '14',
                'fontname': 'Arial Bold'
            }
        else:  # sign == '-'
            edge_style = {
                **base_style,
                'color': '#DC143C',      # Crimson
            }
            label_style = {
                'label': '−',
                'fontcolor': '#DC143C',
                'fontsize': '14',
                'fontname': 'Arial Bold'
            }
        
        edge = pydot.Edge(src, dst, **edge_style, **label_style)
        graph.add_edge(edge)
    
    # Save file
    Path(outfile).parent.mkdir(parents=True, exist_ok=True)
    
    # Determine format based on extension
    file_ext = Path(outfile).suffix.lower()
    if file_ext == '.svg':
        graph.write_svg(outfile)
    elif file_ext == '.png':
        graph.write_png(outfile)
    elif file_ext == '.pdf':
        graph.write_pdf(outfile)
    elif file_ext == '.dot':
        graph.write_dot(outfile)
    else:
        # Default to SVG
        outfile = str(Path(outfile).with_suffix('.svg'))
        graph.write_svg(outfile)
    
    print(f"\n📊 Graphviz diagram saved to: {outfile}")
    
    # Detailed report
    print(f"\n{'='*60}")
    print("DETAILED SYSTEM ANALYSIS")
    print(f"{'='*60}")
    
    print(f"\n🎯 NODE CLASSIFICATION:")
    print(f"   Central ({len(node_categories['central'])}): {', '.join(node_categories['central'])}")
    print(f"   Intermediate ({len(node_categories['intermediate'])}): {', '.join(node_categories['intermediate'])}")
    print(f"   Peripheral ({len(node_categories['peripheral'])}): {', '.join(node_categories['peripheral'])}")
    
    if loops:
        print(f"\n🔄 IDENTIFIED LOOPS ({len(loops)}):")
        for i, loop_info in enumerate(loops, 1):
            loop_str = " → ".join(loop_info['loop'] + [loop_info['loop'][0]])
            print(f"\n   Loop {i}: {loop_str}")
            print(f"   📍 Type: {loop_info['type']} ({loop_info['negative_count']} negative signs)")
            
            if loop_info['type'] == 'Reinforcing':
                print(f"   📈 Behavior: Amplifies changes (exponential growth)")
                print(f"   ⚠️  Warning: May lead to uncontrolled growth or collapse")
            else:
                print(f"   ⚖️  Behavior: Seeks equilibrium (self-regulation)")
                print(f"   ✅ Effect: Stabilizes the system")
    else:
        print(f"\n❌ No loops detected in the system")
    
    print(f"\n📈 SYSTEM METRICS:")
    print(f"   • Total variables: {len(all_nodes)}")
    print(f"   • Total relations: {len(edges)}")
    print(f"   • Positive relations: {sum(1 for _, _, s in edges if s == '+')}")
    print(f"   • Negative relations: {sum(1 for _, _, s in edges if s == '-')}")
    print(f"   • Layout used: {layout}")
    
    return graph, loops, node_categories

def create_optimized_layouts(edges, base_filename="cld_optimized"):
    """Creates optimized layouts to minimize crossings"""
    layouts = {
        'sfdp': 'Scalable Force-Directed (Recommended for Anti-Crossing)',
        'fdp': 'Force-Directed with Optimizations',
        'circo': 'Optimized Circular Layout',
        'neato': 'Spring Model with Crossing Reduction'
    }
    
    print(f"\n🎯 Generating optimized layouts to minimize crossings...")
    
    results = {}
    for layout, description in layouts.items():
        outfile = f"{base_filename}_{layout}.svg"
        try:
            print(f"   🔧 Creating {description}...")
            graph, loops, categories = create_professional_cld(edges, outfile, layout, minimize_crossings=True)
            results[layout] = {
                'file': outfile,
                'description': description,
                'graph': graph,
                'loops': loops,
                'categories': categories
            }
        except Exception as e:
            print(f"   ❌ Error in layout {layout}: {e}")
    
    return results

def create_multiple_layouts(edges, base_filename="cld_comparison"):
    """Creates multiple layouts for comparison"""
    layouts = {
        'circo': 'Circular Layout (Recommended for CLDs)', 
        'fdp': 'Force-Directed Placement',
        'neato': 'Spring Model', 
        'twopi': 'Radial Layout'
    }
    
    print(f"\n🎨 Generating multiple layouts for comparison...")
    
    results = {}
    for layout, description in layouts.items():
        outfile = f"{base_filename}_{layout}.svg"
        try:
            print(f"   📐 Creating {description}...")
            graph, loops, categories = create_professional_cld(edges, outfile, layout)
            results[layout] = {
                'file': outfile,
                'description': description,
                'graph': graph,
                'loops': loops,
                'categories': categories
            }
        except Exception as e:
            print(f"   ❌ Error in layout {layout}: {e}")
    
    return results

if __name__ == "__main__":
    import sys
    
    # Command line arguments
    arquivo = sys.argv[1] if len(sys.argv) > 1 else "cld.txt"
    saida = sys.argv[2] if len(sys.argv) > 2 else "cld_graphviz.svg"
    layout = sys.argv[3] if len(sys.argv) > 3 else "circo"
    minimize_crossings = "--no-crossings" not in sys.argv  # Enabled by default
    
    # Load data
    edges = load_edges(arquivo)
    if not edges:
        print(f"❌ Error: No relations found in {arquivo}")
        sys.exit(1)
    
    # Show system information
    num_nodes = len(set([src for src, _, _ in edges] + [dst for _, dst, _ in edges]))
    num_edges = len(edges)
    print(f"📊 System with {num_nodes} variables and {num_edges} relations")
    
    if minimize_crossings:
        print(f"🎯 Anti-crossing mode ACTIVE")
    else:
        print(f"⚠️  Anti-crossing mode DISABLED")
    
    # Generate main diagram
    print(f"🚀 Generating professional CLD with Graphviz...")
    graph, loops, categories = create_professional_cld(edges, saida, layout, minimize_crossings)
    
    # Option to generate multiple layouts
    if len(sys.argv) <= 3:  # If no layout specified, generate comparison
        base_name = str(Path(saida).with_suffix(''))
        
        # Generate normal and optimized layouts for comparison
        print(f"\n📊 Generating complete comparison...")
        results_normal = create_multiple_layouts(edges, f"{base_name}_normal")
        results_optimized = create_optimized_layouts(edges, f"{base_name}_optimized")
        
        print(f"\n🎯 RECOMMENDATIONS TO MINIMIZE CROSSINGS:")
        print(f"   🥇 Best option: 'sfdp' (scalable force)")
        print(f"   🥈 Second option: 'fdp' (force-directed)")
        print(f"   🥉 For smaller CLDs: optimized 'circo'")
        print(f"   📐 For hierarchies: 'dot' with orthogonal splines")
        
        print(f"\n📂 Generated files:")
        print(f"   📁 Normal layouts:")
        for layout_name, result in results_normal.items():
            print(f"      • {result['file']} - {result['description']}")
        print(f"   🎯 Anti-crossing layouts:")
        for layout_name, result in results_optimized.items():
            print(f"      • {result['file']} - {result['description']}")
        
        print(f"\n💡 TIP: Use 'python cld_graphviz.py file.txt output.svg sfdp' for optimized result")
        print(f"💡 TIP: Add '--no-crossings' to disable optimizations") 