"""
Emergent Biology Test Suite

Tests whether the distinction graph exhibits structural diversity necessary
for life-like computation. Specifically validates that both chain-like
structures (information storage) and clump-like structures (catalytic action)
emerge from the synthesis process.

Falsification Target:
Structural sterility - the system produces only one type of topological
structure, preventing the emergence of genome-like computational substrates.
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestEmergentBiology(unittest.TestCase):

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

    def _evolve_universe_locally(self, steps: int):
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

    def test_falsify_structural_sterility(self):
        """
        Falsification Test: Structural Sterility

        Hypothesis: The synthesis process generates topologically diverse
        structures including both high-clustering regions (catalytic sites)
        and extended path structures (information chains).

        Falsifies if: The graph exhibits only one structural motif (all gas,
        all clump, or all chain), preventing genome-like computation.

        Measurements:
        - Average clustering coefficient (clumpiness)
        - Average shortest path length (chain-like extent)
        """
        print("\nTest: Structural Sterility Falsification")

        print("   Executing 5000 synthesis operations...")
        self._evolve_universe_locally(steps=5000)

        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)

        if not nx.is_connected(g):
            largest_cc_nodes = max(nx.connected_components(g), key=len)
            g = g.subgraph(largest_cc_nodes)
            print("   Graph disconnected. Analyzing largest connected component.")

        if g.number_of_nodes() < 500:
            self.fail("Evolution failed to produce a large enough connected universe.")

        print("   Measuring topological properties...")

        # Average clustering coefficient measures local density (clumpiness)
        emergent_coherence = nx.average_clustering(g)

        # Average shortest path length measures topological extent (chain-like structure)
        avg_path_length = nx.average_shortest_path_length(g)

        print(f"\n   Results:")
        print(f"   Average Clustering Coefficient: {emergent_coherence:.4f}")
        print(f"   Average Shortest Path Length: {avg_path_length:.4f}")

        # Verify presence of clump-like structures (catalytic sites)
        self.assertGreater(emergent_coherence, 0.01,
                         f"FALSIFIED: Insufficient clustering (coherence: {emergent_coherence:.4f})."
                         " Graph lacks clump-like structures necessary for catalytic action.")

        # Verify presence of chain-like structures (information storage)
        self.assertGreater(avg_path_length, 3.0,
                         f"FALSIFIED: Insufficient path length ({avg_path_length:.4f})."
                         " Graph lacks chain-like structures necessary for information storage.")

        print(f"\n   Hypothesis sustained.")
        print(f"   Graph exhibits both clustering (coherence > 0.01) and extended paths (length > 3.0).")
        print(f"   Structural diversity sufficient for genome-like computation.")

if __name__ == '__main__':
    unittest.main()