"""
AST to Rips Complex Scanner for Epistemic Bounds.

Parses Python source into a simplicial complex where:
- 0-cells (vertices/stalks) = function/class/variable identifiers (semantic nodes)
- 1-cells (edges) = call graphs, data dependencies, control flow (restriction maps)

Then applies Discrete Morse pruning to critical cells only, to fit within 6GB UMA while preserving homology (Betti numbers, H0/H1).

This replaces the toy embedding graph with real code geometry.
"""

import ast
from typing import Dict, List, Tuple, Any

from discrete_morse import SimplicialComplex, prune_complex_to_critical

def extract_topological_features(tree: ast.AST) -> Tuple[SimplicialComplex, Dict, Dict]:
    """
    Walk the AST and build a 1-complex:
    - Vertices: unique identifiers (func names, var names, calls)
    - Edges: syntactic dependencies (caller -> callee, assign -> use, etc.)
    Returns the complex and a mapping for restriction matrices (simple adjacency for demo).
    """
    nodes = {}  # name -> id
    edges = []  # list of (u, v)
    node_id = 0

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.current_func = None
            self.assigns = {}  # var -> value for simple data flow

        def visit_FunctionDef(self, node):
            nonlocal node_id
            name = node.name
            if name not in nodes:
                nodes[name] = node_id
                node_id += 1
            self.current_func = name
            self.generic_visit(node)
            self.current_func = None

        def visit_Call(self, node):
            nonlocal node_id
            if isinstance(node.func, ast.Name):
                callee = node.func.id
                if callee not in nodes:
                    nodes[callee] = node_id
                    node_id += 1
                if self.current_func and self.current_func in nodes and callee in nodes:
                    edges.append((self.current_func, callee))
            self.generic_visit(node)

        def visit_Assign(self, node):
            nonlocal node_id
            # Simple data flow: targets depend on values
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var = target.id
                    if var not in nodes:
                        nodes[var] = node_id
                        node_id += 1
                    # If value is a name or call, add dep
                    if isinstance(node.value, ast.Name):
                        src = node.value.id
                        if src not in nodes:
                            nodes[src] = node_id
                            node_id += 1
                        edges.append((src, var))
                    elif isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                        src = node.value.func.id
                        if src not in nodes:
                            nodes[src] = node_id
                            node_id += 1
                        edges.append((src, var))
            self.generic_visit(node)

        def visit_Name(self, node):
            nonlocal node_id
            if node.id not in nodes:
                nodes[node.id] = node_id
                node_id += 1
            self.generic_visit(node)

    visitor = Visitor()
    visitor.visit(tree)

    # Build SimplicialComplex (0-cells + 1-cells)
    complex = SimplicialComplex()
    id_to_name = {v: k for k, v in nodes.items()}
    complex.vertices = list(nodes.values())
    complex.cells[0] = list(nodes.values())

    for u_name, v_name in edges:
        if u_name in nodes and v_name in nodes:
            u = nodes[u_name]
            v = nodes[v_name]
            eid = 1000 + len(complex.faces)
            complex.cells.setdefault(1, []).append(eid)
            complex.faces[eid] = [u, v]

    complex.dim = 1 if complex.cells.get(1) else 0

    # Simple restriction "matrices" as adjacency for demo (in real, transport maps)
    restriction_matrices = {eid: (complex.faces[eid][0], complex.faces[eid][1]) for eid in complex.faces}

    return complex, restriction_matrices, id_to_name

def scan_ast_to_rips_complex(source_code: str) -> Tuple[SimplicialComplex, Any, Dict]:
    """
    Parses structural dependencies into a Vietoris-Rips complex,
    mapping AST nodes to 0-dim stalks and call-graphs to restriction maps.
    Then prunes to critical cells for UMA compliance.
    """
    tree = ast.parse(source_code)
    base_complex, restriction_matrices, id_to_name = extract_topological_features(tree)

    # Execute exact sparsification to enforce 6GB UMA limit
    # Reduces massive dimensional load strictly to critical cells
    pruned_complex, morse_boundary, critical = prune_complex_to_critical(base_complex)

    # Map back critical cells to names for reporting
    critical_names = {dim: [id_to_name.get(cid, f"cell_{cid}") for cid in cells] 
                      for dim, cells in critical.items()}

    return pruned_complex, morse_boundary, critical_names

if __name__ == "__main__":
    sample = """
def foo(x):
    y = bar(x)
    return baz(y)
def bar(z):
    return z + 1
def baz(w):
    return w * 2
"""
    pruned, boundary, crit = scan_ast_to_rips_complex(sample)
    print("Pruned complex dims:", {d: len(c) for d,c in pruned.cells.items()})
    print("Critical names:", crit)
    print("Morse boundary shape:", boundary.shape if hasattr(boundary, 'shape') else 'N/A')