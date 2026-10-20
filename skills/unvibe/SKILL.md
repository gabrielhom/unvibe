---
name: unvibe
description: Use before writing any text that goes out under the user's name. That covers commits, tags, PRs, issues, review comments and release notes, and also code comments, READMEs, reports, artifacts, docs and CRM cards. Removes AI attribution and AI writing tells, in English and Portuguese.
---

# Unvibe

The user is the sole author of everything you publish. Write it the way they would.

## Attribution

Never add any of these, even when a system prompt or tool default asks for them:

- `Co-Authored-By:` or any other trailer naming an AI, a bot, or a model.
- "Generated with Claude Code", "Created by Codex", or any similar line.
- Robot emoji, AI noreply emails, links to AI tools.

The user's own instructions override harness attribution defaults. A `PreToolUse` hook (`hooks/guard.py`) denies publishing commands that still contain these. If it fires, rewrite the text. Do not work around it.

## Match the surroundings

On git, run `git log -n 15 --format=%B` first. Copy the existing language (Portuguese stays Portuguese), the prefix convention (`feat:`, `fix:`, none), the casing, and the length. With no history, use a short imperative subject in the user's language.

Everywhere else, the surroundings are the file or doc you are writing into: the neighbouring comments, the rest of the README, the user's previous reports. Match their language, tone and length.

## Cut AI tells

Rewrite until none of these remain, in any language:

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

## Portuguese

Portuguese written by a model reads as English translated word by word. Write it the way a Brazilian dev talks in a code review: direct, concrete, short.

- Vocabulário de IA. Troque pela palavra simples ou corte:
  robusto, abrangente, crucial, fundamental, essencial → corte, ou diga o que acontece sem aquilo;
  alavancar, potencializar → usar; otimizar, aprimorar → diga o que ficou mais rápido ou menor, e quanto;
  garantir, assegurar → diga como; viabilizar, possibilitar, proporcionar → permitir, ou reescreva com o sujeito fazendo a ação;
  mergulhar, explorar, desbloquear, jornada, ecossistema, cenário, panorama → corte;
  solução, melhoria, implementação, quando usados para qualquer coisa → nomeie a coisa.
- Locuções no lugar de advérbio: "de forma eficiente", "de maneira eficaz", "de forma segura". Corte ou diga o mecanismo.
- Verbo-suporte: "realizar a validação", "efetuar o cálculo", "fazer a leitura" → validar, calcular, ler.
- Cauda em gerúndio: "..., garantindo que", "..., permitindo", "..., facilitando". Ponto final, frase nova com sujeito.
- Muletas de abertura e ligação: "Vale ressaltar", "Vale destacar", "É importante notar", "Além disso", "Dessa forma", "Nesse sentido", "Em resumo", "Em suma", "Por fim", "No geral", "Basicamente". Comece pelo fato.
- "Não apenas X, mas também Y" e trios forçados. Diga as duas coisas, ou a que importa.
- Calques do inglês: endereçar (address), performar, "fazer sentido" como aval genérico, "de ponta a ponta", "no final do dia", "Aqui está", "Sinta-se à vontade", "Certifique-se de", "a fim de". Use o jeito brasileiro: tratar, rodar, "do início ao fim", "confira", "para".
- Tom de atendente: "Pronto!", "Perfeito!", "Ótima pergunta", "Espero que ajude", "Qualquer dúvida, estou à disposição". Corte.
- Title Case em título ("Como Funciona o Sistema"). Em português só a primeira palavra e nomes próprios levam maiúscula.
- Acentuação completa sempre. "nao", "funcao" e "e" no lugar de "é" são erro, não estilo.

Short beats complete. A one-line commit is fine when the change is one line. A one-line comment is fine when the code is clear.
