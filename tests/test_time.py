"""
Foundational (Research) Test for Time Dynamics

This test suite attacks the "Arrow of Time" claim of the "timeless" theory.

Emergent Claim Tested:
1.  Is the "universal rhythm" (the local process) an
    expansive and irreversible "Arrow of Time"?
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestTimeDynamics(unittest.TestCase):

    def setUp(self):
        """
        Create a fresh, clean "universe" (Engine) for each experiment.
        """
        self.engine = DistinctionEngine()
        self.origin_id = self.engine.d0.id # The "Big Bang" point

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

    def _get_emergent_age_radius(self, g: nx.Graph) -> int:
        """
        THE "TIME RULER": Measures the "Age" (Radius) of the
        universe by finding the longest causal chain (shortest path)
        from the origin "d0".
        """
        all_ages = []
        for node_id in g.nodes():
            if node_id == self.origin_id:
                continue
            try:
                age = nx.shortest_path_length(g, source=self.origin_id, target=node_id)
                all_ages.append(age)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue # Disconnected node, has no "age"
        
        return max(all_ages) if all_ages else 0

    # --- FOUNDATIONAL TEST 9: THE ARROW OF TIME ---

    def test_falsify_arrow_of_time(self):
        """
        FALSIFICATION TEST 9: The Arrow of Time
        
        Hypothesis: The "universal rhythm" (local evolution)
        is an expansive and irreversible process.
        
        Falsification: The process is not an "arrow." The "Age"
        (causal radius) of the universe fluctuates, shrinks,
        or stagnates.
        """
        print("\n⏳ ATTACKING TIME: Is the 'universal rhythm' an 'Arrow of Time'?")
        
        num_epochs = 10
        steps_per_epoch = 500
        
        universe_age_history = []
        
        # Measure the "Age" at step 0
        initial_state = self.engine.get_state_snapshot()
        initial_graph = self._build_graph_from_snapshot(initial_state)
        initial_age = self._get_emergent_age_radius(initial_graph)
        universe_age_history.append(initial_age)
        
        print(f"   Epoch 0 (Initial State): Emergent Age = {initial_age}")

        # 1. Evolve the universe in stages
        for i in range(1, num_epochs + 1):
            print(f"   ...Running Epoch {i} (steps {i*steps_per_epoch})...")
            self._evolve_universe_locally(steps=steps_per_epoch)
            
            # 2. Get the state and measure the *new* age
            state = self.engine.get_state_snapshot()
            g = self._build_graph_from_snapshot(state)
            current_age = self._get_emergent_age_radius(g)
            
            print(f"   Epoch {i}: Emergent Age = {current_age}")
            
            # 3. The Falsification:
            #    We assert that the new age is *at least* as large
            #    as the previous age. Time cannot run backward.
            self.assertGreaterEqual(current_age, universe_age_history[-1],
                                  f"🚩 FALSIFIED: The Arrow of Time is broken. "
                                  f"Age shrank from {universe_age_history[-1]} to {current_age} in Epoch {i}.")
            
            universe_age_history.append(current_age)
        
        # 4. Final Falsification:
        #    We assert that the universe *actually grew*.
        #    If it just sat at Age=1, it's not an expansive process.
        self.assertGreater(universe_age_history[-1], universe_age_history[0] + (num_epochs / 2),
                         "🚩 FALSIFIED: The process is not expansive. The universe stagnated.")
        
        print(f"\n   --- Arrow of Time Test Results ---")
        print(f"   Age History: {universe_age_history}")
        print(f"\n   ✅ THEORY VALIDATED: The 'universal rhythm' is an")
        print("      expansive and irreversible 'Arrow of Time.'")

if __name__ == '__main__':
    unittest.main()