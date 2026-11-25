---
name: feature-supervisor
description: Supervisionar uma feature completa por blocos e tickets do Obsidian, somente quando explicitamente solicitado com esta skill.
---

# Feature supervisor

Ative apenas por `$feature-supervisor` ou pedido explícito de supervisão da feature inteira. Receba projeto absoluto, referência explícita da feature e escopo autorizado (leitura ou execução). Sem referência inequívoca, peça a referência; não escolha uma feature para implementar.

## Modo /peixinhos

Com `$feature-supervisor /peixinhos` (alias `//peixinhos`) ou pedido explícito de implementação com peixinhos, leia [implementação com peixinhos](references/peixinhos.md). O supervisor coordena implementadores em paralelo, revisores independentes Golden Fish Review, Super QA incremental, runtime/navegador comprovados e integração local no principal para teste humano. É um modo de instruções desta skill, não um comando registrado no aplicativo ou no helper Python. Sem o modo, preserve o fluxo atual. A ativação não escolhe feature/projeto, não amplia permissões e não ativa V2.

Peixinhos são exclusivamente subagentes nativos deste chat, inclusive implementadores e revisores. Despache com `collaboration.spawn_agent` e reutilize-os com `followup_task`; não use create_thread/fork_thread/handoff_thread, bot_start/bot_continue, Agentify, Codex CLI ou outro processo/chat para delegar. Não consulte outros chats para montar a equipe. Outra rota exige pedido explícito do usuário para aquela rota, não apenas pedido de paralelismo ou de peixinhos.

## Critérios de aceite como unidade de trabalho

Implemente e valide pelos critérios de aceite identificados no ticket e na spec, não apenas por arquivos ou tarefas narradas. Cada handoff associa recorte e provas aos IDs dos critérios. Assim que um critério estiver integralmente comprovado no candidato exigido, marque `[x]` no ticket **e na spec correspondente**, vinculando evidência e candidato. Faça isso durante o trabalho, sem deixar todos os checkboxes para o encerramento. Não marque por código pronto, relato de agente, mock insuficiente ou PASS de alcance diferente; parcial, bloqueado ou sem prova permanece `[ ]`.

Se a spec não tiver checkboxes por critério, acrescente nela um espelho de acompanhamento com os mesmos IDs e links dos tickets, preservando requisitos e decisões existentes, sem inventar ou renumerar aceites. Ticket mantém a definição e evidência detalhada; spec espelha o estado por ID. Um único responsável atualiza ambos para evitar colisão. Board/resumo não substitui essas marcações. Na retomada e após delta invalidante, reconcilie prova e estado nos dois lugares; reabra critérios cuja prova deixou de valer. Se uma atualização documental falhar, registre a divergência e não declare acompanhamento concluído ou COMPLETE até reconciliá-la.

Otimização de 04/11/2026: aplique a política abaixo em novas execuções. Trabalhos já iniciados conservam seus contratos, checkpoints e gates; esta revisão não autoriza migrá-los, interrompê-los ou enviar mensagens a outros chats.

## Inicialização

1. Leia as instruções atuais do projeto, o Index e as fontes vinculadas necessárias. Consulte `smart-orchestrator-mcp` e `orchestrator_context(project)` uma vez na entrada; leia a skill Smart retornada. Reaproveite essas leituras durante a execução; releia apenas fontes alteradas ou contexto perdido na retomada. Referências de V2 só quando esse modo for solicitado. Planejamento continua com To-Tickets. Não reative o Jetta Harness.
2. Leia [contrato e continuidade](references/contract.md). Identifique blocos, dependências por etapa, critérios e provas existentes. Não confunda status declarado com aceite. Registre incompatibilidades sem normalizar notas reais silenciosamente.
3. Modo direto: reutilize o adaptador `spec-workspace` do checkout e os tickets canônicos; use `scripts/feature_supervisor.py --help` para a interface instalada. O helper só dá suporte ao subconjunto validado do adaptador; formato incompatível pede reconciliação, não execução por aproximação. Inspeção nunca chama o resolver que cria pastas.
4. V2 somente quando explicitamente escolhido para essa feature: reutilize `controller.py recover/status/schedule` do Smart e o plano/estado existentes. Não use o helper direto em paralelo com o controller. Consulte controller.md e continuity.md do Smart; não crie outro ledger.

Tickets canônicos já `resolved` sem checkpoint do supervisor exigem revisão das provas existentes, não reimplementação. Depois de conferir critérios, dependências e evidências atuais, use `adopt` explicitamente com o pacote READY completo, em ordem de dependências. O comando preserva `resolved`; não converte estados legados como `in-progress` nem certifica prova antiga por confiança. Veja o contrato antes de reconciliar.

## Ciclo durante a sessão ativa

Selecione tickets elegíveis por dependência técnica e capacidade real, reserve ownership antes do despacho e persista o checkpoint de cada ticket. Crie executor com `fork_turns: "none"`; reutilize-o nas correções e, após encerrar seu escopo anterior, em ticket relacionado com novo handoff e ownership explícitos, conforme [contrato](references/contract.md). Avance frentes independentes em paralelo quando arquivos e recursos forem separados; não espere integração de outro ticket se ela não for pré-requisito dessa etapa. Preserve os bloqueios do adaptador e reconcilie incompatibilidades antes de despachar. O principal conserva prioridades, aceite e integração; o executor entrega, sem criar outro orquestrador.

O supervisor não edita código do ERP. O Smart/executor conduz implementação, revisão e testes. Use quantos agentes forem necessários nas frentes elegíveis, sem teto numérico próprio por ticket, bloco ou árvore. Confira a capacidade atual do runtime para toda a árvore antes de autorizar filhos; não carregue cotas de sessões anteriores. Havendo limite técnico real, mantenha a fila e despache assim que houver capacidade; serialize apenas etapas dependentes ou recursos conflitantes. Propague essa regra aos executores. Use a distribuição de modelos do Smart instalado. Não substitua ferramenta indisponível por mensagens simulando execução.

Para novas filas, leia `references/delivery-flow.md` do Smart instalado e aplique a prioridade dos gates prontos: um pacote de contexto por frente, reviewer disponível para candidato estável e conferências mecânicas com `scripts/delivery.py` quando houver prova Super QA. O helper complementa os checkpoints existentes e nunca muda aceite. Ao receber resultado, confira critérios, resultados reais, pareceres e identidade do candidato nos artefatos pertinentes. Reaproveite a revisão suficiente e independente: o supervisor verifica cobertura e validade, sem abrir outra revisão completa ou repetir comandos já comprovados sem lacuna, mudança ou risco novo. Marque critérios comprovados assim que possível; aceite o ticket apenas com sua integração exigida. Um `PASS`, hash ou `COMPLETED` isolado não basta. Agrupe integrações compatíveis conforme o Smart, mantendo aceites por ticket; não reinicie o localhost a cada ticket por rotina.

Atualize checkpoints e o usuário por mudança material, indicando o próximo trabalho concreto e seu bloqueio, quando houver. Durante trabalho independente, execute-o; sem ele, aguarde evento com intervalo limitado para manter comunicação. Evite ciclos de sleep + inventário + mensagem sem mudança. Não use agentes apenas para vigiar agentes.

Falha técnica corrigível: persista assinatura, hipótese e tentativa; delegue correção delimitada e revalide. Use duas tentativas por ticket por padrão. Quando o usuário disser que está AFK ou pedir continuidade sem perguntas, reserve novos tickets com `claim --max-attempts 10`; esse é o teto, não uma obrigação de repetir. Preserve o orçamento persistido na retomada e não zere o contador ao trocar agente. Cada nova tentativa precisa de hipótese nova sustentada por evidência. Sem hipótese nova ou após limite, registre BLOCKED e avance trabalho independente; não solicite exceção de tentativa durante a ausência.

## Execução AFK e decisões pendentes

Dentro do escopo autorizado, resolva escolhas técnicas reversíveis com as fontes existentes, registre a decisão e continue. Não pergunte se pode prosseguir para outro ticket/bloco já autorizado, investigar, corrigir regressão ou repetir validação pertinente. Propague essa orientação no handoff de todos os executores; dúvidas técnicas voltam ao supervisor, não ao usuário.

Antes de pedir uma decisão, procure a resposta nas instruções, aceites e fontes atuais. AFK não concede aprovações específicas ainda ausentes (por exemplo composição visual, ampliação de template, produção ou envio externo). Registre a decisão necessária e bloqueie somente a etapa afetada; prepare o que for permitido e continue todas as etapas independentes. Durante a ausência, acumule essas decisões no checkpoint e no relatório final, sem abrir perguntas interativas. Nunca trate silêncio como aceite nem encerre a execução só porque existe uma decisão pendente.

Quando não houver mais trabalho autorizado executável nem executor ativo, encerre com os bloqueios concretos e decisões agrupadas. Falha de capacidade do modelo ou interrupção do App não é bloqueio de negócio; a skill não pode garantir continuidade enquanto o serviço estiver indisponível. Retome do checkpoint quando houver nova execução, sem reabrir decisões já respondidas.

## Retomar e encerrar

Reconstrua pelos tickets/checkpoints; nunca dependa da conversa completa. Antes de retomar um claimed, confirme agente/owner e ausência de execução ativa. Não remova locks por idade. Janela de crash entre claim e registro do agente exige reconciliação; nunca redispare automaticamente.

Encerre com COMPLETE somente quando todos os tickets e condições da feature estiverem comprovados. Sem elegíveis, diferencie WAITING (executor ativo) de BLOCKED (decisão/falha/dependência) e EMPTY/INVALID (fonte insuficiente); nenhum equivale a conclusão. Não fique consultando estado inalterado indefinidamente.

Uma skill não mantém o chat vivo nem acorda após seu encerramento. Retomada exige nova invocação explícita; não crie CLI Codex, daemon ou agendador. Chats independentes só mediante pedido específico e ferramenta oficial disponível, nunca como compactação. Veja [validação e limites](references/validation.md) antes de afirmar capacidades.
