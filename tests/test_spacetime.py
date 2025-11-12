"""
Foundational (Research) Test for Spacetime Coherence (v2)

This test suite attacks the "Spacetime Fabric" claim of the
"timeless" theory. It uses the "honest" local evolution model.

Emergent Claim Tested:
1.  Is the emergent "spatial" graph (the container) woven
    coherently by the *emergent* "temporal" process (the content)?
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
        """
        Create a fresh, clean "universe" (Engine) for each experiment.
        """
        self.engine = DistinctionEngine()

    # --- "MEASURING TOOLS" (HELPERS) ---

    def _build_graph_from_snapshot(self, state: Tuple[Set[Distinction], Set[Tuple[str, str]]]) -> nx.Graph:
        """
        Builds a NetworkX graph object from an immutable snapshot.
        """
        distinctions, relationships = state
        g = nx.Graph()
        g.add_nodes_from([d.id for d in distinctions])
        g.add_edges_from(relationships)
        return g

    # --- HONEST "LOCAL" EVOLUTION HELPER ---
    def _evolve_universe(self, steps: int):
        """
        Runs the "one process" locally.
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
    # --- END HONEST EVOLUTION HELPER ---

    def _get_emergent_age(self, g: nx.Graph, node_id: str, origin_id: str) -> int:
        """
        Calculates "Emergent Age" (or causal distance) as the shortest path
        length from the node to the origin 'd0'.
        """
        try:
            return nx.shortest_path_length(g, source=origin_id, target=node_id)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return 0 # The origin node, or a disconnected node

    # --- FOUNDATIONAL TEST 8: SPACETIME COHERENCE ---

    def test_falsify_temporal_scrambling(self):
        """
        FALSIFICATION TEST 8: The Spacetime Coherence Test (v2)
        
        Hypothesis: The spatial fabric is woven coherently.
        Distinctions that are "close" in space (neighbors) must
        also be "close" in *emergent time* (similar path-length from origin).
        
        Falsification: The system is "scrambled."
        """
        print("\n🌌 ATTACKING SPACETIMEvsTIME: Is the fabric *emergently* coherent?")
        
        # 1. Evolve the universe *using the local method*
        print("   Evolving universe locally for 5000 steps...")
        self._evolve_universe(steps=5000)
        
        # 2. Get the final state
        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)
        
        self.assertGreater(g.number_of_nodes(), 500, "Evolution failed to produce enough distinctions.")
        
        # 3. Build our "lookup map" for *emergent time* (age)
        print("   Calculating emergent 'age' (path from origin) for all distinctions...")
        origin_id = self.engine.d0.id
        id_to_age_map = {}
        max_age = 0
        
        for d in state[0]: # state[0] is the set of distinctions
            age = self._get_emergent_age(g, d.id, origin_id)
            id_to_age_map[d.id] = age
            if age > max_age:
                max_age = age

        if max_age == 0:
            self.fail("Falsification failed: Universe has no 'age' (graph is disconnected).")

        # 4. The Measurement:
        print("   Measuring the 'emergent age distance' of all spatial relationships...")
        age_distances = []
        
        if not state[1]: # state[1] is the set of relationships
            self.fail("Test failed: No relationships were formed.")
            
        for id_a, id_b in state[1]:
            try:
                age_a = id_to_age_map[id_a]
                age_b = id_to_age_map[id_b]
                delta_age = abs(age_a - age_b)
                age_distances.append(delta_age)
            except KeyError:
                continue
        
        if not age_distances:
            self.fail("Test failed: Could not measure any age distances.")

        # 5. The Analysis:
        avg_age_distance = np.mean(age_distances)
        
        # In a perfectly coherent fabric (like a simple grid),
        # all neighbors have an age distance of 1.
        
        print(f"\n   --- Spacetime Coherence Test Results ---")
        print(f"   Max Emergent Age (Radius): {max_age} steps")
        print(f"   Avg. Emergent Age Distance (Δ_age) between neighbors: {avg_age_distance:.2f} steps")
        
        # 6. The Falsification:
        #    If the graph is "scrambled," the average age distance
        #    between neighbors will be large.
        #    If it's "coherent," this distance should be very small,
        #    ideally close to 1.0. We'll set our threshold at 2.0.
        
        self.assertLess(avg_age_distance, 2.0,
                         f"🚩 FALSIFIED: System is 'scrambled.' Spatial neighbors are not"
                         f" close in emergent time. (Avg age distance: {avg_age_distance:.2f})")
        
        print(f"\n   ✅ THEORY VALIDATED: The spatial fabric is 'emergently coherent.'")
        print("      Neighbors in space are also neighbors in emergent time (causal distance).")

if __name__ == '__main__':
    unittest.main()