"""
Robustness and Resilience Test Suite

Tests structural integrity under node removal, validating scale-free network
behavior through differential vulnerability to random versus targeted attacks.

Falsification Target:
Uniform vulnerability - system exhibits equal fragility under random and
targeted hub removal, proving absence of scale-free topology.
"""

import unittest
import networkx as nx
import random
from engine import Distinction, DistinctionEngine

class TestRobustness(unittest.TestCase):

    def setUp(self):
        self.engine = DistinctionEngine()

    def _build_graph(self):
        """Convert engine state snapshot to NetworkX graph for analysis."""
        state = self.engine.get_state_snapshot()
        g = nx.Graph()
        g.add_nodes_from([d.id for d in state[0]])
        g.add_edges_from(state[1])
        return g

    def _evolve_scale_free(self, steps: int):
        """
        Execute synthesis operations with degree-biased selection.

        Preferentially selects high-degree nodes for synthesis to produce
        scale-free topology through preferential attachment.
        """
        for _ in range(steps):
            nodes = list(self.engine.all_distinctions.values())
            if len(nodes) < 2: continue

            g = self._build_graph()
            degrees = dict(g.degree())
            weights = [degrees.get(d.id, 0) + 1 for d in nodes]

            parents = random.choices(nodes, weights=weights, k=2)
            self.engine.synthesize(parents[0], parents[1])

    def test_falsify_uniform_vulnerability(self):
        """
        Falsification Test: Uniform Vulnerability

        Hypothesis: Scale-free topology exhibits differential vulnerability,
        with targeted hub removal causing greater fragmentation than random
        node removal.

        Falsifies if: Survival rates are similar under both attack strategies,
        proving uniform vulnerability structure.

        Measurement:
        - Build degree-biased graph through preferential attachment
        - Compare largest component survival under random vs targeted removal
        - Measure vulnerability gap between strategies
        """
        print("\nTest: Uniform Vulnerability Falsification")

        print("   Executing 3000 synthesis operations...")
        self._evolve_scale_free(3000)

        original_graph = self._build_graph()
        if not nx.is_connected(original_graph):
            largest = max(nx.connected_components(original_graph), key=len)
            original_graph = original_graph.subgraph(largest).copy()

        initial_size = original_graph.number_of_nodes()
        print(f"   Graph size: {initial_size} nodes")

        attack_percent = 0.20
        num_to_remove = int(initial_size * attack_percent)

        g_random = original_graph.copy()
        nodes_to_remove = random.sample(list(g_random.nodes()), num_to_remove)
        g_random.remove_nodes_from(nodes_to_remove)

        if nx.is_empty(g_random):
            largest_random = 0
        else:
            largest_random = len(max(nx.connected_components(g_random), key=len))

        survival_random = largest_random / initial_size
        print(f"   Survival after random removal ({attack_percent:.0%}): {survival_random:.2%}")

        g_target = original_graph.copy()
        degrees = sorted(g_target.degree, key=lambda x: x[1], reverse=True)

        hubs_to_remove = [n for n, d in degrees[:num_to_remove]]
        g_target.remove_nodes_from(hubs_to_remove)

        if nx.is_empty(g_target):
            largest_target = 0
        else:
            largest_target = len(max(nx.connected_components(g_target), key=len))

        survival_target = largest_target / initial_size
        print(f"   Survival after targeted hub removal ({attack_percent:.0%}): {survival_target:.2%}")

        diff = survival_random - survival_target
        print(f"   Vulnerability gap: {diff:.2f}")

        self.assertGreater(diff, 0.20,
            f"FALSIFIED: Uniform vulnerability observed (gap: {diff:.2f}).")

        print(f"\n   Hypothesis sustained.")
        print(f"   Hub-dependent topology exhibits differential vulnerability.")

if __name__ == '__main__':
    unittest.main()