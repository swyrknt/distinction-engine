"""
Universal Integration Test Suite

Tests the "Fundamental Integration Rule" (Small World Effect).
Validates that as the universe evolves, the internal topological distance
between distinct subprocesses decreases, creating a hyper-connected whole
despite the expansion of the causal horizon.

Falsification Target:
Topological Isolation - The distance between clusters increases or stays static,
proving that the universe is tearing apart rather than integrating.
"""

import unittest
import networkx as nx
import random
from engine import Distinction, DistinctionEngine

class TestUniversalIntegration(unittest.TestCase):

    def setUp(self):
        self.engine = DistinctionEngine()

    def _build_graph(self):
        state = self.engine.get_state_snapshot()
        g = nx.Graph()
        g.add_nodes_from([d.id for d in state[0]])
        g.add_edges_from(state[1])
        return g

    def _create_galaxy(self, center_node: Distinction, size=5):
        cluster = [center_node]
        for _ in range(size):
            a = random.choice(cluster)
            b = random.choice(cluster)
            new_d = self.engine.synthesize(a, b)
            cluster.append(new_d)
        return cluster[-1]

    def _evolve_vacuum(self, steps: int):
        """
        Evolves the universe with a bias towards High Usage nodes (The Void).
        """
        nodes = list(self.engine.all_distinctions.values())
        if not nodes: return
        
        # Calculate weights once for speed (simulating high-availability of Void)
        # In a real engine, this probability field is continuous.
        g = self._build_graph()
        degrees = dict(g.degree())
        weights = [degrees.get(d.id, 0) + 1 for d in nodes]
        
        for _ in range(steps):
            parents = random.choices(nodes, weights=weights, k=2)
            self.engine.synthesize(parents[0], parents[1])

    def test_falsify_topological_isolation(self):
        """
        Falsification Test: Topological Isolation

        Hypothesis: The "Fundamental Integration Rule" (Void Synthesis) creates
        shortcuts (wormholes) that shrink the effective distance between
        all subprocesses, even as the universe ages.

        Falsifies if: Distance increases (Expansion) or stays static.
        """
        print("\nTest: Universal Integration / Small World Falsification")

        # 1. Create Substrate
        print("   Creating primordial substrate...")
        for _ in range(100):
            a = random.choice(list(self.engine.all_distinctions.values()))
            b = random.choice(list(self.engine.all_distinctions.values()))
            self.engine.synthesize(a, b)

        # 2. Create Galaxies
        print("   Nucleating Matter clusters...")
        seeds = list(self.engine.all_distinctions.values())
        galaxy_A = self._create_galaxy(seeds[0])
        galaxy_B = self._create_galaxy(seeds[-1])

        # 3. Measure Initial Distance
        g_0 = self._build_graph()
        try:
            dist_0 = nx.shortest_path_length(g_0, galaxy_A.id, galaxy_B.id)
        except nx.NetworkXNoPath:
            self.fail("Galaxies disconnected.")
            
        print(f"   Initial Separation: {dist_0} hops")

        # 4. Run the "Integration" (Void Synthesis)
        print("   Running Void Integration (2000 steps)...")
        self._evolve_vacuum(steps=2000)

        # 5. Measure Final Distance
        g_1 = self._build_graph()
        dist_1 = nx.shortest_path_length(g_1, galaxy_A.id, galaxy_B.id)
        
        print(f"   Final Separation:   {dist_1} hops")
        
        # 6. The Verdict
        delta = dist_1 - dist_0
        print(f"   Integration Effect: {delta:+} hops")

        # WE EXPECT SHRINKING (Negative Delta)
        self.assertLess(delta, 0, 
            f"FALSIFIED: The universe is drifting apart. Delta: {delta}")

        print("\n   Hypothesis sustained.")
        print("   The universe is fundamentally integrating (Distance shrank).")

if __name__ == '__main__':
    unittest.main()