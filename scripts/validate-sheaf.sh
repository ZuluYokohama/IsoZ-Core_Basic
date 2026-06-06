#!/usr/bin/env bash
# Simple validation helper for the specialized-agents / sheaf-guardian plugin.
# Run from the plugin root.
# Mirrors the spirit of plugin-dev validate-agent.sh etc.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "Validating specialized-agents plugin at $ROOT"

fail=0

check_file() {
  if [[ ! -f "$1" ]]; then
    echo "MISSING: $1"
    fail=1
  else
    echo "OK: $1"
  fi
}

echo "== Core structure =="
check_file "$ROOT/.claude-plugin/plugin.json"
check_file "$ROOT/.mcp.json"
check_file "$ROOT/agents/sheaf-guardian.md"
check_file "$ROOT/skills/sheaf-guardian/SKILL.md"
check_file "$ROOT/scripts/rotary_condition_state.py"
check_file "$ROOT/scripts/oracle.py"
check_file "$ROOT/scripts/mcp_server.py"
check_file "$ROOT/scripts/hardware_piping.py"
check_file "$ROOT/README.md"

echo

echo "== Agent frontmatter checks =="
if grep -q 'name: sheaf-guardian' "$ROOT/agents/sheaf-guardian.md" && \
   grep -q 'description:' "$ROOT/agents/sheaf-guardian.md" && \
   grep -q '<example>' "$ROOT/agents/sheaf-guardian.md"; then
  echo "OK: agent frontmatter and examples present"
else
  echo "FAIL: agent/sheaf-guardian.md frontmatter or triggering examples look incomplete"
  fail=1
fi

echo

echo "== MCP manifest =="
if grep -q 'sheaf-condition-mcp\|sheaf-condition' "$ROOT/.mcp.json" && grep -q 'scripts/mcp_server.py' "$ROOT/.mcp.json"; then
  echo "OK: .mcp.json references the server script"
else
  echo "FAIL: .mcp.json"
  fail=1
fi

echo

echo "== Python syntax (basic) =="
for py in scripts/*.py; do
  python -m py_compile "$py" && echo "OK syntax: $py" || { echo "FAIL syntax: $py"; fail=1; }
done

echo
if [[ $fail -eq 0 ]]; then
  echo "=== VALIDATION PASSED ==="
else
  echo "=== VALIDATION HAD FAILURES ==="
  exit 1
fi
