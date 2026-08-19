---
name: review-workflow-global
description: Orquestra revisao completa com agentes secundarios em paralelo (codigo, seguranca, layout, UX/performance), consolida achados e retorna um parecer tecnico unico com severidade, evidencias e proximos passos.
---

# Review Workflow Global

## Objetivo

Executar um workflow de revisao multiagente, com spawn de agentes secundarios especializados, para analisar mudancas de ponta a ponta e devolver uma consolidacao unica com prioridade tecnica clara.

## Quando usar

Use quando o pedido for revisar mudancas, PRs, diffs, fluxos ou codigo em escopo medio/alto, especialmente quando houver risco de regressao, seguranca, UX, performance, permissao ou integracao.

Nao use para ajustes triviais de 1 arquivo sem superficie real de risco.

## Pre-Checks obrigatorios

1. Ler as instrucoes de repositorio (ex.: `AGENTS.md`) e obedecer politicas locais.
2. Carregar o padrao de qualidade em `C:\Users\Jetta\.codex\skills\_shared\tdd-decente.md` para qualquer mudanca comportamental detectada.
3. Mapear contexto minimo: objetivo da mudanca, arquivos tocados, risco e testes existentes.

## Regra de spawn

Esta skill deve criar agentes secundarios quando o usuario pedir analise ampla, multiangulo ou "revisar tudo".

Spawn padrao recomendado:

1. `reviewer` (corretude, regressao, cobertura, arquitetura)
2. `hacker-safado` (seguranca ofensiva realista)
3. `layout-reviewer` (layout/responsividade) quando houver UI
4. `designer` (hierarquia visual/polish) quando houver UI sensivel ao cliente
5. `ux-performance-auditor` (fluidez/performance percebida) quando houver UI, listas, tabelas, dashboards, modais
6. `severino` (triagem de ambiguidade e risco residual) para escopos nao triviais

## Contrato dos agentes

Cada agente deve receber apenas:

- objetivo da revisao
- diff/arquivos alterados
- riscos conhecidos
- criterios de aceitacao
- limites de escopo

Cada agente deve retornar:

- `verdict`: `APROVADO`, `APROVADO COM AJUSTES` ou `REPROVADO`
- achados com severidade (`CRITICO`, `ALTO`, `MEDIO`, `BAIXO`)
- evidencia objetiva (arquivo/linha/comportamento)
- impacto
- correcao requerida
- nivel de confianca

## Consolidacao obrigatoria

A consolidacao final deve:

1. Unificar duplicatas por causa raiz.
2. Priorizar por risco real, nesta ordem:
   - corretude critica e risco de dados
   - seguranca exploravel
   - regressao funcional
   - UX/performance quebrada
   - layout/design
   - lacuna de teste/TDD
3. Separar `confirmado` de `provavel`.
4. Destacar explicitamente lacunas de evidencia (ex.: testes nao executados).

## Politica de testes

Para mudanca comportamental:

1. Exigir teste de regressao que falharia sem a correcao.
2. Exigir teste no nivel mais proximo do uso real praticavel (fluxo/interacao/contrato), evitando cobertura apenas de helper.
3. Quando aplicável no ERP JETTA, exigir os comandos automatizados nativos mais próximos do escopo alterado, como `npm run test --workspace @erp-jetta/api`, `npm run test --workspace @erp-jetta/web`, `npm run lint` ou `npm run build`.
4. Não exigir o runner Python em reviews de rotina; usar a central de automação somente quando o usuário pedir ou quando um fluxo de deploy executado exigir isso.
5. Se testes não rodarem, marcar como risco residual bloqueante ou ressalva explícita.

## Formato da saida final

1. `Resumo tecnico`
2. `Escopo analisado`
3. `Agentes acionados`
4. `Findings consolidados` (ordenado por severidade)
5. `Cobertura e evidencias de teste`
6. `Status final` (`APROVADO`, `APROVADO COM RESSALVAS`, `REPROVADO`)
7. `Proximas acoes`
8. `Riscos remanescentes`

## Guardrails

- Nao permitir que agentes reviewers editem codigo de producao.
- Nao aprovar com finding critico confirmado em aberto.
- Nao inventar vulnerabilidade sem evidencia minima.
- Nao diluir achados importantes em preferencia de estilo.
- Nao ignorar falta de teste quando comportamento mudou.

## Prompt base de orquestracao

Use este prompt curto ao iniciar:

"Execute revisao multiagente do escopo informado. Rode em paralelo: reviewer, seguranca, e se houver UI tambem layout/design/ux-performance. Traga apenas achados com evidencia, severidade, impacto e correcao requerida. Consolide duplicatas por causa raiz e devolva parecer final unico com status e riscos remanescentes."

