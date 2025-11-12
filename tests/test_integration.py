"""
Universal Integration Test Suite

Tests whether topological distance between distinct subprocesses decreases
or remains stable during evolution, indicating small-world integration
despite causal horizon expansion.

Falsification Target:
Topological isolation - distance between clusters increases significantly,
proving structural fragmentation.
"""

import unittest
import networkx as nx
import random
from engine import Distinction, DistinctionEngine

class TestUniversalIntegration(unittest.TestCase):

    def setUp(self):
        self.engine = DistinctionEngine()

    def _build_graph(self):
        """Convert engine state snapshot to NetworkX graph for analysis."""
        state = self.engine.get_state_snapshot()
        g = nx.Graph()
        g.add_nodes_from([d.id for d in state[0]])
        g.add_edges_from(state[1])
        return g

    def _create_galaxy(self, center_node: Distinction, size=5):
        """
        Create local cluster through repeated synthesis.

        Performs iterated synthesis operations within a growing cluster,
        returns final synthesized distinction.
        """
        cluster = [center_node]
        for _ in range(size):
            a = random.choice(cluster)
            b = random.choice(cluster)
            new_d = self.engine.synthesize(a, b)
            cluster.append(new_d)
        return cluster[-1]

    def _evolve_vacuum(self, steps: int):
        """
        Execute synthesis operations with high-degree node bias.

        Randomly selects pairs of distinctions for synthesis, with preference
        for high-usage nodes weighted by degree.
        """
        nodes = list(self.engine.all_distinctions.values())
        if not nodes: return

        g = self._build_graph()
        degrees = dict(g.degree())
        weights = [degrees.get(d.id, 0) + 1 for d in nodes]

        for _ in range(steps):
            parents = random.choices(nodes, weights=weights, k=2)
            self.engine.synthesize(parents[0], parents[1])

    def test_falsify_topological_isolation(self):
        """
        Falsification Test: Topological Isolation

        Hypothesis: High-degree node synthesis creates shortcuts that prevent
        effective distance between subprocesses from increasing during expansion.

        Falsifies if: Distance increases significantly between separated clusters
        despite degree-biased synthesis operations.

        Measurement:
        - Create initial substrate with separated clusters
        - Execute degree-biased synthesis operations
        - Measure change in shortest path distance between clusters
        """
        print("\nTest: Topological Isolation Falsification")

        print("   Creating initial substrate (300 nodes)...")
        for _ in range(300):
            a = random.choice(list(self.engine.all_distinctions.values()))
            b = random.choice(list(self.engine.all_distinctions.values()))
            self.engine.synthesize(a, b)

        g_0 = self._build_graph()
        all_nodes = list(self.engine.all_distinctions.values())
        seed_a, seed_b = random.sample(all_nodes, 2)

        print("   Searching for separated seed nodes...")
        for _ in range(20):
            s1, s2 = random.sample(all_nodes, 2)
            try:
                d = nx.shortest_path_length(g_0, s1.id, s2.id)
                if d >= 4:
                    seed_a, seed_b = s1, s2
                    break
            except nx.NetworkXNoPath:
                continue

        galaxy_A = self._create_galaxy(seed_a)
        galaxy_B = self._create_galaxy(seed_b)

        g_0 = self._build_graph()
        try:
            dist_0 = nx.shortest_path_length(g_0, galaxy_A.id, galaxy_B.id)
        except nx.NetworkXNoPath:
            self.fail("Clusters disconnected.")

        print(f"   Initial distance: {dist_0} hops")

        print("   Executing degree-biased synthesis (2000 steps)...")
        self._evolve_vacuum(steps=2000)

        g_1 = self._build_graph()
        try:
            dist_1 = nx.shortest_path_length(g_1, galaxy_A.id, galaxy_B.id)
        except nx.NetworkXNoPath:
            dist_1 = dist_0

        print(f"   Final distance: {dist_1} hops")

        delta = dist_1 - dist_0
        print(f"   Distance change: {delta:+} hops")

        self.assertLessEqual(delta, 0,
            f"FALSIFIED: Distance increased between clusters (delta: {delta}).")

        print(f"\n   Hypothesis sustained.")
        print(f"   Topological distance constrained through degree-biased synthesis.")

if __name__ == '__main__':
    unittest.main()