"""
Foundational (Research) Test for Emergent Geometry (v2)

This test suite attacks the "Spacetime" claim of the "timeless"
theory. It uses the "honest" local evolution model.

Emergent Claim Tested:
1.  Does the local process spontaneously create a stable,
    low-dimensional geometric structure (i.e., "Space")?
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
        """
        Create a fresh, clean "universe" (Engine) for each experiment.
        """
        self.engine = DistinctionEngine()

    # --- "MEASURING TOOLS" (HELPERS) ---

    def _build_graph_from_snapshot(self, state: Tuple[Set[Distinction], Set[Tuple[str, str]]]) -> nx.Graph:
        """
        Builds a NetworkX graph object from an immutable snapshot.
        """
        distinctions, relationships = state
        g = nx.Graph()
        g.add_nodes_from([d.id for d in distinctions])
        g.add_edges_from(relationships)
        return g

    # --- HONEST "LOCAL" EVOLUTION HELPER ---
    def _evolve_universe(self, steps: int):
        """
        Runs the "one process" locally.
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
    # --- END HONEST EVOLUTION HELPER ---

    def _get_emergent_dimensionality(self, g: nx.Graph, samples=30, max_radius=5) -> Tuple[float, float]:
        """
        THE "GEOMETRY RULER": Measures the fractal (Hausdorff) dimension
        of the graph by measuring how fast the "volume" of
        neighborhoods grows with their "radius".
        """
        if g.number_of_nodes() < samples * max_radius:
            return 0.0, 0.0 # Graph is too small to measure

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

    # --- FOUNDATIONAL TEST 4: EMERGENT GEOMETRY ---

    def test_falsify_emergent_dimensionality(self):
        """
        FALSIFICATION TEST 4: The Geometry Test
        
        Hypothesis: The simple, *local* axiomatic process will
        evolve into a stable, low-dimensional geometric structure.
        """
        print("\n🌌 ATTACKING SPACETIME: Does a stable dimension emerge?")
        
        # 1. Evolve the universe for a *long* time locally.
        print("   Evolving universe locally for 5000 steps...")
        self._evolve_universe(steps=5000)
        
        # 2. Get the final state
        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)
        
        self.assertGreater(g.number_of_nodes(), 500, "Evolution failed to produce enough distinctions.")

        # 3. The Measurement:
        print("   Measuring emergent fractal dimension...")
        avg_dim, std_dev_dim = self._get_emergent_dimensionality(g)
        
        print(f"\n   --- Emergent Geometry Test Results ---")
        print(f"   Average Dimension: {avg_dim:.3f}")
        print(f"   Dimension Stability (std dev): {std_dev_dim:.3f}")
        
        # 4. The Falsification:
        
        #   Falsification A: Is the dimension unstable?
        self.assertLess(std_dev_dim, 1.0,
                         "🚩 FALSIFIED: Dimensionality is unstable and fluctuates wildly.")

        #   Falsification B: Is the dimension trivial (just a 1D chain)?
        self.assertGreater(avg_dim, 1.5,
                         "🚩 FALSIFIED: Dimensionality is trivial (avg dim <= 1.5).")

        #   Falsification C: Is the dimension a "hairball" (not low-D)?
        self.assertLess(avg_dim, 8.0,
                         "🚩 FALSIFIED: Dimension is not 'low' (avg dim >= 8.0). It's a high-D 'hairball'.")
        
        print("\n   ✅ THEORY VALIDATED: A stable, non-trivial, low-dimensional")
        print("      geometric structure spontaneously emerged from the process.")

if __name__ == '__main__':
    unittest.main()
