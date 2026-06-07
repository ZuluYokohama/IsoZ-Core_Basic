# Phase-0 PR #1 Review & Diff Navigation Guide

**Goal**: Make the full phase-0 diff reliably consumable by humans and Grok Heavy even when GitHub''s large-diff UI is broken ("too big", load errors on Files changed / comments, slow rendering).

**PR**: https://github.com/ZuluYokohama/IsoZ-Core_Basic/pull/1
**Current tip**: cd0eb25 (the merge that connected histories)
**Large file status**: 82 MB ternary_70b_ggufmap.json removed from tip (raw.githubusercontent.com .../phase-0/config/ternary_70b_ggufmap.json → 404). .gitignore already protects it. Future pushes of small diffs will be clean.

## Why GitHub diff/comments are painful here
- Merge of completely unrelated histories (original main was a tiny skeleton; phase-0 carries the entire harness + WORMHOLE-PATH 5 + spectral + automation work).
- 8 commits, 42 files, thousands of lines.
- GitHub renderer chokes on the size + history.

This is a GitHub limitation, not a problem with the artifacts.

## Best ways to review the diff (199% reliable)

### 1. Commits tab on the PR (step-by-step, no big renderer)
Open the PR → "Commits" tab. The 8 commits are:

1. d49f6a9 — 2010HRS-2105HRS WORMHOLE-PATH 5 bare-metal llama.cpp (sheaf_svd_quantizer.py, src/ggml_ternary_shim.cpp, hardware_piping.py LlamaCppTopologicalBridge + governor + RLM, mcp_server tools, phase lock update)
2. 73dc88c — 2105 full plugin state after Path 5 (all deliverables + supporting night_cycle, README, maps)
3. 6e6b723 — 2112 HOTFIX (forward apply_discrete_morse through pulse wrapper + harden .gitignore for large artifacts)
4. b59e546 — 2142 spectral-auditor agent + skill (persistent homology whole-codebase audits)
5. 5a91546 — 2210/2215 Harness automation layer (harness-task-yield skill, harness-backlog-reviewer subagent, scripts/bootstrap-harness.sh, .mcp.json with GitHub MCP, PostToolUse hook for auto sheaf_coderabbit + task-yield, phase lock)
6. fadbfe2 — Improve bootstrap-harness.sh (the clean, functional VM version with dynamic python sheaf_coderabbit calls and fresh dated report)
7. 09559df — chore: untrack 82MB ternary_70b_ggufmap.json (the cleanup that stops GH001 on future pushes)
8. cd0eb25 — Merge main into phase-0 (connects the histories so the PR and diff became visible at all)

### 2. Local commands (exact diff, perfect for harness / Grok Heavy parsing)
```powershell
git fetch origin
git checkout phase-0
git reset --hard origin/phase-0   # make sure you are on the pushed merge

# Quick overview
git diff main...phase-0 --stat

# Full diff for parsing / saving
git diff main...phase-0 > phase0-full.diff

# Or per-file / per-commit style
git log --oneline main..phase-0
```

### 3. Existing dated task-yield reports (already in the tree)
- reports/2026-06-06_2210_2210-automation-synthesis-task-yield.md
- reports/2026-06-06_2215_2210-automation-verification-task-yield.md
- Earlier ones for spectral-auditor, full-backlog QC, etc.

These contain the guardian pulses, hot linkages, OBSTRUCTED verdicts (with the 5 linkages that this PR + automations close), and rectification steps.

### 4. This guide file (self-contained navigation)
The file `reports/phase0-pr-review-guide.md` (this content) lives in the branch for anyone who checks out phase-0.

## What the PR actually ships (high-level)
- The harness is now the operating system: task-yield automation, backlog reviewer subagent, VM bootstrap that does real dynamic verification, GitHub MCP for autonomous PRs/comments, PostToolUse A4 enforcement.
- Complete WORMHOLE-PATH 5 / LLM component / ternary / sheaf / night-cycle stack.
- All under Epistemic Bounds (prune-first, ker L⁰_F only, A4/pre-tool-use, Gini gate, dated task-yield with pull/diff/oversight/rectification, zero-bypass).
- The previous self-audits that correctly flagged OBSTRUCTED are now part of the public record and addressed.

## After this PR (exact next steps from the PR body)
1. Inside a grok session with the plugin: invoke harness-task-yield and/or the harness-backlog-reviewer subagent to expand sheaf_coderabbit across the remaining backlog files (sheaf_svd_quantizer.py, hardware_piping.py, mcp_server.py, README, hooks/pre-tool-use.sh, src/ggml_ternary_shim.cpp, more reports/config).
2. Produce the consolidated Sparsification & Preservation Report.
3. Close phase-0 only on CONSISTENT.
4. Proceed to gated benchmarks, IP draft, v0.2 packaging, night-cycle to bare-metal target.

Future work on the branch: just `git push origin phase-0` after normal commits. The PR will receive the new commits. No more history or large-file drama on the tip.

The diff is now pushed and public for Grok Heavy + the harness to parse as we discussed.

If anything else surfaces on the comments or diff rendering, paste the symptom and we will iterate immediately.
