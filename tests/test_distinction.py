"""
Axiomatic (Unit) Tests for the DistinctionEngine

This file validates the core, non-negotiable axioms of the 
"timeless" Distinction Process Theory implementation.

Axioms Tested:
1. Irreflexivity: A(A) -> A
2. Symmetry & Determinism: A(B) == B(A)
3. Synthesis (Diamond Unit): A(B) -> C, (C,A), (C,B)
4. Idempotency (New): A(B) -> C, A(B) -> C (returns same C)
"""

import unittest
import hashlib
from typing import Set, Tuple

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestAxioms(unittest.TestCase):

    def setUp(self):
        """
        Create a fresh, clean "universe" (Engine) for each test.
        """
        self.engine = DistinctionEngine()
        self.d0 = self.engine.d0
        self.d1 = self.engine.d1

    def test_axiom_irreflexivity(self):
        """
        Tests: engine.synthesize(A, A) must return A.
        """
        initial_distinctions = len(self.engine.all_distinctions)
        initial_relationships = len(self.engine.relationships)

        result = self.engine.synthesize(self.d1, self.d1)

        # 1. Test that the returned object *is* the original object
        self.assertIs(result, self.d1)
        
        # 2. Test that no new distinctions were created
        self.assertEqual(len(self.engine.all_distinctions), initial_distinctions)

        # 3. Test that no new relationships were created
        self.assertEqual(len(self.engine.relationships), initial_relationships)

    def test_axiom_symmetry_and_determinism(self):
        """
        Tests: engine.synthesize(A, B) must produce the exact 
               same distinction (same id) as engine.synthesize(B, A).
        """
        # 1. Synthesize (A, B)
        c_ab = self.engine.synthesize(self.d0, self.d1)

        # 2. Synthesize (B, A) in a *new* universe
        engine2 = DistinctionEngine()
        c_ba = engine2.synthesize(engine2.d1, engine2.d0)

        # Test that their IDs are identical (proving determinism)
        self.assertEqual(c_ab.id, c_ba.id)
        
        # Test that the objects themselves are equal
        self.assertEqual(c_ab, c_ba)

    def test_axiom_synthesis_diamond_unit(self):
        """
        Tests: When C = synthesize(A, B), the relationships 
               (C.id, A.id) and (C.id, B.id) must be created.
        """
        self.assertEqual(len(self.engine.relationships), 1)
        self.assertEqual(len(self.engine.all_distinctions), 2)

        # Run the synthesis
        c = self.engine.synthesize(self.d0, self.d1)
        
        # 1. Test that a new distinction was created
        self.assertEqual(len(self.engine.all_distinctions), 3)
        
        # --- FIX ---
        # Was: self.assertIn(c, self.engine.all_distinctions)
        # Now: We check for the ID in the *dictionary keys*
        self.assertIn(c.id, self.engine.all_distinctions)
        # --- END FIX ---

        # 2. Test that the new relationships exist
        rel_c_d0 = (self.d0.id, c.id) if self.d0.id < c.id else (c.id, self.d0.id)
        self.assertIn(rel_c_d0, self.engine.relationships)

        rel_c_d1 = (self.d1.id, c.id) if self.d1.id < c.id else (c.id, self.d1.id)
        self.assertIn(rel_c_d1, self.engine.relationships)

        # 3. Test that the total number of relationships is correct
        self.assertEqual(len(self.engine.relationships), 3)

    # --- NEW TEST ---
    def test_axiom_synthesis_idempotency(self):
        """
        Tests: A(B) -> C, and a second call A(B) -> C (returns same C).
        This validates the "timeless" graph, where a distinction
        is only created once.
        """
        # 1. Synthesize (A, B) for the first time
        c1 = self.engine.synthesize(self.d0, self.d1)
        
        # 2. Get the state of the universe
        count_distinctions_1 = len(self.engine.all_distinctions)
        count_relationships_1 = len(self.engine.relationships)
        
        # 3. Synthesize the *exact same pair* again
        c2 = self.engine.synthesize(self.d0, self.d1)
        
        # 4. Get the *new* state of the universe
        count_distinctions_2 = len(self.engine.all_distinctions)
        count_relationships_2 = len(self.engine.relationships)

        # 5. The Verdict
        # Test that the *exact same object* was returned
        self.assertIs(c1, c2)
        
        # Test that no new distinctions were created
        self.assertEqual(count_distinctions_1, count_distinctions_2)
        
        # Test that no new relationships were created
        self.assertEqual(count_relationships_1, count_relationships_2)
    # --- END NEW TEST ---

if __name__ == '__main__':
    unittest.main()