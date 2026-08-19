# Contrato Connect: Agente IA + Chatbot de Automacao

## Autenticacao

Use a sessao logada da Connect pelo Chrome/CDP. Para endpoints `api.app.connectchannels.com.br`, o token do `localStorage` pode estar vencido mesmo com a UI autenticada. Quando uma chamada direta der 401, capture o header `Authorization` de uma requisicao real da UI:

1. Abrir ou reutilizar aba Connect no CDP.
2. Ativar `Network.enable`.
3. Navegar para `https://app.connectchannels.com.br/chatbots/list/automation`.
4. Capturar `Network.requestWillBeSent` de `api.app.connectchannels.com.br`.
5. Guardar o header em memoria e nao imprimir.

Headers minimos:

```http
Authorization: Bearer <capturado>
Accept: application/json, text/plain, */*
Content-Type: application/json
Origin: https://app.connectchannels.com.br
Referer: https://app.connectchannels.com.br/
```

## Endpoints Uteis

Chatbots de automacao:

```http
GET /chat/v1/chatbot/automation?page=1&pageSize=100&orderBy=name&archived=false
PUT /chat/v1/chatbot/automation/{automationId}
GET /chat/v1/chatbot/{chatbotId}
PUT /chat/v1/chatbot/{chatbotId}
GET /chat/v1/chatbot/{chatbotId}/nodes?includeDetails=All
GET /chat/v1/chatbot/{chatbotId}/version/url
POST /chat/v1/chatbot/{chatbotId}/version/url
```

Agentes IA e knowledge usam endpoints `core/v1`/`ai/v1` da Connect. Descubra o contrato pela UI ou por registros existentes antes de criar em massa. Nao inventar payload quando o backend responder erro generico.

## Criacao de Automacao

`POST /chat/v1/chatbot/automation` exige campos do formulario que podem variar por conta/canal. Se o backend retornar `FORM_ERROR`, nao insistir no chute.

Alternativas seguras:

- clonar uma automacao modelo pela UI/API quando o contrato estiver conhecido;
- reaproveitar um rascunho claramente criado para o mesmo escopo;
- pedir confirmacao antes de mexer em automacao antiga em uso.

Uma automacao funcional deve listar:

```json
{
  "automation": true,
  "builderType": "HELENA_ADVANCED",
  "publishStatus": "NOT_PUBLISHED"
}
```

## Payload do Builder

Salvar rascunho:

1. `GET /chat/v1/chatbot/{chatbotId}/version/url`
2. `PUT` do JSON completo na URL S3
3. `POST /chat/v1/chatbot/{chatbotId}/version/url` com `{ "key": "...", "url": "..." }`

Formato:

```json
{
  "startGroupClientGeneratedId": "grupo-inicial",
  "nodes": [],
  "edges": [],
  "groups": [],
  "notes": [],
  "config": {},
  "triggers": []
}
```

## No AI_TEAM

Contrato validado em rascunho real:

```json
{
  "clientGeneratedId": "uuid",
  "type": "AI_TEAM",
  "groupClientGeneratedId": "uuid-do-grupo",
  "order": 0,
  "level": 0,
  "waitAnswer": null,
  "key": "cb-<slug>-team-<short>",
  "message": null,
  "action": null,
  "template": null,
  "conditions": null,
  "aiAgentConfig": {
    "aiAgentId": "<supervisor-id>",
    "aiAgentName": "<supervisor-name>",
    "aggregation": {
      "timeoutBeforeUseGlobal": true,
      "timeoutAfterUseGlobal": false,
      "timeoutBeforeMessageMs": null,
      "timeoutAfterMessageMs": 0,
      "enableFallbackNodeGroup": null,
      "fallbackNodeGroupClientId": null,
      "clientGeneratedId": null
    },
    "subAgentsConfig": { "configs": [] },
    "customTargets": { "targets": [] }
  }
}
```

Se o supervisor ou subagentes tiverem skills de `REDIRECT_FLOW`, o editor pode gerar `customTargets.targets`. Para um recepcionista simples, `targets: []` e sem filhos funciona.

## Fluxo Minimo

Grupos:

```json
[
  { "clientGeneratedId": "g-boas-vindas", "name": "Boas-vindas", "xPosition": 280, "yPosition": 180 },
  { "clientGeneratedId": "g-ai", "name": "Supervisor IA Padaria", "xPosition": 760, "yPosition": 180 }
]
```

Edge linear:

```json
{
  "clientSourceGroupId": "g-boas-vindas",
  "clientSourceId": "g-boas-vindas-EXIT",
  "clientTargetGroupId": "g-ai"
}
```

Nao adicionar `EXIT` em grupos que terminam com `MENU`, `CONDITION`, `COMPLETE_SESSION` ou `TRANSFER_CHATBOT`.

## Validacao

Depois de salvar, ler:

```http
GET /chat/v1/chatbot/{chatbotId}/nodes?includeDetails=All
```

Confirmar:

- `nodes` contem `AI_TEAM`;
- `aiAgentConfig.aiAgentId` e o supervisor correto;
- grupos e edges batem;
- nao ha `�`;
- nao ha `?` em lugar de acento;
- `publishStatus` segue `NOT_PUBLISHED` ate autorizacao explicita.

## Limpeza

Antes de excluir:

1. listar IDs e nomes;
2. confirmar que foram criados no trabalho atual;
3. preferir `archived: true`/endpoint de archive quando DELETE nao estiver confirmado;
4. validar que nao aparecem mais nas listas ativas.

Nao apagar automacoes em uso (`inUse: true`) sem confirmacao explicita.
