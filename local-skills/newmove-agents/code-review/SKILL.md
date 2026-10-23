---
name: code-review
description: Revisar um diff proporcionalmente ao risco, cobrindo Standards e Spec, invariantes e impactos relacionados de correções.
---

# Code Review — Standards e Spec

Fonte do protocolo de revisão. [Implement](../implement/SKILL.md) define execução, gates e validade da evidência. Review estático encontra defeitos e lacunas; não certifica browser, API ou transporte não executados.

## Recorte comum

Resolva a base confiável para SHA; registre HEAD, arquivos/hunks da tarefa e novos arquivos. Use `git diff <base>...HEAD -- <arquivos>`, acrescido de `git diff --cached`, `git diff` e conteúdo dos novos arquivos pertinentes de `git ls-files --others --exclude-standard`. Recorte vazio/base inválida exige correção antes de delegar; não faça staging para revisar. Congele o recorte ou invalide conclusões afetadas por edições concorrentes.

Use o pedido e fontes já fornecidos como contrato. Se faltar referência, procure a issue vinculada conforme `docs/agents/issue-tracker.md`, depois spec relacionada; pergunte somente se a autoridade permanecer ambígua. Obsidian explícito/herdado usa o [adaptador](../spec-workspace/SKILL.md). Leia só critérios/decisões apontados. Sem spec disponível, declare o eixo Spec não executado, nunca aprovado.

Use recorte, contrato, padrões aplicáveis e provas/resultados/limites já disponíveis; quando houver reviewers, forneça o mesmo pacote. **Em delta de correção**, acrescente quatro respostas curtas:

1. Que comportamento motivou a correção e qual sua causa conhecida?
2. Que regra deve permanecer verdadeira?
3. Que estados/consumidores compartilham a condição alterada?
4. Qual menor cenário pode demonstrar regressão e que prova existe dele?

O reviewer verifica essas respostas no fluxo relacionado; não as aceita como verdade automática. Se estiverem ausentes, derive do diff/critério ou registre a lacuna específica, sem redescobrir todo o ambiente.

## Revisão proporcional

Use o risco classificado em [Implement](../implement/SKILL.md), preservando requisitos explícitos de revisão do ticket:

- **Baixo:** uma revisão focal pelo executor cobre Standards e Spec; sem dois subagentes automáticos. Não a apresente como revisão independente.
- **Médio:** revisão conjunta por padrão; separe Standards/Spec quando acoplamento compartilhado, variantes de comportamento, ambiguidade de regra ou interação entre fronteiras justificar análise independente. Registre brevemente o motivo no registro existente; risco crítico ou incerteza material pede escalonamento.
- **Alto:** um revisor independente cobre Standards e Spec e aprofunda as fronteiras afetadas. Dois revisores somente por exigência explícita ou riscos distintos que justifiquem a separação; autorização não implica dois agentes automaticamente.

Reutilize executor/revisor e subagentes já mobilizados nas reavaliações; revise delta e impactos no modo do risco atual. Amplie somente diante de nova superfície ou evidência invalidada. Tarefas já cobertas não pedem novos agentes.

- **Standards:** confira padrões documentados pertinentes e impacto técnico. Cite regra + arquivo/hunk em violações. Smells (duplicação, acoplamento, nomes opacos, abstração especulativa) são heurísticas, não obrigação automática de refatorar. Só destaque quando houver consequência concreta; padrões do projeto prevalecem. Não replique diagnóstico já coberto por ferramenta.
- **Spec:** confronte comportamento com requisitos e decisões; identifique omissão, implementação incorreta e escopo extra. Cite critério + cenário observável que falharia. Confira se a evidência contém o mecanismo necessário; mock/inspeção estática não provam fronteira real ausente.

Em qualquer modo, verifique impactos **relacionados ao delta**, sem revisar o ERP inteiro:

| Mudança | Impacto a conferir quando alcançável |
|---|---|
| Condição/estado | Outros estados no mesmo ramo; ordem temporal, revogação e efeitos. |
| Query/filtro | NULL, legado, outros clientes/unidades e estados derivados. |
| Componente compartilhado | Consumidores atingidos, CSS herdado, viewport e ação nativa. |
| Acesso/identidade | Efeitos antes de autorização, IDs alternativos, fallbacks e rotas genéricas. |
| Schema/bootstrap | Banco vazio e compatibilidade dos consumidores afetados. |
| Confirmação externa | Sucesso confirmado, rejeição e incerteza; variantes de campos obrigatórios conforme [TDD](../tdd/SKILL.md). |

Cada achado material informa violação, evidência, cenário de falha e impacto. Diferencie **defeito**, **lacuna de prova** e **sugestão opcional**. Uma hipótese sem mecanismo demonstrado pede investigação delimitada; não vira bug confirmado. Agrupe todos os achados materiais observados na rodada, sem truncá-los para cumprir limite artificial de palavras.

## Resultado

Na revisão conjunta, um parecer cobre Standards e Spec; na independente, preserve conclusões separadas. Mantenha IDs/origem dos achados e deduplique apenas ações equivalentes. Parecer aprovado vale para o recorte e alcance observados, não para o aceite integrado. Delta posterior pede revisão do delta e impactos; nova exploração ampla só com evidência de superfície adicional.

Use a resposta normal de revisão. Só persista artefato se solicitado; em Obsidian, use Validation/Index existentes. Sugestões sem violação não reabrem entrega atendida. O executor corrige achados materiais e fecha conforme Implement.
