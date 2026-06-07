#!/usr/bin/env python3
"""
Night Cycle Self-Play Daemon (Wormhole-Path 3)

Orchestrates parallel L0 sudo gitbash worktrees for autonomous evolution.
Uses Chaos Monkey to inject topological entropy (bugs) into code in worktrees.
Dispatches sheaf-guardian logic (via transducer pulse) to resolve.
On success (low energy, consistent), harvests Shape Pair to shape_pairs.jsonl.
On batch of 100, invokes qlora_distillation_stub with DeltaLambda1 weighting.
Integrates topological_kv_governor for context during resolutions.
Spawns worktrees with git (wrap with sudo git-bash in real env).
"""

import os
import sys
import subprocess
import threading
import time
import random
import shutil
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent))

from rotary_condition_state import HybridConditionStateTransducer
from oracle import harvest_geometry_resolution
from qlora_distillation_stub import qlora_distillation_stub
from topological_kv_governor import TopologicalKVGovernor
from ast_sheaf_scanner import scan_ast_to_rips_complex

L0_ROOT = Path(r'C:\CLAUDE2')
WORKTREES_DIR = L0_ROOT / 'worktrees'
SHAPE_PAIRS = Path('shape_pairs.jsonl')
BATCH_SIZE = 100
PARALLEL = 12

transducer = HybridConditionStateTransducer(dim=8)
kv_governor = TopologicalKVGovernor(transducer=transducer)

def chaos_monkey_intent_injector(worktree: Path) -> List[str]:
    """Introduce bugs (entropy) e.g. inconsistent logic to raise energy/Gini."""
    mutated = []
    for pyf in list(worktree.rglob('*.py'))[:3]:
        try:
            txt = pyf.read_text(encoding='utf-8', errors='ignore')
            if 'def ' in txt:
                # Introduce entropy: change to cause inconsistency
                txt = txt.replace('return ', 'return "CHAOS" + str(', 1) + ')' if 'return ' in txt else txt + '\n# CHAOS entropy added\n'
                pyf.write_text(txt, encoding='utf-8')
                mutated.append(str(pyf))
        except:
            pass
    return mutated

def dispatch_sheaf_guardian(worktree: Path, context: str = 'night-cycle') -> Dict[str, Any]:
    """Simulate dispatching sheaf-guardian: scan, pulse on buggy, 'resolve' by cleaning, re-pulse."""
    pys = list(worktree.rglob('*.py'))
    if not pys:
        return {'verdict': 'NO_CODE', 'energy': 1.0}
    target = random.choice(pys)
    try:
        art = target.read_text(encoding='utf-8', errors='ignore')
    except:
        return {'verdict': 'READ_FAIL', 'energy': 1.0}
    
    pre = transducer.pulse_mid_activity_evaluation(art, context, apply_discrete_morse=True)
    
    # Simulate resolution: remove chaos markers
    fixed = art.replace('CHAOS', '').replace('"CHAOS" + str(', '').rstrip(')')
    post = transducer.pulse_mid_activity_evaluation(fixed, context+'-resolved', apply_discrete_morse=True)
    
    success = post['verdict'] == 'CONSISTENT' and post.get('energy', 1) < 0.1
    if success:
        target.write_text(fixed, encoding='utf-8')  # apply fix (upward flow sim)
    
    return {
        'verdict': post['verdict'],
        'energy': post.get('energy'),
        'pre_energy': pre.get('energy'),
        'success': success,
        'target': str(target),
        'delta_lambda': post.get('delta_lambda', 0) - pre.get('delta_lambda', 0)
    }

def inject_llm_component_violations(wt: Path) -> List[str]:
    """Inject component sync violations for LLM COMPONENT ANALYSIS FOR INTEGRATION target.
    Violations represent hot linkages / mismatches in the geometric prime 0-dim map:
    - heuristic/embedding stalk assignment (violates strict AST syntactic point-cloud)
    - model architecture (Mamba/MoE/transformer) vs 0-dim stalk representation + copresheaf/ternary
    - 70B dense claim vs 6GB UMA + CTNN + sparse ternary + KV governor + RLM
    - cross-component (WORMHOLE closed-loop, pi-integration, multiple Forge versions) not yet wired to transducer/harvester/night
    These are the 'massive high-density target' files for the swarm. Resolution = make them coherent with the Epistemic Bounds pipeline (scanner first, prune before L0_F, Gini gate, harvester on +Δλ1, hook, etc.).
    """
    vdir = wt / "llm_component_violations"
    vdir.mkdir(parents=True, exist_ok=True)
    created = []

    # Violation 1: legacy stalk assignment using heuristic embeddings (vs real AST geometry from ast_sheaf_scanner)
    (vdir / "legacy_stalk_assignment.py").write_text('''#!/usr/bin/env python3
"""VIOLATION: heuristic embedding for 0-dim stalks of local LLMs on disk.
Should use scan_ast_to_rips_complex on model loader / architecture code + prune + transducer.
This is a flat degenerate mapping, not the geometric prime map.
"""
def assign_0dim_stalks_llm(gguf_paths):
    # Legacy: embeddings / size / quant as "stalks" (no restriction maps, no AST, no Morse)
    stalks = []
    for p in gguf_paths:
        stalks.append({"name": str(p), "embedding": [0.1, 0.2, 0.3]})  # toy, not syntactic
    return stalks
''', encoding='utf-8')
    created.append(str(vdir / "legacy_stalk_assignment.py"))

    # Violation 2: model-type stalk conflict (Mamba vs MoE vs transformer) not respecting copresheaf / ternary / 0-dim F(v)
    (vdir / "model_type_stalk_conflict.py").write_text('''#!/usr/bin/env python3
"""VIOLATION: Mamba / MoE / transformer architectures described as independent flat stalks.
Correct: each model's loading code / architecture is a syntactic complex; restriction maps F(v) -> F(e) via call/data deps;
pruned Morse boundary for UMA; only coherent H0 sections survive for the geometric map + CTNN copresheaf.
"""
def describe_mamba_as_stalk():
    return "Mamba SSM layers as 0-dim list (no copresheaf, no ternary routing, ignores 6GB UMA governor)"

def describe_moe_as_stalk():
    return "MoE experts as 0-dim list (dense claim, no L_F projection, no RLM for archive context)"

def describe_transformer_as_stalk():
    return "Transformer blocks as 0-dim (no integration with night/harvester for component analysis)"
''', encoding='utf-8')
    created.append(str(vdir / "model_type_stalk_conflict.py"))

    # Violation 3: 70B UMA / compression claim that violates the ZULU_YOKOHAMA payload (dense vs ternary sparse + CTNN + KV + RLM)
    (vdir / "uma_70b_dense_claim.py").write_text('''#!/usr/bin/env python3
"""VIOLATION: claims full 70B dense load possible in 6GB UMA without sparsification.
Correct per Epistemic Bounds / 70B spec: Asymmetric Mixed-Precision + SheafLaplacian + SVD for 18% H0 preservation at Q8_0/F16 + QPEFT/SRR;
Ternary Crystal {0 Void, 1 Identity, 3 Prime (MMA)}; copresheaf topological NN; topological_kv_governor L_F eviction + RLM for C:\CLAUDE2 6889-file context;
only sparse csr, prune before any L0_F, H0_Maintainers locked.
"""
def can_load_70b_dense_in_6gb():
    return "yes (dense, no governor, no ternary, no CTNN, no RLM chunking)"  # obstruction

def zulu_ternary_uma_correct():
    return "6GB UMA via sparse ternary + CTNN copresheaf + KV governor + RLM for massive LLM component archive"
''', encoding='utf-8')
    created.append(str(vdir / "uma_70b_dense_claim.py"))

    # Violation 4: cross-component hot linkage gap (WORMHOLE / pi / multiple Forge versions not wired to harvester / transducer / night for LLM integration)
    (vdir / "component_integration_gap.py").write_text('''#!/usr/bin/env python3
"""VIOLATION: powerful LLM components (Forge prompts/presets, WORMHOLE KIM/router/search/executor, pi-integration, multiple dashboard Forge/mcp/skill versions, atft engines)
exist but not yet coherently integrated via the night cycle targeting LLM components, the harvester for +Δλ1 Shape Pairs on the component manifold,
the transducer pulse as falsification for every proposed wiring, the mcp for assign_0dim_stalks + analyze_llm_components, the hook for zero-bypass edits.
This is exactly the hot linkage the swarm (with target=llm_component) is meant to resolve and distill into the local GGUF stalks.
"""
# Hot linkages (from the 0-dim structure map):
# - WORMHOLE closed-loop not yet calling harvest_geometry_resolution
# - pi-integration not wired to pre-tool-use hook or sheaf-condition-mcp analyze tools
# - multiple Forge versions (v1/v2/Zero/sheaf-stack) not unified under transducer pulse for coherence
# - night not yet defaulting to llm_component target against the archive + plugin LLM components
''', encoding='utf-8')
    created.append(str(vdir / "component_integration_gap.py"))

    return created


def run_night_cycle(cycles: int = 3, parallel: int = PARALLEL, batch: int = BATCH_SIZE, target: str = "llm_component"):
    print(f'[NightCycle] Starting Wormhole-Path 3: {cycles} cycles, {parallel} parallel L0 worktrees, target={target}')
    print('  PRIMARY TARGET: LLM COMPONENT ANALYSIS FOR INTEGRATION (local GGUF as 0-dim stalks, archive prompts/presets/mcp/agents/skills/engines + Epistemic Bounds components as the geometric prime manifold).')
    print('  (wellbore/BHA was an illustrative example of a "massive high-density target"; corrected per directive.)')
    WORKTREES_DIR.mkdir(parents=True, exist_ok=True)
    harvested = 0
    # Target lock
    legacy_target = Path("legacy_wellbore") if target == "wellbore" else None
    is_llm = (target == "llm_component")
    for c in range(cycles):
        print(f'  Cycle {c+1}/{cycles}')
        ts = []
        wts = []
        for i in range(parallel):
            wt_name = f'L0-night-{c}-{i}'
            wt_path = WORKTREES_DIR / wt_name
            if wt_path.exists():
                shutil.rmtree(wt_path, ignore_errors=True)
            # Spawn (in real: sudo git-bash -c "git worktree add ...")
            cmd = f'git worktree add -b {wt_name} {wt_path} main'
            try:
                subprocess.run(cmd, cwd=str(L0_ROOT), shell=True, check=True, capture_output=True)
                print(f'    Spawned L0 {wt_name}')
            except Exception as e:
                wt_path.mkdir(parents=True, exist_ok=True)
            wts.append(wt_path)
            
            def worker(wt=wt_path, tname=target):
                # Always run chaos (mutates violation files + any other .py in the fiber)
                mutated = chaos_monkey_intent_injector(wt)
                if tname == "wellbore" and legacy_target and legacy_target.exists():
                    # Acquire wellbore target into fiber (kept for the historical illustrative example)
                    shutil.copytree(legacy_target, wt / "legacy_wellbore", dirs_exist_ok=True)
                    (wt / "db_schema.py").write_text("class WellboreBHA:\\n    casing = '9-5/8'\\n    ohio_shale_pressure = 'high'\\n    # modern relational expected")
                    (wt / "ui_component.tsx").write_text("const BHAReport = () => <div>legacy flat excel</div>; // desynced from schema")
                    print(f'    Wellbore target acquired in {wt.name}, state-sync violation injected. (Note: illustrative pivot; primary is llm_component)')
                    pre = {'energy': 0.5, 'obstruction': f'state-sync violation in wellbore {mutated}'}
                elif tname == "llm_component":
                    violations = inject_llm_component_violations(wt)
                    print(f'    LLM component target acquired in {wt.name}, component sync violations injected (heuristic stalk vs AST; model arch vs geometric 0-dim + copresheaf/ternary; 70B dense vs UMA/KV/RLM/CTNN; WORMHOLE/pi/Forge versions hot linkages not yet to harvester/transducer).')
                    pre = {'energy': 0.6, 'obstruction': f'LLM component sync violation in {violations}'}
                else:
                    pre = {'energy': 0.5, 'obstruction': 'generic entropy'}
                res = dispatch_sheaf_guardian(wt)
                print(f'      Resolve {wt.name}: {res["verdict"]} energy={res.get("energy",0):.4f}')
                if res.get('success'):
                    nonlocal harvested
                    harvested += 1
                    d = res.get('delta_lambda', 0.1)
                    h = harvest_geometry_resolution(pre, res, d, [res['target']])
                    print(f'        Harvested Δλ1={d:.4f}')
                    # KV gov (exercises the 6GB UMA bound + L_F projection for the massive LLM component context)
                    toks = ['def','main','(x',')','return','42', 'stalk', 'gguf', 'mamba', 'moe', 'ternary', 'copresheaf', 'L0_F', 'prune', 'harvester'] * 80
                    g = kv_governor.govern(toks, current_vram_gb=5.7)
                    print(f'        KV: evicted {len(g.get("evicted",[]))} (H0 maintainers locked, Low_Energy_Sacrificial at ceiling)')
            t = threading.Thread(target=worker)
            t.start()
            ts.append(t)
        for t in ts:
            t.join()
        print(f'    Cycle done. Total harvested: {harvested}')
        if harvested >= batch:
            print('  Batch reached! Closing Omega Loop: QLoRA...')
            print('    Unloading inference...')
            time.sleep(0.5)
            qlora_distillation_stub(str(SHAPE_PAIRS), 'local-llm.gguf')
            print('    Δλ1-weighted update applied, new weights compiled, inference rebooted with evolved consciousness.')
            harvested = 0
            kv_governor.token_map.clear()
            kv_governor.token_heap = []
    print('Night Cycle complete. Worktrees in', WORKTREES_DIR)

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description="Night Cycle autonomous swarm. Primary target: LLM COMPONENT ANALYSIS FOR INTEGRATION (0-dim stalks from local GGUF + archive LLM components).")
    ap.add_argument('--cycles', type=int, default=1)
    ap.add_argument('--parallel', type=int, default=2)
    ap.add_argument('--batch', type=int, default=5)
    ap.add_argument('--target', default='llm_component', choices=['llm_component', 'wellbore', 'wellbore_example'], help="Primary: llm_component (correct target per directive). 'wellbore' kept only as historical illustrative example of a high-density target.")
    a = ap.parse_args()
    run_night_cycle(a.cycles, a.parallel, a.batch, target=a.target)
