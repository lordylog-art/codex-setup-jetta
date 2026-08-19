---
name: webhook
description: Criar, adaptar e documentar webhooks do ERP Jetta no mesmo padrao dos webhooks atuais, com foco em integracoes de chatbot da Connect Channels. Use quando Codex precisar adicionar um novo endpoint em `/api/webhooks/*`, reaproveitar o servidor dedicado de webhook, incluir ou ajustar a tela administrativa de links de webhook, manter compatibilidade com o deploy dedicado e com o blue/green da VPS, ou entender como token, payload, rota publica, Caddy e PM2 se encaixam nesse fluxo.
---

# Webhook

Seguir o padrao real do projeto. Nao inventar uma arquitetura nova de webhook quando o fluxo existente ja cobre a necessidade.

## Fluxo Base

1. Mapear o contexto antes de editar.
2. Confirmar se a webhook nova entra no servidor dedicado existente.
3. Implementar o endpoint no modulo ou controller certo.
4. Atualizar a tela administrativa se a webhook precisar de link copiavel.
5. Preservar deploy, rota publica e comportamento de VPS.
6. Validar so o necessario para a tarefa pedida.

## Mapear O Padrao Atual

Abrir primeiro estes arquivos:

- `E:\ERP jetta\apps\api\src\webhook-main.ts`
- `E:\ERP jetta\apps\api\src\webhook.module.ts`
- `E:\ERP jetta\apps\api\src\modules\availability\availability-webhook.controller.ts`
- `E:\ERP jetta\apps\api\src\modules\webhooks\calendar-webhook.controller.ts`
- `E:\ERP jetta\apps\web\src\app\admin\webhooks\page.tsx`
- `E:\ERP jetta\apps\web\src\app\admin\webhooks\webhook-links.ts`
- `E:\ERP jetta\deploy-webhooks.ps1`
- `E:\ERP jetta\tools\vps-deploy-webhooks.ps1`
- `E:\ERP jetta\infra\caddy\Caddyfile`

Se precisar de um mapa resumido, ler `references/erp-webhook-pattern.md`.

## Implementar Na API

Manter a webhook dentro do processo dedicado que ja existe.

- O bootstrap dedicado e `webhook-main.ts`.
- O prefixo continua vindo de `API_PREFIX`, entao as rotas publicas seguem `/api/webhooks/...`.
- A porta padrao do processo dedicado e `WEBHOOK_PORT=3003`.
- Nao criar porta nova, processo novo ou Caddy novo sem requisito explicito.

Antes de confiar apenas em decorators do Nest, revisar se a rota nova pode conflitar com rotas dinamicas ja existentes.

- Neste projeto, caminhos como `/webhooks/availability/:clientSlug/:unit` podem capturar acidentalmente uma rota estatica como `/webhooks/availability/occurrence-alert/client-delay`.
- Quando houver esse risco, nao confiar apenas na ordem aparente dos metodos do controller.
- Preferir uma protecao explicita: restringir melhor a rota dinamica, separar controller ou registrar uma rota exata no `webhook-main.ts` antes do fluxo global do Nest quando o conflito for real em producao.
- Se aparecer `401 Invalid webhook token.` numa webhook que deveria ser publica, suspeitar primeiro de colisao com a rota protegida por token.

Escolher a localizacao do endpoint pelo dominio:

- Se for disponibilidade, telefone, status do motorista ou chatbot desse fluxo, preferir `apps/api/src/modules/availability/availability-webhook.controller.ts`.
- Se for um webhook mais generico e separado, avaliar `apps/api/src/modules/webhooks/`.
- Se precisar de novo controller, importar no `WebhookModule` apenas o que for necessario. Evitar levar schedulers, modulos grandes ou controllers fora de webhook.

Seguir os padroes existentes do controller:

- Aceitar `GET` e `POST` apenas quando isso ja fizer sentido para automacao atual.
- Ler dados de `query`, `body` e `headers` no mesmo estilo dos webhooks existentes.
- Reaproveitar metodos auxiliares para `phone`, `sessionId`, `lastContactMessage` e payloads parecidos da Connect Channels quando possivel.
- Falhar de forma explicita. Nao esconder erro real com retorno vazio.
- Se a regra de negocio mudar, parar e pedir confirmacao.
- Se a webhook for acionada pela Connect Channels com `POST`, conferir se o `body` continua chegando no handler certo. Se o caminho cair no handler generico, o endpoint pode acabar usando token ou ignorando o payload sem deixar isso obvio.

## Token, Header E Seguranca

Usar o padrao atual antes de inventar autenticacao nova.

- O fluxo protegido existente usa `WebhookTokenService`.
- O segredo atual de disponibilidade usa `AVAILABILITY_WEBHOOK_SECRET_ID`.
- O controller atual aceita `X-Webhook-Token` e tambem `Authorization: Bearer ...`.
- A tela admin gera e salva token para esse fluxo.

Se a nova webhook precisar do mesmo modelo de protecao:

1. Reaproveitar `WebhookTokenService`.
2. Expor a regra na tela admin se o usuario precisar copiar URL ou header.
3. Nao colocar token na query string se o padrao atual nao faz isso.

Se a webhook for publica por requisito funcional, deixar isso explicito no codigo e na entrega.

## Tela Administrativa

Quando a webhook precisar aparecer na tela de copia:

1. Atualizar `apps/web/src/app/admin/webhooks/webhook-links.ts`.
2. Definir `id`, `label`, `description`, `method`, `path` e `headerName` quando houver.
3. Preservar o uso de `buildWebhookUrl(origin, webhook)` para o host mudar sozinho entre ambiente local, dominio e VPS.
4. Nao embutir token dentro da URL copiada. O padrao atual separa URL e header.
5. Se a nova webhook nao precisar aparecer nessa tela, nao adicionar por oportunismo.

## Connect Channels

Assumir que a origem principal da integracao e chatbot da Connect Channels.

Consultar a documentacao oficial quando o payload ou o comportamento do bot nao estiver claro:

- Docs gerais: `https://connect-channels.gitbook.io/connect-channels-docs`
- Link tecnico de API citado pela propria base: `https://connectapi-sbai.readme.io/reference`

Cruzar a doc externa com o que o projeto ja usa hoje. Neste repositorio, os webhooks atuais ja esperam campos como:

- `contact.phonenumber`
- `contact.display-phonenumber`
- `lastContactMessage`
- `lastMessage.text`
- `sessionId`
- estruturas aninhadas em `menus`

Se a doc da Connect Channels pedir um payload diferente do padrao atual, adaptar com o menor desvio possivel e destacar a diferenca na entrega.

## VPS, PM2 E Caddy

Preservar o circuito operacional existente:

- Processo PM2 principal do webhook: `jetta-webhooks`
- Deploy dedicado: `E:\ERP jetta\deploy-webhooks.ps1`
- Deploy remoto assistido: `E:\ERP jetta\tools\vps-deploy-webhooks.ps1`
- Rota publica: `https://www.ciadm.com.br/api/webhooks/*`
- Proxy local padrao do Caddy para webhook: `localhost:3003`

Depois de deployar, confirmar se nao ficaram processos duplicados de webhook no PM2.

- Ja ocorreu de a VPS manter `jetta-webhooks` e `jetta-webhooks-3003` ao mesmo tempo.
- Nesse cenario, a porta `3003` pode ficar servindo um processo legado e mascarar a correcao nova.
- Conferir `pm2 status jetta-webhooks` e `pm2 status jetta-webhooks-3003`.
- Se houver legado sobrando, limpar o processo antigo antes de concluir o teste final.

Considerar tambem o blue/green:

- Porta candidata de webhook no deploy principal: `3203`
- O `NewDeploy.ps1` faz cutover do Caddy para `/api/webhooks/*`
- Nao assumir que webhook sempre fica preso em `3003` durante deploy zero downtime

Se a webhook nova depender de rota publica, manter o prefixo `/api/webhooks/*` para continuar coberta pelo Caddy atual. So mexer no `Caddyfile` se surgir uma exigencia real fora desse padrao.

## Entrega

Na resposta final, resumir:

1. Onde o endpoint foi criado.
2. Se entrou na tela admin.
3. Como fica a rota publica.
4. Se usa token ou header.
5. Se ha algum passo manual na Connect Channels ou na VPS.

Quando o objetivo for validar webhook da Connect Channels em producao, incluir tambem:

6. Se o teste real retornou `401`, `404`, `400` ou `200`, e o que esse status prova sobre o roteamento.
7. Se a VPS ficou com apenas um processo canonico dono da `3003`.

## Referencia

Ler `references/erp-webhook-pattern.md` para portas, arquivos, rotas e checklist rapido do projeto.
