# Contrato de entrega proporcional

## Padrão: tickets diretos

Entregue o pedido com o menor processo suficiente. Pedido e decisões atuais do usuário definem o comportamento; regras do projeto preservam segurança e dados. Critérios adicionais precisam apontar requisito aplicável ou risco concreto causado pela mudança. Melhorias opcionais ficam fora do aceite.

- Ticket: resultado, escopo/delta sobre base existente, poucos critérios observáveis, dependências técnicas por etapa e verificação focal. Não exigir runtime disponível para escrever tickets.
- Verificação: selecionar o mecanismo alterado e as regressões relacionadas. Teste de componente/função pode bastar para lógica local; fronteira de autorização, persistência ou migração exige prova pertinente dessa fronteira. Uma mesma execução pode cobrir vários critérios.
- Revisão: consolidar achados materiais conforme risco e protocolo aplicável. Revalidar apenas alterações e impactos; conservar provas equivalentes. Não gerar reviewer ou arquivo de evidência por critério como padrão.
- Dependência: nomear o contrato/código/ambiente necessário e a etapa bloqueada. Fechamento de issue ou aceite global de outra feature não é pré-requisito automático para começar código independente. Respeitar conflitos reais de escrita e ativação segura.
- Conclusão: comportamento pedido implementado, verificação pertinente realizada, integração exigida validada e defeitos materiais resolvidos. Registrar resultado e limitações uma vez no ticket/registro existente. Documentação administrativa não cria outra rodada de QA.
- Estagnação: após duas tentativas equivalentes sem informação nova, mudar hipótese/método e buscar a menor reprodução. Sem ação útil autorizada, informar impedimento concreto e condição de retomada uma vez; retomar após mudança relevante, sem turnos sucessivos de espera nem PASS presumido.

Planos e provas existentes continuam úteis. Na revisão de uma fila, separar requisitos do usuário de exigências adicionadas pelo agente. Quando o usuário autorizar simplificar o processo, reconciliar as últimas no registro existente sem apagar histórico ou enfraquecer segurança/dados. Não editar silenciosamente um plano ativo com hash controlado: manter o estado histórico e registrar a mudança de modo/regras antes de continuar. O controller não é requisito para o modo direto.

## Modo V2: somente quando explicitamente solicitado

As seções abaixo descrevem compatibilidade com planos V2 e seu controlador. São aplicáveis apenas ao modo V2 escolhido; não devem ser importadas como gates de tickets diretos. Ter vários tickets ou encontrar um JSON antigo não seleciona esse modo automaticamente.

To-Tickets prepara este contrato para feature complexa; Smart Orchestrator o consome após autorização de execução. Preserve a decomposição coesa, tracker, aprovação e protocolo local. Use referências à SPEC/tickets/decisões como requisitos canônicos, sem recopiá-los em outro documento. Campos operacionais adicionais não substituem o contrato aprovado.

## Localização e vínculo

1. Resolver o workspace/tracker pela To-Tickets e Spec Workspace existentes. Procurar o plano semântico equivalente no Index e na categoria pertinente antes de criar.
2. Em workspace Obsidian, reutilizar `Research/<feature>/execution-plan.json` quando já houver a pasta da feature; na estrutura rasa usar `Research/execution-plan-<feature>.json`. Em tracker local usar `.scratch/<feature>/execution-plan.json`. Preservar caminhos anteriores válidos.
3. Vincular o caminho canônico nos tickets e na seção gerada do Index, conservando seções manuais. Para tracker externo, manter o plano técnico local vinculado aos IDs reais; Obsidian conserva seu override de tracker.
4. Estado/eventos/cache do controlador ficam no worktree em `.local/orchestration/<feature>/`, ignorado pelo Git por configuração local apropriada. O JSON é plano operacional; tracker conserva seus estados e documentos canônicos. Não transformar `PLANNED` etc. em novos valores de `ticket_status` do adaptador. O orquestrador reconcilia ponteiros e conclusão; aceite de código sozinho não resolve ticket.

## Campos e condições

Use [execution-plan.example.json](../assets/execution-plan.example.json) como formato executável e `scripts/controller.py` como autoridade de validação. O exemplo é sintético: substitua escopo, gates, IDs, critérios e recursos pela feature; não copie seus gates sem analisar risco.

| Campo | Conteúdo obrigatório do planejamento |
|---|---|
| `version`, `feature`, `spec` | Versão 2, identificador estável da feature e referência à SPEC aprovada. |
| `shared_contracts` | Referências canônicas dos contratos compartilhados, com owner e condição de congelamento nas fontes vinculadas. |
| `criteria` | Todos os critérios obrigatórios identificados: `id`, ticket responsável e `gate` requerido. O gate correspondente inclui o ID em `criteria`. |
| `capacity` | Capacidade real disponível de implementação/validação; distinguir estimativa de medição. |
| `tickets[].id`, `ticket`, `author`, `scope` | ID/tracker canônico, executor responsável e fronteira de escrita/arquivos. Consumers e exclusões relevantes constam no ticket/contrato vinculado. |
| `integration_owner` | Titular único da operação de integração. Autoridade/permissões e condição de integração constam na fonte vinculada. |
| `maturity` | `expected`: comportamento completo desta etapa; `incomplete`: referências de obrigações futuras e respectivos destinos; `functional_review`: prontidão esperada para revisão funcional; `final_qa`: incremento apto ao QA final integrado. |
| `dependencies` | `ticket`, `type`, `source_stage`, `target_stage`, `condition` e, para liberação por prova, `gate` do predecessor. |
| `resources` | Identificadores de recursos exclusivos; usar o mesmo ID e ledger compartilhado entre worktrees que disputem o mesmo browser/runner. |
| `estimate_minutes` | Duração restante estimada positiva ou `null` quando desconhecida; fonte/incerteza na nota existente. |
| `gates` | `id`, `stage`, `kind`, `required`, `scope`, IDs de `artifacts`, IDs de `criteria`; `independent: true` quando obrigatório. Gate de integração pode usar `final_qa: false` para prova local do incremento; o padrão é true em `ACCEPTED`. |

Os campos de maturidade descrevem o resultado esperado do incremento, não uma afirmação de que ele já existe. Antes de avançar a `REVIEW_READY`, o autor demonstra conclusão da unidade relevante; o controlador exige declaração `functional_review: true` e gates anteriores válidos, mas não inspeciona semântica do produto. `maturity.final_qa: true` habilita prova de gate com `final_qa: true`, com dependências satisfeitas. Integração local usa `gate.final_qa: false` quando o incremento conserva futuros explícitos; a feature exige ao menos um gate obrigatório de integração final em `ACCEPTED` ligado a critério. Incremento propositalmente imaturo não recebe QA final; planejar checkpoint/contrato antecipado ou completar o incremento, preservando requisitos.

Cada obrigação futura em `incomplete` tem a forma `{"criterion":"C2","ticket":"T2","gate":"integration"}` e aponta para o mapeamento obrigatório exato na mesma feature; o controlador rejeita IDs ausentes ou divergentes. `shared_contracts` é uma lista obrigatória de referências, vazia quando não houver contrato compartilhado. Conferir cobertura total com a SPEC antes da aprovação. O controlador verifica critérios declarados; o planejador/reviewer verifica que nenhum requisito da SPEC ficou fora deles. “Futuro” altera o momento de validação, nunca dispensa a obrigação final.

## Dependências por estágio

Tipos: `contract`, `implementation`, `review`, `integration`; `validation` é compatibilidade com To-Tickets existente, equivalente a dependência de revisão/prova. Preferir source/target explícitos e `condition: "stage_reached"`, a condição determinística suportada. Sem especificação, contract/implementation liberam em `CODE_READY`; review/validation usam predecessor `REVIEWED`; integration usa predecessor `ACCEPTED`, com destino de revisão/integração conforme controlador.

Um contrato publicado cedo pode usar predecessor `PLANNED`/`IN_PROGRESS`, gate obrigatório de `kind: "contract"` com prova válida, e destino `IN_PROGRESS`. Isso libera trabalho independente antes do aceite do predecessor. Dependência de integração pode bloquear somente `INTEGRATION_READY`; trabalho anterior continua elegível. Use `gate` quando o estágio isolado não demonstra a condição de liberação. Condições semânticas são avaliadas pelo agente e demonstradas no artefato desse gate, sem inventar condições CLI não suportadas.

Conservar a projeção `Blocked by`/`blocked_by` conservadora do tracker. O mapa tipado não autoriza ignorar um bloqueio do adaptador original; distinguir elegibilidade operacional de claim permitido. Detectar ciclos, contratos indefinidos, ownership sobreposto e recursos incompatíveis antes da publicação.

## Critério → gate → evidência

Para cada critério, definir no ticket/contrato vinculado: superfície local/contratual/integrada; mecanismo real e consumidores pertinentes; estágio; risco; reviewer e independência; recurso/ambiente necessário; comando/interação discriminante e prova esperada. Mapear identificadores no JSON. Um critério composto conserva obrigações observáveis separadas (CAS, rollback, auditoria, idempotência etc.).

Escolher gates conforme [contextual-review.md](contextual-review.md) e protocolos especialistas. Gates locais precedem `CODE_READY`; review maduro conclui em `REVIEWED`; prova de integração local pode liberar `INTEGRATION_READY` a partir de `REVIEWED` quando seus pré-requisitos forem satisfeitos, ou concluir em `ACCEPTED`. QA final fica no gate de aceite correspondente. Revisão antecipada usa `kind: "contract"`/segurança/arquitetura pertinente, sem fingir `kind: "review"` funcional antes da maturidade.

Cada ID em `artifacts` exige arquivo de prova, resultado explícito, autor/reviewer, fingerprint de código, configuração e ambiente sanitizado, além do próprio artefato. Declarar todos os arquivos/dependências que podem invalidar a conclusão; hash não identifica sozinho um consumidor omitido. Ambiente sanitizado registra versões, contexto, dataset sintético, identidade não sensível e condições relevantes; não copiar credenciais/dumps operacionais.

Mudança focal revalida delta/impactos e conserva provas não atingidas. Mudança estrutural ou segurança amplia invalidação conforme política; preservar gates obrigatórios. Plano alterado após inicialização exige migração explícita/reconciliação, pois o controlador rejeita hash divergente: não editar silenciosamente o plano para afrouxar um gate nem descartar ledger/provas.

## Pronto para execução

Antes do handoff: aprovação local atendida; cobertura de todos os requisitos; referências resolvidas; maturidade/futuros definidos; ownership e integração atribuídos; dependências acíclicas; gates/provas/recursos mapeados; capacidades/permissões verificadas. Falta bloqueia apenas a decisão ou etapa dependente. O handoff fornece plano canônico, tracker/workspace, fila autorizada e bloqueios; Smart Orchestrator decide recursos e agenda. Aprovação de planejamento não autoriza automaticamente codificação.
