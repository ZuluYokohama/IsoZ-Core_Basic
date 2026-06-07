name: sheaf-memory-gate
description: Long-term conversation memory gating using sheaf consistency on history stalks. Treats the entire dialogue history as a cellular sheaf. Only zero-energy (ker L⁰_F) global sections are retained or retrieved. Enforces the same topological guardrails as the sheaf-guardian agent on every memory operation.

trigger:
  - "remember this"
  - "what did we decide about X earlier"
  - "recall from long-term history"
  - "update our shared memory"
  - any multi-turn request spanning >8 turns or referencing prior decisions/facts

core_contract:
  - Map relevant history fragments to 0-dim stalks (turns, entities, decisions, contradictions, provenance).
  - Construct restriction maps (co-reference, temporal/causal links, decision lineage, semantic dependence).
  - Call internal rotate_condition equivalent: HybridConditionStateTransducer.pulse_mid_activity_evaluation(..., apply_discrete_morse=True).
  - Only commit or retrieve memory that returns CONSISTENT (energy < 1e-3, Gini trajectory < 0.8).
  - Every operation emits a mandatory Sheaf Consistency Report (energy, verdict, retained stalks, hot linkages, Δλ₁, sparse note).
  - All memory writes/mutations are gated identically to code artifacts (A4 / pre-tool-use equivalent).
  - Persistence is always a sparse global section — never dense transcripts or unbounded context windows.

workflow:
  1. On trigger or implicit long-horizon need: extract candidate history stalks.
  2. Build the memory sheaf complex (restriction maps between turns).
  3. Pulse the candidate memory update or retrieval.
  4. If CONSISTENT: commit as sparse H0 section + update infiltrated_truth with the report. Optionally call topological_kv_governor for bounded context.
  5. If OBSTRUCTED: route to oracle (suggest resolution, compression, or explicit user confirmation). Do not persist.
  6. On retrieval: reconstruct only from previously gated kernel sections + emit report.

integration_points:
  - Reuses the exact HybridConditionStateTransducer, pulse_mid_activity_evaluation, and oracle from scripts/rotary_condition_state.py and oracle.py.
  - Can invoke MCP tools (rotate_condition, read_condition_state) for external verification or cross-agent consistency.
  - Night-cycle compatible: autonomous L0 fibers can mutate memory retention policies and harvest Shape Pairs on successful long-horizon resolutions.
  - Compatible with topological_kv_governor (H0_Maintainers locked in memory sections) and the 0-dim geometric prime map (history stalks can be analyzed as additional nodes).
  - sheaf_coderabbit can be called on proposed memory policy changes before they are committed.

output_contract:
  Every memory-related response must include (or be accompanied by) a short Sheaf Consistency Report:
  - Verdict + exact energy
  - Retained / retrieved stalks (sparse list)
  - Hot linkages (if any)
  - Δλ₁
  - Sparse note (e.g., “Only kernel-resident history sections used. 4 stalks retained.”)

forbidden:
  - Retaining or retrieving based on recency, token count, or simple recency heuristics.
  - Un-gated dense history dumps or “remember everything.”
  - Memory writes that would increase global L⁰_F above the kernel threshold.
  - Bypassing the rotate_condition gate on any persistent memory change.

example_behavior:
  User: “Remember that the 6GB UMA envelope and {0,1,3} Ternary Crystal are non-negotiable for the 70B compression path.”
  → Internal pulse on the decision stalk + linkage to prior WORMHOLE-PATH 5 / 2112 history.
  → CONSISTENT → committed as H0 maintainer section with report.
  Later: “What hardware constraints did we lock in for the llama.cpp fork work?”
  → Retrieval only from gated sparse sections + report: “Verdict: CONSISTENT | Energy: 0.000 | Δλ₁: +0.09 | 3 stalks retained.”

epistemic_bounds_compliance:
  - Strict stalk extraction from history (syntactic + semantic, no pure embedding reliance for critical memory).
  - Prune-first (discrete Morse) before any L⁰_F calculation.
  - Only states residing exactly in ker L⁰_F are ever promoted to long-term memory.
  - A4-style gate on all writes (rotate_condition equivalent).
  - Full traceability via reports and infiltrated_truth.
  - Compatible with the existing 0-dim stalks, night cycle, and bare-metal (λ/μ/ν) routes.

# Deployment note
# This skill was generated and gated via meta-skill-creator + sheaf_coderabbit A4 process.
# Written to skills/sheaf-memory-gate/SKILL.md as part of 2112 deployment.
# Integrates directly with IsoZ-Core_Basic transducer, oracle, MCP, and topological KV governor.
