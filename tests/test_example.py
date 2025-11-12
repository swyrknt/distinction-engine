"""
Example Test Suite Template

Template for writing new research tests. Tests whether the graph maintains
a single connected component during growth, indicating structural unity
rather than fragmentation.

Falsification Target:
Structural fragmentation - largest connected component drops below 90% of
total nodes, proving the system disintegrates under synthesis operations.
"""

import unittest
import networkx as nx
import random
from typing import Tuple, Set

from engine import Distinction, DistinctionEngine

class TestTemplate(unittest.TestCase):

    def setUp(self):
        """Initialize fresh engine instance for each test."""
        self.engine = DistinctionEngine()

    def _build_graph(self):
        """Convert engine state snapshot to NetworkX graph for analysis."""
        state = self.engine.get_state_snapshot()
        g = nx.Graph()
        g.add_nodes_from([d.id for d in state[0]])
        g.add_edges_from(state[1])
        return g

    def _evolve_substrate(self, steps: int):
        """
        Execute synthesis operations with random selection.

        Randomly selects pairs of distinctions for synthesis. Customize
        selection bias as needed for specific test requirements (e.g.,
        degree-weighted selection, spatial proximity).
        """
        current_distinctions = list(self.engine.all_distinctions.values())
        if len(current_distinctions) < 2:
            return

        for i in range(steps):
            a = random.choice(current_distinctions)
            b = random.choice(current_distinctions)

            c = self.engine.synthesize(a, b)

            if c not in current_distinctions:
                current_distinctions.append(c)

    def test_falsify_fragmentation(self):
        """
        Falsification Test: Structural Fragmentation

        Hypothesis: The graph maintains a single connected component as it
        grows through synthesis operations, indicating structural unity.

        Falsifies if: Largest connected component drops below 90% of total
        nodes, proving the system disintegrates.

        Measurement:
        - Execute random synthesis operations
        - Calculate largest connected component size using NetworkX
        - Compare ratio against threshold
        """
        print("\nTest: Structural Fragmentation Falsification")

        print("   Executing 1000 synthesis operations...")
        self._evolve_substrate(steps=1000)

        g = self._build_graph()
        total_nodes = g.number_of_nodes()

        if total_nodes < 100:
            self.fail("Graph too small to test.")

        print("   Measuring component sizes...")

        if nx.is_empty(g):
            largest_size = 0
        else:
            largest_component = max(nx.connected_components(g), key=len)
            largest_size = len(largest_component)

        ratio = largest_size / total_nodes

        print(f"\n   Results:")
        print(f"   Total nodes: {total_nodes}")
        print(f"   Largest component ratio: {ratio:.2%}")

        self.assertGreater(ratio, 0.90,
            f"FALSIFIED: Structural fragmentation observed ({ratio:.2%} connectivity).")

        print(f"\n   Hypothesis sustained.")
        print(f"   System maintains structural unity (connectivity > 90%).")

if __name__ == '__main__':
    unittest.main()