---
name: new-move
description: Use when changing or planning Move's central multi-operation interface migration, operation-scoped data/actions, or reusable screen templates.
metadata:
  short-description: New Move
---

# New Move

Use este contexto ao trabalhar na transição do Move para uma base central, escalável e multioperação. Leia [o contexto completo da migração](../../../docs/move-central-migration.md) antes de alterar telas, navegação, dados por CC ou automações.

Regras de trabalho:

- Confirme a worktree, branch, estado de integração e rotas presentes antes de assumir que `/templates` ou uma tela migrada está disponível. Candidatos em worktrees isoladas e arquivos `.scratch` não comprovam integração.
- Reutilize os templates compartilhados do Move quando estiverem disponíveis na base autorizada; não replique telas legadas por operação.
- Preserve regras de negócio, scripts, integrações e automações que ainda tenham uso. Remova uma regra somente quando o escopo pedir e seus efeitos/consumidores estiverem compreendidos.
- Mantenha operação/CC explícito em dados e ações. A autorização é server-side; interface, rota antiga, cliente ou marca não concedem acesso.
- Isole listas, cargas, filtros, menus flutuantes, barras de ação e automações pelo CC selecionado. Preserve acesso e contexto ao alternar operações.
- Faça mudanças por fluxo, respeite consumidores legados ainda ativos e valide o comportamento real afetado.
- Esta skill fornece contexto, não autorização para CI, push, deploy, produção, integração de worktrees ou envios externos.

