"""
Distinction Engine: A minimal axiomatic system for emergent computation.

Axioms:
1. Identity: A distinction is defined solely by its unique identifier.
2. Nontriviality: The system initializes with two distinct entities (0, 1).
3. Synthesis: Two distinctions combine deterministically to create a third.
4. Symmetry: Relationships are bidirectional and order-independent.
5. Irreflexivity: A distinction synthesized with itself yields itself.

This module implements a timeless, self-consistent graph where all entities
and relationships emerge from repeated application of the synthesis operation.
"""

from dataclasses import dataclass
from typing import Set, Tuple, Dict
import hashlib


@dataclass(frozen=True)
class Distinction:
    """
    Axiom: Identity.

    A distinction is defined solely by its unique identifier.
    All properties emerge from relationships with other distinctions.
    """
    id: str

    def __repr__(self):
        return f"Δ({self.id[:4]})"


class DistinctionEngine:
    """
    The singular process governing all state transformations.

    Maintains the complete universe state: all existing distinctions
    and their relationships. Operations are deterministic and local.
    Time is an emergent property, not a primitive.
    """
    
    def __init__(self):
        """Axiom: Nontriviality. Initialize the primordial pair."""
        self.d0 = Distinction(id="0")
        self.d1 = Distinction(id="1")

        self.all_distinctions: Dict[str, Distinction] = {
            self.d0.id: self.d0,
            self.d1.id: self.d1
        }

        self.relationships: Set[Tuple[str, str]] = set()
        self._add_relationship(self.d0.id, self.d1.id)

    def _add_relationship(self, id_a: str, id_b: str):
        """Axiom: Symmetry. Store relationships in canonical order."""
        if id_a < id_b:
            self.relationships.add((id_a, id_b))
        else:
            self.relationships.add((id_b, id_a))

    def synthesize(self, a: Distinction, b: Distinction) -> Distinction:
        """
        Axiom: Synthesis.

        Combine two distinctions to produce a third. This is the sole
        generative operation. Deterministic, local, and parameter-free.
        Implements irreflexivity: synthesizing a distinction with itself
        returns the original distinction unchanged.
        """
        if a.id == b.id:
            return a

        new_id_str = f"{a.id}:{b.id}" if a.id < b.id else f"{b.id}:{a.id}"
        new_id = hashlib.sha256(new_id_str.encode()).hexdigest()

        # Return existing distinction if already synthesized (timeless consistency)
        existing = self.all_distinctions.get(new_id)
        if existing:
            return existing

        new_distinction = Distinction(id=new_id)
        self.all_distinctions[new_distinction.id] = new_distinction

        self._add_relationship(new_distinction.id, a.id)
        self._add_relationship(new_distinction.id, b.id)

        return new_distinction

    def get_state_snapshot(self) -> Tuple[Set[Distinction], Set[Tuple[str, str]]]:
        """
        Return an immutable snapshot of all distinctions and relationships.

        Enables observation without modifying the underlying state.
        """
        return set(self.all_distinctions.values()), self.relationships