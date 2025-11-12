"""
Emergent Forces Test Suite

Tests whether interactions between distinct subprocesses produce
measurable changes in topological distance, indicating non-trivial
interaction dynamics between structural entities.

Falsification Target:
Interaction neutrality - cross-subprocess synthesis produces no change
in topological distance between subprocess centers, proving interactions
lack directional dynamics.
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestEmergentForces(unittest.TestCase):

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

    def _get_subprocess_coherence(self, g: nx.Graph, subprocess_nodes: Set[str]) -> float:
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

    def test_falsify_emergent_forces(self):
        """
        Falsification Test: Interaction Neutrality

        Hypothesis: Cross-subprocess synthesis produces measurable change
        in topological distance between subprocess centers, indicating
        directional interaction dynamics (attractive or repulsive forces).

        Falsifies if: Interaction produces no distance change, proving
        cross-subprocess synthesis lacks directional dynamics.

        Measurement:
        - Shortest path distance between subprocess centers before and after interaction
        """
        print("\nTest: Emergent Forces Falsification")

        print("   Executing 5000 synthesis operations...")
        self._evolve_universe_locally(steps=5000)

        state_0 = self.engine.get_state_snapshot()
        g_0 = self._build_graph_from_snapshot(state_0)

        if g_0.number_of_nodes() < 200:
            self.fail("Graph too small to test.")

        all_distinctions = list(state_0[0])
        sample_nodes = random.sample(all_distinctions, 2)

        subprocess_A_nodes = self._get_local_subprocess(g_0, sample_nodes[0].id)
        subprocess_B_nodes = self._get_local_subprocess(g_0, sample_nodes[1].id)

        while not subprocess_A_nodes.isdisjoint(subprocess_B_nodes):
            sample_nodes = random.sample(all_distinctions, 2)
            subprocess_A_nodes = self._get_local_subprocess(g_0, sample_nodes[0].id)
            subprocess_B_nodes = self._get_local_subprocess(g_0, sample_nodes[1].id)

        print(f"   Found two distinct subprocesses (A: {len(subprocess_A_nodes)} nodes, B: {len(subprocess_B_nodes)} nodes).")

        try:
            distance_0 = nx.shortest_path_length(g_0, source=sample_nodes[0].id, target=sample_nodes[1].id)
        except nx.NetworkXNoPath:
            self.fail("Could not run test: Subprocesses are in disconnected graph components.")

        print(f"   Executing cross-subprocess synthesis (100 steps)...")
        state_1 = self._evolve_subprocess_A_with_B(state_0, subprocess_A_nodes, subprocess_B_nodes, steps=100)

        g_1 = self._build_graph_from_snapshot(state_1)

        try:
            distance_1 = nx.shortest_path_length(g_1, source=sample_nodes[0].id, target=sample_nodes[1].id)
        except nx.NetworkXNoPath:
            distance_1 = distance_0 + 100
        except nx.NodeNotFound:
            self.fail("Test logic error: Original nodes were removed.")

        delta_distance = distance_1 - distance_0

        print(f"\n   Results:")
        print(f"   Initial distance: {distance_0} steps")
        print(f"   Final distance: {distance_1} steps")
        print(f"   Distance change: {delta_distance:+.0f} steps")

        self.assertNotEqual(delta_distance, 0,
                         "FALSIFIED: Interaction produced no distance change. No directional dynamic detected.")

        print(f"\n   Hypothesis sustained.")
        if delta_distance < 0:
            print(f"   Attractive dynamic detected (distance decreased by {abs(delta_distance)}).")
        else:
            print(f"   Repulsive dynamic detected (distance increased by {delta_distance}).")

if __name__ == '__main__':
    unittest.main()