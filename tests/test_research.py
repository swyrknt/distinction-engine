"""
Foundational Research Test Suite

Tests emergent properties of the distinction graph including self-organization,
complexity, and correlations between internal structure (coherence) and
external position (causal distance from origin).

Measurements use entirely emergent properties:
- Coherence: clustering coefficient
- Usage: normalized degree
- Age: shortest path distance from primordial node d0
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestFoundationalResearch(unittest.TestCase):

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

    def test_falsify_spontaneous_organization(self):
        """
        Test: Self-Organization

        Validates that average clustering coefficient exceeds minimal threshold,
        indicating spontaneous structural organization.
        """
        print("\nTest: Self-Organization")
        self._evolve_universe(steps=2000)

        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)

        self.assertGreater(g.number_of_nodes(), 100, "Evolution failed to produce enough distinctions.")

        emergent_coherence = nx.average_clustering(g)
        print(f"   Average clustering coefficient: {emergent_coherence:.6f}")

        self.assertGreater(emergent_coherence, 0.001,
                         "FALSIFIED: System did not self-organize.")
        print("   Hypothesis sustained: Spontaneous self-organization detected.")

    def test_falsify_emergent_complexity(self):
        """
        Test: Emergent Complexity

        Validates that degree distribution exhibits high variance relative to mean,
        indicating fat-tailed complexity rather than uniform structure.
        """
        print("\nTest: Emergent Complexity")
        self._evolve_universe(steps=3000)
        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)
        self.assertGreater(g.number_of_nodes(), 150)

        degrees = [d for n, d in g.degree()]
        if not degrees:
            self.fail("Could not measure degrees; graph is empty.")

        mean_degree = np.mean(degrees)
        std_dev_degree = np.std(degrees)
        print(f"   Degree distribution: mean={mean_degree:.2f}, std_dev={std_dev_degree:.2f}")

        self.assertGreater(std_dev_degree, mean_degree * 0.5,
                         "FALSIFIED: System lacks complexity.")
        print("   Hypothesis sustained: Fat-tailed complexity detected.")

    def _get_emergent_age(self, g: nx.Graph, node_id: str, origin_id: str) -> int:
        """
        Calculate causal distance from origin.

        Returns shortest path length from primordial node d0, or 0 if unreachable.
        """
        try:
            return nx.shortest_path_length(g, source=origin_id, target=node_id)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return 0

    def _get_emergent_state_vector(self, g: nx.Graph, d: Distinction, metrics: Dict) -> np.ndarray:
        """
        Calculate emergent state vector for a distinction.

        Returns [coherence, normalized_usage, normalized_age] where:
        - coherence: clustering coefficient
        - usage: degree / max_degree
        - age: path_from_origin / max_path_from_origin
        """
        if d is None or d.id not in g:
            return np.array([0, 0, 0])

        coherence = nx.clustering(g, d.id)
        usage = g.degree(d.id) / metrics["max_degree"] if metrics["max_degree"] > 0 else 0
        age = self._get_emergent_age(g, d.id, metrics["origin_id"]) / metrics["max_age"] if metrics["max_age"] > 0 else 0

        vector = np.array([coherence, usage, age])
        return vector

    def test_correlation_of_content_and_container(self):
        """
        Test: Content-Container Correlation

        Validates that internal node structure (coherence) correlates with
        external node position (causal distance from origin), indicating
        systemic coupling between local and global properties.

        Measurement:
        - Pearson correlation between clustering coefficient and age across all nodes
        """
        print("\nTest: Content-Container Correlation")

        print("   Executing 2000 synthesis operations...")
        self._evolve_universe(steps=2000)

        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)
        all_distinctions = list(state[0])

        if len(all_distinctions) < 100:
            self.fail("Universe too small to test.")

        print("   Calculating emergent properties...")
        all_degrees = dict(g.degree())
        all_coherences = nx.clustering(g)
        origin_id = self.engine.d0.id

        all_ages = {}
        max_age = 0
        for d in all_distinctions:
            age = self._get_emergent_age(g, d.id, origin_id)
            all_ages[d.id] = age
            if age > max_age:
                max_age = age

        max_degree = max(all_degrees.values()) if all_degrees else 1

        if max_age == 0:
            self.fail("Universe has no age (graph is disconnected).")

        coherence_list = []
        age_list = []

        for d in all_distinctions:
            if d.id == origin_id: continue
            coherence_list.append(all_coherences[d.id])
            age_list.append(all_ages[d.id])

        if not coherence_list:
             self.fail("Could not measure any properties.")

        correlation_matrix = np.corrcoef(coherence_list, age_list)
        correlation = correlation_matrix[0, 1]

        print(f"\n   Results:")
        print(f"   Coherence-Age correlation: {correlation:.4f}")

        self.assertGreater(abs(correlation), 0.1,
                         "FALSIFIED: Internal state not correlated with external position.")

        print(f"\n   Hypothesis sustained.")
        print(f"   Content (coherence) correlates with container (age).")

if __name__ == '__main__':
    unittest.main()