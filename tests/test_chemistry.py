"""
Emergent Chemistry Test Suite

Tests whether the synthesis process generates cyclic structures,
specifically triangles (3-cycles), which represent the minimal
bound states necessary for complex structure formation.

Falsification Target:
Acyclicity - the system produces only tree-like structures without
any closed cycles, preventing the emergence of atomic bound states.
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestEmergentChemistry(unittest.TestCase):

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
        for immediate neighbors (1-hop neighborhoods). Builds the computational
        substrate through iterated local operations.
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
                # Use 1-hop neighborhood for tight local selection
                neighborhood_ids = set(g.neighbors(a.id))
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

    def test_falsify_atomic_emergence(self):
        """
        Falsification Test: Acyclicity

        Hypothesis: The synthesis process generates triangles (3-cycles),
        which represent minimal bound states necessary for complex structure.

        Falsifies if: The graph remains acyclic (tree-like) with no triangles,
        proving the process cannot create bound states.

        Measurement:
        - Triangle count via NetworkX triangles() function
        """
        print("\nTest: Atomic Emergence Falsification")

        print("   Executing 5000 synthesis operations...")
        self._evolve_universe_locally(steps=5000)

        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)

        self.assertGreater(g.number_of_nodes(), 500, "Evolution failed to produce enough distinctions.")

        print("   Counting triangles...")

        try:
            triangle_dict = nx.triangles(g)
            # Each triangle counted by all 3 nodes, divide by 3 for actual count
            total_triangles = sum(triangle_dict.values()) // 3
        except Exception as e:
            self.fail(f"Could not calculate triangles: {e}")

        print(f"\n   Results:")
        print(f"   Total triangles found: {total_triangles}")

        self.assertGreater(total_triangles, 0,
                         f"FALSIFIED: Graph is acyclic. No triangles formed.")

        print(f"\n   Hypothesis sustained.")
        print(f"   Triangles spontaneously emerge ({total_triangles} found).")
        print(f"   Minimal bound states present.")

if __name__ == '__main__':
    unittest.main()