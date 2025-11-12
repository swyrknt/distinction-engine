"""
Foundational (Research) Test for Emergent "Biology"

This test suite attacks the "Coding Law" claim of the theory.
It tests for the fundamental *structural prerequisites* of
"life" (a "genome").

Emergent Claim Tested:
1.  Is the "primordial soup" (the graph) complex enough
    to support *both* "chain-like" (information storage)
    and "clump-like" (catalytic) structures?
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestEmergentBiology(unittest.TestCase):

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
    def _evolve_universe_locally(self, steps: int):
        """
        Runs the "one process" locally to create the substrate.
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


    # --- FOUNDATIONAL TEST 14: "GENOME" PREREQUISITES ---

    def test_falsify_structural_sterility(self):
        """
        FALSIFICATION TEST 14: The "Genome" Test
        
        Hypothesis: The process creates a "primordial soup" rich
        enough for "life," meaning it produces *both* "clumps"
        (for catalytic action) and "chains" (for information storage).
        
        Falsification: The universe is "sterile"—it only
        produces one type of structure.
        """
        print("\n🧬 ATTACKING BIOLOGY: Does a 'primordial soup' for 'life' emerge?")
        
        # 1. Evolve the universe
        print("   Evolving universe locally for 5000 steps...")
        self._evolve_universe_locally(steps=5000)
        
        # 2. Get the final state
        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)
        
        if not nx.is_connected(g):
            # If the graph is not one "universe," our rulers won't work.
            # We can take the largest connected component.
            largest_cc_nodes = max(nx.connected_components(g), key=len)
            g = g.subgraph(largest_cc_nodes)
            print("   ...Graph is not fully connected. Analyzing largest component.")
        
        if g.number_of_nodes() < 500:
            self.fail("Evolution failed to produce a large enough connected universe.")
            
        # 3. The "Rulers"
        print("   Measuring structural properties of the soup...")
        
        # Ruler 1: "Clumps" (for Catalysis)
        # We use the Average Clustering Coefficient (Coherence).
        # A high value means the graph is "clumpy."
        emergent_coherence = nx.average_clustering(g)
        
        # Ruler 2: "Chains" (for Information Storage)
        # We use the Average Shortest Path Length.
        # A high value means the graph is "stringy" and "chain-like."
        avg_path_length = nx.average_shortest_path_length(g)

        print(f"\n   --- Emergent Biology Test Results ---")
        print(f"   'Clumpiness' (Avg. Coherence): {emergent_coherence:.4f}")
        print(f"   'Stringiness' (Avg. Path Length): {avg_path_length:.4f}")

        # 4. The Falsification:
        
        # Falsification A: Is the soup "all gas" (no clumps)?
        # (We already proved this in test_chemistry.py, but we re-test)
        self.assertGreater(emergent_coherence, 0.01,
                         f"🚩 FALSIFIED: The soup is 'all gas' (Coherence: {emergent_coherence:.4f})."
                         " No 'clumps' for catalytic action found.")
        
        # Falsification B: Is the soup "all clump" (no chains)?
        # A "clumpy" (small-world) graph would have a very low path length.
        # We assert the path length is "non-trivial."
        self.assertGreater(avg_path_length, 3.0,
                         f"🚩 FALSIFIED: The soup is 'all clump' (Path Length: {avg_path_length:.4f})."
                         " No 'chains' for information storage found.")
        
        print(f"\n   ✅ THEORY VALIDATED: The 'primordial soup' is fertile.")
        print(f"      The process creates *both* 'clumps' (Coherence > 0) *and* 'chains' (Path Length > 3).")
        print(f"      This provides the necessary structural diversity for a 'genome'.")

if __name__ == '__main__':
    unittest.main()