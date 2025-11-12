"""
Emergent Geometry Test Suite

Tests whether the synthesis process generates stable, low-dimensional
geometric structure by measuring fractal (Hausdorff) dimension of the
resulting graph.

Falsification Targets:
1. Dimensional instability - fractal dimension exhibits high variance
2. Trivial dimensionality - structure is essentially 1-dimensional
3. High dimensionality - structure lacks geometric coherence (hairball)
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestEmergentGeometry(unittest.TestCase):

    def setUp(self):
        """Initialize a fresh engine instance for each test."""
        self.engine = DistinctionEngine()

    def _build_graph_from_snapshot(self, state: Tuple[Set[Distinction], Set[Tuple[str, str]]]) -> nx.Graph:
        """Convert engine state snapshot to NetworkX graph for analysis."""
        distinctions, relationships = state
        g = nx.Graph()
        g.add_nodes_from([d.id for d in distinctions])
        g.add_edges_from(relationships)
        return g

    def _evolve_universe(self, steps: int):
        """
        Execute synthesis operations with local selection bias.

        Randomly selects pairs of distinctions for synthesis, with preference
        for topologically proximate pairs (within 2-hop neighborhoods).
        Builds the computational substrate through iterated local operations.
        """
        current_distinctions = list(self.engine.all_distinctions.values())
        if len(current_distinctions) < 2:
            return

        distinction_map = {d.id: d for d in current_distinctions}

        for i in range(steps):
            state = self.engine.get_state_snapshot()
            g = self._build_graph_from_snapshot(state)
            
            if len(current_distinctions) < 2:
                break
                
            a = random.choice(current_distinctions)
            b = None

            try:
                neighborhood_ids = set(g.neighbors(a.id))
                for neighbor_id in list(neighborhood_ids):
                    neighborhood_ids.update(g.neighbors(neighbor_id))
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

    def _get_emergent_dimensionality(self, g: nx.Graph, samples=30, max_radius=5) -> Tuple[float, float]:
        """
        Estimate fractal (Hausdorff) dimension via volume-radius scaling.

        Measures how neighborhood volume scales with radius. Returns mean
        dimension and standard deviation across sampled nodes.
        """
        if g.number_of_nodes() < samples * max_radius:
            return 0.0, 0.0

        dimensions = []
        node_list = list(g.nodes())
        
        for _ in range(samples):
            try:
                sample_node = random.choice(node_list)
                paths = nx.single_source_shortest_path_length(g, sample_node, cutoff=max_radius)
                
                radii = []
                volumes = []
                current_volume = 0
                
                for r in range(1, max_radius + 1):
                    nodes_at_this_radius = [node for node, dist in paths.items() if dist == r]
                    current_volume += len(nodes_at_this_radius)
                    
                    if current_volume > 0:
                        radii.append(r)
                        volumes.append(current_volume)
                
                if len(radii) < 2:
                    continue

                log_r = np.log(radii)
                log_v = np.log(volumes)
                
                slope, _ = np.polyfit(log_r, log_v, 1)
                
                dimensions.append(slope)
                
            except (nx.NetworkXNoPath, Exception):
                continue
        
        if not dimensions:
            return 0.0, 0.0
            
        return np.mean(dimensions), np.std(dimensions)

    def test_falsify_emergent_dimensionality(self):
        """
        Falsification Test: Emergent Geometry

        Hypothesis: The synthesis process generates stable, low-dimensional
        geometric structure with fractal dimension between 1.5 and 8.0.

        Falsifies if:
        - Dimension exhibits high variance (instability)
        - Dimension is trivial (≤ 1.5, essentially linear)
        - Dimension is too high (≥ 8.0, lacks geometric coherence)

        Measurement:
        - Fractal dimension via volume-radius scaling across sampled nodes
        """
        print("\nTest: Emergent Dimensionality Falsification")

        print("   Executing 5000 synthesis operations...")
        self._evolve_universe(steps=5000)

        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)

        self.assertGreater(g.number_of_nodes(), 500, "Evolution failed to produce enough distinctions.")

        print("   Measuring fractal dimension...")
        avg_dim, std_dev_dim = self._get_emergent_dimensionality(g)

        print(f"\n   Results:")
        print(f"   Average dimension: {avg_dim:.3f}")
        print(f"   Standard deviation: {std_dev_dim:.3f}")

        self.assertLess(std_dev_dim, 1.0,
                         "FALSIFIED: Dimensionality is unstable (high variance).")

        self.assertGreater(avg_dim, 1.5,
                         "FALSIFIED: Dimensionality is trivial (≤ 1.5).")

        self.assertLess(avg_dim, 8.0,
                         "FALSIFIED: Dimensionality is too high (≥ 8.0).")

        print("\n   Hypothesis sustained.")
        print("   Stable, low-dimensional geometric structure detected.")

if __name__ == '__main__':
    unittest.main()
