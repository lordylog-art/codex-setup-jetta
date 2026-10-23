# Controlador local

Antes de delegar, consulte `schedule`, confirme elegibilidade, slots e disponibilidade de recursos; reserve recursos exclusivos com `reserve` e use a ferramenta nativa de subagentes com o modelo explícito definido em [Delegação](../SKILL.md#delegação). O controlador não escolhe modelos nem despacha agentes. `status --summary --after N --limit 10` devolve estado compacto, state_path, motivos de bloqueio/invalidação e uma página de eventos novos. Use next_cursor enquanto has_more; cursor indica o total, não o fim da página. A saída sem --summary permanece integral. Leia arquivos com ferramentas locais; não substitua contratos obrigatórios nem aceite semântico por recortes/hashes. `close` verifica os gates reais do controlador antes de encerrar.

`scripts/controller.py` usa Python e biblioteca padrão. Opera arquivos locais, sem Node, daemon, banco ou inicialização da aplicação. Use o plano canônico preparado por [planning-contract.md](planning-contract.md); consulte `--help` e `<comando> --help` para a interface instalada.

## Invocação

```powershell
python "<skill>/scripts/controller.py" --plan "<execution-plan.json>" --root "<worktree>" init
python "<skill>/scripts/controller.py" --plan "<execution-plan.json>" --root "<worktree>" status
python "<skill>/scripts/controller.py" --plan "<execution-plan.json>" --root "<worktree>" schedule
```

Opções globais precedem o comando: `--plan` e `--root` obrigatórias; `--state-root` e `--resources-root` opcionais. Caminhos de código/configuração/ambiente/artefatos relativos resolvem contra `--root`, não contra a pasta do plano. Caminho absoluto também é aceito.

| Comando | Argumentos após o comando | Efeito |
|---|---|---|
| `init` | nenhum | Criar ledger; recomeço com mesmo plano/root conserva estado existente. |
| `status` | nenhum | Ler estado, provas, achados e histórico. |
| `schedule` | nenhum | Mostrar fila elegível, bloqueios, recursos, capacidade e sugestão conservadora de dispatch. |
| `transition` | `--ticket ID --to ESTAGIO` | Avançar exatamente um estágio, exigindo dependências e gates pertinentes. |
| `evidence` | `--ticket ID --gate ID --proof ID --artifact ARQUIVO --actor IDENTIDADE --code ARQUIVO... --config ARQUIVO... --env ARQUIVO... --result PASS\|FAIL` | Registrar artefato declarado e fingerprints com resultado observado explícito; omissão é rejeitada. |
| `change` | `--ticket ID --kind focused\|structural\|security --paths ARQUIVO...` | Invalidar provas atingidas e recuar para a etapa de recomprovação. |
| `block` | `--ticket ID --reason MOTIVO` | Preservar estágio anterior e registrar BLOCKED. |
| `resume` | `--ticket ID` | Restaurar estágio anterior; não fabrica provas nem remove pré-requisitos. |
| `reserve` | `--ticket ID --resource ID` | Reservar recurso declarado; disputa entre titulares registra BLOCKED e falha. Segunda reserva do mesmo ticket também é rejeitada, preservando a primeira operação; reserve não é idempotente. |
| `release` | `--ticket ID --resource ID [--confirm-owner UUID]` | Liberar reserva própria ou reserva cujo owner foi confirmado manualmente. |
| `attempt` | `--ticket ID --failure ASSINATURA [--hypothesis TEXTO] [--information TEXTO] [--progress ARQUIVO]` | Registrar diagnóstico; repetição exige hipótese/informação nova ou fingerprint diferente de progresso. |
| `finding` | `--ticket ID --id ID --evidence ARQUIVO --status open\|resolved` | Registrar achado; resolvido não reabre com a mesma prova. |
| `close` | nenhum | Conferir aceite de todos os tickets, gates válidos, dependências e liberação dos recursos desta execução; encerrar. |

IDs de gate/proof/resource devem existir no plano. Prova de integração exige ator igual ao integration_owner designado. Strings de ator e hipótese são fornecidas pelo agente: o controlador compara identidades e novidade literal, sem autenticar pessoas ou julgar a qualidade do diagnóstico. Resolver achado significa que o reviewer confirmou a correção; escrever `resolved` sozinho não prova isso.

## Estados, provas e retomada

Sequência: `PLANNED → IN_PROGRESS → CODE_READY → REVIEW_READY → REVIEWED → INTEGRATION_READY → ACCEPTED`. `BLOCKED` armazena motivo e estágio anterior. Alteração invalidante recua o ticket; histórico conserva eventos. Transição nunca transforma prova ausente, FAIL ou stale em PASS. Independência exige ator diferente do autor declarado; obrigação de reviewers distintos Standards/Spec continua sendo responsabilidade do orquestrador/protocolo.

Gate obrigatório cobra todos os IDs de artefatos no estágio definido e nos posteriores. Prova guarda fingerprints dos arquivos de código, configuração, ambiente e artefato; arquivos ausentes/alterados invalidam sua utilização. Declarar configuração pertinente e um manifesto sanitizado do ambiente, com versões/contexto/dataset/identidade não sensíveis; credenciais ficam fora desses arquivos. Mecanismos externos precisam da evidência real no artefato: o controlador não executa teste/browser, não verifica semântica do conteúdo e não detecta consumidores omitidos do fingerprint.

Maturidade planejada `functional_review: true` permite revisão funcional a partir de `REVIEW_READY`; agente primeiro comprova o escopo concluído. Gates `kind: review` concluem em `REVIEWED` ou posterior. Revisões antecipadas de contrato usam o kind pertinente. Prova de integração pode ser registrada a partir de `REVIEWED`, após checar os pré-requisitos de `INTEGRATION_READY`; assim um gate local pode liberar essa transição sem circularidade. `gate.final_qa` é booleano opcional, padrão true quando o gate conclui em `ACCEPTED`; true exige `maturity.final_qa: true`. Integração local de incremento com futuros explícitos usa `gate.final_qa: false`. O plano ainda exige pelo menos um gate obrigatório de integração final em `ACCEPTED` ligado a critério: a obrigação final da feature permanece.

Dependências usam source/target explícitos, `condition: stage_reached` e gate opcional do predecessor. Contrato congelado com prova pode liberar implementação cedo; integração continua bloqueada pelo seu pré-requisito. `close` cobra todos os critérios declarados por seus gates; completude desses critérios contra a SPEC é responsabilidade do planejamento/review.

Mudança `focused` invalida fingerprints atingidos; `structural` amplia invalidação do ticket; `security` preserva gate obrigatório de segurança e amplia review/integração pertinentes. O agente declara impactos indiretos e mudanças relacionadas nos demais tickets. Conserva provas não afetadas quando equivalência é demonstrável. Fechado o ledger, novas mutações são rejeitadas, salvo liberação de recurso.

O plano é imutável durante uma execução: hash divergente rejeita retomada. Não há comando de migração automática. Se precisar alterar plano/autor/contratos, reconciliar explicitamente fora do controlador, preservar plano e ledger anteriores e aprovar a mudança segundo o processo; não apagar estado para simular execução limpa. Tickets em andamento não são migrados automaticamente para V2.

## Concorrência e limites

Estado padrão: `<worktree>/.local/orchestration/<feature>/state.json`, protegido por `state.lock`; histórico está em `history`. Escritas usam arquivo temporário, flush/fsync e replace atômico; trava Windows usa `msvcrt`. Ledger identifica root e owner da execução; root incompatível é rejeitado. Mantenha o diretório ignorado localmente pelo Git. `--state-root` permite isolamento explícito em testes; não compartilhar estado entre worktrees.

Recursos padrão: `~/.codex/orchestration/resources/resources.json`, protegido por `resources.lock`, com histórico de reservas/liberações. Worktrees usam o mesmo `--resources-root` e ID exato para o mesmo recurso. Garantia cobre processos cooperantes neste controlador: não é trava do sistema operacional sobre browser/runner e não impede ferramentas externas de usá-los. Todos os participantes reservam antes de usar e liberam ao terminar.

Não há TTL nem recuperação automática de owner abandonado. Após verificar que a operação e os processos responsáveis realmente pararam, conferir owner UUID no ledger e liberar com `--confirm-owner` exato; nenhuma idade da reserva prova abandono. Ledger guarda owner/root/ticket, não autentica quem confirma. Travas são liberadas pelo sistema ao encerrar processo, mas reservas persistidas permanecem até liberação explícita. Arquivos de estado e recursos são substituídos individualmente; após queda, reconciliar seus registros antes de retomar operações.

`schedule` é aconselhamento determinístico de fila/capacidade e caminho crítico estimado agregado, não solver ótimo de RCPSP nem reserva automática. Em trabalho iniciado, duração restante desconhecida aparece como unknown; não representar estimativa como medição. O agente aplica CPM/RCPSP/WIP, compara benefício esperado do paralelismo com overhead, resolve prioridades semânticas e respeita recursos/slots reais. Escolha de próximos agentes não concede permissões externas.
