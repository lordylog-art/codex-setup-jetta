---
name: smart-orchestrator
description: "Execute authorized multi-ticket features or dependent increments through implementation, review, integration and acceptance. Handle trivial changes directly."
---

# Smart Orchestrator

Otimização de 04/11/2026: aplique esta política em novas execuções. Preserve contratos, checkpoints e gates de trabalhos já iniciados; não migre, interrompa ou envie mensagens a outros chats por causa desta atualização.

## Execução pela skill local

A entrada vigente é [SKILL.md](SKILL.md): aplique a lógica no chat atual por chamada explícita ou antes de implementar, com execução proporcional. Consulte fontes locais e o ai-memory já conectado; preserve o contexto resolvido, as decisões confirmadas e os gates pertinentes. O MCP Smart Orchestrator está desativado: referências antigas a contexto ou bots desse servidor não exigem inicialização, conexão stdio ou servidor substituto.

Use subagentes nativos apenas nas frentes independentes ou revisões necessárias e autorizadas pela skill vigente. Bots separados e ponte-chatgpt continuam exigindo pedido explícito. O principal mantém investigação, decisões e coordenação; preserve checkpoints de trabalhos já iniciados e nunca migre controller ativo silenciosamente.

Entregue os tickets autorizados com implementação direta, verificação proporcional e conclusão clara. Use o [contrato proporcional](references/planning-contract.md): reaproveite a base pronta, execute o delta restante e pare após cumprir o pedido. Critérios vêm do usuário, das regras aplicáveis ou de risco concreto introduzido pela mudança; melhorias opcionais não bloqueiam entrega.


Execute as skills especialistas diretamente, preservando seus gates e permissões. Selecione modelos pelas regras de [Delegação](#delegação); profundidade de QA e modelo são decisões independentes.

## Entrada e estado

Identifique objetivo autorizado, fontes canônicas, tickets existentes, trabalho concluído/em andamento, regras aplicáveis e ferramentas disponíveis. Preserve trabalho alheio. Criar a skill ou discutir uma fila não autoriza executar produto. Coordene **quando e por que**; skills especialistas instaladas definem **como**, sem substituir gates existentes.

Para novas filas, use o [fluxo de entrega](references/delivery-flow.md): pacote de contexto único por frente, implementação e revisão sobrepostas em recortes estáveis, prova focal durante o trabalho e integração no marco necessário. Resolva contexto e skills uma vez; releia apenas deltas, dúvidas concretas ou contexto perdido. [quality-gates.md](references/quality-gates.md) continua definindo todos os gates.

Padrão, inclusive em filas: entrega direta e verificação focal, sem DAG formal, controller ou relatório dedicado obrigatórios; aplique a distribuição de modelos e os gates de delegação abaixo. Leia [quality-gates.md](references/quality-gates.md) para escolher revisão/prova conforme risco. Consulte scheduling/metrics apenas quando houver problema concreto de escalonamento ou pedido de estimativa. Não acione um playbook de missão completo apenas por haver mudança durável ou vários tickets.

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

### ChatGPT Web por ativação explícita

Quando o usuário chamar este orquestrador junto com `$ponte-chatgpt`, leia `C:/Users/caila/.codex/skills/ponte-chatgpt/SKILL.md` e seu `references/review.md`. Nessa execução, substitua os reviewers subagentes por revisão no ChatGPT Web via Agentify MCP: candidato isolado, commit/push autorizado em branch de revisão, confirmação do SHA remoto, exportação do snapshot publicado via Git no Codex, revisão do anexo no GPT Web temporário Não personalizado + Extra High e reavaliação das correções publicadas. Preserve Standards/Spec, profundidade por risco, provas e gates; Codex mantém implementação, arquivos, testes, QA, integração e aceite. Se a rota falhar, bloqueie a revisão afetada, sem fallback automático para subagentes. Sem ativação explícita da ponte, mantenha o fluxo normal. O fluxo manual antigo não governa esta rota MCP já autorizada.

A ativação conjunta também encaminha automaticamente ao GPT Web, quando necessários à tarefa, pesquisa/consultas, imagens e os fluxos de `C:/Users/caila/.codex/skills/ponte-chatgpt/references/auxiliares.md`: requisitos, planejamento, diagnóstico, cenários de teste, arquitetura, documentação/textos e QA visual auxiliar por capturas reais. Não peça nova ativação a cada fluxo nem execute todos por rotina; selecione apenas os pertinentes e reutilize contexto/evidência válidos. GPT Web analisa e redige; Codex implementa, altera arquivos, captura/confere a UI, executa comandos/testes e confere resultados. Propostas não ampliam escopo nem substituem gates, provas ou aprovações humanas. Falha da ponte bloqueia só o apoio afetado e deve ser informada, sem fallback automático.

Antes de delegar, confirme autorização, slot, ownership disjunto e capacidade de aceite. Conte o principal quando incluído no limite da ferramenta e todos os agentes descendentes no mesmo limite global. Combine no handoff a capacidade disponível para reviewers filhos; novos filhos dependem de slots e recursos confirmados. Respeite o inventário real e execute etapas sequencialmente quando necessário.

Preencha slots com frentes tecnicamente independentes quando arquivos, build, banco e portas permitirem; ordem de tickets não cria dependência. Reserve capacidade para revisar o candidato próximo de ficar pronto. Reutilize implementador e reviewers nas correções; um ticket relacionado pode reutilizar executor após encerrar o escopo anterior e receber novo ownership. Nunca reutilize o autor como seu revisor independente. O implementador envia achados diretamente ao reviewer e resolve-os sem passagem repetida pelo supervisor; o supervisor verifica cobertura e validade no aceite, sem uma segunda auditoria integral automática.

Distribua as tarefas pelos modelos disponíveis, selecionando explicitamente o modelo no despacho quando necessário:

- **Sol (`gpt-6.2-sol`)**: implementação, correções e revisão de código. Prefira revisão independente por outro agente Sol, proporcional ao risco; quando indisponível e não obrigatória, registre a limitação. Análises complexas ou de segurança ficam com Sol.
- **Terra (`gpt-6.1-terra`)**: QA visual e navegação dos fluxos reais necessários à validação, comparando resultados com o esperado e registrando evidências e limitações. Em Jetta, siga o gate de `jetta-qa`, inclusive a reinspeção após correções.
- **Luna (`gpt-6-luna`)**: pesquisas simples, busca de fontes e preparação de resumos. Encaminhe análises complexas ou de segurança ao Sol.

Ajuste o esforço de raciocínio ao risco e às opções do modelo. Se um modelo necessário ou sua delegação estiver indisponível, informe a limitação e mantenha bloqueado o gate que dependa dele; não declare uma validação não executada. A rota explícita ChatGPT Web acima mantém seu review externo e não substitui o gate visual do Terra.

Handoff: objetivo/escopo, arquivos/fronteiras exclusivas, dependências, critérios, verificação e permissões; retorno com candidato, arquivos, resultados e bloqueios. O implementador conduz testes, correções e revisão quando exigida pelo risco, conforme [contextual-review.md](references/contextual-review.md); inclua essa responsabilidade no prompt. Informe que outros agentes atuam e devem preservar suas alterações.

Confirme ownership e disponibilidade dos recursos usados antes de delegar; ledger formal só no modo V2. Ownership exclusivo para escrita; worktrees isoladas quando justificadas, reutilizando organização existente. Worktree não isola navegador, banco, portas, runner ou index Git compartilhado. Um titular controla cada integração/reconciliação. Sobreposição inesperada suspende escritas afetadas e preserva diffs para esse titular.

Principal conserva prioridades, ownership, integração e responsabilidade pela entrega. DAG e reservas formais apenas no modo V2. Use subagentes para aplicar a distribuição acima e quando houver ganho concreto ou revisão independente exigida; chats separados só se solicitados pelo usuário. Delegar não amplia autorização para CI, deploy, publicação ou ações externas.

## Gargalos, falhas e conclusão

Validação congestionada reduz novos candidatos; gate indisponível prioriza recuperação e trabalho independente útil, preservando estoque. Falha repetida exige assinatura/etapa, hipótese causal discriminante e menor prova útil. Repita só após mudança de hipótese, código ou ambiente. Sem ação viável, registre bloqueio, responsável e condição de retomada. Separe defeito do produto de infraestrutura.

Agrupe candidatos aprovados compatíveis numa integração e build comuns quando isso reduzir reinícios sem bloquear dependências nem atrasar a entrega solicitada. Preserve prova por ticket, backups/migrações necessários, dados e ativações. Integre antes quando outra etapa precisar do contrato real. Revalide o delta e as fronteiras integradas; integração parcial não aceita a feature inteira.

Encerre quando todos os critérios tiverem provas válidas e integração exigida, sem achados materiais pendentes. Informe aceitos, falhas, bloqueados e superfícies não executadas com rastreabilidade. Pare de ampliar provas após gates cumpridos; sugestões opcionais não reabrem escopo. Estimativa não é promessa; bloqueio nunca vira aceite.
