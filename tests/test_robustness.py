"""
Robustness & Resilience Test Suite

Tests the structural integrity of the universe under "attack."
Validates that the system exhibits "Scale-Free" behavior.
"""

import unittest
import networkx as nx
import random
from engine import Distinction, DistinctionEngine

class TestRobustness(unittest.TestCase):

    def setUp(self):
        self.engine = DistinctionEngine()

    def _build_graph(self):
        state = self.engine.get_state_snapshot()
        g = nx.Graph()
        g.add_nodes_from([d.id for d in state[0]])
        g.add_edges_from(state[1])
        return g

    def _evolve_scale_free(self, steps: int):
        for _ in range(steps):
            nodes = list(self.engine.all_distinctions.values())
            if len(nodes) < 2: continue
            
            g = self._build_graph()
            degrees = dict(g.degree())
            weights = [degrees.get(d.id, 0) + 1 for d in nodes]
            
            parents = random.choices(nodes, weights=weights, k=2)
            self.engine.synthesize(parents[0], parents[1])

    def test_falsify_uniform_vulnerability(self):
        print("\nTest: Robustness / Attack Tolerance Falsification")

        print("   Building mature universe (3000 steps)...")
        self._evolve_scale_free(3000)
        
        original_graph = self._build_graph()
        if not nx.is_connected(original_graph):
            largest = max(nx.connected_components(original_graph), key=len)
            original_graph = original_graph.subgraph(largest).copy()
            
        initial_size = original_graph.number_of_nodes()
        print(f"   Universe Size: {initial_size} nodes")

        # --- INCREASED ATTACK SEVERITY TO 20% ---
        attack_percent = 0.20
        num_to_remove = int(initial_size * attack_percent)

        # 2. SIMULATION A: Random Failure
        g_random = original_graph.copy()
        nodes_to_remove = random.sample(list(g_random.nodes()), num_to_remove)
        g_random.remove_nodes_from(nodes_to_remove)
        
        if nx.is_empty(g_random):
            largest_random = 0
        else:
            largest_random = len(max(nx.connected_components(g_random), key=len))
            
        survival_random = largest_random / initial_size
        print(f"   Survival after Random Attack ({attack_percent:.0%}):   {survival_random:.2%}")

        # 3. SIMULATION B: Targeted Attack (Attack the Void)
        g_target = original_graph.copy()
        degrees = sorted(g_target.degree, key=lambda x: x[1], reverse=True)
        
        # Remove the top 20% (Hubs)
        hubs_to_remove = [n for n, d in degrees[:num_to_remove]]
        g_target.remove_nodes_from(hubs_to_remove)

        if nx.is_empty(g_target):
            largest_target = 0
        else:
            largest_target = len(max(nx.connected_components(g_target), key=len))

        survival_target = largest_target / initial_size
        print(f"   Survival after Targeted Attack ({attack_percent:.0%}): {survival_target:.2%}")

        # 4. The Verdict
        diff = survival_random - survival_target
        print(f"   Vulnerability Gap: {diff:.2f}")
        
        self.assertGreater(diff, 0.20, 
            f"FALSIFIED: System is not dependent on Hubs. Diff: {diff:.2f}")

        print("\n   Hypothesis sustained.")
        print("   Targeted destruction of the Void shatters the universe.")

if __name__ == '__main__':
    unittest.main()