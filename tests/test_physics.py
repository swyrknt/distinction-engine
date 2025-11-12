"""
Emergent Physics Test Suite

Tests whether interaction dynamics (forces) correlate with initial
structural states of interacting subprocesses, specifically their
coherence (local integration) and age (causal distance from origin).

Falsification Target:
Force randomness - interaction outcomes show no correlation with
initial subprocess states, proving forces are non-deterministic
functions of structure.
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestEmergentPhysics(unittest.TestCase):

    def setUp(self):
        """Initialize a fresh engine instance for each test."""
        self.engine = DistinctionEngine()
        self.origin_id = self.engine.d0.id

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

    def _get_local_subprocess(self, g: nx.Graph, start_node_id: str, radius=2) -> Set[str]:
        """Return node IDs within specified radius of start node."""
        return set(nx.ego_graph(g, start_node_id, radius=radius).nodes())

    def _get_emergent_state(self, g: nx.Graph, node_id: str) -> Dict[str, float]:
        """
        Measure structural state of a node.

        Returns coherence (clustering coefficient) and age (shortest path
        distance from primordial node d0).
        """
        coherence = nx.clustering(g, node_id)

        try:
            age = nx.shortest_path_length(g, source=self.origin_id, target=node_id)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            age = 0
            
        return {"qm_coherence": coherence, "gr_age": float(age)}


    def _evolve_subprocess_A_with_B(self, engine_state: Tuple[Set[Distinction], Set[Tuple[str, str]]],
                                     subprocess_A_nodes: Set[str],
                                     subprocess_B_nodes: Set[str],
                                     steps: int) -> Tuple[Set[Distinction], Set[Tuple[str, str]]]:
        """
        Execute cross-subprocess synthesis operations.

        Creates engine clone and synthesizes pairs where one member is from
        subprocess A and the other from subprocess B. Measures interaction
        dynamics between distinct structural regions.
        """
        temp_engine = DistinctionEngine()
        distinctions, relationships = engine_state
        temp_engine.all_distinctions = {d.id: d for d in distinctions}
        temp_engine.relationships = relationships.copy()

        distinctions_A = [d for d in temp_engine.all_distinctions.values()
                          if d.id in subprocess_A_nodes]
        distinctions_B = [d for d in temp_engine.all_distinctions.values()
                          if d.id in subprocess_B_nodes]

        if not distinctions_A or not distinctions_B:
            return temp_engine.get_state_snapshot()

        for _ in range(steps):
            a = random.choice(distinctions_A)
            b = random.choice(distinctions_B)
            c = temp_engine.synthesize(a, b)

        return temp_engine.get_state_snapshot()

    def test_falsify_force_correlation(self):
        """
        Falsification Test: Force Randomness

        Hypothesis: Interaction dynamics (distance change) correlate with
        initial structural states (coherence and age) of interacting
        subprocesses, proving forces are deterministic functions of structure.

        Falsifies if: Distance changes show no correlation with initial
        states, proving forces are random.

        Measurement:
        - Sample 100 subprocess pair interactions
        - Correlate initial state (coherence + age) with resulting force (distance change)
        """
        print("\nTest: Force Correlation Falsification")

        print("   Executing 5000 synthesis operations...")
        self._evolve_universe_locally(steps=5000)

        state_0 = self.engine.get_state_snapshot()
        g_0 = self._build_graph_from_snapshot(state_0)
        all_distinctions = list(state_0[0])

        if g_0.number_of_nodes() < 200:
            self.fail("Graph too small to test.")

        print("   Sampling subprocess interaction dynamics...")

        initial_states = []
        resulting_forces = []

        sample_size = 100

        print(f"   Testing {sample_size} interactions...")

        for _ in range(sample_size):
            try:
                node_A, node_B = random.sample(all_distinctions, 2)
                subprocess_A_nodes = self._get_local_subprocess(g_0, node_A.id)
                subprocess_B_nodes = self._get_local_subprocess(g_0, node_B.id)

                if not subprocess_A_nodes.isdisjoint(subprocess_B_nodes):
                    continue

                state_A = self._get_emergent_state(g_0, node_A.id)
                state_B = self._get_emergent_state(g_0, node_B.id)
                distance_0 = nx.shortest_path_length(g_0, source=node_A.id, target=node_B.id)

                initial_qm_state = state_A["qm_coherence"] + state_B["qm_coherence"]
                initial_gr_state = state_A["gr_age"] + state_B["gr_age"]
                initial_states.append((initial_qm_state, initial_gr_state))

                state_1 = self._evolve_subprocess_A_with_B(state_0, subprocess_A_nodes, subprocess_B_nodes, steps=50)

                g_1 = self._build_graph_from_snapshot(state_1)
                distance_1 = nx.shortest_path_length(g_1, source=node_A.id, target=node_B.id)

                delta_distance = distance_1 - distance_0
                resulting_forces.append(delta_distance)

            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue

        if len(resulting_forces) < 20:
            self.fail(f"Could not gather enough valid interaction data (only {len(resulting_forces)} samples).")

        print("   Sampling complete.")

        initial_qm_data = [s[0] for s in initial_states]
        initial_gr_data = [s[1] for s in initial_states]

        corr_qm_vs_force = np.corrcoef(initial_qm_data, resulting_forces)[0, 1]
        corr_gr_vs_force = np.corrcoef(initial_gr_data, resulting_forces)[0, 1]

        print(f"\n   Results:")
        print(f"   Coherence-Force correlation: {corr_qm_vs_force:.4f}")
        print(f"   Age-Force correlation: {corr_gr_vs_force:.4f}")

        total_correlation = abs(corr_qm_vs_force) + abs(corr_gr_vs_force)

        self.assertGreater(total_correlation, 0.1,
                         "FALSIFIED: Forces show no correlation with initial structural states.")

        print(f"\n   Hypothesis sustained.")
        print(f"   Forces correlate with initial subprocess structure (total correlation: {total_correlation:.4f}).")

if __name__ == '__main__':
    unittest.main()
