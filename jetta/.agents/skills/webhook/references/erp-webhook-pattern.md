# Padrao de webhooks do ERP Jetta

## Arquivos centrais

- API dedicada: `E:\ERP jetta\apps\api\src\webhook-main.ts`
- Modulo dedicado: `E:\ERP jetta\apps\api\src\webhook.module.ts`
- Controller de disponibilidade: `E:\ERP jetta\apps\api\src\modules\availability\availability-webhook.controller.ts`
- Controller de calendario: `E:\ERP jetta\apps\api\src\modules\webhooks\calendar-webhook.controller.ts`
- Tela admin: `E:\ERP jetta\apps\web\src\app\admin\webhooks\page.tsx`
- Lista de webhooks da tela: `E:\ERP jetta\apps\web\src\app\admin\webhooks\webhook-links.ts`
- Deploy dedicado: `E:\ERP jetta\deploy-webhooks.ps1`
- Deploy remoto: `E:\ERP jetta\tools\vps-deploy-webhooks.ps1`
- Proxy publico: `E:\ERP jetta\infra\caddy\Caddyfile`

## Portas e rotas

- Web local: `3000`
- API principal local: `3001`
- Webhook dedicado local padrao: `3003`
- Webhook candidato no blue/green: `3203`
- Prefixo HTTP: `/api`
- Prefixo publico de webhook: `/api/webhooks/*`
- Dominio publico atual: `https://www.ciadm.com.br`

## Processo operacional

- PM2 do webhook: `jetta-webhooks`
- Health do processo dedicado: `http://localhost:3003/api/health`
- Caddy roteia `/api/webhooks/*` antes de `/api/*`
- `deploy-webhooks.ps1` sobe apenas o processo de webhook
- `NewDeploy.ps1` trata webhooks dentro do blue/green, inclusive cutover do Caddy

### Alerta real de producao

- Rotas estaticas de webhook podem colidir com `:clientSlug/:unit` dentro de `availability-webhook.controller.ts`.
- O caso real ja ocorrido foi `/api/webhooks/availability/occurrence-alert/client-delay`.
- Sintoma observado: resposta `401` com `"Invalid webhook token."` mesmo para uma webhook que deveria ser publica.
- Isso prova que a requisicao caiu no fluxo protegido por token, nao no fluxo da webhook de ocorrencia.
- Correcao que funcionou no projeto: registrar a rota exata no `apps/api/src/webhook-main.ts` e garantir que o handler publico seja alcançado antes da captura generica.
- Para `POST`, validar tambem que o `body` continua chegando ao handler certo.

### Higiene de PM2 na VPS

- Depois de alguns deploys, a VPS pode ficar com `jetta-webhooks` e `jetta-webhooks-3003` ao mesmo tempo.
- Se isso acontecer, a `3003` pode continuar presa ao processo errado.
- Antes de concluir um teste de producao, verificar qual PID esta ouvindo a `3003` e limpar o processo legado do PM2.
- Estado esperado ao final: apenas o processo canonico necessario para a `3003`.

## Padrao da tela admin

Cada item usa:

- `id`
- `label`
- `description`
- `method`
- `path`
- `headerName` opcional

O host final vem de `buildWebhookUrl(origin, webhook)`. A tela copia URL e header separadamente. Nao colocar token dentro da URL.

## Seguranca atual

- O fluxo de disponibilidade usa `WebhookTokenService`
- Header principal: `X-Webhook-Token`
- Tambem aceita `Authorization: Bearer ...`
- O token pode vir do banco ou do `.env`

## Campos de payload ja usados com Connect Channels

- `contact.phonenumber`
- `contact.display-phonenumber`
- `lastContactMessage`
- `lastMessage.text`
- `sessionId`
- `menus.*.answer`

Tratar payload desconhecido com erro claro. Nao mascarar ausencia de `phone`, `sessionId` ou outro campo obrigatorio.

## Docs externas

- Docs gerais Connect Channels: `https://connect-channels.gitbook.io/connect-channels-docs`
- API tecnica citada na doc: `https://connectapi-sbai.readme.io/reference`

## Checklist rapido para nova webhook

1. Confirmar se entra no servidor dedicado existente.
2. Escolher o controller certo ou criar um controller novo de webhook.
3. Importar o controller no `WebhookModule` se necessario.
4. Reaproveitar helpers e padroes de token ou payload.
5. Adicionar item na tela admin so se a webhook precisar ser copiada por operador.
6. Manter a rota em `/api/webhooks/*`.
7. Verificar se a rota nova pode colidir com `:clientSlug/:unit`; se puder, proteger explicitamente no bootstrap ou separar melhor as rotas.
8. Verificar impacto em `deploy-webhooks.ps1`, `tools\vps-deploy-webhooks.ps1` e `infra/caddy/Caddyfile` apenas se houver desvio real do padrao.
9. Na VPS, garantir que nao ficou um `jetta-webhooks-3003` legado concorrendo com `jetta-webhooks`.
