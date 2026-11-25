# Revisão Goldfish do fluxo híbrido

Leia [a integração Codex oficial](egm/docs/codex.md) ao iniciar a primeira revisão. Use as personas e padrões oficiais EGM incluídos em `references/egm/`, sem reescrevê-los. Resolva esses arquivos contra esta skill global, independentemente do projeto atual; a licença original está em `egm/LICENSE`. As instruções de instalação do plugin na integração oficial não são pré-requisito deste fluxo híbrido. Este fluxo chama suas lentes diretamente; não declara ter executado `egm-brainstorm`, `egm-draft`, cinco etapas de `egm-review` ou convergência de `egm-review-loop` quando isso não ocorreu.

## Selecionar lentes

Escolha lentes distintas pelo risco; normalmente duas por pacote material, não duas por artefato. Correção mecânica já decidida não recebe enxame. Acrescente especialista por lacuna concreta de cobertura, não por preferência por mais agentes.

| Modo | Lentes usuais | Pergunta adicional de revisão |
| --- | --- | --- |
| grooming | design_critic em BRAINSTORM e comprehension em BRAINSTORM | Que decisão ainda aberta muda comportamento, limite ou experiência? |
| spec | design_critic e comprehension em REVIEW | A spec é consistente, compreensível e verificável sem a conversa? |
| blocos | implementation_readiness e zoom_out em REVIEW | Cada bloco entrega algo observável e a progressão cobre o escopo? |
| tickets | implementation_readiness e codebase_details em REVIEW | Tickets cobrem requisitos/blocos sem inventar APIs, dependências ou trabalho? |

Personas: [design_critic](egm/agents/design_critic.md), [comprehension](egm/agents/comprehension.md), [implementation_readiness](egm/agents/implementation_readiness.md), [zoom_out](egm/agents/zoom_out.md), [codebase_details](egm/agents/codebase_details.md). Em REVIEW, use o padrão pertinente: [feature-spec](egm/resources/document_standards/feature-spec-standard.md), [implementation-readiness](egm/resources/document_standards/implementation-readiness-standard.md) ou [zoom-out](egm/resources/document_standards/zoom-out-standard.md). Comprehension não recebe padrão de implementação.

Calibre a prontidão ao artefato: blocos são estágios funcionais, não tickets detalhados. Neles, use o formato original de blocos como contrato e o padrão zoom-out quando pertinente; não aplique o padrão de implementação para exigir lista exaustiva de arquivos ou decomposição técnica prematura. Reserve implementation-readiness para tickets/planos de implementação. Uma área conceitual identificada como tal não é caminho inexistente afirmado como fato.

Distinga a **persona `implementation_readiness`**, que pode avaliar a prontidão funcional de um bloco, do **padrão `implementation-readiness-standard`**, cujo detalhamento de execução se aplica a tickets/planos e não deve ser imposto aos blocos.

Para tickets, passe spec/origem e blocos selecionados como baseline explícita. Para grooming, passe somente hipótese, decisões registradas e dúvidas no documento; não perguntas/respostas da transcrição. Uma capacidade ausente não vira parecer vazio.

### Pacote integrado

Para spec + blocos + tickets da mesma versão, use **implementation_readiness** para resultados observáveis, decisões, testes, divisão/dependências e cobertura; **codebase_details** para confrontar todos os contratos com as fontes, acesso, dados e efeitos. Ambos leem fonte e pacote atual. Prontidão de blocos significa incremento funcional; tickets exigem passos verificáveis. Se aparência/UX material ficar descoberta, substitua uma lente ou acrescente especialista visual com recorte explícito; não imponha três revisores a backend ou ajuste mecânico.

Agrupar não reduz o contrato de revisão: dê à lente de prontidão os padrões **feature-spec** para spec e **implementation-readiness** para tickets, mais o formato funcional de blocos quando selecionados. Exija motivação/alternativas e riscos da spec, compreensão das jornadas, critérios/provas e dependências do pacote. Escolha outros especialistas se uma dessas obrigações ficar descoberta; duas lentes não são um teto de qualidade. Racional ausente de decisão já tomada pede documentação da razão, não reabrir a escolha no grill.

Achados identificam requisitos/critérios e artefatos atingidos. O principal reúne duplicatas mantendo evidências: contrato contradito em três arquivos é um problema em três locais, não três perguntas. Critério sem ticket/prova continua lacuna mesmo repetido na spec. Migração, concorrência, retry, cancelamento e escala ampliam cobertura somente quando aplicáveis.

## Despachar e aguardar

Inspecione o schema nativo: use `fork_turns: "none"` ou equivalente `fork_context: false`. Cada nova rodada/materialização recebe novos revisores, não follow-up de um contexto antigo. Não troque o modelo da sessão por conta própria. Respeite a capacidade disponível; ondas/execução serial são permitidas, com alcance declarado. Não inicie bot, chat separado visível no sidebar, serviço ou MCP novo.

Pode usar o pool Codex MCP já conectado se fornecer threads independentes sem histórico do pai. `agent_start` inicia revisores read-only; passe só persona/padrão/recorte e fontes aprovadas. Colete a frota por `agent_result`/`agent_wait` em lote, sem espera serial. Isso não autoriza instalar/conectar serviço ou ampliar permissões. Não afirme configuração/modelo não exposto pelo runtime.

**Antes da frota**, comprove no runtime uma leitura representativa dos arquivos necessários. Acesso do principal não prova acesso dos filhos; outro disco pode ser bloqueado mesmo com raiz declarada. Se houver falha compartilhada de acesso/capacidade, pare novos disparos e resolva o insumo autorizado antes da nova bateria; não desperdice um retry por revisor na mesma falha de infraestrutura. Snapshots de teste só de fontes autorizadas, com caminhos/versões rastreáveis e sem ampliar permissões. Parecer sem leitura de persona/padrão/fontes é incompleto, mesmo que opine pelo texto disponível.

O primeiro revisor pode completar sua revisão após o preflight bem-sucedido, sem agente extra. Reutilize a prova para os mesmos caminhos/permissões; não abra uma sonda por arquivo ou revalide ambiente já comprovado sem mudança.

Passe caminhos absolutos da persona, documento, padrão quando houver e leituras aprovadas. Defina modo e faixa/artefatos alvo. Revisores são read-only e não negociam diretamente com o usuário. Peça leitura integral das fontes fornecidas, achados com severidade, localização, evidência, consequência e pergunta/recomendação; zero achados é um resultado válido. Não forneça gabarito, transcrição, conclusões do autor ou memória para preencher lacunas.

Peça retorno completo; aguarde conclusão efetiva. Falha ou timeout: uma tentativa adicional, depois estado “não executado” com impacto. Nunca marque revisão como limpa ou consenso quando faltou um revisor. Sem ferramenta de contexto fresco, pare a etapa dependente e informe a limitação; não simule Goldfish na conversa principal.

## Consolidar e devolver ao grill

O principal verifica evidências, deduplica e classifica achados como correção documental, fato a investigar, decisão do usuário, contestado com fonte ou melhoria opcional. Mantenha a severidade original; discordância é contestação fundamentada, não rebaixamento silencioso. Achado não confirmado é hipótese, não requisito.

Perguntas dos revisores entram na fronteira do grill somente quando afetam uma decisão e seus pré-requisitos estão resolvidos. O principal escolhe a ordem, não a resposta de produto. Conserve achados abertos e riscos expressamente aceitos na versão vigente. Depois de corrigir, revise o delta pertinente; mudança de escopo invalida aprovação da versão anterior e exige nova aprovação.

Para entregas, verifique cobertura requisito/critério → bloco/ticket, resultado observável, dependências acíclicas, contratos disponíveis e provas propostas. Não aceite “teste passou” como prova de função ainda inexistente; documentação não é implementação. Aprovação do documento não é autorização para executar código.
