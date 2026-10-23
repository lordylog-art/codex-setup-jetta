# Contratos nativos — agentes e supervisores

Leia antes de criar/editar. Data: 13/10/2026. Fonte atual `C:/Users/caila/Documents/Codex/connect-channels-ai-agents/artifacts/`. Offsets são caracteres base zero do JS original: **M** = main.c1b6a1d22d66025d.js; **A** = 8492.ea311dabe5541af9.js. `module-index.json` e `methods.json` localizam os trechos completos. Valores de backend ainda não exercitados ficam separados em evidence.md.

## Esquema e fronteiras

Empresa contextual (`aicompany`) e credencial (`aicredential`) são recursos independentes. Agente e supervisor usam o mesmo `aiagent`; o discriminante é `promptConfig.isTeam`. Equipe humana (`department`) é fila de atendimento, não supervisor IA. Base de conhecimento associa por IDs. O nó AI_AGENT/AI_TEAM de chatbot referencia o agente; criar esse nó não provisiona a IA.

API efetiva reutilizada: `https://api.wts.chat` com sessão de usuário, validada por leitura. A base pública Connect também existe; confirme a base/tenant do cliente antes de escrever. A configuração de produção está em módulo18260; não trocar host para contornar autorização.

## Endpoints do serviço atual

M@3633219–3641711, módulo14824:

| Finalidade | Método / path e entrada |
|---|---|
| Listar agentes/supervisores | GET `/ai/v1/aiagent` com archived, page, pageSize, orderByDesc=createdat, aiAgentType=AGENT ou TEAM |
| Contagem | GET `/ai/v1/aiagent/count` |
| Ler | GET `/ai/v1/aiagent/{id}`; filtros opcionais archived,name,aiAgentType,status |
| Ler lote | GET `/ai/v1/aiagent/batch?ids={id}&ids={id}` |
| Criar | POST `/ai/v1/aiagent` com DTO abaixo |
| Atualizar | PUT `/ai/v1/aiagent/{id}` com DTO abaixo |
| Arquivar | DELETE `/ai/v1/aiagent/{id}`; UI trata como archive, não supor remoção física |
| Reativar | POST `/ai/v1/aiagent/{id}/reactivate` com `{}` |
| Colar/duplicar | POST `/ai/v1/aiagent/{id}/paste` com `{}`; não chamar clone informalmente com metadata inventada |
| Privar / desprivar | PUT `/ai/v1/aiagent/{id}/privatize` ou `/desprivatize` com `{}` |
| Gerar resumo | PUT `/ai/v1/aiagent/{id}/generate-summary` com `{}`; chama IA, muda recurso |
| Dependência supervisor | GET `/ai/v1/aiagent/{id}/is-subagent` |
| Empresas | GET/POST `/ai/v1/aicompany`; PUT/DELETE `/ai/v1/aicompany/{id}` |
| Credenciais | GET/POST `/ai/v1/aicredential`; PUT `/ai/v1/aicredential/{id}`; DELETE com transferCredentialId opcional |
| Permissões IA | GET `/ai/v1/aipermissionconfig/current`; PUT `/ai/v1/aipermissionconfig` |
| Teste agente | POST `/ai/v1/aiagent/sandbox`, contrato em testing-and-integration.md |
| Otimizador | POST `/ai/v1/aiagent/agent-optimization`, contrato em testing-and-integration.md |

DELETE, reativação, privacidade, credenciais e permissões exigem pedido correspondente. O helper de agentes implementa a criação/edição/leitura principal; operações adicionais usam o transporte compartilhado com payload da referência e provas proporcionais. Não deduzir endpoint `/deploy`: nenhum aparece neste serviço. Estados observados são DRAFT, PUBLISHING, FAILED e READY. Agentes existentes READY não provam escrita nova.

Listagem real devolve `{items,totalItems,countPages,isLastPage,page,pageSize,nextPageToken,...}`. `aicredential` devolve array. Continue páginas/tokens e reconcilie os contadores; pageSize grande não prova inventário completo. A listagem do frontend usa 10000 para agentes e 1000 para conhecimento, sem isso estabelecer limites de capacidade.

## DTO de save

Builder de save A@520334–524493; configuração usada no sandbox A@485149–487212:

```text
{
  name, credentialId, aiCompanyId,
  companyId: null, partnerId: null, isPrivate,
  promptConfig: {
    agentName, nickName, shouldSignConversation,
    communicationForm, responseLength, profile, goal,
    temperature, restrictions: string[],
    requiredSteps: [{ order, step }],
    skills: [/* contratos em skills.md */],
    knowledgeIds: UUID[], version,
    reasoningModelConfig: { credentialId?, modelIntegrationId, reasoningEffort? } | null,
    formattingModelConfig: { credentialId?, modelIntegrationId } | null,
    additionalFormattingInstructions: string | null,
    maxTokens?, messageInterval,
    enableHumanTransfer, defaultDepartmentId,
    showHumanTransferMessage, informAboutTransfer, humanTransferMessage,
    fallbackDepartmentId, fallbackTransferMessage,
    isTeam, subAgents: UUID[],
    subAgentSummary: [{ id, agentSummary: { short, long } }],
    shouldNotifyAboutHandoff
  }
}
```

O save atual emite `companyId:null,partnerId:null`; o contexto autenticado define identidade. Ao editar, preserve metadata existente pertinente e o promptConfig integral. `agentName` acompanha nome interno; `nickName` assina a mensagem. A leitura real pode omitir credentialId dentro de modelConfig e adicionar campos de follow-up no nível raiz do promptConfig: preserve-os sem assumir que substituem `skills[].config.followUp`.

## Campos e validações do editor

| Campo | Valores / comportamento atual |
|---|---|
| name | Obrigatório; agentName recebe name no builder |
| nickName | Obrigatório quando assina e versão>=0.7; auto inicialização pega até20 caracteres; preserve apresentação escolhida |
| communicationForm | SUPPORTIVE, NEUTRAL, FORMAL |
| responseLength | SHORT, LONG ou null (automático); depende de motor>=0.8 |
| profile | Seletores Vendedor, SDR, Suporte, Onboarding, Recepcionista, Outro; perfil custom é texto, não enum rígido |
| goal | Obrigatório; instrução central do agente |
| requiredSteps | Lista `{order,step}`; UI ordena por order ao carregar; etapas não são recursos/endpoints independentes |
| restrictions | Lista de textos; UI combina regras padrão selecionadas com texto custom; preserve intenção, não substitua regras existentes por defaults |
| temperature | NO_CREATIVITY, LOW, MEDIUM, HIGH, VERY_HIGH; slider 0/25/50/75/100 converte para enum, não temperatura numérica do provedor |
| version | Menu 0.5,0.6,0.7,0.8; novo usa0.8; preservar versão de existente salvo pedido de upgrade |
| maxTokens | Opcional; onSave rejeita<150 e>2000000000; guia público diz50, divergência registrada. Helper exige inteiro como validação local |
| messageInterval | Segundos:0–10,15,20,25,30,35,40 |
| skills/knowledgeIds | Até50 de cada no editor; skill conta Calendário; base existe e está disponível na conta |
| defaultDepartmentId | Necessário se enableHumanTransfer; null quando desabilitada |
| fallbackDepartmentId | Necessário no canPublish do formulário; não usar primeiro department sem decisão do pedido |
| humanTransferMessage | Obrigatória se transferência+showHumanTransferMessage; null se desligada |
| informAboutTransfer | Builder deriva de showHumanTransferMessage; manter os dois coerentes |
| fallbackTransferMessage | null quando não envia aviso; texto quando solicitado |
| isPrivate | UI opção1=true/opção2=false; acesso posterior depende de permissões |

A@525636 canPublish valida nome/apelido condicional, objetivo, perfil, comunicação, empresa, credencial/modelo, equipes e mensagens. Isso é gate do botão de save, não um endpoint de publicação. O editor escolhe primeiro/default department em A@488483 e, em alguns casos, primeira empresa em bindAgent: esse default de UI não resolve ambiguidade do pedido para a skill.

## Provedor, modelos e motor

Enums M@3641717: OPENAI, ANTHROPIC. Empresa nativa em A@26562:
`{name,industry,mainProduct,valueProposition,targetAudience,id?,active,createdAt?,updatedAt?,companyId?}`.
Credencial A@4773: `{name,provider,providerConfig:{openAi:{apiKey}}}` ou `{name,provider,providerConfig:{anthropic:{apiKey}}}`. GET pode devolver encryptedApiKey e providerConfig: tratar como sensível mesmo sem chave em texto. Nunca copiar snapshot mascarado em PUT de credencial.

Menu de integração de modelos A@476201 — strings literais do fornecedor, sem certificar oferta externa:

- OPENAI: gpt-4.1, gpt-4.1-mini, gpt-5, gpt-5.1, gpt-5.2, gpt-5.4, gpt-5.4-mini, gpt-5.4-nano, gpt-5-mini, gpt-5-nano, gpt-4o, gpt-4o-mini, gpt-5.5, gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna.
- ANTHROPIC: claude-sonnet-4-6, claude-sonnet-5, claude-sonnet-4-5-20250929, claude-haiku-4-5-20251001, claude-opus-5, claude-opus-4-8, claude-opus-4-7, claude-opus-4-6, claude-opus-4-5-20251101.

O editor atual usa **strings modelIntegrationId**, não `GPT_4_1_MINI` da fábrica histórica. Não generalizar esse enum antigo. Ambos modelConfig usam a credencial selecionada; formatação automática pode herdar modelo/default do provedor. Para>=0.8, se modelo de formatação escolhido ainda suportado, mantém; ao mudar versões anteriores recalcula (A@495978). Effort A@477292: gpt-5/mini/nano oferecem NONE,LOW,MEDIUM,HIGH,MINIMAL; gpt-5.1/5.2/5.5/5.6-sol incluem NONE,LOW,MEDIUM,HIGH; terra/luna MEDIUM,HIGH. NONE é omitido no envio. Menu não demonstra enforcement no backend.

## Supervisor e resumos

Supervisor mantém DTO comum e `isTeam:true`. `subAgents` guarda IDs escolhidos; `subAgentSummary` guarda override **por supervisor**, não muda prompt do agente. short orienta triagem; long orienta escopo/transbordo segundo documentação pública. shouldNotifyAboutHandoff controla aviso de troca. A@518475 gera resumo do subagente quando long/short ausentes via generate-summary e atualiza lista por websocket; A@531039 permite edição do resumo no supervisor.

“Vincular chatbot” na lógica de distribuição entra como habilidade pelo seletor filterBot (A@532313), não como department nem nova empresa. Consulte skills.md e contratos do chatbot. Supervisor→supervisor/nesting não teve comportamento runtime exercitado; não tratar marketing como prova de ciclos/roteamento suportados.

## Permissões, cópias e dependências

A@489297 combina SUPER_ADMIN ou ADMIN presente em allowedAdmins para configuração; conhecimento possui gate ADMIN/SUPER_ADMIN próprio. Private pode impedir edição por outro usuário. Permissão no código cliente não prova autorização backend: tratar403 como bloqueio e preservar sessão. Enum de admin é diferente de supervisor de IA.

Arquivamento interfere em chatbot/supervisores, reativação pode republicar segundo changelog. Antes de lifecycle, leia dependências atuais e mantenha consumidor operativo conforme pedido. Não chamar DELETE para limpar um teste ou repetir criação incerta automaticamente.
