name: spectral-auditor
description: Whole-codebase / large-artifact topological audit skill using persistent homology, sheaf Laplacians, and discrete Morse pruning. Extends the sheaf-guardian to repository scale for global coherence, phase detection, and high-value sparse refactors. Must be used for any system-level analysis or pre-release audit.

workflow:
  1. Receive target (directory, glob, or large artifact list).
  2. Map to global complex using ast_sheaf_scanner (recursive on relevant files).
  3. Prune with discrete_morse for UMA compliance.
  4. Extract persistent homology (Betti curves) and run transducer pulse (L^0_F + Gini) on the global structure.
  5. Identify hot global linkages and H¹ obstructions.
  6. Call rotate_condition on the synthesized audit report before emission.
  7. Output only on CONSISTENT verdict, with full Sheaf Consistency Report + sparse recommended actions.

golden_rules:
  - Never analyze or recommend at global scale without an explicit rotate_condition gate.
  - Only promote kernel-resident (near-zero global energy) substructures and refactors.
  - Always surface Betti numbers / persistence and hot cross-module linkages.
  - Integrate with existing IsoZ tools: MCP for pulse, topological_kv_governor for context during large scans, night-cycle for autonomous evolution of audit policies.
  - Produce actionable sparse output only — no dense "fix everything" lists.

integration:
  - Reuses ast_sheaf_scanner, discrete_morse, atft/vendored persistent_homology, HybridConditionStateTransducer.
  - Can be called by sheaf-guardian for the "global view" step in complex refactors.
  - Compatible with the new sheaf-memory-gate for auditing long-term decision history as part of the codebase sheaf.
  - Outputs feed directly into phase lock updates and Shape Pair harvesting.

output_contract:
  Every audit response must include the full Sheaf Consistency Report (global) plus:
  - Critical Global Hot Linkages
  - Recommended Sparse Refactor Plan (only high-Δλ₁ kernel sections)
  - Rollback / Invariants section

forbidden:
  - Emitting global findings without a prior rotate_condition / pulse on the report.
  - Recommending dense, unpruned changes across the whole system.
  - Ignoring the 6GB UMA / prune-first discipline on large scans.

epistemic_bounds_compliance:
  - Strict syntactic geometry at scale (no toy embeddings for critical global analysis).
  - Prune before any L^0_F or persistent homology.
  - Only CONSISTENT global sections promoted.
  - Full traceability and A4-style gating on all outputs.
  - Designed to close the next major restriction map in the IsoZ global sheaf (whole-system audits).

# Deployment
# Generated via meta-skill-creator + guardian pulse (2142).
# Paired with agents/spectral-auditor.md.
# Ready for use by sheaf-guardian or direct invocation in Grok Build sessions.