# Feature supervisor — instalação e validação

Data local: 02/11/2026 (America/Sao_Paulo). Evidências UTC podem mostrar 03/11.

## A. Arquitetura encontrada

O Smart instalado em `C:/Users/caila/.agents/skills/smart-orchestrator/SKILL.md` e o pacote retornado por `orchestrator_context(project="D:/newmove")` usam entrega direta por padrão. O principal investiga e coordena; subagentes nativos recebem trabalho delimitado. O MCP fornece contexto, não constitui um executor em segundo plano. O acesso real respondeu AVAILABLE.

To-Tickets local (`D:/newmove/.agents/skills/to-tickets/SKILL.md`) cria critérios verificáveis e preserva o tracker existente. Com referência Obsidian, `spec-workspace` mantém Index, Tickets, `triage_role`, `ticket_status`, `blocked_by`, comentários, travas por arquivo e substituição atômica. Esse é o mecanismo reutilizado.

O Controller Smart existe em `C:/Users/caila/.agents/skills/smart-orchestrator/scripts/controller.py`: plano V2, estágios, provas, reservas, checkpoints e recover. É opt-in, não requisito do modo direto. A cópia em `C:/Scripts/Jetta Harness` ainda tem instruções antigas incompatíveis; o Harness permanece desativado. Nenhuma instalação original foi editada.

A configuração local declara agentes habilitados e limite de threads próprio; o contrato efetivo desta ferramenta ofereceu três slots contando a árvore. Os testes respeitaram root + executor + reviewer. Disponibilidade deve ser conferida novamente em outra sessão.

## B. Arquitetura implementada

A skill explícita mantém prioridades da feature e delega tickets pelo Smart em subagentes com `fork_turns: "none"`. O helper Python reaproveita funções reais do adaptador para descoberta, locks, transições e comentários. Não há banco, tracker, controller, processo permanente, agendamento ou invocação Codex CLI novo.

Checkpoints ficam no próprio ticket, contendo feature, bloco, dependências, owner/run/agente, tentativa, timestamp, provas/hash, validadores e próxima ação. A transição canônica permanece open → claimed → resolved. BLOCKED é um resultado do checkpoint, preservando claimed. O supervisor realiza o julgamento semântico; o helper confere consistência e identidade das provas.

Uma região crítica usa as travas nativas do Index e tickets em ordem estável para revalidar antes de gravar. A garantia cobre escritores cooperantes; edição direta fora dessas travas não fica bloqueada. Claim e comentário são duas gravações: queda entre elas exige reconciliação manual, não novo despacho automático.

## C. Arquivos instalados

Raiz única: `C:/Users/caila/.codex/skills/feature-supervisor/`. Descoberta adicional: junction `C:/Users/caila/.agents/skills/feature-supervisor` para a mesma raiz, sem cópia divergente. A [documentação oficial de skills](https://developers.openai.com/codex/skills) identifica `~/.agents/skills` como diretório pessoal e mantém invocação explícita quando `allow_implicit_invocation` é false.

| Arquivo | Finalidade |
|---|---|
| SKILL.md | Ativação explícita, ciclo, delegação e limites |
| agents/openai.yaml | Metadados e `allow_implicit_invocation: false` |
| references/contract.md | Entradas, retorno compacto, ownership e retomada |
| references/validation.md | Operação, reprodução e limites do formato |
| scripts/feature_supervisor.py | Helper determinístico sobre adaptador existente |
| tests/test_feature_supervisor.py | Regressões permanentes com fixtures temporárias |
| tests/test_isolation.py | CLI real sob auditoria de escritas, escapes bloqueados e retomada em novos processos |
| tests/test_v2_integration.py | Controller V2 instalado, provas, checkpoints, recover e adaptador canônico |
| tests/native_fixture.py | Fixture persistente e snapshots de não interferência |
| tests/native_verify.py | Validador independente exclusivo da fixture sintética |
| tests/evidence/ | Resultados reais, checkpoints e artefatos sintéticos |
| REPORT.md | Este relatório solicitado |

Nenhuma alteração de configuração global, Smart original, tickets reais ou código ERP foi necessária. A documentação está junto à skill global; não foi gerada documentação na worktree nem executada sincronização do vault real.

## D. Capacidades

| Capacidade | Classificação | Fronteira |
|---|---|---|
| A. Subagentes em contextos separados | SUPORTADO E TESTADO | T01/T02 e reviewer com `fork_turns:none` e IDs distintos |
| B. Executor Smart coordena filho | SUPORTADO E TESTADO | `/root/native_t02/byte_review` fez revisão real |
| C. Retorno sem histórico integral | SUPORTADO E TESTADO | JSON/resumos curtos e referências; logs persistidos em arquivos |
| D. Novo chat independente do App | SUPORTADO E TESTADO | create_thread oficial, com autorização humana específica; chat 01a19eed-e86a-7883-94fe-d43b08e26cb7 |
| E. Retomar após encerrar a execução do supervisor | SUPORTADO E TESTADO | Turno concluído, chat arquivado/reaberto e nova invocação recuperou arquivos e executou só T02/T03; não houve reinício do processo do App |

Instalação e frontmatter foram validados por `quick_validate.py`, inclusive pelo caminho de descoberta `~/.agents/skills`. A presença no seletor visual do Codex foi **confirmada pelo usuário** nesta conversa: “Sim, aparece”, ao perguntar por `$feature-supervisor`. Evidência: `tests/evidence/skill-selector-human-verification.json`. Essa é uma verificação humana, não uma captura automatizada. A execução no chat independente localizou e carregou a skill pelo filesystem; o mecanismo interno de resolução do chip não foi instrumentado. A política permanece exclusivamente explícita.

## E. Testes

Comando permanente: `python -B -m unittest discover -s C:/Users/caila/.codex/skills/feature-supervisor/tests -v`.

Resultado final: **32 testes PASS**, em `tests/evidence/final-suite.txt`: 25 do helper, 1 de isolamento em sete subprocessos e 6 de V2. Essa suíte inclui integração local com os componentes reais e dois processos concorrentes reais; atores/validadores de cenário V2 são sintéticos. Ela não substitui os testes nativos abaixo. O registro inicial de 19 testes permanece em `unit-tests.txt`.

Validador oficial: `python -B C:/Users/caila/.codex/skills/.system/skill-creator/scripts/quick_validate.py C:/Users/caila/.codex/skills/feature-supervisor` → `Skill is valid!`, em `tests/evidence/skill-validation.txt`.

Integração real: `tests/evidence/native/Index.md` contém B01/T01→T02 e B02/T03. T01 foi executado por `/root/native_t01`; após verificação independente e aceite, T02 foi despachado automaticamente para `/root/native_t02`, que criou `/root/native_t02/byte_review`. Resultados, comandos e checkpoints estão em `native/artifacts/` e `native/Tickets/`.

Smoke real: `tests/evidence/real-smoke.json` registra leitura de `D:/Obsidian/Obsidian/New move/Projetos/Templates interativos/Spec Driven/Index.md`, spec e dois tickets. Os dois usam `in-progress`, incompatível com o adaptador; seis critérios seguem desmarcados. Nenhum bloco formal foi inventado. O plano identifica dependência de integração T02→T01, mas não despacha código. O helper também recusou a fonte com erro explícito, em `real-helper-smoke.txt`.

Falhas encontradas e corrigidas: revisão independente reproduziu aceite após edição concorrente e aceite ignorando dependência adicionada depois do claim. As regressões `test_accept_rereads_native_writer_edit_before_ticket_lock`, `test_checkpoint_rereads_native_writer_status_before_ticket_lock` e `test_accept_rechecks_changed_dependencies_after_fresh_ready` agora passam. Provas alteradas, aceites históricos sem comprovação e sintaxe de dependência incompatível também são recusados.

Super QA foi consultado: inventário encontrou 1.054 testes do ERP e o plano foi lido. Análise da skill global pelo projeto D:/newmove foi BLOCKED porque o caminho fica fora da raiz. Não alterei `.super-qa.json` nem o agregado ERP para registrar testes externos. A prova desta skill é seu runner permanente; não existe PASS global do ERP nesta entrega.

Retomada real em contexto novo: `/root/resume_supervisor` reconstruiu somente dos arquivos, identificou T03 e delegou `/root/resume_supervisor/t03_executor`. A primeira tentativa produziu erro controlado `WRONG` (exit 1); diagnóstico e RETRY foram persistidos. A segunda produziu `3\n` (exit 0), seguida de validação independente e aceite. `native/artifacts/resume-report.json` registra tentativas 2/2, todos resolvidos, frontier vazia e nove hashes T01/T02 preservados. Isso prova nova invocação lógica, não desligamento real do App.

| Teste solicitado | Resultado | Evidência e alcance |
|---|---|---|
| T01 — descoberta | PASS | Fixture com dois blocos, três tickets e dependências; inspect e teste discovery |
| T02 — ordenação | PASS | claim fora da frontier recusado; T02 só despachado após T01 ACCEPTED |
| T03 — delegação real | PASS | Agentes native_t01, native_t02 e t03_executor aplicaram Smart real |
| T04 — isolamento | PASS | IDs distintos e despachos `fork_turns:none`; nenhum chat App novo |
| T05 — avanço automático | PASS | T01→T02→retomada T03, sem nova instrução manual do usuário |
| T06 — falha recuperável | PASS | T03-failure.json exit 1, RETRY, T03-result.json exit 0 e aceite posterior |
| T07 — falha persistente | PASS | Unitário com adaptador real: orçamento esgotado, BLOCKED persistente; trabalho independente continua |
| T08 — retomada | PASS | Nova invocação lógica resume_supervisor reconstruiu e executou somente T03 |
| T09 — idempotência | PASS | Replays e subprocesso; nove artefatos T01/T02 preservados na retomada |
| T10 — não interferência | PASS | Novo teste isolado com helper real, adaptador idêntico, escrituras auditadas e escapes bloqueados; fontes e arquivos protegidos sintéticos inalterados |
| T11 — concorrência | PASS | Dois processos reais: um claim vencedor; locks, dependências e regressões de edição concorrente |
| T12 — Obsidian real | PASS | MCP + leitura real com hashes, sem implementação; incompatibilidades reportadas |
| T13 — persistência e sincronização | PASS | Seis testes com Controller V2 instalado, gates/provas, checkpoints, recover em processo novo e transições do adaptador; sem ledger direto duplicado |
| T14 — recuperação de contexto | PASS | Novo supervisor recebeu caminhos/contrato sem transcript e recuperou checkpoints |
| T15 — encerramento | PASS | Todos resolvidos/frontier vazia no nativo; bloqueados sem elegíveis não recebem conclusão falsa no teste de cenário |

São **15 PASS na matriz T01–T15**, dentro dos alcances declarados, além dos 32 testes permanentes. Não há falha conhecida restante nos caminhos exercitados; a falha injetada e os defeitos corrigidos permanecem registrados. Isso não certifica produção, uma sandbox do sistema operacional ou funcionamento 24/7.

Não interferência inicial: `before-native.json` contém 2.650 hashes; `after-native.json`, 2.652. `noninterference.json` detectou quatro arquivos modificados e dois novos em `apps/api/src/modules/incidents`, fora dos caminhos escritos pelos agentes desta missão. Não atribuí autoria nem reverti essas alterações. Nenhuma mudança foi detectada no Smart original, no adaptador ou na feature real incluídos no snapshot. Essa comparação inicial continua inconclusiva para atividade global. A pendência T10 foi resolvida por nova execução isolada: `evidence/isolation-audit.json` registra sete processos e escritas Python observadas, incluindo rejeição de duas rotas de escape. Fontes originais e stand-ins protegidos mantêm seus hashes; não se afirma certificação de toda a máquina.

Complemento V2: `tests/evidence/v2-results.json` registra seis PASS. O Smart não oferece um sincronizador automático: o orquestrador confere `acceptance_current` e usa os primitivos existentes do adaptador. Alteração de plano, prova stale, artefato ou ledger ausente bloqueiam recuperação/aceite. Nota já resolved mantém histórico se a prova ficar stale; Controller passa a indicar trabalho restante, sem normalização silenciosa.

Correção adicional: `adopt` permite reconciliar tickets históricos já resolved após revisão atual, sem reimplementar ou alterar seu status. Recusa provas ausentes/stale, critérios desmarcados, dependentes não aceitos e owner divergente; repetição idêntica não escreve. Recupera também o crash entre resolved e checkpoint ACCEPTED, somente com o pacote READY original. Seis regressões novas passaram e a revisão independente não encontrou defeito material.

Critérios finais:

- [x] Arquivos da skill instalados e validados estruturalmente; ativação explícita exercitada por caminho.
- [x] Presença no seletor visual do Codex App confirmada pelo usuário; invocação explícita executada no chat de teste.
- [x] Descoberta, delegação nativa, sequência e critérios demonstrados na fixture.
- [x] Checkpoints, retomada lógica, concorrência, retries e isolamento demonstrados.
- [x] Smoke real somente leitura, preservando fontes e reportando incompatibilidade.
- [x] Compatibilidade mecânica V2/controller/adaptador comprovada em feature sintética.
- [x] Não interferência do fluxo Python comprovada em execução isolada, sem depender da atividade global.
- [x] Retomada após conclusão do turno e arquivamento/reabertura de chat independente comprovada.

Teste App autorizado: `tests/evidence/app-lifecycle-tools.json` registra criação oficial, conclusão do primeiro turno, archive true, archive false e despacho de retomada. `app-lifecycle/artifacts/app-first-session.json` registra T01 aceito, T02/T03 abertos. `app-resumed-session.json` registra reconstrução pelos checkpoints, executores novos para T02/T03, os três aceites e hashes T01 preservados. O segundo turno terminou sem erro. O teste não reiniciou o processo do aplicativo e não prova execução sem sessão ativa. ai-memory da fixture estava indisponível; persistência canônica e continuidade funcionaram sem ele. A presença no seletor foi verificada separadamente pelo usuário.

## F. Impacto no contexto

Cada executor recebe caminhos e contrato delimitados, sem herdar conversa. O supervisor lê resumos e provas pontuais, preservando estado em tickets. O teste de retomada usa um novo subagente, não o histórico anterior. Ainda há custo de supervisão, mensagens e leitura de critérios; não foi medido consumo de tokens em dezenas de tickets. Nenhuma garantia de contexto ilimitado ou compactação própria é oferecida.

## G. Uso

`$feature-supervisor Projeto D:/newmove; feature D:/Obsidian/Obsidian/New move/Projetos/Templates interativos/Spec Driven/Index.md; modo somente leitura. Reconstrua estado e mostre o próximo trabalho elegível.`

Essa feature real exige reconciliar os estados antigos antes de execução automática. Para outra feature, forneça seu Index explícito e o escopo autorizado. O helper aceita `--adapter` para outro checkout; não mude silenciosamente a fonte canônica nem copie tickets para ajustá-los ao parser.

## H. Veredito

**FUNCIONAL — validado por integração real, no escopo descrito.** Instalada com fonte única e referência no diretório pessoal de descoberta, presente no seletor segundo confirmação humana, executada por agentes nativos e por chat independente oficial. A suíte tem 32 PASS e a matriz T01–T15 tem 15 PASS com fronteiras explicitadas. Foram comprovados Controller V2/adaptador em cenário sintético, isolamento de escritas Python, recuperação em novos processos, encerramento/reabertura de chat e retomada sem duplicar tickets aceitos. Revisão independente não apontou defeitos materiais restantes.

Limites: formatos antigos como in-progress exigem reconciliação; não houve mutação de feature real, validação de produção ou instrumentação do resolvedor interno de chips. A confirmação do seletor é humana. Reinício do aplicativo/máquina e execução 24/7 não foram testados nem prometidos. Uma skill isolada não mantém o chat vivo; continuidade após encerramento exige nova invocação. Nenhum agendador, daemon ou orquestrador externo foi criado.
