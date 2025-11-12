import networkx as nx
import numpy as np
import random
from typing import Set, Tuple, Dict, List
import plotly.graph_objects as go
from engine import Distinction, DistinctionEngine


class UniverseVisualizer:
    def __init__(self, engine: DistinctionEngine):
        self.engine = engine
        self.origin_id = self.engine.d0.id
        self.graph = None 

    def _build_graph_from_snapshot(self, state: Tuple[Set[Distinction], Set[Tuple[str, str]]]) -> nx.Graph:
        """Builds a NetworkX graph object from an immutable snapshot."""
        distinctions, relationships = state
        g = nx.Graph()
        g.add_nodes_from([d.id for d in distinctions])
        g.add_edges_from(relationships)
        return g

    def _evolve_universe_locally(self, steps: int):
        """Runs the "one process" locally to create the substrate."""
        current_distinctions = list(self.engine.all_distinctions.values())
        if len(current_distinctions) < 2:
            return

        distinction_map = {d.id: d for d in current_distinctions}

        for i in range(steps):
            state = self.engine.get_state_snapshot()
            self.graph = self._build_graph_from_snapshot(state) 
            
            if len(current_distinctions) < 2:
                break
                
            a = random.choice(current_distinctions)
            b = None

            try:
                neighborhood_ids = set(self.graph.neighbors(a.id))
                for neighbor_id in list(neighborhood_ids):
                    neighborhood_ids.update(self.graph.neighbors(neighbor_id))
                neighborhood_ids.discard(a.id)
                
                if neighborhood_ids:
                    b_id = random.choice(list(neighborhood_ids))
                    b = distinction_map.get(b_id)
            
            except (nx.NetworkXError, KeyError):
                pass 
            
            if b is None or b.id == a.id:
                others = [d for d in current_distinctions if d.id != a.id]
                if not others:
                    continue
                b = random.choice(others)
            
            c = self.engine.synthesize(a, b)
            
            if c.id not in distinction_map:
                current_distinctions.append(c)
                distinction_map[c.id] = c
                self.graph.add_node(c.id)
                self.graph.add_edge(c.id, a.id)
                self.graph.add_edge(c.id, b.id)


    def _calculate_emergent_properties(self) -> Dict[str, Dict[str, float]]:
        """Calculates emergent properties (Coherence, Usage, Age) for all nodes."""
        if not self.graph:
            raise ValueError("Graph not built. Run _evolve_universe_locally first.")

        properties = {}
        all_nodes = list(self.graph.nodes())

        if not all_nodes:
            return {}

        coherences = nx.clustering(self.graph)
        degrees = dict(self.graph.degree())
        max_degree = max(degrees.values()) if degrees else 1

        ages = {}
        max_age = 0
        if self.origin_id in self.graph:
            for node_id in all_nodes:
                try:
                    age = nx.shortest_path_length(self.graph, source=self.origin_id, target=node_id)
                except (nx.NetworkXNoPath, nx.NodeNotFound):
                    age = 0 
                ages[node_id] = age
                if age > max_age:
                    max_age = age
        
        for node_id in all_nodes:
            props = {
                "coherence": coherences.get(node_id, 0.0),
                "usage": degrees.get(node_id, 0) / max_degree, 
                "age": ages.get(node_id, 0) / (max_age if max_age > 0 else 1)
            }
            properties[node_id] = props
        
        return properties


    def visualize_emergent_space(self, evolution_steps: int = 10000, output_html_file: str = "emergent_universe_spatial_view.html"):
        """
        Evolves the universe and visualizes it in a 3D emergent space.
        Uses a force-directed layout, fixing the origin node at (0,0,0).
        
        Node Color: Emergent Age (normalized causal distance from origin d0)
        Node Size: Emergent Coherence (normalized local clustering coefficient)
        """
        print(f"🌌 Evolving universe for {evolution_steps} steps to generate complex structure...")
        self._evolve_universe_locally(evolution_steps)
        
        if not self.engine.all_distinctions or self.graph.number_of_nodes() < 2:
            print("Not enough distinctions or graph is too small to visualize effectively.")
            return

        print("✨ Calculating emergent properties (Age, Coherence, Usage)...")
        node_properties = self._calculate_emergent_properties()

        print("🔮 Generating force-directed 3D layout (this may take a moment for large graphs)...")
        # Fix the origin_id (d0) at the center (0,0,0)
        fixed_pos = {self.origin_id: [0, 0, 0]}
        
        # Use Fruchterman-Reingold for 3D layout
        # This simulates attractive/repulsive forces based on connections
        pos = nx.spring_layout(self.graph, dim=3, iterations=100, pos=fixed_pos, fixed=[self.origin_id])


        x_coords = []
        y_coords = []
        z_coords = []
        node_colors = [] # Based on Age
        node_sizes = []  # Based on Coherence
        node_texts = []  # Hover text
        
        # Collect data for plotting
        for node_id, props in node_properties.items():
            if node_id in pos:
                x_coords.append(pos[node_id][0])
                y_coords.append(pos[node_id][1])
                z_coords.append(pos[node_id][2])
                
                # Color by Age (GR)
                node_colors.append(props["age"]) 
                # Size by Coherence (QM)
                node_sizes.append(max(3, props["coherence"] * 30)) # Scale for visibility
                
                node_texts.append(f"ID: {node_id[:8]}<br>Age: {props['age']:.2f}<br>Coherence: {props['coherence']:.2f}<br>Usage: {props['usage']:.2f}")

        # Create edges for visualization
        edge_x = []
        edge_y = []
        edge_z = []
        for edge in self.graph.edges():
            id1, id2 = edge
            if id1 in pos and id2 in pos: # Ensure both nodes are in the layout
                edge_x.extend([pos[id1][0], pos[id2][0], None])
                edge_y.extend([pos[id1][1], pos[id2][1], None])
                edge_z.extend([pos[id1][2], pos[id2][2], None])

        # Plotly Trace for Edges
        edges_trace = go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(color='grey', width=0.5),
            hoverinfo='none',
            showlegend=False
        )

        # Plotly Trace for Nodes
        nodes_trace = go.Scatter3d(
            x=x_coords, y=y_coords, z=z_coords,
            mode='markers',
            marker=dict(
                symbol='circle',
                size=node_sizes,
                color=node_colors,
                colorscale='Plasma', # Good for showing gradients from origin (dark/purple) to outer (yellow)
                colorbar=dict(title='Emergent Age (GR)', thickness=20),
                line=dict(color='black', width=0),
                opacity=0.8
            ),
            text=node_texts,
            hoverinfo='text',
            showlegend=False
        )

        # Create the figure
        fig = go.Figure(data=[edges_trace, nodes_trace])

        # Customize layout
        fig.update_layout(
            title=f"Emergent Universe: Spatial View (Nodes: {len(node_properties)})",
            scene=dict(
                xaxis_title="Emergent X (Arbitrary)",
                yaxis_title="Emergent Y (Arbitrary)",
                zaxis_title="Emergent Z (Arbitrary)",
                bgcolor='black',
                xaxis=dict(showgrid=False, zeroline=False), # No grid to emphasize emergent space
                yaxis=dict(showgrid=False, zeroline=False),
                zaxis=dict(showgrid=False, zeroline=False),
            ),
            margin=dict(l=0, r=0, b=0, t=40),
            hovermode='closest'
        )
        
        fig.write_html(output_html_file, auto_open=True)
        print(f"Visualization saved to {output_html_file} and opened in your browser.")
        print("💡 **Central Node (Origin d0)** is fixed at (0,0,0).")
        print("💡 **Node Color represents Emergent Age (GR)**: Darker (purple) = Older, Lighter (yellow) = Younger.")
        print("💡 **Node Size represents Emergent Coherence (QM)**: Larger = More Structured/Complex.")
        print("💡 The spatial layout emerges from the graph's internal connectivity.")


if __name__ == '__main__':
    engine = DistinctionEngine()
    visualizer = UniverseVisualizer(engine)
    visualizer.visualize_emergent_space(evolution_steps=10000)