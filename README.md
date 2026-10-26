# unvibe

Agentes não assinam meus commits. Este plugin faz duas coisas:

- `hooks/guard.py` roda antes de todo `git commit`, `git tag`, `gh pr` (criar, review, comentário e aprovação), `gh issue`, `gh release`, `gh api`, ferramenta MCP do GitHub e do Claude Docs, publicação de artifact e escrita em arquivo `.md`. Se o texto tiver trailer de coautoria, rodapé ou assinatura de agente, email de autor automático, link de execução, badge de ferramenta, frase que entrega a autoria (em inglês ou português) ou travessão, a chamada é negada e o agente reescreve.
- `skills/unvibe/SKILL.md` é a skill (formato Agent Skills) que o agente segue para escrever no estilo do repo e sem cara de IA, em inglês e português. Review, comentário e aprovação seguem a mesma regra. A voz do comentário é a minha.

## Instalar no Claude Code

```sh
claude plugin marketplace add gabrielhom/unvibe
claude plugin install unvibe@unvibe
```

Coloque também no `~/.claude/settings.json`, para o Claude Code parar de pedir a atribuição na origem:

```json
"attribution": { "commit": "", "pr": "" }
```

Outros agentes (Codex, Cursor, Grok, etc.) usam só a skill. Copie `skills/unvibe` para a pasta de skills deles.

## Testar

```sh
python3 hooks/test_guard.py
```

`gh pr create --body-file -` (corpo via stdin) não é verificado.
