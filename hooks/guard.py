#!/usr/bin/env python3
"""PreToolUse guard: blocks git/GitHub publishing, artifacts, docs and .md files that carry AI attribution or obvious AI tells."""
import json
import re
import sys

RULES = [
    (re.compile(r"co-authored-by:", re.I), "Remove the Co-Authored-By trailer. The user is the only author."),
    (re.compile(r"generated (with|by) .{0,40}(claude|codex|copilot|cursor|gpt|gemini|\bai\b)", re.I),
     "Remove the 'Generated with ...' line. No AI attribution."),
    (re.compile(r"🤖"), "Remove the robot emoji."),
    (re.compile(r"noreply@anthropic\.com|noreply@openai\.com", re.I), "Remove the AI author email."),
    (re.compile(r"—|&mdash;|&#8212;|&#x2014;", re.I), "Remove em dashes. Use a period or a comma."),
]

PUBLISH_CMD = re.compile(r"\b(git\s+(commit|tag|notes|merge)|gh\s+(pr|issue|release|api|gist))\b")
FILE_ARG = re.compile(r"(?:-F|--file|--body-file|--notes-file)[=\s]+(\"[^\"]+\"|'[^']+'|\S+)")


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return ""


def publish_text(tool_name, tool_input):
    if tool_name == "Bash":
        cmd = tool_input.get("command", "")
        if not PUBLISH_CMD.search(cmd):
            return ""
        text = cmd
        for path in FILE_ARG.findall(cmd):
            path = path.strip("'\"")
            if path != "-":
                text += "\n" + read(path)
        return text
    if tool_name == "Artifact":
        return read(tool_input.get("file_path", ""))
    # ponytail: only .md, code files carry em dashes in strings and test data
    if tool_name in ("Write", "Edit") and tool_input.get("file_path", "").endswith(".md"):
        return tool_input.get("content") or tool_input.get("new_string") or ""
    if "github" in tool_name.lower() or "claude_docs" in tool_name.lower():
        return json.dumps(tool_input, ensure_ascii=False)
    return ""


def violations(text):
    return [msg for rx, msg in RULES if rx.search(text)]


def main():
    event = json.load(sys.stdin)
    found = violations(publish_text(event.get("tool_name", ""), event.get("tool_input") or {}))
    if not found:
        return
    reason = "unvibe blocked this. This text goes out in the user's name. " + " ".join(found) + \
        " Rewrite it following the unvibe skill and retry."
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))


if __name__ == "__main__":
    main()
