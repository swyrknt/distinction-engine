"""
Information Dynamics Test Suite

Tests whether spatially separated subprocesses exhibit correlated
temporal evolution, indicating systemic information coupling across
the distinction graph.

Falsification Target:
Information independence - subprocess coherence time series show
zero correlation, proving subprocesses evolve independently without
systemic coupling.
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestInformationDynamics(unittest.TestCase):

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

    def _evolve_universe_locally(self, steps: int) -> List[Distinction]:
        """
        Execute synthesis operations with local selection bias.

        Randomly selects pairs of distinctions for synthesis, with preference
        for topologically proximate pairs (within 2-hop neighborhoods).
        Returns final list of all distinctions.
        """
        current_distinctions = list(self.engine.all_distinctions.values())
        if len(current_distinctions) < 2:
            return current_distinctions

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

        return list(self.engine.all_distinctions.values())

    def _get_local_subprocess(self, g: nx.Graph, start_node_id: str, radius=2) -> Set[str]:
        """Return node IDs within specified radius of start node."""
        return set(nx.ego_graph(g, start_node_id, radius=radius).nodes())

    def _measure_subprocess_coherence(self, g: nx.Graph, subprocess_nodes: Set[str]) -> float:
        """
        Calculate average clustering coefficient for a set of nodes.

        Returns mean coherence value across subprocess, or 0.0 if empty.
        """
        if not subprocess_nodes:
            return 0.0

        all_coherence_levels = nx.clustering(g)
        
        subprocess_coherence = [all_coherence_levels.get(node_id, 0) 
                                for node_id in subprocess_nodes]
                                
        if not subprocess_coherence:
            return 0.0
            
        return np.mean(subprocess_coherence)

    def test_falsify_information_independence(self):
        """
        Falsification Test: Information Independence

        Hypothesis: Spatially separated subprocesses exhibit correlated
        temporal evolution of their coherence values, indicating systemic
        information coupling.

        Falsifies if: Subprocess coherence time series show near-zero
        Pearson correlation, proving independent evolution.

        Measurement:
        - Time series of average clustering coefficient for two disjoint subprocesses
        - Pearson correlation between time series
        """
        print("\nTest: Information Independence Falsification")

        print("   Executing 3000 synthesis operations to create substrate...")
        all_distinctions = self._evolve_universe_locally(steps=3000)

        state_0 = self.engine.get_state_snapshot()
        g_0 = self._build_graph_from_snapshot(state_0)

        if len(all_distinctions) < 100:
            self.fail("Graph too small to test.")

        sample_nodes = random.sample(all_distinctions, 2)
        subprocess_A_nodes = self._get_local_subprocess(g_0, sample_nodes[0].id)
        subprocess_B_nodes = self._get_local_subprocess(g_0, sample_nodes[1].id)

        while not subprocess_A_nodes.isdisjoint(subprocess_B_nodes):
            sample_nodes = random.sample(all_distinctions, 2)
            subprocess_A_nodes = self._get_local_subprocess(g_0, sample_nodes[0].id)
            subprocess_B_nodes = self._get_local_subprocess(g_0, sample_nodes[1].id)

        print(f"   Found two disjoint subprocesses (A: {len(subprocess_A_nodes)} nodes, B: {len(subprocess_B_nodes)} nodes).")

        time_series_A = []
        time_series_B = []

        observation_steps = 1000

        print(f"   Observing temporal dynamics for {observation_steps} steps...")

        for _ in range(observation_steps):
            self._evolve_universe_locally(steps=1)

            state_t = self.engine.get_state_snapshot()
            g_t = self._build_graph_from_snapshot(state_t)

            current_A_nodes = self._get_local_subprocess(g_t, sample_nodes[0].id)
            current_B_nodes = self._get_local_subprocess(g_t, sample_nodes[1].id)

            state_A = self._measure_subprocess_coherence(g_t, current_A_nodes)
            state_B = self._measure_subprocess_coherence(g_t, current_B_nodes)

            time_series_A.append(state_A)
            time_series_B.append(state_B)

        correlation_matrix = np.corrcoef(time_series_A, time_series_B)
        correlation = correlation_matrix[0, 1]

        print(f"\n   Results:")
        print(f"   Temporal correlation: {correlation:.4f}")

        self.assertGreater(abs(correlation), 0.05,
                         f"FALSIFIED: Subprocesses are statistically independent (correlation={correlation:.4f}).")

        print(f"\n   Hypothesis sustained.")
        print(f"   Systemic correlation detected between spatially separated subprocesses.")

if __name__ == '__main__':
    unittest.main()