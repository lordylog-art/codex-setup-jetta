---
name: smart-orchestrator
description: "Execute authorized multi-ticket features or dependent increments through implementation, review, integration and acceptance. Handle trivial changes directly."
---

# Smart Orchestrator

Entregue os tickets autorizados com implementação direta, verificação proporcional e conclusão clara. Use o [contrato proporcional](references/planning-contract.md): reaproveite a base pronta, execute o delta restante e pare após cumprir o pedido. Critérios vêm do usuário, das regras aplicáveis ou de risco concreto introduzido pela mudança; melhorias opcionais não bloqueiam entrega.


Execute as skills especialistas diretamente, preservando seus gates e permissões. Selecione modelos pelas regras de [Delegação](#delegação); profundidade de QA e modelo são decisões independentes.

## Entrada e estado

Identifique objetivo autorizado, fontes canônicas, tickets existentes, trabalho concluído/em andamento, regras aplicáveis e ferramentas disponíveis. Preserve trabalho alheio. Criar a skill ou discutir uma fila não autoriza executar produto. Coordene **quando e por que**; skills especialistas instaladas definem **como**, sem substituir gates existentes.

Padrão, inclusive em filas: execução direta e verificação focal, sem DAG formal, controller, subagentes ou relatório dedicado obrigatórios. Leia [quality-gates.md](references/quality-gates.md) para escolher revisão/prova conforme risco. Consulte scheduling/metrics apenas quando houver problema concreto de escalonamento ou pedido de estimativa. Não acione um playbook de missão completo apenas por haver mudança durável ou vários tickets.

Mantenha no ticket/registro existente apenas resultado atual, trabalho restante, verificação e bloqueio concreto quando houver. Estimativas, CP e ledger de recursos pertencem ao modo V2 ou a uma necessidade demonstrada.

Distinga pendente, em execução, candidato pronto, em validação, validado, integrado, aceito e bloqueado. Bloqueio pertence à etapa afetada; código pronto não implica aceite. Reaproveite registros, sem criar sistema de tickets paralelo.

## Contrato e controlador V2 — modo explícito

Use este modo somente quando explicitamente solicitado; complexidade ou existência de plano antigo não o ativam automaticamente. No modo direto, tickets e decisões atuais bastam; falta de JSON/controller não bloqueia código. Se o usuário pedir simplificação de uma fila V2 ativa, registre a reconciliação uma vez, conserve histórico/provas e requisitos do produto e prossiga no modo direto. Não altere silenciosamente hashes ou declare gates antigos aprovados.

Quando V2 for escolhido, leia as seções V2 de [planning-contract.md](references/planning-contract.md) e consuma o execution-plan vinculado à SPEC/Index. Respeite decisões e restrições atuais, inclusive isolamento e gates explícitos de produto.

Antes de dispatch/review/integração/aceite, use [controller.md](references/controller.md): inicialize ou retome estado da worktree, confira elegibilidade, reserve recursos e registre provas/transições. Não improvise esses controles em tabelas do chat. O controlador verifica registros, dependências e hashes; os agentes decidem suficiência semântica, classificação de risco e alcance. Sincronize o status no tracker canônico pelo adaptador existente; estado operacional não é outro tracker. Não importe PASS histórico sem conferir equivalência e artefatos.

Estados: PLANNED → IN_PROGRESS → CODE_READY → REVIEW_READY → REVIEWED → INTEGRATION_READY → ACCEPTED; BLOCKED preserva etapa e causa. CODE_READY não autoriza QA funcional final: a maturidade e dependências do gate precisam estar satisfeitas. Review antecipado de contrato/segurança tem recorte próprio e não certifica jornada futura. Use [contextual-review.md](references/contextual-review.md) no handoff e nas correções. Revisão local não substitui integração exigida.

## Continuidade

No modo direto, retome pelo ticket e registro existentes, preservando provas válidas. Somente no modo V2, checkpoints são automáticos nas gravações do controller e a retomada usa `recover` conforme [continuity.md](references/continuity.md). A compactação pertence ao runtime nativo; nunca troque de chat para compactar.

## Decisão por evento

Eventos: conclusão, candidato disponível, validação aprovada/reprovada, bloqueio/resolução, contrato alterado, integração ou mudança material de recursos.

A cada mudança relevante, escolha trabalho útil: implementar, corrigir, verificar ou integrar. Dependência de integração bloqueia a integração afetada; avance código independente contra o contrato disponível, preservando ownership e ativação segura. Issue OPEN ou metadado ausente não demonstram indisponibilidade técnica. Prossiga até cumprir critérios autorizados ou encontrar impedimento real; sem mudança material, continue a ação escolhida em vez de replanejar.

Use espera por evento apenas quando a mudança esperada puder liberar uma ação concreta. Sem trabalho independente nem nova informação, relate uma vez o bloqueio e sua condição de retomada; evite turnos sucessivos apenas para reler o mesmo status. Nenhum agente existe apenas para vigiar outro.

## Delegação

Antes de delegar, confirme autorização, ganho plausível após coordenação/validação, slot, ownership disjunto e capacidade de aceite. Conte o principal quando incluído no limite da ferramenta e todos os agentes descendentes no mesmo limite global. Combine no handoff a capacidade disponível para reviewers filhos; novos filhos dependem de slots e recursos confirmados. Adapte ao inventário real, sem número fixo de agentes/modelos. Sem subagentes disponíveis/autorizados, execute sequencialmente e declare a limitação.

Pesquisas/research, leitura de documentação, exploração de código e levantamentos usam **GPT-6 Luna** (`gpt-6-luna`) por padrão, inclusive quando delegados por implementadores ou reviewers Sol. Informe o modelo explicitamente no handoff e no despacho, evitando herdar Sol do agente pai. Use esforço low para coleta objetiva, medium para cruzar fontes e high para investigação delimitada mais complexa. Escale a pesquisa para GPT-6.1 Sol somente por indisponibilidade do Luna, lacuna material demonstrada após tentativa Luna ou decisão crítica que a pesquisa não resolva; registre a justificativa. Use ferramentas diretamente para buscas determinísticas simples e preserve fontes, evidências e critérios de conclusão.

Code review independente escolhe modelo e esforço pelo risco. Para autorização, segurança e fluxos críticos, use GPT-6.1 Sol (`gpt-6.1-sol`) com esforço medium. Para deltas simples e bem delimitados, use GPT-6 Luna (`gpt-6-luna`) com esforço high. Não use Sol com esforço high por padrão; reserve-o para risco crítico ou complexidade demonstrada e registre a justificativa. Se o modelo indicado estiver indisponível, escolha a combinação disponível mais próxima e registre a substituição.

Handoff: objetivo/escopo, arquivos/fronteiras exclusivas, dependências, critérios, verificação e permissões; retorno com candidato, arquivos, resultados e bloqueios. O implementador conduz testes, correções e revisão quando exigida pelo risco, conforme [contextual-review.md](references/contextual-review.md); inclua essa responsabilidade no prompt. Informe que outros agentes atuam e devem preservar suas alterações.

Confirme ownership e disponibilidade dos recursos usados antes de delegar; ledger formal só no modo V2. Ownership exclusivo para escrita; worktrees isoladas quando justificadas, reutilizando organização existente. Worktree não isola navegador, banco, portas, runner ou index Git compartilhado. Um titular controla cada integração/reconciliação. Sobreposição inesperada suspende escritas afetadas e preserva diffs para esse titular.

Principal conserva prioridades, ownership, integração e responsabilidade pela entrega. DAG e reservas formais apenas no modo V2. Use subagentes quando houver ganho concreto ou revisão independente exigida; chats separados só se solicitados pelo usuário. Delegar não amplia autorização para CI, deploy, publicação ou ações externas.

## Gargalos, falhas e conclusão

Validação congestionada reduz novos candidatos; gate indisponível prioriza recuperação e trabalho independente útil, preservando estoque. Falha repetida exige assinatura/etapa, hipótese causal discriminante e menor prova útil. Repita só após mudança de hipótese, código ou ambiente. Sem ação viável, registre bloqueio, responsável e condição de retomada. Separe defeito do produto de infraestrutura.

Integre candidatos aprovados progressivamente quando contratos, dependências, conflitos, provas e permissões permitirem. Revalide delta/impactos invalidantes. Integração parcial não aceita a feature inteira.

Encerre quando todos os critérios tiverem provas válidas e integração exigida, sem achados materiais pendentes. Informe aceitos, falhas, bloqueados e superfícies não executadas com rastreabilidade. Pare de ampliar provas após gates cumpridos; sugestões opcionais não reabrem escopo. Estimativa não é promessa; bloqueio nunca vira aceite.
