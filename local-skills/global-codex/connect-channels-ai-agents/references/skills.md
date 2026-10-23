# Habilidades — catálogo e serialização

Fonte A = `artifacts/8492.ea311dabe5541af9.js`, dentro da pasta técnica indicada em SKILL.md. Catálogo A@293825–296802; form groups A@283597–285758; builder A@285947–289822. O enum UNDEFINED é estrutural, não uma décima segunda opção pronta. O catálogo atual contém **11 tipos**.

## Envelope comum

```text
{ name, description, type, active, supressMessage, config }
```

O nome real é **supressMessage**, com essa grafia. `active` controla execução; skill presente/inativa não equivale a ausência. Nome tem limite50 em vários subformulários; descrição explica quando executar. Suprimir mensagem controla resposta após a ferramenta, não impede efeitos externos. Preserve IDs/aiAgentId e demais campos existentes recebidos do backend.

Motor<0.7 força supressMessage=false e transferência stopBot=true no builder. Ao editar versões antigas, mantenha compatibilidade sem upgrade implícito. Calendar/FOLLOW_UP são únicos por tipo. Calendar não é removível no editor: ao criar, o stub é ativo; ao abrir agente existente sem esse tipo, o editor garante stub inativo. O helper não injeta nem ativa ferramentas silenciosamente: o Codex monta esse comportamento explicitamente no payload solicitado. Até50 skills, contando defaults.

## Todos os tipos

| type | config nativa e decisões |
|---|---|
| DATE_TOOLS | `{}`. Calendário de datas relativas; active controla disponibilidade. Sem formulário adicional. |
| FOLLOW_UP | `{followUp:{followUpTimeoutMs,maxFollowUps,followUpPrompt,breakUpPrompt}}`. Prompts definidos pelo pedido; breakup=null quando desabilitado. |
| GET_CONTACT_INFO | `{getContactInfo:{name,description,allowedFieldsIds:UUID[]}}`. Campos CONTACT não readonly/valueRange; grupos têm filhos filtrados. Nome/descrição também dentro desta config. |
| UPDATE_CONTACT_TAG | `{updateContactTag:{tagIds:UUID[],addOrRemove:boolean}}`. true adiciona/false remove. Selecione tags reais. |
| TRANSFER_DEPARTMENT | `{transferDepartment:{departmentId,stopBot}}`. stopBot=true default; versão>=0.7 permite continuar se pedido. Department é equipe humana. |
| COMPLETE_SESSION | `{completeSession:{completeMessage,statusReasonId,statusReasonEnum,statusReasonAmount}}`. Texto final opcional. Cliente atual usa reason enumOTHER/amount0. |
| ADD_CRM_CARD | `{addCrmCard:{title,panelId,stepId,description,variables,cardDescription,tags,dueDate,customFields,customFieldValues}}`. Painel/etapa/título obrigatórios; filtrar campos PANEL visíveis. |
| CALL_API | `{callApi:{url,method,body,response,variables,headers:[{key,value}]}}`. method GET/POST/PUT/PATCH/DELETE. body/response são campos próprios; não inferir OpenAPI ou JSON estruturado por rótulo. |
| REDIRECT_FLOW | `{redirectFlow:{flowId}}`. Builder deriva flowId do nome: espaços→underscore, lowercase. Conferir saídas do nó chatbot. |
| UPDATE_CONTACT_FIELD | `{updateContactField:{variables,fields:[{customFieldKey,value}]}}`. Campos CONTACT editáveis, sem tags/valueRange. Impedir duplicidade; preservar tipo/semântica do campo. |
| MCP | `{mcp:{name,description,url,auth:{key,value},toolsMode:"ALL",tools:[]}}`. URL/header opcional na UI; esse builder fixa ALL e lista vazia. Não promete seletor de tools ou protocolo sem prova. |

Nome/descrição são obrigatórios em transferência/conclusão/CRM/etiquetas/fluxo/campo. CALL_API tem validação separada de nome/descrição/método/URL com trim. MCP verifica nome/descrição; não há validators de URL/auth no group observado. Ausência de validação cliente não prova aceitação backend.

CompleteSession A@285947 usa a constante `626fb5de-0cc2-4209-b456-47b454ee6e14`; isso foi observado no bundle atual. Antes de executar encerramento, confirme sua adequação à conta/fluxo; não usar a constante como prova de IDs universais. Configurar essa habilidade não encerra conversa durante a investigação.

## Follow-up e agregação

UI oferece 600,1800,3600,10800,28800,86400,172800 **segundos**. Serialização converte para ms. maxFollowUps selecionável1–3; followUpPrompt required e não whitespace. breakUpPrompt required se habilitado.

A@283597 tem default900 e um patch limita até5; esses trechos contradizem opções da dropdown. Para novo, usar as opções selecionáveis comprovadas; para existente fora delas, preservar e registrar necessidade de prova. Não expandir “suporta5 tentativas” por essa normalização.

A@265158 calcula indicação de inatividade mínima do nó:
`ceil((maxFollowUps + 1) * timeoutSeconds / 60)` minutos. O +1 considera o fechamento final. Cruce com aggregation do nó AI_AGENT/AI_TEAM e regras do canal antes de ativar follow-up; mudar skill não atualiza automaticamente os timeouts do chatbot.

## Variáveis e placeholders

A@285758 converte seleção em:

```text
{ name: label, key: value, source: "AI_INPUT" | "SYSTEM", description, dataType: "STRING" }
```

Enum tem STRING/NUMBER/BOOLEAN, mas **este formulário emite STRING**. Tipos adicionais aceitos pela fábrica local histórica não foram comprovados no backend atual. AI_INPUT orienta coleta; SYSTEM referencia contexto. Placeholders `{{chave}}` precisam corresponder ao catálogo recuperado.

API filtra variáveis usadas em url/method/body/response/valores dos headers. CRM filtra title/cardDescription/dueDate/customFieldValues.value. Campo de contato conserva lista inteira; não aplicar o filtro CRM a todos os tipos. Builder deduplica chaves e descarta referências que não existem no catálogo. Renomear variável sem atualizar placeholders muda comportamento.

Catálogo customizado usa GET `/core/v1/custom-field?nestedList=true`; chave `customField.{field.key}`. SINGLESELECT/MULTISELECT/valueRange aparecem inativos na lista de variáveis. Isso não é igual à lista de campos editáveis do formulário de habilidade.

CRM/campo: boolean→`"true"/"false"`, multiselect→CSV; entradas customizadas vazias são filtradas. Conserve IDs do painel/etapa/campo e confira valor esperado. A fábrica histórica possui compilador `tools/connect-agent-factory/skill-contracts.mjs`; pode ajudar em casos alinhados, mas seu HTTPS/JSON/no-secrets e modelo único são restrições do MVP, não limitações globais do Connect.

## API e MCP sensíveis

O fornecedor permite headers/auth configuráveis. O helper mascara headers/auth e chaves nas leituras; atualização parte do objeto original em memória. Se o usuário pedir nova credencial, use entrada protegida/variável de ambiente e jamais embuta segredo em relatório ou exemplo. URL/body/response podem carregar segredo fora de campos óbvios; revise antes de salvar compartilhável.

MCP tem auth `{key,value}` para header, não configuração comprovada de OAuth. Discovery de ferramentas, handshake/transporte, timeout, retries e retornos dinâmicos não foram exercitados. CALL_API configurar e executar são ações distintas: validação local não consulta a URL e sandbox pode ter efeitos ainda desconhecidos.

## Chatbot em supervisor

A@532313 chama seletor filterBot e adiciona habilidade, preservando config retornada. Nos nós do Builder, REDIRECT_FLOW se conecta às saídas por flowId. Leia a skill chatbots antes de mudar targets, subAgentsConfig ou aggregation. Não converter chatbotId em departmentId/subAgentId sem o contrato apropriado.
