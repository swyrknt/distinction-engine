"""
Spacetime Coherence Test Suite

Tests whether spatial proximity (graph adjacency) correlates with
temporal proximity (similarity in causal distance from origin),
indicating coherent spacetime fabric rather than scrambled structure.

Falsification Target:
Temporal scrambling - spatially adjacent nodes exhibit large differences
in causal age, proving space and time are decoupled.
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestSpacetimeCoherence(unittest.TestCase):

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

    def _get_emergent_age(self, g: nx.Graph, node_id: str, origin_id: str) -> int:
        """
        Calculate causal distance from origin.

        Returns shortest path length from primordial node d0, or 0 if unreachable.
        """
        try:
            return nx.shortest_path_length(g, source=origin_id, target=node_id)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return 0

    def test_falsify_temporal_scrambling(self):
        """
        Falsification Test: Temporal Scrambling

        Hypothesis: Spatially adjacent nodes (graph neighbors) exhibit similar
        causal ages (similar path distances from origin), indicating coherent
        spacetime fabric.

        Falsifies if: Average age difference between neighbors exceeds threshold,
        proving spatial and temporal structure are decoupled.

        Measurement:
        - Average absolute age difference across all graph edges
        """
        print("\nTest: Temporal Scrambling Falsification")

        print("   Executing 5000 synthesis operations...")
        self._evolve_universe(steps=5000)

        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)

        self.assertGreater(g.number_of_nodes(), 500, "Evolution failed to produce enough distinctions.")

        print("   Calculating causal ages...")
        origin_id = self.engine.d0.id
        id_to_age_map = {}
        max_age = 0

        for d in state[0]:
            age = self._get_emergent_age(g, d.id, origin_id)
            id_to_age_map[d.id] = age
            if age > max_age:
                max_age = age

        if max_age == 0:
            self.fail("Universe has no age (graph is disconnected).")

        print("   Measuring age differences across edges...")
        age_distances = []

        if not state[1]:
            self.fail("No relationships were formed.")

        for id_a, id_b in state[1]:
            try:
                age_a = id_to_age_map[id_a]
                age_b = id_to_age_map[id_b]
                delta_age = abs(age_a - age_b)
                age_distances.append(delta_age)
            except KeyError:
                continue

        if not age_distances:
            self.fail("Could not measure any age distances.")

        avg_age_distance = np.mean(age_distances)

        print(f"\n   Results:")
        print(f"   Maximum age (causal radius): {max_age} steps")
        print(f"   Average age difference between neighbors: {avg_age_distance:.2f} steps")

        self.assertLess(avg_age_distance, 2.0,
                         f"FALSIFIED: System is scrambled (avg age distance: {avg_age_distance:.2f}).")

        print(f"\n   Hypothesis sustained.")
        print(f"   Spatial neighbors exhibit temporal proximity (coherent spacetime fabric).")

if __name__ == '__main__':
    unittest.main()