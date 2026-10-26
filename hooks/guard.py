#!/usr/bin/env python3
"""PreToolUse guard: blocks git, GitHub reviews, artifacts, docs and .md files that carry agent attribution or obvious AI tells."""
import json
import re
import sys

# Unambiguous product names. Bare "cursor" is not in this list.
TOOLS = (
    r"claude(?:\s+code)?|codex|(?:github\s+)?copilot|cursor\s+agent|"
    r"chatgpt|grok(?:\s+bot)?|devin|junie|junin|coderabbit|jules|aider|"
    r"amazon\s+q|codeium|sourcery|tabnine"
)
# "cursor" and "gpt" also name ordinary things. Product casing always counts.
# Lowercase counts only when a noun does not follow ("cursor pagination" stays).
AMBIG = (
    r"Cursor\b|CURSOR\b|cursor\b(?!\s+[a-z])|"
    r"Gemini\b|GEMINI\b|gemini\b(?!\s+[a-z])|"
    r"GPT(?:[-\s]?\d+)?\b|gpt(?:[-\s]?\d+)?\b(?!\s+[a-z])|"
    r"Windsurf\b|WINDSURF\b|windsurf\b(?!\s+[a-z])|"
    r"Bot\b|BOT\b|bot\b(?!\s+[a-z])"
)
AI_WORD = r"ai\b(?:\s+assistant|\s+language\s+model|\s+model)?"
VERBS = (
    r"generated|written|created|made|authored|drafted|sent|assisted|powered|"
    r"reviewed|built|answered"
)
CREDIT_NAME = rf"(?:(?i:{AI_WORD}|{TOOLS})\b|{AMBIG})"
# Junin is also a place name. "via Junin" stays. "Written by Junin" does not.
VIA_TOOLS = (
    r"claude(?:\s+code)?|codex|(?:github\s+)?copilot|cursor\s+agent|"
    r"chatgpt|grok(?:\s+bot)?|devin|junie|coderabbit|jules|aider|"
    r"amazon\s+q|codeium|sourcery|tabnine"
)

RULES = [
    (re.compile(r"co-authored-by:", re.I),
     "Remove the Co-Authored-By trailer. The user is the only author."),
    (re.compile(r"\b(?:generated-by|assisted-by|made-with|written-by|created-by):", re.I),
     "Remove the attribution trailer. The user is the only author."),
    (re.compile(
        rf"(?i:\b(?:{VERBS})\s+(?:automatically\s+)?(?:with|by|via|from)\s+\[?\s*"
        rf"(?:(?:an?|the)\s+)?(?:(?:help|assistance)\s+of\s+)?(?:an?\s+)?)"
        rf"{CREDIT_NAME}"),
     "Remove the attribution line. The user is the only author."),
    (re.compile(rf"(?i:\bvia\s+(?:the\s+)?)(?:(?i:{VIA_TOOLS})\b)"),
     "Remove the via-tool footer."),
    (re.compile(
        r"\b(?:as an ai(?:\s+assistant|\s+language\s+model)?|as a language model|"
        r"i am an ai(?:\s+assistant|\s+language\s+model)?|"
        r"i['’]m an ai(?:\s+assistant|\s+language\s+model)?)\b",
        re.I),
     "Remove the line that speaks as an assistant. The voice is the user's."),
    (re.compile(r"\bai[\s-](?:generated|assisted|written|authored)\b", re.I),
     "Remove the authorship phrase."),
    (re.compile(
        r"\b(?:gerad[oa]s?|escrit[oa]s?|feit[oa]s?|criad[oa]s?|produzid[oa]s?|revisad[oa]s?|"
        r"redigid[oa]s?|assinad[oa]s?|respondid[oa]s?)"
        r"(?:\s+automaticamente)?\s+(?:por|pelo|pela)\s+(?:um |uma |o |a )?"
        r"(?:ia\b|i\.a\.|intelig[eê]ncia artificial|grok(?:\s+bot)?|claude(?:\s+code)?|codex|"
        r"(?:github\s+)?copilot|cursor\s+agent|chatgpt|devin|junie|junin|coderabbit|gemini|"
        r"gpt(?:[-\s]?\d+)?|assistente de ia|bot)\b",
        re.I),
     "Remove the Portuguese authorship line. The user is the only author."),
    (re.compile(
        r"\b(?:como\s+(?:um |uma )?)?assistente de\s+(?:ia\b|i\.a\.|intelig[eê]ncia artificial)\b|"
        r"\b(?:eu\s+)?sou\s+(?:um |uma )?(?:ia\b|i\.a\.|assistente de ia|modelo de ia)\b",
        re.I),
     "Remove the assistant sign-off."),
    (re.compile(
        r"\brevis[aã]o\s+(?:feita\s+)?por\s+(?:um |uma )?(?:ia\b|i\.a\.|intelig[eê]ncia artificial)\b|"
        r"\breview(?:ed)?\s+by\s+(?:an?\s+)?(?:ai(?:\s+assistant)?|grok(?:\s+bot)?|junin|junie|"
        r"cursor(?:\s+agent)?|copilot|claude|codex|devin)\b|"
        r"\((?:review|reviewed|revis[aã]o)(?:\s+feita)?\s+(?:by|por)\s+(?:an?\s+|um |uma )?"
        r"(?:ai(?:\s+assistant)?|ia|assistente de ia|grok(?:\s+bot)?|claude|codex|copilot|"
        r"cursor(?:\s+agent)?|junin|junie|devin)\)",
        re.I),
     "Remove the review signature. The review is the user's."),
    (re.compile(
        r"(?:^|[\s(])(?:—|–|--|-)\s*(?:grok bot|cursor agent|github copilot|junin|junie|"
        r"copilot|claude|codex|devin|grok|coderabbit|chatgpt|tabnine|codeium|sourcery|aider)\b"
        r"[ \t]*['\").,;:]*[ \t]*$",
        re.I | re.M),
     "Remove the bot signature."),
    (re.compile(
        r"(?:--author|user\.name)(?:=|\s+)['\"][^'\"]{0,120}"
        r"(?:cursor\s+agent|grok\s+bot|github\s+copilot|junie|junin)[^'\"]*['\"]",
        re.I),
     "The git author is the user. Remove the agent author."),
    (re.compile(r"🤖"), "Remove the robot emoji."),
    (re.compile(
        r"(?<![A-Za-z0-9._%+-])(?:"
        r"cursoragent@cursor\.com|"
        r"noreply@(?:anthropic|openai)\.com|"
        r"[\w.+-]+@x\.ai|"
        r"[\w.+-]*copilot[\w.-]*(?:\[bot\])?@(?:users\.noreply\.github\.com|github\.com)|"
        r"[\w.+-]*(?:devin-ai-integration|coderabbitai|gemini-code-assist|"
        r"google-labs-jules|jetbrains-junie)(?:\[bot\])?@users\.noreply\.github\.com"
        r")(?![A-Za-z0-9.-])",
        re.I),
     "Remove the agent author email."),
    (re.compile(
        r"(?<![A-Za-z0-9])cursor\.com/(?:agents|background-agent)(?![A-Za-z0-9-])|"
        r"cursor://\S*background-agent|"
        r"\bbcId=|"
        r"claude\.ai/code(?![A-Za-z0-9-])|"
        r"claude\.com/claude-code(?![A-Za-z0-9-])|"
        r"chatgpt\.com/(?:share|c|g|codex)(?![A-Za-z0-9-])|"
        r"chat\.openai\.com/(?:share|codex)(?![A-Za-z0-9-])|"
        r"(?<![A-Za-z0-9])(?:grok\.com|grok\.x\.ai|x\.ai/grok)\b|"
        r"x\.com/i/grok\b|"
        r"open-in-(?:cursor|web)\b|"
        r"\bopen in cursor\b|"
        r"\bopen in web\b(?!\s+[a-z])",
        re.I),
     "Remove the agent link or tool badge."),
    (re.compile(r"—|&mdash;|&#8212;|&#x2014;", re.I),
     "Remove em dashes. Use a period or a comma."),
]

# Flags may sit between git and the subcommand (`git -c user.email=... commit`).
_GIT_OPT = r"(?:-(?:c|C)\s+(?:\S*=)?(?:\"[^\"]*\"|'[^']*'|\S+)\s+|-[^\s]+\s+)"
PUBLISH_CMD = re.compile(
    rf"\bgit\s+(?:{_GIT_OPT})*(?:commit|tag|notes|merge)\b|\bgh\s+(?:pr|issue|release|api|gist)\b"
)
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
