# Contrato e continuidade

## Entrada mínima

`project`: checkout absoluto; `feature`: nota/Index explícito; `mode`: read-only ou execute; `authorized_scope`: trabalho permitido; `tracker`: fonte canônica descoberta. A referência deve resolver sem ambiguidade. Leia blocos e insumos técnicos vinculados; não carregue o vault inteiro.

No ambiente investigado: Smart em `C:/Users/caila/.agents/skills/smart-orchestrator/SKILL.md` e pacote retornado pelo MCP; adaptador em `<project>/.agents/skills/spec-workspace/scripts/spec_workspace.py`. Confirme existência e regras antes de usar. A cópia de `C:/Scripts/Jetta Harness` é histórica e desabilitada. O controller Smart instalado é independente desse Harness, porém continua opt-in V2.

O adaptador mantém `ticket_status: open/claimed/resolved`, `triage_role`, `blocked_by` e `## Comments`. Checkpoints diretos são comentários no próprio ticket, não outro arquivo de status. Bloco vem dos documentos/metadados existentes. `Index.md` aponta tickets; nunca infira dependência só pela ordem alfabética.

## Handoff ao executor

Para criar executor, use `collaboration.spawn_agent` com `fork_turns: "none"`. Reutilize o mesmo executor em correções e tickets relacionados após fechar seu escopo anterior; registre o vínculo real em cada checkpoint. Mantenha critérios, tentativas e aceite separados por ticket, sem reiniciar contadores. Revisor permanece distinto do autor dos arquivos avaliados. Passe somente:

- projeto, ticket e trecho/referências dos critérios, dependências e decisão aprovada;
- caminho da skill Smart atual, adaptador e instruções do projeto que governam o trabalho;
- owner/run, tentativa, escopo exclusivo de escrita e fontes necessárias;
- validação/revisão esperadas e permissões (não autoriza CI/push/deploy/envios);
- IDs de aceite atendidos pelo recorte, spec correspondente e responsável por atualizar os checkboxes em ticket e spec após prova suficiente; executor não declara critério concluído só por ter produzido código;
- capacidade atual do runtime para especialistas, sem cota artificial por executor, e limite do retorno; usar quantos agentes forem necessários, coordenando a capacidade compartilhada com o supervisor.
- indicação de usuário AFK, orçamento persistido de tentativas e orientação para devolver dúvidas ao supervisor; escolhas técnicas reversíveis dentro do escopo não exigem pergunta ao usuário.

Diga que outros agentes trabalham no ambiente e suas edições devem ser preservadas. O executor aplica o Smart diretamente ao ticket, inclusive investigação local e revisão proporcional. Não inicia `bot_start`, Codex CLI ou chat independente. A função principal continua no chat supervisor; não crie um segundo planejador da feature.

Retorno JSON compacto (até cerca de 2 KB; detalhes em arquivos):

```json
{"ticket":"T01","agent":"native identifier","status":"candidate|blocked|failed","attempt":1,"changed":[],"criteria":[{"id":"C1","result":"PASS","evidence":"absolute path"}],"validation":[{"command":"actual command","exit_code":0,"artifact":"absolute path"}],"review":"path or justified not-required","blocker":null,"next_action":"verify candidate"}
```

O retorno transporta resultado, não histórico. O principal verifica conteúdo dos artefatos e semântica dos critérios antes de qualquer aceite. Não aceite artefato que apenas repete o pedido. Hash garante identidade do arquivo, não sua veracidade nem validade futura do código; inclua arquivos alterados, testes/config pertinentes no conjunto de evidências e revalide após mudanças.

Referencie provas e pareceres existentes em vez de copiá-los para cada retorno. Aceites distintos podem compartilhar a mesma execução suficiente, com alcance explícito por critério. Integração agrupada não dispensa checkpoint, revisão ou prova de cada ticket.

## Ownership e recuperação

Use a trava e transição do adaptador, nunca um segundo banco. O helper direto acrescenta checkpoints compactos aos comentários e coordena participantes cooperantes. Editor humano ou ferramenta que não participa do protocolo pode modificar notas; detectar mudança e reconciliar, não prometer exclusão global.

Reserve antes de despachar. Depois persista ID nativo. Se houver crash entre operações, claimed sem agente é estado incerto e não é elegível. Para retomar claimed, confira o executor anterior, código e provas; continue o mesmo trabalho com o owner persistido apenas depois de confirmar parada, sem novo claim. Bloqueio mantém claimed e comentário BLOCKED, sem inventar novo ticket_status.

O resumo pode guardar status derivado, bloco/ticket, dependências, owner/agente, tentativas, resultados de validadores, referências de provas e próxima ação. Ao reler, estado canônico e evidências atuais prevalecem sobre resumo. Não copie logs longos para checkpoints. Tentativas e provas não concedem autorização.

Para reconciliar histórico comprovado no modo direto, use `python scripts/feature_supervisor.py --workspace <workspace> adopt --ticket <id> --owner <owner> --run <run> --data <ready.json>`. O JSON contém exatamente status READY, checkpoint, next_action, evidence, validators e supervisor_review, no formato do helper. Só notas já resolved são admitidas; critérios precisam estar marcados e provas atuais, com dependências adotadas antes. Não altera status, não reimplementa e não adota automaticamente. Repetição idêntica não escreve; alteração de candidato ou owner exige decisão explícita. Também recupera a janela resolved + checkpoint READY quando owner/run e o mesmo pacote de provas são confirmados. Não use para claimed sem checkpoint ou trabalho possivelmente ativo.

V2: entregue plano/root/state-root/resources-root originais ao Smart; use seus checkpoints/recover. Não reconstrua ou migre plano automaticamente, não modifique hashes para aceitar histórico. A composição com o adaptador foi exercitada por `tests/test_v2_integration.py` com plano sintético e os componentes instalados reais.

Não existe API automática de sincronização V2/Obsidian no Smart instalado. O orquestrador consulta `status`/`recover` e exige `acceptance_current` antes de resolver a nota pelo `transition_ticket` do adaptador. Claim da nota e progressão do Controller permanecem separados; confira ambos após falha parcial. Critérios e provas semânticas devem ser revisados antes de marcar e resolver. Estado operacional fica exclusivamente no Controller: não use claim/checkpoint/accept/adopt do helper direto para V2. Se uma prova de ticket já resolved ficar stale, recover deve tratá-lo como restante; preserve o histórico canônico, bloqueie dependentes e reconcilie explicitamente. O adaptador não oferece transição resolved → open. Checkpoint não substitui ledger ausente nem autoriza reconstruí-lo com init.
