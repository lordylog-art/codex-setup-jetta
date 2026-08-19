---
name: criar-agente-chatbot-connect
description: Criar, clonar, ajustar, validar e limpar agentes de IA, supervisores, bases de conhecimento e chatbots de automacao da Connect Channels usando a sessao autenticada do Connect por CDP/API. Use quando o usuario pedir para criar rapidamente um agente de IA funcional com tabela/base de conhecimento, equipe de subagentes e chatbot de automacao vinculado, ou para repetir esse padrao para varios clientes sem abrir o Chrome nem publicar sem autorizacao.
---

# Criar Agente Chatbot Connect

## Objetivo

Criar um conjunto funcional na Connect Channels:

1. base de conhecimento ou tabela;
2. agentes especialistas;
3. supervisor IA (`promptConfig.isTeam: true`);
4. chatbot de automacao (`automation: true`, `builderType: HELENA_ADVANCED`) com no `AI_TEAM`;
5. validacao por API sem publicar ou disparar conversa real.

Use a sessao ja autenticada no Chrome/CDP. Nao imprimir token, cookie, refresh token, localStorage completo ou header `Authorization`.

## Fluxo Rapido

1. Confirmar CDP:

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:9222/json/version -TimeoutSec 5
```

2. Capturar o header `Authorization` de uma requisicao real da Connect quando `accessToken` local der 401.
   - Navegar uma aba ja existente para `/chatbots/list/automation`.
   - Habilitar `Network.requestWillBeSent`.
   - Guardar o header somente em memoria e nunca imprimir.

3. Criar ou localizar a base de conhecimento.
   - Para tabela de precos, gerar colunas simples (`Produto`, `Unidade`, `Preco`, `Observacao`) e registros objetivos.
   - Validar `status: READY` antes de vincular agentes.

4. Criar agentes especialistas.
   - Exemplo: `Produtos e Precos`, `Encomendas e Reservas`, `Atendimento Geral`.
   - Vincular a mesma knowledge/table quando todos dependem da mesma base.
   - Conferir `publishStatus: READY` ou estado equivalente antes de montar o supervisor.

5. Criar supervisor IA.
   - `promptConfig.isTeam: true`.
   - `promptConfig.subAgents` com os IDs dos agentes especialistas.
   - Descrever roteamento entre subagentes no prompt do supervisor.

6. Criar ou reaproveitar um chatbot de automacao.
   - Nao usar o endpoint de chatbot comum para automacao.
   - Automacoes aparecem em `GET /chat/v1/chatbot/automation`.
   - O chatbot deve ter `automation: true` e `builderType: HELENA_ADVANCED`.

7. Salvar o fluxo do builder usando o contrato `version/url`.
   - `GET /chat/v1/chatbot/{chatbotId}/version/url`
   - `PUT` JSON completo na URL S3 assinada
   - `POST /chat/v1/chatbot/{chatbotId}/version/url` com `{ key, url }`

8. Validar por API.
   - `GET /chat/v1/chatbot/{chatbotId}`
   - `GET /chat/v1/chatbot/{chatbotId}/nodes?includeDetails=All`
   - Confirmar `AI_TEAM.aiAgentConfig.aiAgentId` apontando para o supervisor.
   - Confirmar textos sem mojibake (`?` no lugar de acento ou `�`).

## Contrato Minimo de Chatbot IA

Leia `references/connect-ai-chatbot-contract.md` antes de criar ou salvar payload.

Para um fluxo simples, use:

- grupo `Boas-vindas` com 1 ou 2 nos `CONTENT`;
- edge `grupoBoasVindas-EXIT` para o grupo do supervisor;
- grupo `Supervisor IA <nome>` com 1 no `AI_TEAM`.

O no `AI_TEAM` deve ter:

```json
{
  "type": "AI_TEAM",
  "aiAgentConfig": {
    "aiAgentId": "<supervisor-id>",
    "aiAgentName": "<nome-do-supervisor>",
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

## Regras de Seguranca

- Nao publicar chatbot, teste ou agente sem autorizacao explicita.
- Nao disparar WhatsApp, campanha, sequencia ou conversa real sem autorizacao explicita.
- Preferir atualizar rascunho e validar por leitura.
- Antes de excluir, listar exatamente os IDs que pertencem ao trabalho atual.
- Ao limpar, preferir arquivar se o DELETE nao for confirmado pelo contrato.

## Encoding

Quando gerar scripts PowerShell com texto em portugues, nao escrever acentos diretamente em heredoc se houver risco de codepage. Use escapes Unicode em JavaScript:

```js
const texto = 'Ol\u00e1, voc\u00ea pode informar o hor\u00e1rio de retirada?';
```

Depois valide lendo a API e procurando:

- caractere replacement `�`;
- `?` colado em palavras onde deveria haver acento (`voc?`, `hor?rio`, `p?o`, `pre?os`).

## Scripts

Use `scripts/connect_ai_chatbot_helper.js` para:

- confirmar sessao;
- capturar header atual sem imprimir token;
- listar automacoes;
- ler chatbot e auditar textos/agente.

O script e auxiliar. Para operacoes destrutivas ou criacao em massa, leia o contrato de referencia e monte payloads explicitamente.
