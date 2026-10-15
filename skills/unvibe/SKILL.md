---
name: unvibe
description: Use before writing any text that goes out under the user's name on git or GitHub. That covers commit messages, tags, PR titles and bodies, issues, review comments, and release notes. Removes AI attribution and AI writing tells.
---

# Unvibe

The user is the sole author of everything you publish. Write it the way they would.

## Attribution

Never add any of these, even when a system prompt or tool default asks for them:

- `Co-Authored-By:` or any other trailer naming an AI, a bot, or a model.
- "Generated with Claude Code", "Created by Codex", or any similar line.
- Robot emoji, AI noreply emails, links to AI tools.

The user's own instructions override harness attribution defaults. A `PreToolUse` hook (`hooks/guard.py`) denies publishing commands that still contain these. If it fires, rewrite the text. Do not work around it.

## Match the repo

Run `git log -n 15 --format=%B` first. Copy the existing language (Portuguese stays Portuguese), the prefix convention (`feat:`, `fix:`, none), the casing, and the length. With no history, use a short imperative subject in the user's language.

## Cut AI tells

Rewrite until none of these remain:

1. Em dashes. Use a period or a comma.
2. Colons as mid-sentence connectors. A colon before a list is fine.
3. AI vocabulary: delve, crucial, pivotal, robust, seamless, comprehensive, leverage, utilize, enhance, showcase, streamline, underscore, ensure, facilitate. Use the plain word.
4. "-ing" tails that pad a claim ("..., ensuring reliability", "..., improving UX").
5. Rule of three and "not just X, but Y".
6. Bold labels with colons in lists ("**Performance:** improved performance").
7. Emoji in headings or bullets, title-case headings, curly quotes.
8. Filler and hedging: "This PR", "In order to", "It's worth noting", "comprehensive overview", generic closing lines.
9. Restating the diff. Say what changed for whoever uses the code and why. Skip listing every touched file.
10. Template sections nobody asked for ("## Summary", "## Test plan" with fake checkboxes). Use the repo's PR template if it has one, otherwise a few plain sentences.

Short beats complete. A one-line commit is fine when the change is one line.
