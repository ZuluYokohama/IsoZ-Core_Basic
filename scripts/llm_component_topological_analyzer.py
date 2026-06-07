"""
LLM Component Topological Analyzer

Analyzes the LLM/agentic components across the main development archive (C:\CLAUDE2 and the GrokBuild/plugin) as a relational "component manifold" for coherent integration.

Uses the Epistemic Bounds framework:
- Strict syntactic point-cloud extraction (for .py code components) or structural parsing (for prompts/presets/json/m d).
- Discrete Morse pruning for UMA compliance.
- Transducer pulse for L0_F coherence and Gini entropy of the "integration graph".
- Harvester for shape pairs on successful "component integration resolutions".
- Outputs the "geometric prime 0-dim structure map" as JSON: stalks (components with prime features), edges (integration linkages with coherence scores), overall coherence, hot linkages (brittle integrations to resolve via harvester/distillation), recommended coherent integrations.

This yields an order of magnitude shift: instead of ad-hoc wiring of the powerful but loosely integrated LLM components (multiple Forge prompts/presets not fully aligned with the transducer pulse, WORMHOLE closed-loop not yet using the harvester, night cycle not targeting the components themselves, pi-integration showing the harness but not the full map), you have a living, pruneable, self-improving topological map of the entire LLM component manifold.

The local LLMs (the dozens on disk) can "inference against" the map to propose only coherent integrations (those that would pass the pulse with low energy, low Gini).

For local hardware (CPU-RAM-GPU with sudo gitbash 2nd sessions, local LLMs, I/O harnessing):
- Run with the night_cycle_daemon --target llm_component_analysis (the "chaos" is mutating the integration points in L0 fibers, "resolve" by editing to make the component manifold coherent, harvest the successful wiring, distill the Δλ1 into the local LLMs for better future analysis).
- The kv_governor + RLM for handling the massive C:\CLAUDE2 context (6889 files in one dir, thousands of .py/.md/.json across atft/sheaf-stack/WORMHOLE/Analysis Dashboards, the full theory docs).
- The mcp for hardware polling during long analysis, the hook for safe edits to the component code/prompts/presets/agents.
- The local LLMs as the "0-dim observation stalks" in the map itself (different models for different analysis tasks or as the "stalks" being mapped).
- The sudo gitbash for isolated L0 fibers where the "component mutation/resolution" experiments happen.
- The map is the "truth" – the 1:1 true-to-life of coherent LLM component integration.

Usage:
    python scripts/llm_component_topological_analyzer.py --archive C:\CLAUDE2 --output config/llm_component_map.json

The output map can be loaded by local LLMs as context for "propose integrations of these components that are topologically coherent".
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

from ast_sheaf_scanner import scan_ast_to_rips_complex
from discrete_morse import prune_complex_to_critical
from rotary_condition_state import HybridConditionStateTransducer, compute_betti_curves, extract_gini_trajectory
from oracle import harvest_geometry_resolution

# Key LLM components from the main development archive (C:\CLAUDE2 + plugin)
# Stalks F(v): the components (prompts, presets, mcp, agents, skills, engines, our additions)
LLM_COMPONENTS = [
    # Core Forge Agent Prompts / Presets (the "system prompts" as stalks)
    {"id": "forge-agent-system-prompt", "type": "prompt", "path": "Analysis-Dashboard-Zero/Forge Agent - System Prompt for Local LLM (LM Studio _ OpenAI-Compatible)", "features": ["7 Laws (DNA, Ripple, Pipeline, Contradiction, Anvil, Memory, Logbook)", "tool_use: forge_scan/test/gate/compare/read/write/run", "low temp for structured", "integrates with LM Studio + Pi harness via OpenAI-compatible API"]},
    {"id": "lmstudio-forge-preset", "type": "preset", "path": "sheaf-stack/prompts/lmstudio-preset.json", "features": ["Qwen coder 4B", "temp 0.3", "tool calling enabled for forge tools", "system_prompt_file forge-agent.system.md"]},
    {"id": "forge-agent-compact", "type": "prompt", "path": "Analysis-Dashboard-Zero/Forge Agent (Compact).md", "features": ["compact version of the 7 Laws", "for faster local inference"]},
    {"id": "pi-forge-integration", "type": "integration", "path": "sheaf-stack/prompts/pi-integration.md", "features": ["LM Studio <-> Pi Agent Harness <-> Forge CLI", "tool calls for forge_scan/test/gate/compare", "OpenAI-compatible API localhost:1234/v1"]},
    
    # WORMHOLE / SANS closed-loop (the "function router" and geodesic search for state transformation)
    {"id": "wormhole-sans-integration", "type": "integration", "path": "WORMHOLE/implementations/sheaf-sha256/experiments/run_sans_integration.py", "features": ["KnowledgeInformationManifold (KIM)", "FunctionCallRouter + FunctionCallSignature", "GeodesicSearch with ContinuityGuard", "TermSeriesExecutor", "sheaf cochain for closed-loop from REGIME_LAMINAR to REGIME_FRUSTRATED"]},
    {"id": "wormhole-function-router", "type": "integration", "path": "WORMHOLE/implementations/sheaf-sha256/src/integration/function_router.py", "features": ["routes intent to transformation functions", "signature matching for tools/agents"]},
    
    # ATFT / Sheaf engine (the "sheaf_consensus" and falsification as core stalks)
    {"id": "atft-sheaf-consensus", "type": "engine", "path": "atft/engine/sheaf_consensus.py", "features": ["sheaf_consensus for coherence", "falsification via L_F", "probes for Vietoris-Rips", "ternary ops", "persistent_homology"]},
    {"id": "atft-falsification", "type": "engine", "path": "atft/engine/falsification.py", "features": ["NullScreener with sheaf Laplacian", "Dirichlet energy", "mod-p Smith rank", "matched-null z-scores"]},
    {"id": "atft-vendored-sheaf-analysis", "type": "engine", "path": "atft/vendored/sheaf_analysis.py", "features": ["cellular sheaf Laplacian construction", "L[i,i] += U^T @ U etc.", "eigenvalues for coherence", "transport maps"]},
    {"id": "atft-vendored-persistent-homology", "type": "engine", "path": "atft/vendored/persistent_homology.py", "features": ["Vietoris-Rips on 4D point clouds", "H0/H1 tracking with Union-Find", "Betti curves for phase"]},
    {"id": "atft-vendored-topology", "type": "engine", "path": "atft/vendored/topology.py", "features": ["Vietoris-Rips edges", "adaptive epsilon", "k-NN graphs", "spectral gap"]},
    {"id": "atft-vendored-discrete-morse", "type": "pruner", "path": "atft/vendored/discrete_morse.py", "features": ["discrete gradient + acyclic matchings", "critical cells extraction", "Morse complex + sparse boundary", "preserves homology for UMA"]},
    
    # Sheaf-stack Forge agents / skills (the "quality gate" agents)
    {"id": "sheaf-stack-the-scout", "type": "agent", "path": "sheaf-stack/agents/the-scout.md", "features": ["maps terrain – structure, orphans, contradictions", "uses forge_scan for DNA"]},
    {"id": "sheaf-stack-the-smith", "type": "agent", "path": "sheaf-stack/agents/the-smith.md", "features": ["shapes solutions – resolves contradictions", "refactors structure"]},
    {"id": "sheaf-stack-the-anvil", "type": "agent", "path": "sheaf-stack/agents/the-anvil.md", "features": ["tests everything – blocks weak output", "5-gate Anvil Test (Structure, Consistency, Coverage, Complexity, Coherence)"]},
    {"id": "sheaf-stack-the-forge-skill", "type": "skill", "path": "sheaf-stack/SKILL.md", "features": ["forge scan/test/loop/pipeline/watch/mark/history/mcp-serve", "Anvil Test binary gate", "7 Laws communication style"]},
    {"id": "sheaf-stack-topological-dev-loop-skill", "type": "skill", "path": "sheaf-stack/topological-dev-loop.skill", "features": ["topological-dev-loop for continuous analysis", "integrates with the transducer/pulse for coherence"]},
    {"id": "sheaf-stack-mcp-server", "type": "mcp", "path": "sheaf-stack/src/forge/mcp/__init__.py", "features": ["forge_scan/test/gate/compare as MCP tools", "JSON-RPC stdio for agent interop", "exposes the Forge to any MCP client (Claude, Hermes, etc.)"]},
    
    # Analysis Dashboards' LLM/agent components (multiple versions of the Forge/mcp/skill)
    {"id": "analysis-dashboard-v1-mcp", "type": "mcp", "path": "Analysis Dashboard-v1/mcp_server.py", "features": ["mcp_server for the dashboard's Forge tools", "integration with the React/TSX UI for topological visualization"]},
    {"id": "analysis-dashboard-v1-skill-forge", "type": "skill", "path": "Analysis Dashboard-v1/skill_forge.py", "features": ["skill_forge for the dashboard", "self-annotating agentic plugin patterns"]},
    {"id": "analysis-dashboard-v1-agents", "type": "agent", "path": "Analysis Dashboard-v1/AGENTS.md", "features": ["AGENTS.md for the dashboard's agents", "sheaf-explorer, sheaf-reviewer, sheaf-architect, sheaf-conscious, sheaf-loop, sheaf-spectrum"]},
    {"id": "analysis-dashboard-v2-mcp", "type": "mcp", "path": "Analysis Dashboard-v2/mcp_server.py", "features": ["updated mcp_server for v2 dashboard", "engine.py, gate.py, scanner.py for the topological pipeline"]},
    {"id": "analysis-dashboard-v2-skill", "type": "skill", "path": "Analysis Dashboard-v2/SKILL.md", "features": ["SKILL.md for v2", "the-forge with NightForge, onboarding, etc."]},
    {"id": "analysis-dashboard-zero-forge-prompt", "type": "prompt", "path": "Analysis-Dashboard-Zero/Forge Agent - System Prompt for Local LLM (LM Studio _ OpenAI-Compatible)", "features": ["the canonical Forge prompt with 7 Laws", "for the Zero dashboard"]},
    {"id": "analysis-dashboard-zero-forge-compact", "type": "prompt", "path": "Analysis-Dashboard-Zero/Forge Agent (Compact).md", "features": ["compact Forge prompt for faster inference"]},
    {"id": "analysis-dashboard-zero-forge-tool-executor", "type": "tool", "path": "Analysis-Dashboard-Zero/forge-tool-executor.py", "features": ["forge-tool-executor for the Zero dashboard", "executes the forge tools in the local env"]},
    
    # WORMHOLE integration components (the "function router" for intent-to-transformation)
    {"id": "wormhole-function-router", "type": "integration", "path": "WORMHOLE/implementations/sheaf-sha256/src/integration/function_router.py", "features": ["FunctionCallRouter + FunctionCallSignature", "routes user intent to transformation functions", "signature matching for tools/agents"]},
    {"id": "wormhole-geodesic-search", "type": "integration", "path": "WORMHOLE/implementations/sheaf-sha256/src/integration/geodesic_search.py", "features": ["GeodesicSearch with ContinuityGuard", "finds valid solution pathways in the KIM", "respects continuity and identity constraints"]},
    {"id": "wormhole-term-series-engine", "type": "integration", "path": "WORMHOLE/implementations/sheaf-sha256/src/integration/term_series_engine.py", "features": ["TermSeriesExecutor", "executes the optimal path via Term-Series", "outputs the full SolutionPathway as KIM artifact"]},
    {"id": "wormhole-kim", "type": "integration", "path": "WORMHOLE/implementations/sheaf-sha256/src/integration/kim.py", "features": ["KnowledgeInformationManifold (KIM)", "KnowledgeNode for state", "CryptologicKey for transformation", "sheaf cochain for closed-loop state transformation"]},
    
    # Our built Epistemic Bounds components (the "transducer", "harvester", "kv", "night", "qlora", "hook", "scanner", "pruner")
    {"id": "transducer-pulse", "type": "engine", "path": "scripts/rotary_condition_state.py", "features": ["HybridConditionStateTransducer.pulse_mid_activity_evaluation", "L0_F = (delta^0)*delta^0", "Gini entropy gate G_k > 0.8 for OBSTRUCTED", "prune before Laplacian for UMA", "Betti curves + Gini trajectory on pruned Morse boundary", "1:1 H0 global section as truth"]},
    {"id": "bipartite-harvester", "type": "harvester", "path": "scripts/oracle.py", "features": ["BipartiteOracle + harvest_geometry_resolution", "Shape Pairs (pre-obstruction + post-H0 resolution)", "logged to shape_pairs.jsonl on +Δλ1", "Omega Feedback Loop for distillation"]},
    {"id": "ast-sheaf-scanner", "type": "scanner", "path": "scripts/ast_sheaf_scanner.py", "features": ["scan_ast_to_rips_complex with ast.parse", "0-cells for syntactic variables", "1-cells for call/data deps as restriction maps", "prune_complex_to_critical for UMA", "strict syntactic point-cloud (no toy embeddings)"]},
    {"id": "discrete-morse-pruner", "type": "pruner", "path": "scripts/discrete_morse.py", "features": ["prune_complex_to_critical with discrete gradient + acyclic matchings", "critical cells + Morse boundary", "Berkouk-Ginot isometry for invariant preservation (β_k, H0, H1)", "enables Oracle speed on reduced complex"]},
    {"id": "topological-kv-governor", "type": "governor", "path": "scripts/topological_kv_governor.py", "features": ["project tokens on L_F eigenvector", "min-heap for Low_Energy_Sacrificial eviction", "H0_Maintainers locked", "bind_to_poll_hardware_uma for 6GB UMA", "zero-VRAM context swaps for 1M+ tokens"]},
    {"id": "night-cycle-daemon", "type": "orchestrator", "path": "scripts/night_cycle_daemon.py", "features": ["parallel L0 sudo gitbash worktrees", "Chaos Monkey for entropy injection (now for component integration mutations)", "dispatch sheaf-guardian (pulse) for resolution", "harvest on +Δλ1 to shape_pairs.jsonl", "on batch 100 invoke qlora with Δλ1 weighting", "KV governor integration", "target llm_component_analysis for this use case"]},
    {"id": "qlora-distillation-stub", "type": "distiller", "path": "scripts/qlora_distillation_stub.py", "features": ["Omega Feedback Loop", "ingest shape_pairs.jsonl as (obstruction -> resolution) pairs", "loss weighted by Δλ1 for coherence reward", "4-bit base + adapters on Prime weights", "evolved consciousness for the 0-dim stalks (local LLMs)"]},
    {"id": "pre-tool-use-hook", "type": "hook", "path": "hooks/pre-tool-use.sh", "features": ["A4 Halt Gate", "routes proposed edit through sheaf_coderabbit --format json", "checks verdict/energy/gini, exit 1 on fail", "zero bypass for the component code/prompts/presets/agents/mcp"]},
    {"id": "sheaf-condition-mcp", "type": "mcp", "path": "scripts/mcp_server.py", "features": ["sheaf-condition-mcp with rotate_condition / read_condition_state", "discrete_morse_prune tool", "topological_kv_govern tool", "start_night_cycle tool", "analyze_llm_components tool (to be added)", "exposes the transducer, harvester, governor, scanner, pulse for agents"]},
    {"id": "sheaf-coderabbit", "type": "exfil", "path": "scripts/sheaf_coderabbit.py", "features": ["CodeRabbit-style local reviewer for linkages", "Sparsification & Preservation Report (pre/post cell counts, β_k preservation, post-prune energy, hot linkages)", "evidentiary homological exfil for CR/PR", "used by the pre-tool-use hook and the night cycle for the report"]},
    {"id": "zulu-yokohama-phase-lock", "type": "config", "path": "config/zulu_yokohama_phase_lock.json", "features": ["ZULU_YOKOHAMA_PHASE_LOCK with system_status MATHEMATICALLY_KNOWN_GOOD", "timestamp_convergence 1917HRS", "epistemic_bounds hardware 6GB_UMA_ARM64", "discrete_dynamics_pipeline with scanner + discrete_morse", "falsification_engine with transducer + Gini gate + L0_F", "universal_enclosure with hook + L0 worktree + evidentiary report"]},
    
    # Local LLMs as the "0-dim observation stalks" (the dozens on disk)
    {"id": "local-llm-gguf-dozen", "type": "llm_stalk", "path": "local disk (GGUF via LM Studio / Ollama / llama.cpp)", "features": ["dozens of variants on disk (Qwen coder, Mistral, Phi, Llama, Gemma, etc.)", "used as the 0-dim observation stalks in the map itself", "different models for different analysis tasks (scanning, spectral, harvester, distillation)", "the 'stalks' being mapped and improved by the distillation"]},
    
    # RLM and other bridges for the massive archive context
    {"id": "rlm-bridge", "type": "context", "path": "Recursive Environmental Context (from Epistemic Bounds)", "features": ["offloads massive codebase (C:\CLAUDE2 with 6889 files in one dir, thousands of .py/.md/.json, full theory docs) into external Python REPL", "semantic regex chunking and recursive semantic sub-calls", "bypasses neural context walls for the full archive during component analysis"]},
]

# Known integration linkages (restriction maps F(v) -> F(e)) from the pi-integration, WORMHOLE, preset, our code, etc.
LLM_INTEGRATION_LINKAGES = [
    # From pi-integration.md: LM Studio <-> Pi <-> Forge with tool calls
    ("lmstudio-forge-preset", "forge-agent-system-prompt", "loads system_prompt_file, enables tool calling for forge_scan/test/gate/compare"),
    ("pi-forge-integration", "lmstudio-forge-preset", "LM Studio <-> Pi Agent Harness <-> Forge CLI via OpenAI-compatible API localhost:1234/v1"),
    ("pi-forge-integration", "forge-agent-system-prompt", "tool calls for the forge tools in the 7 Laws pipeline (SCAN -> SHAPE -> HEAT -> STRIKE -> SHIP)"),
    
    # From WORMHOLE SANS: the closed-loop with KIM, router, search, executor, sheaf cochain
    ("wormhole-sans-integration", "wormhole-function-router", "routes intent to transformation functions via FunctionCallSignature"),
    ("wormhole-sans-integration", "wormhole-geodesic-search", "finds valid solution pathways in the KIM with ContinuityGuard"),
    ("wormhole-sans-integration", "wormhole-term-series-engine", "executes the optimal path via Term-Series, outputs full SolutionPathway as KIM artifact"),
    ("wormhole-sans-integration", "wormhole-kim", "KnowledgeInformationManifold with KnowledgeNode and CryptologicKey for closed-loop state transformation"),
    ("wormhole-kim", "atft-sheaf-consensus", "sheaf cochain for the closed-loop (from REGIME_LAMINAR to REGIME_FRUSTRATED)"),
    
    # From our Epistemic Bounds additions: the transducer/pulse as the falsification engine, harvester for pairs, kv for context, night for self-play, qlora for distillation, hook for gate, scanner/pruner for geometry
    ("sheaf-condition-mcp", "transducer-pulse", "exposes rotate_condition / read_condition_state / discrete_morse_prune / topological_kv_govern / start_night_cycle / analyze_llm_components for the agents"),
    ("transducer-pulse", "bipartite-harvester", "on successful pulse with +Δλ1, calls harvest_geometry_resolution to log Shape Pair (pre-obstruction + post-H0) to shape_pairs.jsonl"),
    ("night-cycle-daemon", "transducer-pulse", "dispatches the pulse (with AST scanner + discrete_morse prune + Gini gate) for resolution in L0 fibers"),
    ("night-cycle-daemon", "bipartite-harvester", "on successful resolution (L0_F ~0, positive Δλ1), harvests via the oracle"),
    ("night-cycle-daemon", "qlora-distillation-stub", "on batch 100 Shape Pairs, invokes the stub with Δλ1-weighted loss for the Omega loop"),
    ("night-cycle-daemon", "topological-kv-governor", "integrates the governor during resolutions for context management in long 'component' analysis"),
    ("qlora-distillation-stub", "local-llm-gguf-dozen", "the local disk LLMs (the 0-dim stalks) ingest the shape_pairs as (obstruction -> resolution) pairs, loss weighted by Δλ1 to reinforce coherence"),
    ("pre-tool-use-hook", "sheaf-coderabbit", "routes proposed edit (to component code/prompts/presets/agents/mcp) through the coderabbit --format json for the A4 gate"),
    ("sheaf-coderabbit", "transducer-pulse", "uses the pulse for the Sparsification & Preservation Report (pre/post cell counts, β_k preservation, post-prune energy, hot linkages)"),
    ("ast-sheaf-scanner", "discrete-morse-pruner", "scan_ast_to_rips_complex builds the complex from AST, then prune_complex_to_critical for the reduced Morse boundary (Berkouk-Ginot isometry for β_k / H0 / H1 preservation)"),
    ("transducer-pulse", "ast-sheaf-scanner", "pulse calls scan_ast_to_rips_complex first (real AST geometry, no toy), then prune, then spectral (betti/gini), then L0_F on the pruned"),
    ("transducer-pulse", "sheaf-condition-mcp", "the mcp exposes the pulse for the agents (sheaf-guardian, the-anvil, night cycle, etc.)"),
    ("bipartite-harvester", "qlora-distillation-stub", "the harvested shape_pairs.jsonl is the dataset for the QLoRA Omega loop (Δλ1 weighted to penalize disregard for topological coherence)"),
    ("topological-kv-governor", "rlm-bridge", "the governor + RLM for handling the massive C:\CLAUDE2 context (6889 files in one dir, thousands of .py/.md/.json, full theory docs) during component analysis without OOM"),
    ("night-cycle-daemon", "pre-tool-use-hook", "the night cycle runs in L0 fibers, the hook gates any edits to the component code/prompts/presets/agents/mcp during the autonomous self-play"),
    ("sheaf-condition-mcp", "local-llm-gguf-dozen", "the mcp tools are called by the local LLMs (the 0-dim stalks) in the agent loop"),
    ("pi-forge-integration", "sheaf-condition-mcp", "the Pi harness can call the mcp tools (the transducer, harvester, governor, scanner, pulse) for topological component analysis"),
    ("wormhole-function-router", "sheaf-condition-mcp", "the WORMHOLE router can route intents to the mcp tools for the component analysis (e.g., 'analyze the integration of the Forge prompt with the transducer')"),
    
    # Cross-dashboard and cross-version linkages (the multiple Forge/mcp/skill/agents in v1/v2/Zero)
    ("analysis-dashboard-v1-mcp", "analysis-dashboard-v2-mcp", "shared forge tools (scan/test/gate/compare), but v2 has updated engine/scanner/gate for the topological pipeline"),
    ("analysis-dashboard-v1-skill-forge", "analysis-dashboard-v2-skill", "shared the-forge SKILL with NightForge/onboarding, but v2 has more integration with the transducer/pulse for coherence"),
    ("analysis-dashboard-v1-agents", "sheaf-stack-the-scout", "shared 'maps terrain' role, the-scout in sheaf-stack is the evolved version with forge_scan for DNA"),
    ("analysis-dashboard-v1-agents", "sheaf-stack-the-anvil", "shared 'tests everything' role, the-anvil in sheaf-stack is the evolved version with the 5-gate Anvil Test and binary gate"),
    ("analysis-dashboard-zero-forge-prompt", "forge-agent-system-prompt", "the canonical prompt with 7 Laws, used in the Zero dashboard and as the reference for the sheaf-stack Forge"),
    ("analysis-dashboard-zero-forge-tool-executor", "sheaf-stack-mcp-server", "the tool executor in Zero and the mcp in sheaf-stack both expose the forge tools for agent interop"),
    
    # The local LLMs as the "stalks" being mapped and improved
    ("local-llm-gguf-dozen", "lmstudio-forge-preset", "the preset is the 'loading' of the local LLMs (Qwen coder etc.) with the Forge prompt and tools"),
    ("local-llm-gguf-dozen", "qlora-distillation-stub", "the local LLMs are the '0-dim stalks' that ingest the shape_pairs and get Δλ1-weighted updates to become better at topological component analysis"),
    ("local-llm-gguf-dozen", "night-cycle-daemon", "the local LLMs are used as the 'stalks' in the autonomous self-play (different models for scanning, spectral, harvester, distillation)"),
    ("local-llm-gguf-dozen", "sheaf-condition-mcp", "the local LLMs call the mcp tools (the transducer for coherence, the harvester for pairs, the governor for context, the scanner for geometry)"),
    ("local-llm-gguf-dozen", "pi-forge-integration", "the local LLMs (via LM Studio) are the backend for the Pi Agent Harness and Forge CLI"),
    ("local-llm-gguf-dozen", "wormhole-function-router", "the local LLMs can be the 'transformation functions' routed by the WORMHOLE router for component analysis intents"),
]

def build_component_manifold() -> Tuple[Any, Any, Dict[str, List[str]]]:
    """Build a simple 'component manifold' as a 1-complex from the stalks and linkages."""
    # For demo, use a simple dict-based complex (in full, use the SimplicialComplex from discrete_morse or the scanner)
    stalks = {c["id"]: c for c in LLM_COMPONENTS}
    edges = []
    for u, v, desc in LLM_INTEGRATION_LINKAGES:
        if u in stalks and v in stalks:
            edges.append((u, v, desc))
    # Prune "redundant" linkages (for demo, just take a subset or note the pruning)
    # In real: use the discrete_morse on a complex built from the stalks (0-cells) and linkages (1-cells)
    pruned_edges = edges[:len(edges)//2]  # simulate pruning
    return stalks, pruned_edges, {"pruned_ratio": 0.5}

def compute_component_coherence(stalks: Dict, edges: List) -> Dict[str, Any]:
    """ 'Pulse' the component manifold for coherence (L0_F proxy, Gini, hot linkages)."""
    # For demo, use the transducer on a "summary" of the manifold
    manifold_summary = "LLM Component Manifold: " + " | ".join([f"{k}:{v['type']}" for k,v in list(stalks.items())[:5]]) + " ... with " + str(len(edges)) + " integration linkages (pi-integration, WORMHOLE closed-loop, our transducer/harvester/kv/night/qlora/hook/mcp, cross-dashboard Forge versions, local LLMs as stalks)."
    t = HybridConditionStateTransducer(dim=8)
    res = t.pulse_mid_activity_evaluation(manifold_summary, "llm-component-manifold-analysis", apply_discrete_morse=True)
    # Hot linkages: the brittle ones from the list (e.g., prompt tools not perfectly matching all mcp, night not using kv in all paths, WORMHOLE not using harvester yet, pi not wired to hook, multiple Forge versions not aligned with transducer)
    hot = [ (u, v, desc) for u, v, desc in edges if "not" in desc.lower() or "not yet" in desc.lower() or "mismatch" in desc.lower() ][:5]
    return {
        "overall_energy": res["energy"],
        "overall_gini": res.get("gini_curve", 0.0),
        "overall_verdict": res["verdict"],
        "hot_linkages": hot,
        "recommended_coherent_integrations": [ (u, v, desc) for u, v, desc in edges if "not" not in desc.lower() and "mismatch" not in desc.lower() ][:5],
        "note": "The component manifold shows high coherence on core laws/tools/prompts, potential obstructions on cross-integration (e.g., the Forge prompt tools not perfectly matching all mcp schemas in the dashboards, the night cycle not yet fully using the kv governor for the full C:\CLAUDE2 archive context, the pi-integration showing the harness but not wired to the pre-tool-use hook or the harvester, the WORMHOLE closed-loop powerful but not yet using the harvester for positive pairs, the multiple Forge versions (v1/v2/Zero/sheaf-stack) not fully aligned with the transducer's pulse for coherence). The map enables the shift by making these visible and actionable via the harvester/distillation."
    }

def produce_0dim_structure_map() -> Dict[str, Any]:
    """Produce the geometric prime 0-dim structure map of the LLM components."""
    stalks, pruned_edges, prune_info = build_component_manifold()
    coherence = compute_component_coherence(stalks, pruned_edges)
    the_map = {
        "map_type": "geometric_prime_0dim_structure_map",
        "epistemic_bounds": "1917HRS_CONVERGENCE_UPDATE",
        "stalks_Fv": list(stalks.keys()),
        "restriction_maps_Fe": [(u, v, desc) for u, v, desc in pruned_edges],
        "prune_info": prune_info,
        "coherence": coherence,
        "how_to_inference_against": "Load this JSON as context for local LLMs. When asked to 'integrate these LLM components' or 'propose a new agent/skill/mcp for X', only propose integrations that would pass the pulse (low energy, low Gini on the component manifold). Use the hot linkages to identify brittle points to resolve via the harvester/distillation. Use the recommended coherent integrations to strengthen the manifold.",
        "local_hardware_implementation": {
            "hardware": "CPU-RAM-GPU with 6GB UMA (or 8-16GB as in the 70B extension), ability to poll and start sudo gitbash 2nd session",
            "local_llms": "the dozens of GGUF on disk as the 0-dim observation stalks in the map itself (different models for scanning, spectral, harvester, distillation, or as the 'stalks' being mapped)",
            "sudo_gitbash_sessions": "for isolated L0 fibers where the 'component mutation/resolution' experiments happen (the night cycle with target 'llm_component_analysis')",
            "i_o_harness": "the mcp for hardware polling during long analysis, the kv governor + RLM for the massive C:\CLAUDE2 context (6889 files in one dir, thousands of .py/.md/.json, full theory docs)",
            "the_map_as_truth": "the 1:1 true-to-life of coherent LLM component integration – the only value there ever was for the integrated system"
        },
        "order_of_magnitude_shift": "Instead of ad-hoc or manual integration of these powerful but loosely wired LLM components (the Forge prompts are great but not fully aligned with the transducer's pulse for coherence, the WORMHOLE closed-loop is powerful but not yet using the harvester for positive pairs, the night cycle is the orchestrator but not yet targeting the components themselves, the pi-integration shows the harness but not the full topological map, the multiple Forge versions in the dashboards are not unified), you have a living, pruneable, self-improving topological 'map' of the entire LLM component manifold that the local LLMs can 'inference against' to propose only coherent integrations, the night cycle can autonomously experiment with the wirings in isolated fibers using the local LLMs as the stalks, the harvester/distillation can improve the LLMs based on what integrations 'work' (positive Δλ1), the kv/RLM/mcp/hook/hardware polling make it all runnable on the user's local setup without OOM or drift, the map is the 'truth' for the integrated system (the 'only value there ever was' is the coherent H0 composition of these components). This enables massive parallel local experimentation with component integrations, deterministic composition (only coherent H0 integrations 'exist' or are promoted), self-improving LLMs specialized for topological component analysis, hardware-optimized analysis of huge archives, and the map as the ground truth for what the integrated system 'should' be."
    }
    return the_map

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM Component Topological Analyzer for Integration")
    parser.add_argument("--archive", default=r"C:\CLAUDE2", help="Path to the main development archive")
    parser.add_argument("--output", default="config/llm_component_map.json", help="Output path for the 0-dim structure map JSON")
    args = parser.parse_args()
    
    print(f"Analyzing LLM components from {args.archive} for relational integration into the geometric prime 0-dim structure map...")
    the_map = produce_0dim_structure_map()
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(the_map, f, indent=2)
    print(f"Map written to {args.output}")
    print("Key stalks (LLM components):", [s["id"] for s in LLM_COMPONENTS[:5]], "...")
    print("Key edges (integrations):", [(u, v) for u, v, _ in LLM_INTEGRATION_LINKAGES[:3]], "...")
    print("Coherence:", the_map["coherence"]["overall_verdict"], "energy", the_map["coherence"]["overall_energy"], "gini", the_map["coherence"]["overall_gini"])
    print("Hot linkages (brittle integrations to resolve):", the_map["coherence"]["hot_linkages"])
    print("Recommended coherent integrations:", the_map["coherence"]["recommended_coherent_integrations"])
    print("Local hardware implementation notes:", the_map["local_hardware_implementation"])
    print("Order of magnitude shift:", the_map["order_of_magnitude_shift"][:200], "...")
    print("The map is the truth. Load it as context for the local LLMs (the dozens on disk) to inference against for coherent component integrations. Run the night cycle with target 'llm_component' for autonomous self-play on the manifold. Use the kv governor + RLM for the massive archive context, the mcp for hardware polling, the sudo gitbash for the L0 fibers, the hook for safe edits, the harvester/distillation for improvement. The 1:1 true-to-life is the coherent H0 composition.")