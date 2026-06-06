"""
rotary_condition_state.py
The Mathematical Engine (Node β core + L0/L3 fiber).

Implements the HybridConditionStateTransducer that evaluates mid-activity
AST / semantic mutations using sheaf-theoretic consistency (simulated + hooks for real).

Key concepts implemented (faithful to spec):
- CRMtex stalk mapping (simplified: symbol nodes -> vector stalks)
- Sheaf Laplacian L°_F computation on a tiny Vietoris-Rips style graph
- pulse_mid_activity_evaluation() that returns energy + kernel membership
- ComputeConsistencyRadius()
- Integration points for neural-sheaf-diffusion (PyG) and Lean-verified kernels

When real hardware/math libs are present, replace the compute_* functions.
"""

from __future__ import annotations
import math
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Stalk:
    """F(v): stalk at vertex v. In real system this would be a Lie algebra element / embedding."""
    node_id: str
    vector: List[float]  # low-dim simulation of embedding
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConditionState:
    """Current global section / coherence state of the sheaf over the workspace fragment."""
    stalks: Dict[str, Stalk] = field(default_factory=dict)
    edges: List[Tuple[str, str]] = field(default_factory=list)  # restriction map edges (v ≼ e) - these are the "linkages"
    edge_energies: Dict[Tuple[str, str], float] = field(default_factory=dict)  # per-linkage contribution to truth/consistency
    last_energy: float = 0.0
    last_kernel: bool = True
    last_obstruction: Optional[str] = None
    pulse_count: int = 0
    delta_lambda: float = 0.0   # topological coherence shift
    # "Truth" metadata: external facts or requirements that were infiltrated as additional constraints
    infiltrated_truth: List[str] = field(default_factory=list)


class HybridConditionStateTransducer:
    """
    The transducer that sits inside the subagent loop.
    On any candidate generation, call pulse_mid_activity_evaluation(artifact).
    """

    def __init__(self, dim: int = 8):
        self.dim = dim
        self.state = ConditionState()
        self._node_counter = 0

    def _tokenize_to_nodes(self, artifact: str) -> List[str]:
        """Very rough 'AST symbol' extractor for simulation. Real version walks real AST."""
        # Extract plausible identifiers, function names, types
        ids = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]{2,})\b", artifact)
        # Dedup while preserving order
        seen = set()
        nodes = []
        for i in ids:
            if i not in seen:
                seen.add(i)
                nodes.append(i)
        return nodes[:64]  # bound for edge device

    def _embed(self, token: str) -> List[float]:
        """Deterministic cheap embedding for stalk vector (replace with real LLM hidden state projection)."""
        vec = [0.0] * self.dim
        for i, ch in enumerate(token):
            vec[i % self.dim] += (ord(ch) % 23) / 23.0
        # Normalize lightly
        norm = math.sqrt(sum(x*x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def map_to_stalks(self, artifact: str, context_label: str = "artifact") -> Dict[str, Stalk]:
        """Node α: Semantic Encodings × Embeddings (CRMtex Stalks)."""
        nodes = self._tokenize_to_nodes(artifact)
        stalks: Dict[str, Stalk] = {}
        for tok in nodes:
            vid = f"{context_label}:{tok}:{self._node_counter}"
            self._node_counter += 1
            stalks[vid] = Stalk(node_id=vid, vector=self._embed(tok), metadata={"token": tok})
        return stalks

    def _build_edges(self, stalks: Dict[str, Stalk]) -> List[Tuple[str, str]]:
        """Simulate Vietoris-Rips / adjacency for restriction maps.
        In real impl: use metric on the stalks + persistent homology or AST adjacency.
        """
        ids = list(stalks.keys())
        edges: List[Tuple[str, str]] = []
        # Connect nearby in embedding space (toy Rips)
        for i, a in enumerate(ids):
            for b in ids[i+1:]:
                va = stalks[a].vector
                vb = stalks[b].vector
                dist = math.sqrt(sum((x-y)**2 for x,y in zip(va, vb)))
                if dist < 0.8:  # filtration scale
                    edges.append((a, b))
        return edges

    def compute_sheaf_laplacian_energy(self, stalks: Dict[str, Stalk], edges: List[Tuple[str, str]]) -> Tuple[float, bool, Optional[str], Dict[Tuple[str, str], float]]:
        """
        Node β: Compute L°_F = (δ°)* δ° and its kernel membership.
        Real version would use persistent-sheaf-laplacian + PyG BuNN layers.
        Here we do a simple graph Laplacian energy on the 0-cochains (stalk vectors).
        """
        if not stalks:
            return 0.0, True, None, {}

        ids = list(stalks.keys())
        idx = {nid: i for i, nid in enumerate(ids)}
        n = len(ids)

        # Degree matrix + adjacency (undirected for 0-form laplacian simulation)
        deg = [0] * n
        adj_energy = 0.0
        edge_energies: Dict[Tuple[str, str], float] = {}
        for u, v in edges:
            if u in idx and v in idx:
                i, j = idx[u], idx[v]
                deg[i] += 1
                deg[j] += 1
                # "disagreement" energy between stalks (restriction map violation proxy)
                du = stalks[u].vector
                dv = stalks[v].vector
                diff = sum((x - y) ** 2 for x, y in zip(du, dv))
                adj_energy += diff
                edge_energies[(u, v)] = round(diff, 6)  # per-linkage "truth" contribution (lower is more consistent linkage)

        # Very simplified quadratic form energy ~ x^T L x
        # Add self-degree penalty
        self_energy = sum(d * sum(s.vector[k]**2 for k in range(self.dim)) for d, (_, s) in zip(deg, stalks.items()))
        total_energy = (adj_energy + self_energy * 0.1) / max(1, n)

        # Kernel test (energy below threshold ≈ in kernel)
        is_kernel = total_energy < 1e-3
        obstruction = None
        if not is_kernel:
            # Highlight the worst linkages for "streamlining"
            worst_linkages = sorted(edge_energies.items(), key=lambda x: x[1], reverse=True)[:3]
            obstruction = f"H1-knot-like: energy={total_energy:.6f} on {len(edges)} restriction edges. Hot linkages (infil/exfil points to review): {worst_linkages}"

        return total_energy, is_kernel, obstruction, edge_energies

    def pulse_mid_activity_evaluation(self, artifact: str, context: str = "generation") -> Dict[str, Any]:
        """
        Main entry called by MCP / agent before emitting candidate output.
        Returns the condition state after this pulse.
        """
        new_stalks = self.map_to_stalks(artifact, context)
        # Merge into current complex (growing the observed sheaf)
        self.state.stalks.update(new_stalks)

        new_edges = self._build_edges(self.state.stalks)
        self.state.edges = list(set(self.state.edges + new_edges))  # simplistic union

        energy, in_kernel, obstruction, edge_energies = self.compute_sheaf_laplacian_energy(
            self.state.stalks, self.state.edges
        )

        self.state.last_energy = energy
        self.state.last_kernel = in_kernel
        self.state.last_obstruction = obstruction
        self.state.edge_energies = edge_energies
        self.state.pulse_count += 1

        # Simulate topological coherence shift (Δλ₁)
        self.state.delta_lambda = (energy * 0.3) + (0.01 * (self.state.pulse_count % 7))

        return {
            "energy": round(energy, 8),
            "kernel_member": in_kernel,
            "obstruction": obstruction,
            "delta_lambda": round(self.state.delta_lambda, 6),
            "pulse_count": self.state.pulse_count,
            "stalk_count": len(self.state.stalks),
            "edge_count": len(self.state.edges),
            "hot_linkages": dict(sorted(edge_energies.items(), key=lambda x: x[1], reverse=True)[:5]),  # top problematic linkages for review
            "verdict": "CONSISTENT" if in_kernel else "OBSTRUCTED",
        }

    def ComputeConsistencyRadius(self) -> float:
        """Returns a radius within which stalks are considered coherent (toy)."""
        if not self.state.stalks:
            return 0.0
        # In real system: derived from the smallest positive eigenvalue of L or filtration value
        return max(0.01, 0.25 - (self.state.last_energy * 10))

    def get_state(self) -> Dict[str, Any]:
        return {
            "stalk_count": len(self.state.stalks),
            "last_energy": self.state.last_energy,
            "last_kernel": self.state.last_kernel,
            "last_obstruction": self.state.last_obstruction,
            "pulse_count": self.state.pulse_count,
            "delta_lambda": self.state.delta_lambda,
            "consistency_radius": self.ComputeConsistencyRadius(),
            "linkages": {
                "total_edges": len(self.state.edges),
                "hot_linkages": dict(sorted(self.state.edge_energies.items(), key=lambda x: x[1], reverse=True)[:5]) if hasattr(self.state, 'edge_energies') else {},
            },
            "infiltrated_truth": getattr(self.state, 'infiltrated_truth', []),
        }

    def reset(self):
        self.state = ConditionState()
        self._node_counter = 0


# Global singleton transducer for the MCP server process (simple model; real may be per-session)
TRANSDUCER = HybridConditionStateTransducer(dim=8)


def pulse(artifact: str, context: str = "agent-generation") -> Dict[str, Any]:
    """Convenience wrapper used by the MCP server. This is a primary INFIL point for artifacts."""
    return TRANSDUCER.pulse_mid_activity_evaluation(artifact, context)


def read_state() -> Dict[str, Any]:
    """Primary EXFIL point for the current truth (energy, linkages, obstructions) and state."""
    state = TRANSDUCER.get_state()
    # Inject linkage details for CodeRabbit-style review / streamlining
    state["linkages"] = {
        "edge_count": len(TRANSDUCER.state.edges),
        "hot_linkages": getattr(TRANSDUCER.state, 'edge_energies', {}),
    }
    state["infiltrated_truth_count"] = len(getattr(TRANSDUCER.state, 'infiltrated_truth', []))
    return state


if __name__ == "__main__":
    # Quick self-test
    t = HybridConditionStateTransducer()
    res = t.pulse_mid_activity_evaluation("def foo(x): return x + 1\nclass Bar: pass", "test")
    print("Pulse result:", res)
    print("State:", t.get_state())
