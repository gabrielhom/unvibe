import json
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).with_name("guard.py")


def decision(tool_name, tool_input):
    out = subprocess.run([sys.executable, GUARD], input=json.dumps({"tool_name": tool_name, "tool_input": tool_input}),
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else "allow"


def bash(cmd):
    return decision("Bash", {"command": cmd})


assert bash('git commit -m "fix: x\n\nCo-Authored-By: Claude <noreply@anthropic.com>"') == "deny"
assert bash("gh pr create --title t --body '🤖 Generated with [Claude Code](https://claude.com/claude-code)'") == "deny"
assert bash('git commit -m "adiciona cache — mais rápido"') == "deny"
assert bash('git commit -m "fix: corrige timeout do login"') == "allow"
assert bash("echo 'Co-Authored-By: x'") == "allow", "non-publishing commands pass"
assert bash("git log --grep 'Co-authored-by'") == "allow", "reading history passes"

with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
    f.write("Resumo\n\nGenerated with Claude Code")
assert bash(f"gh pr create --title t --body-file {f.name}") == "deny", "body files are scanned"
assert bash(f"git commit -F {f.name}") == "deny", "commit message files are scanned"

assert decision("mcp__github__create_pull_request", {"body": "Co-authored-by: Codex"}) == "deny"
assert decision("Write", {"content": "Co-authored-by: x"}) == "allow"
assert decision("Write", {"file_path": "app.py", "content": "s = 'a — b'"}) == "allow", "code files pass"
assert decision("Write", {"file_path": "README.md", "content": "Rápido — e simples"}) == "deny"
assert decision("Edit", {"file_path": "docs/relatorio.md", "new_string": "ok &mdash; ok"}) == "deny"
assert decision("Edit", {"file_path": "README.md", "new_string": "Roda em 2 s."}) == "allow"
assert decision("mcp__claude_ai_Claude_Docs__batch", {"batch": [{"markdown": "Resumo — fim"}]}) == "deny"

with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
    f.write("<p>Relatório &mdash; outubro</p>")
assert decision("Artifact", {"file_path": f.name}) == "deny", "artifact pages are scanned"
assert decision("Artifact", {"action": "list"}) == "allow"
print("ok")
