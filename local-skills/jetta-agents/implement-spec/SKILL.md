---
name: implement-spec
description: "Implement a specification in code."
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The goal is the authorized spec scope implemented and accepted on its working branch. PR/publication follows AGENTS authorization and CI restrictions.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

When the supplied spec or tickets belong to an Obsidian Spec Driven workspace, follow [the shared Spec Workspace Adapter](../spec-workspace/SKILL.md): read `Index.md`, the spec, and only the relevant frontier tickets; carry the resolved workspace through this workflow. Save workflow Markdown (research notes, handoffs, decisions, validation reports) there. Keep implementation source and required repository files in their technical locations. With no explicit or inherited workspace, use this skill unchanged.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

No ERP Jetta, cada fatia segue o processo canônico de [Implement](../implement/SKILL.md). Paralelismo exige contratos independentes, worktree/branch/runtime próprios e um único escritor por checkout; integração é serial pelo responsável, com revisão do delta e checks invalidados. Reconhecimento e revisão podem ocorrer em paralelo somente leitura. Não use concorrência máxima como objetivo independente do aceite.

## Steps

1. Read the spec and tickets. Read enough to understand the task graph.

2. Delegue reconhecimento somente leitura conforme AGENTS. Receba resumo com evidências e referências; o executor responsável atualiza o registro existente no local definido pelo adaptador, sem cópia paralela fora do workspace.

3. Reuse the verified working branch or isolate according to Implement. Create a draft PR only when authorized and guaranteed not to trigger prohibited CI; otherwise keep the reviewed commits local and report the publication limit.

4. Cada ticket autorizado tem um executor responsável. No ERP Jetta, subagentes fazem reconhecimento, testes e revisão conforme AGENTS; alterações ficam no executor principal. Sessões executoras simultâneas exigem worktrees/branches/runtimes próprios e contratos independentes, seguindo Implement. Sem autorização para novas sessões, execute as fatias atribuídas sequencialmente.

5. Once an **implementer subagent** completes, o responsável verifica diff, evidências e commits e integra serialmente à branch da PR dentro da autorização. No ERP Jetta, decisões, alterações e operações sensíveis permanecem no executor principal, conforme AGENTS; não delegar merge concorrente nem integrar automaticamente em main.

6. Atualize a **frontier** somente após confirmar dependências e integração. Inicie outra fatia apenas dentro do escopo autorizado, com isolamento verificado; ticket único não autoriza avançar a fila.

7. Depois das fatias, preserve /code-review integrado Standards/Spec na branch da PR, usando a mesma matriz e recorte. O executor corrige achados materiais, revisa o delta e executa os gates finais de Implement. Evidências válidas evitam redescoberta; não substituem a revisão nem o percurso integrado exigidos. Sugestões fora do escopo são encaminhadas separadamente.

8. If an authorized PR exists, mark it ready only after complete acceptance; otherwise report the actual delivery state.

9. Clean up all **implementer subagent** worktrees.
