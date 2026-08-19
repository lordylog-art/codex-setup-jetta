# Contrato Builder Connect Channels

## Save de Rascunho

Fluxo confirmado no builder:

1. `GET https://api.app.connectchannels.com.br/chat/v1/chatbot/{chatbotId}/version/url`
2. `PUT` do JSON completo na URL S3 assinada retornada.
3. `POST https://api.app.connectchannels.com.br/chat/v1/chatbot/{chatbotId}/version/url`
   - body: `{ "key": "...", "url": "..." }`
4. Reabrir o builder para validar.

O payload salvo no S3 deve conter:

```json
{
  "startGroupClientGeneratedId": "...",
  "nodes": [],
  "edges": [],
  "groups": [],
  "notes": [],
  "config": {},
  "triggers": []
}
```

## CDP

Usar Chrome controlavel:

```text
http://127.0.0.1:9222
```

Ler `accessToken` do `localStorage` dentro da aba Connect, sem imprimir o valor. Enviar como `Authorization: Bearer ...`.

### Caminho Facil Para Auth/Sessao

Para API interna do builder (`https://api.app.connectchannels.com.br`), usar a sessao Chrome/CDP logada. Nao procurar token em `.env` para esses endpoints.

1. Primeiro tentar reutilizar a sessao CDP ja existente, sem abrir, clicar ou navegar:

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:9222/json/version -TimeoutSec 5
node C:\Users\Jetta\.codex\skills\criar-chatbot-connect\scripts\connect_chatbot_tools.js --session-check
```

2. Se o CDP nao responder, ou se nao houver aba do Connect logada, abrir/reutilizar o Chrome controlavel:

```powershell
& "C:\Users\Jetta\.codex\skills\entrar-connect\scripts\Start-ConnectChannelsChrome.ps1"
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:9222/json/version -TimeoutSec 5
```

3. Selecionar a aba cujo `url` comeca com `https://app.connectchannels.com.br/`.
   - Se houver abas do WhatsApp ou outras, nao usar como fonte de token.
4. Ler o token via CDP:

```js
(() => {
  const raw = localStorage.getItem("accessToken");
  if (!raw) return null;
  try { return JSON.parse(raw); } catch { return raw; }
})()
```

5. Headers minimos para API interna:

```http
Authorization: Bearer <token>
Accept: application/json, text/plain, */*
Content-Type: application/json
Origin: https://app.connectchannels.com.br
Referer: https://app.connectchannels.com.br/
```

6. Se der 401 ou nao houver `accessToken`:
   - verificar se a aba controlavel esta em `/auth/sign-in`;
   - pedir para o usuario logar manualmente;
   - depois repetir a leitura do `accessToken`.
7. Se o builder parecer vazio no DOM controlado, nao concluir logout automaticamente.
   - Verificar rede/console.
   - Ja aconteceu de carregar assets, `refresh` e `GET /nodes?includeDetails=All` com 200, mas o DOM controlado mostrar pouco texto.
   - Nesse caso, validar por API e relatar a limitacao visual.

Regra pratica:

- Builder/API interna (`api.app.connectchannels.com.br`): token da sessao Chrome/CDP.
- API publica WTS/Connect (`api.wts.chat`) para templates/canais/envio: `CONNECT_CHANNELS_API_TOKEN` do `.env` via `$connect-channels`.
- Nunca imprimir token, cookie, refresh token, localStorage completo ou headers sensiveis.

## Endpoint de Leitura

```http
GET /chat/v1/chatbot/{chatbotId}/nodes?includeDetails=All
```

Use um chatbot/molde real como origem quando possivel. O backend aceita melhor payloads transformados a partir de contrato real do proprio app.

## Etiquetas

Endpoint confirmado:

```http
GET /core/v1/tag
```

Etiqueta real usada nos testes:

```text
Outros assuntos = 4f4051d3-50ab-4f8d-9b8e-54694f296828
```

Contrato de tag:

```json
{
  "type": "ACTION",
  "action": {
    "type": "SET_CONTACT_TAG",
    "contactTagIds": ["4f4051d3-50ab-4f8d-9b8e-54694f296828"],
    "removeContactTags": false
  }
}
```

## Edges

Edge tipica:

```json
{
  "chatbotVersionId": "...",
  "clientSourceGroupId": "grupo-origem-client-id",
  "clientSourceId": "handle-ou-option-id",
  "clientTargetGroupId": "grupo-destino-client-id",
  "sourceGroupId": "grupo-origem-backend-id",
  "sourceId": "handle-ou-option-id",
  "targetGroupId": "grupo-destino-backend-id"
}
```

Nao adicionar `id: null`; o builder nao precisa disso e pode marcar inconsistencias visuais.

## Regras de EXIT

O erro mais importante descoberto:

- ter uma edge no JSON nao significa que o builder considera o handle valido;
- `MENU`, `CONDITION`, `COMPLETE_SESSION` e `TRANSFER_CHATBOT` nao devem receber `group-EXIT` artificial;
- esses blocos usam suas proprias saidas ou sao terminais;
- `EXIT` so deve ser usado em grupos lineares.

Validador recomendado:

- `badEnd`: grupos com `MENU`, `CONDITION`, `COMPLETE_SESSION` ou `TRANSFER_CHATBOT` e edge `group-EXIT` devem ser corrigidos.
- `menuMissing`: opcoes de menu sem edge devem ser corrigidas.
- `condMissing`: casos de condicional sem edge devem ser corrigidos.

## Validacao Visual

Depois de salvar:

1. navegar para `/builder/chatbots/{chatbotId}/edit`;
2. esperar carregar;
3. verificar texto visivel;
4. verificar contador vermelho no header;
5. verificar handles vermelhos no DOM:

```js
[...document.querySelectorAll('.react-flow__handle')]
  .filter(el => String(el.className).includes('border-red-500'))
  .map(el => ({
    handle: el.getAttribute('data-handleid'),
    node: el.closest('.react-flow__node')?.getAttribute('data-id')
  }))
```

## Contratos Incertos

- Condicional textual com `CONTACT_LAST_MSG` foi vista no bundle, mas tentativa direta no payload gerou `500`.
- Antes de automatizar condicional textual 100%, criar/editar uma pela UI e interceptar o JSON salvo.
- `AI_AGENT`/`AI_TEAM` em fluxo complexo tambem precisa de contrato real; conversao direta causou `500`.

## Ultimo Fluxo Validado

Chatbot `Atendimento TI`:

- ID: `73dea695-eebb-4ded-965c-c425e328ee2b`
- Versao rascunho funcional: `e62daa4d-b9bd-4295-8426-090e1bda5531`
- 16 grupos
- 29 nos
- 30 ligacoes
- `ACTION.WEBHOOK`: 0
- `TEMPLATE`: 0
- menu com 7 opcoes
- etiquetas reais renderizando
- sem publicar
