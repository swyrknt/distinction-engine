"""
Foundational (Research) Test for Emergent "Forces"

This test suite attacks the "Forces" claim of the theory.
It defines a "force" as the emergent dynamic (the "integration rule")
that occurs when two distinct subprocesses interact.

Emergent Claim Tested:
1.  Do distinct subprocesses (e.g., a "clump" and a "chain")
    have a non-trivial, measurable interaction dynamic (a "force")?
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

    def _get_local_subprocess(self, g: nx.Graph, start_node_id: str, radius=2) -> Set[str]:
        """
        Gets the set of node IDs in a local neighborhood (our "subprocess").
        """
        return set(nx.ego_graph(g, start_node_id, radius=radius).nodes())

    def _get_subprocess_coherence(self, g: nx.Graph, subprocess_nodes: Set[str]) -> float:
        """
        Measures the *average* emergent coherence (clustering)
        of a specific set of nodes (the subprocess).
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
        THE "PETRI DISH" FOR FORCES:
        Evolves a *clone* of a universe by *only* synthesizing
        nodes from subprocess A with nodes from subprocess B.
        """
        # Create a "clone" of the engine's state
        temp_engine = DistinctionEngine()
        distinctions, relationships = engine_state
        temp_engine.all_distinctions = {d.id: d for d in distinctions}
        temp_engine.relationships = relationships.copy()
        
        # Get the Distinction objects for our subprocesses
        distinctions_A = [d for d in temp_engine.all_distinctions.values()
                          if d.id in subprocess_A_nodes]
        distinctions_B = [d for d in temp_engine.all_distinctions.values()
                          if d.id in subprocess_B_nodes]
        
        if not distinctions_A or not distinctions_B:
            return temp_engine.get_state_snapshot() # Nothing to interact with

        for _ in range(steps):
            # 1. Pick one distinction from *each* subprocess
            a = random.choice(distinctions_A)
            b = random.choice(distinctions_B)
            
            # 2. Run the synthesis. This mutates temp_engine
            c = temp_engine.synthesize(a, b)
            
            # 3. Add the *new* distinction to *neither* list
            #    We are only modeling the interaction between the
            #    original two subsystems.
        
        # Return the final state of the *entire cloned universe*
        return temp_engine.get_state_snapshot()

    # --- FOUNDATIONAL TEST 13: EMERGENT FORCES ---

    def test_falsify_emergent_forces(self):
        """
        FALSIFICATION TEST 13: The "Emergent Force" Test
        
        Hypothesis: The "integration rule" (dynamic) between two
        different subprocesses (e.g., "clump" vs "chain") is
        a non-trivial, measurable "force."
        
        Falsification: All interactions are "dumb" and
        do not change the relationship between the subprocesses.
        """
        print("\n💥 ATTACKING 'FORCES': Are interactions just 'dumb' integration?")
        
        # 1. Evolve the universe to create a complex substrate
        print("   Evolving universe locally for 5000 steps...")
        self._evolve_universe_locally(steps=5000)
        
        # 2. Get the initial state and measure everything
        state_0 = self.engine.get_state_snapshot()
        g_0 = self._build_graph_from_snapshot(state_0)
        
        if g_0.number_of_nodes() < 200:
            self.fail("Graph too small to test.")
            
        # 3. Find our two "subprocesses"
        all_distinctions = list(state_0[0])
        sample_nodes = random.sample(all_distinctions, 2)
        
        subprocess_A_nodes = self._get_local_subprocess(g_0, sample_nodes[0].id)
        subprocess_B_nodes = self._get_local_subprocess(g_0, sample_nodes[1].id)
        
        # Ensure they are non-overlapping
        while not subprocess_A_nodes.isdisjoint(subprocess_B_nodes):
            sample_nodes = random.sample(all_distinctions, 2)
            subprocess_A_nodes = self._get_local_subprocess(g_0, sample_nodes[0].id)
            subprocess_B_nodes = self._get_local_subprocess(g_0, sample_nodes[1].id)

        print(f"   ...Found two distinct subprocesses (A: {len(subprocess_A_nodes)} nodes, B: {len(subprocess_B_nodes)} nodes).")

        # 4. "Measure" the Initial "Space" Between Them
        try:
            distance_0 = nx.shortest_path_length(g_0, source=sample_nodes[0].id, target=sample_nodes[1].id)
        except nx.NetworkXNoPath:
            self.fail("Could not run test: Subprocesses are in disconnected graph components.")

        # 5. Run the "Force" Experiment (Petri Dish)
        print(f"   ...Forcing {len(subprocess_A_nodes)} nodes in A to interact with {len(subprocess_B_nodes)} nodes in B...")
        state_1 = self._evolve_subprocess_A_with_B(state_0, subprocess_A_nodes, subprocess_B_nodes, steps=100)

        # 6. The Measurement: Get the *final* state
        g_1 = self._build_graph_from_snapshot(state_1)

        # Measure the *final* "space" between their original centers
        try:
            distance_1 = nx.shortest_path_length(g_1, source=sample_nodes[0].id, target=sample_nodes[1].id)
        except nx.NetworkXNoPath:
            # This is a valid outcome! It means the interaction
            # "destroyed" one of the nodes (e.g., if our impl
            # consumed/replaced them). We'll treat this as a large change.
            distance_1 = distance_0 + 100 # A very large, "repulsive" change
        except nx.NodeNotFound:
            # This can happen if our original nodes are no longer in the graph
            # In our current impl, this is not the case, but it's good to check.
            self.fail("Test logic error: Original nodes were removed.")

        # 7. The Analysis:
        delta_distance = distance_1 - distance_0
        
        print(f"\n   --- Emergent Force Test Results ---")
        print(f"   Initial 'Space' between subprocesses: {distance_0} steps")
        print(f"   Final 'Space' between subprocesses:   {distance_1} steps")
        print(f"   Interaction Dynamic (Δ_distance): {delta_distance:+.0f} steps")

        # 8. The Falsification:
        #    If the interaction is "dumb" or "neutral," the
        #    distance between the centers will not change.
        
        self.assertNotEqual(delta_distance, 0,
                         "🚩 FALSIFIED: The interaction was 'neutral.' No 'force' was detected."
                         " The distance between subprocesses did not change.")
        
        print(f"\n   ✅ THEORY VALIDATED: A non-neutral 'force' was detected.")
        if delta_distance < 0:
            print(f"      The dynamic is 'ATTRACTIVE' (distance decreased by {abs(delta_distance)}).")
        else:
            print(f"      The dynamic is 'REPULSIVE' (distance increased by {delta_distance}).")

if __name__ == '__main__':
    unittest.main()