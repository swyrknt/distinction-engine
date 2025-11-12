"""
Foundational (Research) Test for Emergent Chemistry

This test suite attacks the "Atomic" claim of the theory. It tests
for the most fundamental building block of structure: the "atom"
or 3-node-cycle (triangle).

Emergent Claim Tested:
1.  Does the "one process" (local evolution) spontaneously
    create "atoms" (triangles), or is it an "acyclic"
    process that only creates "gas" (trees)?
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestEmergentChemistry(unittest.TestCase):

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
                # We'll use a tight radius=1 for this "chemistry" test
                neighborhood_ids = set(g.neighbors(a.id))
                neighborhood_ids.discard(a.id) # Remove self

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

    # --- FOUNDATIONAL TEST 13: "ATOMIC" EMERGENCE ---

    def test_falsify_atomic_emergence(self):
        """
        FALSIFICATION TEST 13: The "Atom" (Triangle) Test
        
        Hypothesis: The local process will spontaneously create
        "atoms" (3-node, 3-edge triangles), which are the
        minimal building blocks of all complex structure.
        
        Falsification: The process is "acyclic" (a "gas").
        It only creates "trees" (graphs with no triangles).
        """
        print("\n⚛️  ATTACKING CHEMISTRY: Do 'atoms' (triangles) spontaneously emerge?")
        
        # 1. Evolve the universe locally. We need a good number of
        #    steps to give triangles a chance to form.
        print("   Evolving universe locally for 5000 steps...")
        self._evolve_universe_locally(steps=5000)
        
        # 2. Get the final state
        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)
        
        self.assertGreater(g.number_of_nodes(), 500, "Evolution failed to produce enough distinctions.")
            
        # 3. The "Atom Counter"
        #    nx.triangles(g) returns a dict: {node_id: triangle_count}
        #    We sum all values and divide by 3 (since each triangle
        #    is counted by all 3 of its nodes).
        print("   Surveying universe for 'atoms' (triangles)...")
        
        try:
            triangle_dict = nx.triangles(g)
            total_triangles = sum(triangle_dict.values()) // 3
        except Exception as e:
            self.fail(f"Could not calculate triangles: {e}")
        
        # 4. The Analysis:
        print(f"\n   --- Emergent Chemistry Test Results ---")
        print(f"   Total 'Atoms' (triangles) found: {total_triangles}")

        # 5. The Falsification:
        #    If not a *single* triangle was formed, the theory
        #    is falsified. It proves our "one process" is
        #    incapable of creating the minimal bound state.
        
        self.assertGreater(total_triangles, 0,
                         f"🚩 FALSIFIED: The universe is 100% 'gas' (acyclic). No 'atoms' (triangles) were formed.")
        
        print(f"\n   ✅ THEORY VALIDATED: 'Atoms' (triangles) spontaneously emerge.")
        print(f"      The process creates the minimal bound structures ({total_triangles} found)")
        print(f"      necessary for chemistry and stable matter.")

if __name__ == '__main__':
    unittest.main()