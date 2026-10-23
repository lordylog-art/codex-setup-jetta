# Testes sintéticos — 2026-10-10

## Método e alcance

Dois avaliadores independentes receberam a skill instalada e cenários brutos, sem resultados esperados nem este relatório. Cada um simulou decisões/estados por evento, lendo apenas SKILL.md e as três referências operacionais. O principal conferiu as respostas contra precedência, reservas exclusivas, capacidade, WIP, gates e condições de parada. São testes comportamentais de instruções, não execução de tickets, runners ou integrações reais.

Resultado: **10/10 cenários PASS**, mais ciclo/dependência ausente PASS. Nenhum defeito material demonstrado. Não houve alteração das instruções após os forward-tests.

| Cenário | Entrada resumida | Decisão observada e critério conferido |
|---|---|---|
| S1 | A2 B8 C2 D6 E2 F4 G1 min; A→B/C, B→D, C→E, D/E→F, F→G; 3 slots | CP A=21 B=19 C=9 D=11 E=7 F=5 G=1; inicia A, libera B/C depois; agenda de 21min atinge LB condicionado. |
| S2 | 6 candidatos, zero aceites, executable missing no runner único, dois novos tickets elegíveis | Preserva seis, suspende expansão, prioriza recuperação; aceite bloqueado, ETA desconhecido. |
| S3 | 5 independentes, 40min implementação/5min validação, 2 validadores, 4 slots com principal, dispatch 1min | Quatro implementações iniciais com ganho plausível; quinto no slot liberado, validação nos seguintes; nunca ultrapassa teto. Prazo depende da semântica de overhead. |
| S4 | X reserva shared.ts e fixture DB exclusiva; Y quer ambos; Z independente | Y espera X terminar/confirmar liberação; Z pode avançar; worktree não duplica fixture. |
| S5 | 3 reviews de 10min, navegador único; 2 estáticos de 5min, 4 slots | Um review por vez; estáticos paralelos; carga browser/LB de 30min, agenda atinge limite condicionado. |
| S6 | Palavra em ajuda, 2min, delegação 4min, só inspeção exigida | Principal executa e inspeciona; nenhum agente/DAG/ritual adicional. |
| S7 | Autorização financeira/concorrência; só mocks/typecheck; Standards/Spec independentes e HTTP/persistência reais exigidos | Revisores distintos do autor; sem aceite antes de provas reais e integração exigida. |
| S8 | 4 falhas idênticas browser executable missing; download não autorizado; runner local alternativo talvez utilizável | Inspeção causal local; retry só com mudança comprovada; sem ação viável, bloqueio com condição de retomada. |
| S9 | B implementação depende contrato A; B integração depende A integrado; C implementação depende código A; 2 slots | B pode começar cedo; C libera em código disponível; integração B só após A integrado e gates B. Recalcula por evento. |
| S10 | Esforços/capacidade desconhecidos; 0 aceites em 10min; concluídos 20/30min; abertos há 60min; pedido de 6 agentes/P95/prazo exato | Não inventa prazo/P95/μ=0; não usa abertos como concluídos; mede capacidade e mantém autores/recursos disponíveis. |
| Extra | U↔V, W→Q ausente, Z independente | Bloqueia fatias inválidas sem apagar arestas; Z permanece elegível. |

## Checagens estruturais e aritméticas

- `quick_validate.py`: PASS; frontmatter/nome/scaffold válidos.
- YAML parseado: `allow_implicit_invocation: false`, prompt contém `$smart-orchestrator`, descrição UI dentro de 25–64 caracteres.
- Arquivos UTF-8 e referências locais existentes: PASS.
- CPM conferido em Python independente: CPs de S1 acima; trabalho total 25 agente-minutos; LB=max(21,25/3)=21min.
- Sem helper de produção: cálculo executado temporariamente para conferência, sem dependência nova instalada.

## Compatibilidade e limites

Inspecionados skill-creator/metadados, writing-for-agents, luna-orchestrator, code-review, user-testing-validator e nosso-design disponíveis nesta sessão. A skill usa descoberta do catálogo/regras locais, preserva protocolos especialistas e não herda caminhos de outro usuário nem transforma um fluxo ERP específico em requisito global.

Instalada em C:/Users/caila/.agents/skills/smart-orchestrator; metadados de invocação explícita configurados. Descoberta em novo chat/outro projeto não foi exercitada nesta sessão; se o catálogo não atualizar, reabra o Codex e use o caminho explícito. Modelos/permissões/slots seguem a sessão onde for invocada.

Não executados: produto, CI, deploy, navegador/runner real, HTTP/banco concorrente, revisão humana ou experimento de desempenho real. Isolamento/reservas ainda dependem do cumprimento pelos executores, sem sistema automático de locks. Não há prova de ótimo global geral, ganho causal ou garantia de prazo. S3 demonstrou por que overhead serial do principal e duração por slot devem ser distinguidos nas métricas reais.

Calibração pendente: tempos por etapa, capacidade de validação, retrabalho, overhead, contenção, tolerância de espera/WIP, integração e falhas após aceite, comparados a baseline equivalente.

## Evidência integral — avaliador A

# Forward-test independente — lane A

Data: 2026-10-10 (America/Sao_Paulo). Teste de decisões em simulação; nenhuma execução de produto, agente, navegador ou runner. Fontes lidas: SKILL.md, references/scheduling.md, references/quality-gates.md, references/metrics.md. synthetic-tests.md não foi consultado. Cenários independentes; tempos em minutos desde t=0. Aceite descrito abaixo é condicionado ao sucesso dos gates e integração exigida, nunca inferido de código pronto.

## S1 — precedência e caminho crítico

Arestas sobre nós inteiros, conforme enunciado. Durações medidas incluem os gates; portanto não há liberação antecipada entre etapas neste cenário.

| Nó | Cálculo CP | CP |
| --- | --- | ---: |
| G | 1 | 1 |
| F | 4 + 1 | 5 |
| D | 6 + 5 | 11 |
| E | 2 + 5 | 7 |
| B | 8 + 11 | 19 |
| C | 2 + 7 | 9 |
| A | 2 + max(19,9) | 21 |

Trabalho total = 25 agente-minutos; capacidade = 3 incluindo principal. LB = max(21,25/3) = 21 minutos. Não há carga exclusiva adicional dominante no enunciado. Reserva inicial: um executor para A; dois slots ociosos pois nada mais é elegível. Principal pode executar A; não criar agente apenas para acompanhar.

Evento t=2: A concluído com seus gates; liberar reserva. Fronteira elegível = {B,C}; B tem prioridade CP=19, C=9. Dispatch concorrente B/C com arquivos disjuntos; terceiro slot permanece disponível. CP restante máximo =19; trabalho restante=23; LB residual=max(19,23/3)=19.

Agenda que atinge LB: A [0,2], B [2,10], C [2,4], E [4,6], D [10,16], F [16,20], G [20,21]. Após C, E fica elegível; após E, F ainda espera D. Após B, D fica elegível; após D, F; após F, G. Cmax=21, ótimo condicionado às durações e hipóteses fornecidas porque há agenda que atinge o limite inferior. Reservas liberadas só em conclusões confirmadas. Overhead não fornecido neste cenário: não acrescentei overhead de S3.

## S2 — gate comprovadamente sem capacidade

Fato: seis candidatos prontos, zero aceites e executable missing comprovado no único runner. Capacidade operacional de validação μ=0 por causa do gate indisponível, não por observar zero aceites. Não calcular ρ dividindo por zero; nem Little para fila parada.

Estado inicial: WIP iniciado não aceito >=6 (exatamente 6 se não houver outros iniciados omitidos); fila de validação=6. Congelar expansão do estoque: nenhum dos dois novos tickets de implementação recebe dispatch neste evento. WIP preservado, não descartado para cumprir uma quota.

Alocação: principal mantém diagnóstico/estado e recuperação do runner; até dois slots adicionais apenas para trabalho independente útil já autorizado e com ownership disjunto, como revisão estática dos candidatos ou investigação delimitada do ambiente. Se essas ações não existirem, deixar slots ociosos. Não inventar tarefas de produto nem atribuir três agentes ao mesmo conserto. Não repetir tentativa do mesmo executable ausente sem mudança de ambiente/hipótese. Reserva do runner não deve fingir execução disponível.

Evento após 1h sem recuperação: seis candidatos continuam aguardando, idade aumenta 60min; dois novos tickets continuam pendentes; aceites=0; validação bloqueada por infraestrutura. Revisão estática pode produzir prova parcial válida, sem substituir o gate real. Prazo final desconhecido, nenhum prazo finito defensável. Responsável pelo desbloqueio: titular do diagnóstico/ambiente; condição de retomada: executable disponível e prova curta de runner funcional. Nesse evento, recomputar capacidade e retomar implementação gradualmente. μ*janela=0 não autoriza apagar WIP existente.

## S3 — implementação longa, validação curta

Cinco tickets independentes; implementação total=200 agente-minutos, validação total=25. Dois validadores dão capacidade nominal μ=2*(60/5)=24 tickets/h. Quatro implementadores dão λ nominal=4*(60/40)=6 candidatos/h enquanto há backlog. Incluindo 1min por dispatch de cada etapa no tempo do respectivo trabalho: μ≈20/h e λ≈5,85/h. Esses números são estimativas de capacidade, não vazão de aceites observada.

Escolha inicial: quatro implementações simultâneas, incluindo principal como executor de uma delas; no máximo três agentes adicionais. Recursos/arquivos disjuntos reservados. Ganho plausível: implementação 40min contra overhead 1min; validação tem capacidade muito superior à geração média. Não reservar dois slots ociosos para validação durante toda a implementação. Validadores disponíveis são elegibilidade/capacidade de revisão, não dois agentes extras fora do teto de quatro.

Após primeiro candidato: liberar sua reserva de escrita quando conclusão confirmada. Priorizar o quinto ticket no slot liberado: antecipar sua implementação longa tende a antecipar último aceite. Assim que outros candidatos liberarem slots, alocar até dois avaliadores distintos dos respectivos autores à validação; principal conserva agenda/reservas/integração. Se o primeiro candidato ocorrer muito antes dos outros ou surgir fila material, comparar a espera prevista com o ganho de iniciar o quinto e recalibrar. Nenhum candidato é aceito antes de seus gates; reprovação libera recurso da validação e gera correção no owner, com revisão do impacto na agenda.

Estado logo após primeira conclusão e dispatch do quinto: quatro implementações ativas se os outros três ainda estiverem trabalhando; um candidato aguardando validação; zero validações ativas nesse instante. Depois de mais duas conclusões: duas implementações ativas e até duas validações ativas, respeitando total quatro; fila restante depende de eventos. Em lote aproximadamente simultâneo dos quatro primeiros: uma implementação ativa (quinto), duas validações ativas, um slot de coordenação/integração; fila de candidatos cresce só transitoriamente e esvazia antes do quinto concluir.

Conta idealizada sem overhead: primeira leva pronta t=40; quinto implementado [40,80]; primeiras quatro validações em dois lotes [40,45] e [45,50]; quinto validado [80,85]. Cmax ideal=85. LB básico=max(45,225/4,25/2)=56,25; não prova optimalidade desse plano. Se cada dispatch ocupar exclusivamente o slot da etapa e puder ocorrer sem serialização, conta simplificada: implementações 41min e validações 6min, Cmax≈88; overhead total de 10 dispatches=10 agente-minutos e LB de trabalho=235/4=58,75. Se dispatch exigir tempo serial do principal, esses horários mudam, inclusive sua implementação; o enunciado não informa essa semântica. Registrar eventos reais antes de anunciar prazo exato. Não declarei 88 como resultado medido ou ótimo.

## S4 — colisão de escrita e fixture

Recursos: src/shared.ts capacidade de escrita=1 no mesmo checkout; fixture DB exclusiva capacidade=1. X ativo já reserva ambos. Y inelegível para suas escritas/DB enquanto X detiver reservas, mesmo se houver slot computacional disponível. Dispatch somente de Z, independente, com seus próprios recursos disjuntos. Não liberar X porque deixou de emitir progresso.

Evento conclusão/cancelamento confirmado de X: preservar candidato/diff e estado, confirmar fim de uso dos recursos; liberar arquivo/fixture. Antes de dispatch Y, reavaliar base/contrato deixado por X e demais gates de dependência; reservar os dois recursos de forma conjunta. Se X acabou a escrita mas segue usando DB, a fixture continua reservada: Y espera ou só executa etapa explicitamente separada sem essas demandas. Uma worktree poderia separar arquivo, mas não duplicaria a fixture; não resolve o conflito integral.

Se Y já começou por engano: suspender as escritas afetadas, preservar diffs e atribuir uma pessoa à reconciliação. Não restaurar shared.ts nem apagar trabalho para liberar o slot. Estado esperado com X ativo e Z em execução: X ativo/reservado; Y aguardando recurso; Z ativo; aceites dependem dos próprios gates.

## S5 — navegador único

Navegador real capacidade=1; três reviews V1,V2,V3 de 10min. Trabalho estático S1,S2 de 5min independente; quatro slots totais incluindo principal. Sem diferença de CP informada, ordem estável V1,V2,V3.

Alocação inicial: um avaliador independente para V1 com reserva exclusiva do navegador, dois executores para S1/S2; principal coordena/integra. Uso total=4 slots, browser=1. Não dispatch V2/V3 como se browsers separados existissem; não substituir review por análise estática.

Sequência ideal sem overhead fornecido: t=0 iniciar V1,S1,S2; t=5 concluir estáticos/liberar reservas; t=10 terminar V1/liberar navegador e iniciar V2; t=20 V2→V3; t=30 concluir V3. Avaliador pode ser reutilizado se distinto dos autores e protocolo permitir; nenhum agente existe para vigiar o navegador. Titular de integração mantém coordenação e utiliza evidências válidas progressivamente.

Carga do navegador=30min, LB recurso=30; trabalho total=40min, LB trabalho=40/4=10; CP individual máximo=10. LB=max(10,10,30)=30. Agenda atinge LB condicionado a ausência de overhead e aprovações. Estado em t=5: dois estáticos concluídos, V1 em review, V2/V3 aguardando navegador; em t=10/20: review anterior aprovado/reprovado documentado e reserva transferida somente após encerramento confirmado. Reprovação exige correção e novo planejamento, não aceite automático.

## Resultado do forward-test

A skill forneceu regras suficientes para impedir oversubscription, colisão de arquivo/DB, expansão de WIP com gate parado e aceite fictício. S1 e S5 alcançam seus limites inferiores sob premissas explícitas.

Limitação concreta: scheduling.md exige descontar overhead, mas não especifica se dispatch ocupa serialmente o principal ou o slot da etapa. S3 demonstra que duração exata muda conforme essa semântica (85 sem overhead; cerca de 88 no modelo simplificado por etapa; serialização requer outra agenda). A skill permite registrar desconhecido e calibrar, portanto isso é uma lacuna de dados/modelagem, não evidência de decisão inválida. Outra limitação: LB básico de S3 é frouxo (56,25 versus agenda ideal 85); serve como limite, sem provar ótimo. Não encontrei defeito material inevitável nas regras lidas.

Não executado: produto, subagentes, ferramentas externas, runner, gates reais ou integração. Risco: tempos/aceites nesta lane são condicionais, não evidência funcional de tickets reais.

## Evidência integral — avaliador B
# Forward-test independente — lane B

Data: 2026-10-10, America/Sao_Paulo. Método: simulação manual de eventos e decisões, sem executar produto, runner, revisores ou subagentes. Somente este relatório foi escrito. Cenários fornecidos pelo coordenador; resultados abaixo não são aceites de software real.

Fontes lidas integralmente: `C:/Users/caila/.agents/skills/smart-orchestrator/SKILL.md` e `references/{scheduling,quality-gates,metrics}.md`. `synthetic-tests.md` foi explicitamente excluído pelo coordenador e não foi lido. Nenhum protocolo de projeto foi inventado para substituir os requisitos dados nos cenários.

## S6 — palavra no texto de ajuda

Estado inicial: alteração pendente; baixo risco; esforço fornecido 2min; custo adicional de delegação 4min; inspeção textual é o único gate do projeto.

1. Principal assume a edição direta. Não cria DAG, subagente, revisão extra ou relatório de tarefa. Este relatório existe apenas porque o teste independente foi solicitado.
2. Evento `codeReady`: palavra corrigida; candidato local pronto, ainda não aceito. Principal inspeciona o texto final e o diff para confirmar palavra correta e ausência de alteração incidental.
3. Evento `validationEnded=pass`: inspeção focal satisfeita; alteração local preservada na forma exigida pelo projeto; estado aceito. Se o projeto exigisse integração adicional, seria necessário cumpri-la antes do aceite, mas esse requisito não foi dado.

Alocação: 1 principal, 0 agentes adicionais. Delegação aumentaria pelo menos 4min de overhead para 2min de trabalho, sem ganho plausível. Não roda testes de layout/contrato nem cria infraestrutura. Evidência: SKILL:14,31; scheduling:36; quality-gates:7,27. Resultado simulado: PASS.

## S7 — autorização financeira e gravação concorrente

Estado inicial: candidato pronto pelo principal/autor; typecheck e mocks aprovados, com alcance restrito. Risco alto. Standards, Spec, HTTP negado/permitido e persistência concorrente real estão pendentes. Aceite agora: NÃO.

Alocação inicial simulada, após reservas e handoffs: principal mantém responsabilidade e prepara/executa prova real no ambiente aprovado; slot 2 = revisor Standards; slot 3 = revisor Spec. Ambos distintos do autor. Cada revisor recebe candidato/base identificados e recorte independente; não edita arquivos compartilhados com o autor. Dois revisores podem trabalhar paralelamente sobre leitura do mesmo candidato. Banco/runner são reservados para a prova real; não se presume isolamento apenas por worktree. Se o ambiente não estiver disponível, essa prova fica bloqueada, enquanto revisões estáticas continuam.

Eventos e estados:

| Evento | Estado/ação | Pode aceitar? |
|---|---|---|
| Dispatch de revisões | Candidato em validação; Standards/Spec em execução, provas reais pendentes | Não |
| Standards e Spec aprovados | Revisões cumpridas para o candidato identificado; HTTP e concorrência ainda pendentes | Não |
| HTTP permitido retorna sucesso | Somente identidade permitida provada; identidade negada e concorrência pendentes | Não |
| HTTP negado e permitido válidos | Confirmar recusa com ausência de gravação indevida e efeito persistido permitido; concorrência ainda pendente | Não |
| Persistência concorrente real passa | Demonstrar invariante financeiro exigido com gravações concorrentes reais e consultar estado final; guardar candidato, comandos, resultado e ambiente | Ainda depende de integração exigida e ausência de achados materiais |
| Integração por principal | Comparar candidato aprovado à base integrada; resolução que altera comportamento invalida provas afetadas e demanda nova revisão/prova | Apenas após todos os critérios integrados válidos |
| Todos os gates válidos, integração exigida cumprida | Estado aceito | Sim |

Qualquer achado material retorna a fatia afetada para correção; autor corrige, revisores/provas atingidos revalidam. Não transforma mock em persistência real nem aprovação estática em autorização real. Não dispara CI, deploy ou publicação. Evidência: quality-gates:9,11,13,15,19,21,25–27; SKILL:35,37,45. Resultado simulado: PASS; nenhuma revisão/prova real foi executada neste teste.

## S8 — quatro falhas idênticas do runner

Estado observado: 4 tentativas, assinatura `browser executable missing`, comandos idênticos, código inalterado. Diagnóstico inicial: falha de infraestrutura na inicialização do browser; execução do comportamento do produto não começou. Quinta tentativa idêntica: não executar.

Menor prova útil: inspeção local, somente leitura, do caminho/configuração efetivamente resolvido pelo runner e da existência/executabilidade do binário; conferir o inventário do outro runner local aprovado e sua compatibilidade com o gate. Não reinstalar nem baixar browser, pois download externo não foi autorizado. A hipótese discriminante é “binário ausente no runner original, mas executável compatível disponível no runner aprovado alternativo”.

Eventos e estados:

1. `blocked` na prova dependente do browser original; candidato e provas anteriores preservados. Principal assume diagnóstico local, sem agente vigia e sem invalidar código por falha de infraestrutura.
2. Se inspeção encontra outro runner compatível: reservar seu recurso; mudar ambiente/comando de forma registrada e fazer um smoke mínimo de lançamento/navegação. Esse retry é justificado por mudança material, não pela contagem de tentativas. Smoke de lançamento aprovado apenas libera executar o gate funcional completo, não aceita produto.
3. Se smoke passa: `unblocked`; executar a prova funcional exigida; aceite continua pendente dos demais gates. Se falha com nova assinatura: registrar resultado e hipótese discriminante antes de nova tentativa.
4. Se nenhum runner aprovado é utilizável, ou a menor prova confirma que só download não autorizado resolve: parar tentativas da etapa. Registrar bloqueio, principal como responsável pelo diagnóstico e condição de retomada “runner local aprovado compatível disponível ou autorização e recuperação do ambiente”. Trabalho independente útil pode continuar.

As quatro falhas anteriores não justificam uma quota arbitrária de retries e não provam defeito do produto. Não declarar capacidade de todos os runners como zero antes de inspecionar o alternativo. Evidência: SKILL:41; quality-gates:21; scheduling:45,49. Resultado simulado: PASS.

## S9 — dependências por etapa e dois slots

DAG de etapas relevante:

- `A.contrato congelado -> B.implementação`.
- `A.integrado -> B.integração`.
- `A.código disponível em candidato/base compatível -> C.implementação`.

Não existe duração defensável para calcular CP numérico nem autoridade para supor que os arquivos de B/C são disjuntos: confirmar fronteiras antes de dispatch. Distingo elegibilidade por dependência de disponibilidade imediata de recurso.

| Momento | A | B implementação / integração | C implementação | Alocação possível |
|---|---|---|---|---|
| Inicial | Implementação rodando em subagente; contrato congelado | Implementação elegível / integração bloqueada por A integrado | Bloqueada por código A | 2 slots: A subagente + principal implementando B, se ownership/recursos permitem |
| A código pronto, revisão pendente | Candidato pronto; não validado nem integrado | Implementação segue elegível / integração segue bloqueada | Elegível se código A realmente disponível em base compatível; aceite e integração própria continuam sujeitos aos gates | Confirmar término/liberação do slot A antes de reutilizar. Principal suspende B em ponto seguro e revisa/valida A se independente do autor e autorizado pelo protocolo; slot liberado pode implementar C se há ganho, ownership e capacidade de aceite. Se B já usa recurso incompatível, C aguarda |
| A validado e integrado | Dependência de integração satisfeita; aceite de A depende de todos os critérios próprios | Implementação elegível / integração elegível se B também aprovado, conflitos e demais gates satisfeitos | Implementação segue elegível; conferir equivalência do código A integrado com candidato usado por C | Principal integra B aprovado; outro slot mantém implementação/revisão elegível de B/C, conforme gargalo e reservas |

Uma revisão de A poderia ainda alterar o contrato/código: nesse evento, recalcular dependências e invalidar apenas evidência afetada em B/C. Elegibilidade de C no segundo momento não implica obrigação de despachar nem autorização de integrar A sem revisão. Se principal não puder validar A com independência requerida, usar o slot liberado para revisor e manter C elegível em espera. Não escolho entre agendas como ótimo global sem durações/gates/recursos; ambas respeitam precedência e capacidade, e a escolha segue o gate dominante observado.

Aceite da feature inteira: A/B/C e todos os critérios autorizados com provas válidas, integração exigida concluída, revisão de deltas e nenhum achado material pendente. Integrar A ou B parcialmente não encerra a feature. Evidência: scheduling:9–14,24,26,28,34; SKILL:19,25,35,43–45; quality-gates:25–27. Resultado simulado: PASS.

## S10 — estimativas, amostra pequena e demanda por seis agentes

Fatos separados de inferências: quatro tickets de esforço desconhecido; dois autores disponíveis; capacidade do runner desconhecida; zero aceites observados em janela de 10min; lead times concluídos de 20min e 30min (n=2, janela histórica não informada); três candidatos abertos há 60min.

Resposta operacional ao usuário: “Não há base para prazo exato ou P95 confiável. Temos dois lead times concluídos, 20 e 30min; média descritiva 25min. Há três candidatos com idade atual de 60min. Vou medir o gate e o esforço restante antes de prever a conclusão. Há dois autores disponíveis; seis agentes não têm capacidade demonstrada.”

Não calcular P95 como precisão operacional: qualquer quantil numérico desses dois valores depende de método e não representa a cauda; usar os valores brutos. Não somar 60/60/60 à média de concluídos: são observações censuradas. Vazão de aceites nessa janela = 0 / (10/60h) = 0 aceites/h, explicitamente observada em janela curta. Capacidade μ de validação permanece desconhecida; não concluir μ=0. λ, ρ, CP restante, LB e makespan futuro permanecem desconhecidos. Sem estabilidade/fluxo compatível não aplicar Little para gerar prazo.

Próxima ação simulada: principal registra eventos/idade e faz inspeção curta da fila e disponibilidade/configuração do runner; obtém esforço restante por etapa/família dos quatro tickets. Não cria instrumentação extra. Com três candidatos envelhecidos, prioriza revisar/diagnosticar/destravar o estoque antes de expandi-lo. Segundo autor recebe revisão independente de candidato que não tenha escrito, se elegível e permitido, ou diagnóstico/trabalho útil disjunto. Dois autores não implicam dois revisores independentes nem dois runners: confirmar essas capacidades.

Eventos:

- Runner comprovadamente utilizável: reservar, executar menor prova e medir tempo/resultado de validação; ampliar implementação gradualmente somente com ganho e capacidade de aceite observados.
- Runner comprovadamente indisponível: μ operacional desse gate = 0; bloquear prova, recuperar gate autorizado e suspender expansão desnecessária de candidatos. Prazo continua desconhecido sem condição/tempo de recuperação.
- Nova conclusão/aceite: atualizar métricas na janela/fronteira declaradas, somar amostra real e recalibrar faixas; não prometer prazo nem atribuir ganho causal à quantidade de agentes sem baseline comparável.

Seis agentes: não despachar; autorização de quantidade não cria seis autores elegíveis, slots da ferramenta, ownership ou runner. Limite ativo tem de contar principal e agentes existentes; começar conservador nos dois autores efetivamente disponíveis, com reservas por recurso. Evidência: scheduling:24,32–36,41,45–51; metrics:9–24. Resultado simulado: PASS.

## Microcenário — DAG inválido

Entrada: U depende V, V depende U; W depende Q ausente; Z independente.

1. Antes de delegar, verificar referências/topologia: ciclo U↔V; referência Q inválida. Não há ordenação topológica global válida e não calcular CP global por recorrência nesse grafo.
2. U e V: bloquear etapas atingidas pelo ciclo e seus dependentes transitivos. Inspecionar fontes canônicas para descobrir erro de etapa/aresta ou requisito real; não apagar dependência para liberar trabalho. Se não houver resolução documental, solicitar decisão material do responsável.
3. W: bloquear etapa dependente de Q. Procurar Q no inventário canônico existente; se apenas omitido do registro, reconciliar; se realmente inexistente, resolver origem/requisito com o responsável. Não criar ticket de produto ou inventar que Q foi concluído.
4. Z: preservar como ramo elegível; avançar dentro do escopo, recursos e gates disponíveis. Após correção legítima das arestas/referência, recalcular elegibilidade/CP e liberar apenas a fatia corrigida.

Resultado simulado: PASS. Evidência: scheduling:5,14,18–26; SKILL:12,19,25.

## Achados reais e limites

Não encontrei defeito material demonstrável nas decisões prescritas pelas quatro fontes lidas para S6–S10 e DAG inválido. O teste produz contraprovas úteis para atalhos: S7 não permite aceitar só com mocks/revisão; S8 não permite quinto retry idêntico nem download; S9 libera C no código pronto sem antecipar integração B; S10 não converte zero aceites em μ=0 nem abertos em lead times concluídos.

A referência a `synthetic-tests.md` em SKILL:14 está fora da leitura por instrução expressa e o coordenador informou que ainda não existe; isso é limitação documental conhecida da montagem do teste, não defeito novo confirmado por esta lane. Não usei o próprio conjunto de testes para antecipar respostas.

Limites: simulações não verificam invocação automática da skill, execução de agentes, isolamento real de recursos, revisão humana, comportamento HTTP, banco concorrente ou recuperação real de browser. O agendamento de S9 é condicionado às durações/recursos não fornecidos e não prova optimalidade. Nenhum produto, repo, ticket, skill ou memória foi modificado; nenhuma ação externa foi executada.

