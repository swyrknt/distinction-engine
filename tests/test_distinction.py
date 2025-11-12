"""
Axiomatic Unit Tests for DistinctionEngine

Validates fundamental axioms of the synthesis process:
1. Irreflexivity: synthesize(A, A) returns A unchanged
2. Symmetry: synthesize(A, B) produces identical result to synthesize(B, A)
3. Synthesis: synthesize(A, B) creates C with relationships (C,A) and (C,B)
4. Idempotency: synthesize(A, B) returns same C on repeated calls
"""

import unittest
import hashlib
from typing import Set, Tuple

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestAxioms(unittest.TestCase):

    def setUp(self):
        """Initialize a fresh engine instance for each test."""
        self.engine = DistinctionEngine()
        self.d0 = self.engine.d0
        self.d1 = self.engine.d1

    def test_axiom_irreflexivity(self):
        """
        Axiom: Irreflexivity.

        Validates that synthesizing a distinction with itself returns
        the original distinction without creating new entities or relationships.
        """
        initial_distinctions = len(self.engine.all_distinctions)
        initial_relationships = len(self.engine.relationships)

        result = self.engine.synthesize(self.d1, self.d1)

        self.assertIs(result, self.d1)
        self.assertEqual(len(self.engine.all_distinctions), initial_distinctions)
        self.assertEqual(len(self.engine.relationships), initial_relationships)

    def test_axiom_symmetry_and_determinism(self):
        """
        Axiom: Symmetry.

        Validates that synthesize(A, B) produces the same distinction ID
        as synthesize(B, A), proving order-independence and determinism.
        """
        c_ab = self.engine.synthesize(self.d0, self.d1)

        engine2 = DistinctionEngine()
        c_ba = engine2.synthesize(engine2.d1, engine2.d0)

        self.assertEqual(c_ab.id, c_ba.id)
        self.assertEqual(c_ab, c_ba)

    def test_axiom_synthesis_diamond_unit(self):
        """
        Axiom: Synthesis.

        Validates that synthesize(A, B) creates a new distinction C
        with relationships (C, A) and (C, B) forming a diamond structure.
        """
        self.assertEqual(len(self.engine.relationships), 1)
        self.assertEqual(len(self.engine.all_distinctions), 2)

        c = self.engine.synthesize(self.d0, self.d1)

        self.assertEqual(len(self.engine.all_distinctions), 3)
        self.assertIn(c.id, self.engine.all_distinctions)

        rel_c_d0 = (self.d0.id, c.id) if self.d0.id < c.id else (c.id, self.d0.id)
        self.assertIn(rel_c_d0, self.engine.relationships)

        rel_c_d1 = (self.d1.id, c.id) if self.d1.id < c.id else (c.id, self.d1.id)
        self.assertIn(rel_c_d1, self.engine.relationships)

        self.assertEqual(len(self.engine.relationships), 3)

    def test_axiom_synthesis_idempotency(self):
        """
        Axiom: Idempotency.

        Validates that repeated calls to synthesize(A, B) return the same
        distinction without creating duplicate entities or relationships.
        Ensures timeless consistency.
        """
        c1 = self.engine.synthesize(self.d0, self.d1)

        count_distinctions_1 = len(self.engine.all_distinctions)
        count_relationships_1 = len(self.engine.relationships)

        c2 = self.engine.synthesize(self.d0, self.d1)

        count_distinctions_2 = len(self.engine.all_distinctions)
        count_relationships_2 = len(self.engine.relationships)

        self.assertIs(c1, c2)
        self.assertEqual(count_distinctions_1, count_distinctions_2)
        self.assertEqual(count_relationships_1, count_relationships_2)

if __name__ == '__main__':
    unittest.main()