# Contratos recuperados do Connect Channels

Fontes locais: `C:/Users/caila/Documents/Codex/connect-channels-automation/`.
Offsets abaixo são caracteres base zero no JavaScript minificado. Bundles foram baixados dos URLs reais observados na aba autenticada do Chrome ou dos imports literais desses bundles, sem executar código do fornecedor.

## Evidência e alcance

- Angular: `artifacts/main.f86dbff72de5dbe6.js`; REA Evidence `ev_e55c295a156ff2186685a7c978edc17295a2c9d831d2853fd50e5117bd04857a` em `rea-analysis.json`.
- API Angular: módulo 93483 @3737253, extraído em `library/module-93483.js`.
- Enums Angular: módulo 11332 @3794428, `library/module-11332.js`.
- Editor simples: módulo 79510; formulários em `artifacts/4302.889a9d0a3176f50b.js`, módulo 89618.
- Criação/configuração: `artifacts/7849.1290e1a46a73942b.js` @117227–120552.
- Editor avançado: `builder/index-DNHyfjE_.js`, API @1858606 e serialização @1831541.
- Catálogo real: `builder/ChatbotCreateNodesComponent-DOgOfPZg.js`.
- Formulários avançados: `builder/ChatbotEditNodeComponent-D0vBCtc8.js`.
- Triggers: `builder/ChatbotEditTriggerComponent-D4jjiDnT.js` e `builder/string-utils-DII2pBZF.js`.
- REA do avançado: `rea-builder-analysis.json`. A análise abrange os 14 módulos inicialmente inventariados; os imports adquiridos depois foram inspecionados separadamente.

REA analisou sintaxe inerte e reteve observações estáticas. A análise Angular teve limite de memória para relações expandidas/semântica do bundle principal; fatos estáticos foram retidos. Essas provas não demonstram chamadas autenticadas, defaults do backend ou funcionamento de cada fluxo.

Documentação pública: [índice oficial](https://connectapi-sbai.readme.io/llms.txt), [listar chatbots](https://connectapi-sbai.readme.io/reference/get_v1-chatbot), [autenticação](https://connectapi-sbai.readme.io/reference/autenticação). O índice público observado documenta listagem e envio, não a criação/editor interno. Isso não significa ausência dos endpoints usados pela aplicação.

## Bases, criação e versões

Produção Angular usa `https://api.wts.chat`; existe `https://chatbot.wts.chat` para companhias específicas. A documentação pública usa `https://api.app.connectchannels.com.br`. Escolha a base efetiva da conta, sem trocar a identidade por conveniência.

`Authorization: Bearer <sessão de usuário>` é anexado pelo interceptor do app. Nunca envie esse header à URL assinada de armazenamento.

| Operação | Contrato observado |
|---|---|
| Criar atendimento | POST `/chat/v1/chatbot` |
| Criar automação | POST `/chat/v1/chatbot/automation` |
| Metadados atuais | GET `/chat/v1/chatbot/{id}?deployedVersion=false` |
| Conteúdo avançado | GET `/chat/v1/chatbot/{id}/nodes?includeDetails=All` |
| Versão simples | GET `/chat/v1/chatbot/{id}/version/{versionId}?includeDetails=All&deployedVersion=false` |
| Conteúdo avançado por versão | GET `/chat/v1/chatbot/{id}/version/{versionId}/nodes?includeDetails=All` |
| Listar versões | GET `/chat/v1/chatbot/{id}/version` |
| Preparar gravação | GET `/chat/v1/chatbot/{id}/version/url` → `{url,key,...}` |
| Upload | PUT JSON na `url` recebida, sem Authorization |
| Confirmar gravação avançada | POST `/chat/v1/chatbot/{id}/version/url` → `{key,url}` |
| Confirmar gravação simples | Mesmo endpoint; Angular envia o objeto original recebido no GET |
| Publicar versão | POST `/chat/v1/chatbot/{id}/version/{versionId}/deploy` com `{}` |
| Publicar para teste | POST `/chat/v1/chatbot/{id}/deploy-test` com `{}` |
| Duplicar | POST `/chat/v1/chatbot` com `{name,duplicationMethod:"INDEPENDENT",duplicationSourceId,channelTypes,automationChannelId}` |
| Cópia de substituição | POST `/chat/v1/chatbot` com `{duplicationMethod:"REPLACEMENT",duplicationSourceId}` |
| Índice interno | GET `/chat/v1/chatbot/index` com `page,pageSize,orderBy,includeDetails,archived` |
| Automações | GET `/chat/v1/chatbot/automation` com paginação |

Criação atendimento:

```json
{"name":"Nome","defaultDepartmentId":"UUID real","channelTypes":["CLOUDAPI_WHATSAPP"],"engine":null,"builderType":"HELENA_ADVANCED"}
```

`engine:null` é o builder observado para usuário que não é superadmin. Confirme permissões e seleções reais.

Automação envolve o mesmo objeto dentro de:
`{chatbot,channelId,usage,scope,scopeIds,...}`. `usage` é uma string com valores API,MANUAL,CAMPAIGN,SEQUENCE separados por vírgulas. `scope` é COMPANY ou DEPARTMENT; seus IDs devem vir da conta. Preserve `keepAfterCompleteSession` quando pertinente. WebChat restringe Campaign/Sequence no formulário.

Canais do seletor:

| Família | `channelTypes` |
|---|---|
| WhatsApp oficial | DIALOG360_WHATSAPP, CLOUDAPI_WHATSAPP |
| Z-API | ZAPI_WHATSAPP |
| Evolution | EVOLUTIONAPI_WHATSAPP |
| Instagram/Messenger | INSTAGRAM, MESSENGER |
| WebChat | WEBCHAT |

Não confunda nomes de enum do filtro público (`Reactive`, `Automation`) com tipos internos/valores em maiúsculas do editor.

## Formatos das versões

HELENA_SIMPLE salva o modelo completo recuperado de uma versão: metadados, `nodes`, `config` e propriedades originais. Nós têm `children:[{clientGeneratedId,nodes,...}]`. O Angular ordena/recalcula `order`, remove grupos órfãos e normaliza IDs de parâmetros antes do upload. Reutilize a versão atual como ponto de partida.

HELENA_ADVANCED salva:

```text
{
 startGroupClientGeneratedId,
 nodes:[{clientGeneratedId,groupClientGeneratedId,type,order,level,key,...}],
 groups:[{name,level,clientGeneratedId,parentNodeClientGeneratedId,xPosition,yPosition}],
 edges:[{clientSourceId,clientSourceGroupId,clientTargetGroupId}],
 notes:[{clientGeneratedId,message,color,height,width,xPosition,yPosition}],
 config:{aggregation,beginGroup:{xPosition,yPosition}},
 triggers:{channelTriggers:[{clientGeneratedId,xPosition,yPosition,channelId,type,workingPeriod,keyword}]}
}
```

Primeiro nó de cada grupo recebe `returnPoint:{enabled:true,label:<nome do grupo>}`; demais recebem null. Grupos subordinados da IA são incorporados em subAgentsConfig, não duplicados como grupos independentes. Destinos de saída precisam coincidir no grafo e nos campos do nó; apenas desenhar um edge não configura todas as transições.

Os builders preservam propriedades adicionais. Não elimine campos desconhecidos ao editar. IDs cliente são UUIDs; key do nó simples é `cb-{primeiro segmento chatbotId}-{prefixo tipo}-{primeiro segmento UUID}`.

## Catálogo real: 20 opções

Supervisor IA; agente IA; mensagem; modelo; pergunta; pergunta dinâmica; menu; sequência; etiquetas; transferência; conclusão; criar card; mover card; alterar campos do card; aguardar mensagens; esperar segundos; condicional; outro chatbot; metadados; webhook.

EMPTY/GOTO_RETURN_POINT/NAVIGATION_RETURN existem para estrutura/navegação; não são opções independentes do catálogo avançado. CARD é `ACTION` com `action.type=CARD`, não um tipo de nó separado. Pergunta dinâmica é QUESTION com `question.dynamicMessage`, apesar de DYNAMIC_QUESTION também existir em enum de ações.

## Conteúdo e modelos

CONTENT: `message:{type,text,file,fileId,files,fileIds,sendAsDocument,footerText,params:{items},messageVariations:{variations}}`.

Tipos TEXT,AUDIO,IMAGE,VIDEO,DOCUMENT. Texto precisa conteúdo; mídia precisa arquivos previamente enviados. Avançado aceita `fileIds[]`. Um arquivo usa file/fileId; múltiplos usam files/fileIds e deixam file/fileId null. Áudio limpa text. Variações contêm objetos com text e são removidas ao mudar para mídia.

TEMPLATE: `template:{templateId,params:{items},template,file,fileId,aggregation}`, mais `waitAnswer`. Templates/mídias precisam vir da conta e do canal. Campos do template derivam de seu contrato real; não invente IDs/parâmetros.

Parâmetros: QUESTION,CUSTOMFIELD,SYSTEM,TEMPLATE_DEFAULT,STATIC_VALUE,CONTACT_METADATA,SESSION_METADATA,SESSION. Exemplos de campos condicionais: questionNodeClientId,customFieldId/customFieldKey,systemType,staticValue. `first-name` usa customFieldKey em normalizações do editor.

## Perguntas e menus

`message` acompanha QUESTION/MENU. O objeto `question`/`menu` contém:
`targetType,valueType,targetCustomFieldId,retryText,maxRetries,maxRetriesAchievedText,maxRetriesAchievedAction,options,aggregation,interactiveType`.

- valueType: TEXT,INTEGER,DECIMAL,DATE,TIME,DATETIME,BOOLEAN,CPF_CNPJ,FILE.
- targetType: CONTEXT ou CUSTOMFIELD.
- Interativos: BUTTONS,LIST,NUMBERS,REQUEST_CONTACT_INFO (avançado).
- Opções: `{clientGeneratedId,type,text,order,targetGroupId,targetClientGroupId,targetDepartmentId}`; opções QUESTION são normalizadas para ANSWER.
- Tipos de opção: ANSWER,NAVIGATION,NAVIGATION_DEPARTMENT,NAVIGATION_RETURN,NAVIGATION_COMPLETE,ACTION.
- Retentativas: `maxRetries` 0..10; formulário default 2; texto default "Não entendi, poderia repetir?". Ação final pode transferir/concluir; IGNORE_QUESTION é serializado como ação null no formulário avançado.
- `maxRetriesAchievedAction` inclui type,transferDepartmentId,transferUnavailableText,interpretMessages conforme modo.
- REQUEST_CONTACT_INFO cria uma opção ANSWER "Compartilhar dados de contato" e zera opções/alvo/footer anteriores.
- Opções precisam nomes distintos/preenchidos; limites dependem de channel.templateProperties/useChannelTemplateRules. Não universalize os defaults 3 botões/10 itens.
- Botões são declarados incompatíveis com ZAPI/Evolution; listas com Evolution na biblioteca simples.

Dynamic: `question.dynamicMessage:{webhookUrl,fixedMessageEnabled,clientGeneratedId,fallbackNodeGroupClientId,...}`. Texto fixo usa message.text. URL deve ser válida. O webhook retorna interatividade e opções, mas o contrato exato da resposta ainda não foi recuperado: não invente JSON de botões/lista. Fonte: formulário @960759–968952.

## Ações

`action` tem type e propriedades específicas; serialize campos desabilitados conforme formulário, normalmente null.

| Tipo | Campos recuperados |
|---|---|
| TRANSFER_SESSION | transferDepartmentId,transferUnavailableText,interpretMessages |
| COMPLETE_SESSION | type |
| SET_CONTACT_TAG | contactTagIds,removeContactTags |
| DELAY | delayInMilliseconds |
| GOTO_RETURN_POINT | targetClientNodeId |
| WEBHOOK | webhook:{url,successTarget,failTarget,customTargets,...} |
| SEQUENCE_OPERATION | sequence:{id,operation,name}; ADD/REMOVE |
| AGGREGATE_MESSAGES | aggregation |
| TRANSFER_CHATBOT | transferChatbot:{chatbotKey,returnPointLabel} |
| SET_METADATA | metadataConfig:{items:[{key,value,target}]} |
| CARD | card:{operation,...} |

Targets de webhook incluem clientGeneratedId,clientGroupId/groupId e key quando personalizados. customTargets podem substituir successTarget. Metadados value.type: STATIC_VALUE,CONTACT_FIELD,CONTACT_LAST_MSG,QUESTION,TEMPLATE; campos: staticValue,customFieldId,questionNodeClientId,templateNodeClientId. target é SESSION ou CONTACT. Chaves e referências devem ser válidas; a comparação de duplicatas diverge entre editores.

## Condições

`conditions:[{name,operator,isFallback,target:{groupId,clientGroupId},conditions:[...],order}]`.

Item: `{field,operator,values,customFieldId,questionNodeId,questionNodeClientId,metadataKey,templateId,optionId,...}`.

Campos: WORKING_PERIOD,CONTACT_FIELD,CONTACT_TAG,CONTACT_METADATA,CONTACT_LAST_MSG,QUESTION,TEMPLATE,METADATA,PERIOD_DATE,PERIOD_DAY,PERIOD_HOUR. Combinação AND/OR. Operadores EQUAL,NOT_EQUAL,LESS_THAN,LESS_THAN_EQUAL,GREATER_THAN,GREATER_THAN_EQUAL,CONTAIN,NOT_CONTAIN,NOT_EMPTY,OPTION_SELECTED. A compatibilidade depende do tipo do campo; NOT_EMPTY dispensa valor. Fallback vai por último; mantenha saída explícita.

## CRM/Card

ACTION/CARD, `card.operation`: CREATE,UPDATE,TRANSFER.

CREATE @744281: panelId,stepId,title:{text,params},description:{text,params},dueDate:{text,params},tagIds,responsibleUserId,automaticUserAttribution,customFieldsValues:[{customFieldId,text,params}]. Responsável manual é null quando atribuição automática está ativa. Datas literais usam DD/MM/YYYY ou DD/MM/YYYY HH:mm; a biblioteca verifica formato, não validade do calendário.

UPDATE/TRANSFER @875275: searchType,sourceClientGeneratedId,sourcePanelId,sourceTagIds,updateFields,stepId,customFieldsValues,ignoreMultipleCards,enableFallbackNodeGroup,fallbackNodeGroupClientId,tagIds,responsibleUserId,automaticUserAttribution,title,description,dueDate.

searchType: CREATED_IN (referência a CARD anterior) ou SEARCH_IN_PANEL. TRANSFER força updateFields="STEPID". UPDATE oferece STEPID,TITLE,DESCRIPTION,DUEDATE,RESPONSIBLEUSERID,TAGIDS,CUSTOMFIELDVALUES como string separada por vírgulas. Outros valores do enum não comprovam suporte no seletor. customFieldsValues são convertidos a value.valuesArray/value.valueString conforme conteúdo.

## IA

AI_AGENT e AI_TEAM usam `aiAgentConfig:{aiAgentId,aiAgentName,aggregation,customTargets:{targets},isAgentActive,subAgentsConfig}`. O ID é de agente/equipe já existente; não existe aiTeamId separado.

Targets: `{key,clientGeneratedId,clientGroupId,groupId}`; derivados de skills REDIRECT_FLOW, config.redirectFlow.flowId. Subagente usa key `${aiAgentId}:${flowId}`. AI_TEAM inclui `subAgentsConfig:{configs:[{aiAgentId,clientGeneratedId,positionX,positionY}]}` a partir dos IDs em promptConfig.subAgents. Nó de subagente pode ter notCanSave=true. Fonte: formulário @899533 e normalização index @1834738.

Adicionar nó IA não cria o agente/prompts/ferramentas. A criação/configuração completa de agentes requer investigação do módulo próprio `/ai`; esta referência não afirma cobertura desse módulo.

## Compatibilidade HTTP comprovada no fluxo TI

Provas em `C:/Users/caila/Documents/Codex/connect-channels-automation/ti-helpdesk/`. Em 13/10/2026, o fluxo completo foi gravado e lido de volta com 36 grupos, 83 nós e 69 ligações. Chatbot `e8fb5f57-a378-4270-8c11-2f895cd59f22`, versão final `d1612dfc-bc6e-4c62-af5e-bc7bfd0e7900`; permaneceu NOT_PUBLISHED, sem canais. A compilação por deploy-test terminou READY; a versão principal não foi publicada. `final-snapshot.json`, `test-deploy-result.json` e `verification.json` contêm as provas; gravação/compilação não comprovam execução das conversas.

- Opção `E-mail / acesso` reproduziu HTTP 500; `Email / acesso` passou num payload isolado equivalente. O helper bloqueia o caso observado `E-mail` antes da chamada. Isso não estabelece uma proibição geral de hífens pelo fornecedor; mensagens e outros rótulos não recebem essa restrição.
- **Os parâmetros de card diferem dos parâmetros de mensagem.** `QUESTION` em `card.title.params`/`card.description.params` reproduziu HTTP 500. Trocar por `SESSION_METADATA`, mantendo os parâmetros como arrays, passou. O formulário `ChatbotMarkdownInputComponent` (@715401 do bundle de edição) suporta CUSTOMFIELD, SYSTEM, SESSION e metadados; seu parser não monta QUESTION. Grave a resposta numa ação SET_METADATA antes do card. Não copie os parâmetros QUESTION de uma mensagem de resumo para o card.
- Campos de card usam `params:[...]`; mensagens usam `params:{items:[...]}`. A versão final comprovou título/descrição com metadados, atribuição automática, criação na etapa Novo e fallback configurado. A operação real de criar um card durante uma conversa ainda exige teste integrado.
- QUESTION/FILE é coleta aberta: `interactiveType:null`, `options:[]`. O formulário desabilita FILE quando há interatividade (@965591). Não crie uma pergunta FILE/LIST.
- Omita vencimento ou use null quando nenhum prazo foi definido. Não invente uma data ou um SLA para preencher o formulário.
- Itens de `metadataConfig.items` recebem `clientGeneratedId` UUID, além de key/value/target, conforme o formulário (@762778).
- O serializer nativo ordena `nodes` globalmente por `order`. A ordenação dentro de cada grupo continua em 0..N. `reorderPositions` também preenche previousNodeId/nextNodeId; `createSaveGroupObject` resolve parentNodeClientGeneratedId. Preserve esses campos nativos ao editar; não use uma ordem de array global para inferir a sequência entre grupos.
- `createNode` (@1818627 do index) cria groupId e groupClientGeneratedId; para nós novos ambos recebem o UUID do grupo. Ao editar, preserve id/key e IDs nativos recuperados. No rascunho TI, 58 nós devolveram vínculos legados previousNodeId/nextNodeId que não coincidem com a adjacência esperada dentro do grupo, mesmo após readback/hidratação dos IDs. O grafo avançado/opções/destinos e a compilação passaram, mas o efeito desses vínculos no runtime permanece **não comprovado**. Não declare execução correta só por HTTP 200 ou READY; faça um teste de conversa autorizado antes de publicação operacional.
- GET `/chat/v1/chatbot/{id}/version/{versionId}/validate` retornou comparação de versões (`isSame`, currentVersionId, compareVersionId), **não** validação do grafo. Não apresente essa resposta como prova funcional ou aprovação do fornecedor para o fluxo.

Exemplo de ponte pergunta → metadado → card:

```json
{"type":"ACTION","action":{"type":"SET_METADATA","metadataConfig":{"items":[{"clientGeneratedId":"UUID","key":"ti_solicitante","target":"SESSION","value":{"type":"QUESTION","questionNodeClientId":"UUID da pergunta"}}]}}}
```

```json
{"operation":"CREATE","panelId":"UUID real","stepId":"UUID real","title":{"text":"Chamado de [solicitante]","params":[{"type":"SESSION_METADATA","replacementName":"solicitante","metadataKey":"ti_solicitante"}]}}
```

O helper mantém status HTTP, vendorCode e requestId sanitizados no erro. Não imprime texto livre de diagnóstico, tokens ou URL assinada. Antes de retomar após HTTP 500, leia o estado atual; continue no mesmo chatbot após uma correção fundamentada, sem repetir criação ou presumir que a falha desfez a escrita.

## Agregação e gatilhos

Agregação: timeoutBeforeMessageMs,timeoutAfterMessageMs,timeoutBeforeUseGlobal,timeoutAfterUseGlobal,enableFallbackNodeGroup,fallbackNodeGroupClientId; avançado também usa clientGeneratedId como handle. -2 representa global e -1 sem limite/imediato na UI; gravação usa null e flags. Simples rejeita zero/positivos menores que 1000 ms. Não aplique essa regra indiscriminadamente ao avançado; follow-up adiciona restrições próprias.

Gatilhos UI ANYTIME,IN_WORKING_HOURS,OUT_OF_WORKING_HOURS,KEYWORD viram workingPeriod ANYTIME,IN_COMPANY_HOURS,OUT_COMPANY_HOURS; KEYWORD usa ANYTIME+keyword. `type` no DTO é o tipo do canal. Keyword: trim,lowercase,remoção de diacríticos. Conflictos dependem de canal/horário/palavra e não são resolvidos escolhendo outro canal automaticamente. Para draft novo, mantenha channelTriggers vazio até vinculação autorizada.

## Autenticação HTTP

`library/module-27403.js` recupera:
- POST `/auth/v2/login/send-otp`; recebe email,type="EMAIL",partnerId. Na chamada real a resposta foi `{id}`, não userId.
- POST `/auth/v2/login/authenticate` com id=challenge.userId quando presente,grantType="OTP",partnerId,internalDeviceId,email,password=<OTP>. `id` foi omitido na chamada real por ser undefined, conforme o código do serviço.
- Retorno: accessToken,refreshToken,tenantId,userDetails.
- Refresh: `/auth/v2/login/authenticate/refresh` ou v3, com refreshToken,tenantId,partnerId,internalDeviceId.
- Transferência: `/auth/v2/login/authenticate/transfer-code/exchange`, body `{code}`.

Formulário recuperado de `artifacts/8471.3d59ef167d28ad26.js` @23520–24930; enum EMAIL/OTP em main. Caminho descoberto pela rota auth/sign-in e pelo mapa literal runtime, sem adivinhar filenames.

Partner config vem de `https://cdn.wts.chat/static/partners/app.connectchannels.com.br/config.json`, derivado do resolver do próprio app. O pedido real de OTP foi aceito; a autenticação inicial retornou tokens, mas a primeira gravação local falhou por autoload de módulo PowerShell. DPAPI nativo foi corrigido/testado; a repetição do OTP consumido recebeu HTTP 500. Considere esse histórico separado de uma sessão persistida e validada.

O Gmail conectado encontrou a mensagem em spam e mascarou o código como `one-time authentication code withheld`. Bootstrap precisa do código fornecido pelo usuário nesse ambiente; após sessão válida, use refresh via HTTP. Não criar token permanente nem trocar permissões como atalho de autenticação.

Atualização 13/10/2026: o usuário aceitou informar OTP quando necessário. Um código posterior concluiu login HTTP e gravação DPAPI; um processo novo usou a sessão numa consulta autenticada. A criação/gravação/readback de um rascunho avançado foi comprovada sem browser. O histórico da falha inicial acima não é o estado atual. A renovação real não foi forçada, pois a sessão estava válida.
