---
name: connect-channels
description: Executar tarefas da Connect Channels/WTS Chat usando a documentação oficial indicada pelo usuário e o token CONNECT_CHANNELS_API_TOKEN do .env, como listar canais, listar modelos/templates, enviar modelo de mensagem para WhatsApp, consultar status de envio e montar payloads seguros. Use quando o usuário pedir ações da Connect Channels, envio de template/modelo, WhatsApp via Connect, consulta de templates/canais/status de mensagem ou automações usando a API da Connect.
---

# Connect Channels

## Fonte e Segurança

- Use esta skill quando o usuário pedir qualquer ação da Connect Channels, WTS Chat, Connect+, envio de template/modelo, consulta de canais/modelos ou status de mensagem.
- Primeiro consulte a documentação oficial já indicada pelo usuário:
  - Biblioteca principal: `https://connect-channels.gitbook.io/connect-channels-docs`
  - API técnica linkada pela própria biblioteca: `https://connectapi-sbai.readme.io/reference`
- Não use fontes de terceiros para contrato de API.
- Nunca imprima `CONNECT_CHANNELS_API_TOKEN`, Authorization header completo, `.env` real, respostas com segredo ou payload com token.
- Para chamadas reais, leia o token do `.env` local do projeto atual por padrão. Se estiver trabalhando na VPS, leia do `.env` remoto apenas por SSH seguro e sem exibir valor.
- Se o contrato da ação estiver incompleto, pare e diga exatamente o campo faltante. Não invente endpoint, ID, nome de parâmetro, canal ou payload.

## Endpoints Confirmados

Base confirmada no OpenAPI da documentação técnica:

```text
https://api.wts.chat
```

Endpoints úteis confirmados:

```text
GET  /chat/v1/channel
GET  /chat/v1/template
POST /chat/v1/message/send
GET  /chat/v1/message/{id}/status
```

Autenticação:

```http
Authorization: Bearer <CONNECT_CHANNELS_API_TOKEN>
Accept: application/json
Content-Type: application/json
```

## Fluxo Para Enviar Template

1. Ler `CONNECT_CHANNELS_API_TOKEN` do `.env` sem exibir valor.
2. Consultar o template por nome:

```http
GET https://api.wts.chat/chat/v1/template?Name=<NOME>&ApprovedOnly=true&IncludeDetails=All&PageSize=10
```

3. Confirmar que existe exatamente um template aprovado e ativo.
4. Obter:
   - `id` do template.
   - `channelId` do template.
   - `params` obrigatórios.
5. Consultar canais WhatsApp:

```http
GET https://api.wts.chat/chat/v1/channel?ChannelType=Whatsapp
```

6. Escolher o canal cujo `id` bate com `template.channelId`.
7. Enviar:

```http
POST https://api.wts.chat/chat/v1/message/send
```

Payload confirmado pelo OpenAPI:

```json
{
  "from": "+55|19996502923",
  "to": "5535998182404",
  "body": {
    "templateId": "uuid-do-template",
    "parameters": {
      "[NOME]": "Motorista"
    }
  },
  "options": {
    "hiddenSession": false
  }
}
```

Regras:

- `to` deve ser número do destinatário. Para telefone brasileiro sem DDI, normalize para `55` + DDD + número quando fizer sentido.
- `from` deve ser o número do canal cadastrado na Connect, no formato retornado pela API, por exemplo `+55|19996502923`.
- Se o template tiver parâmetros, preencha todos. Se o usuário não passar valor para um parâmetro obrigatório, use apenas um default óbvio e seguro quando houver contexto suficiente. Exemplo: `[NOME] = "Motorista"` para disparo operacional sem nome informado.
- Após enviar, reporte apenas dados não sensíveis: template, destinatário, canal formatado, status, id da mensagem e `statusUrl`.

## Script Auxiliar

Prefira usar `scripts/connect_channels.py` para operações reais. Ele evita vazar token nos logs e padroniza consultas.

Exemplos:

```powershell
python C:\Users\Jetta\.codex\skills\connect-channels\scripts\connect_channels.py list-templates --name Disponibilidade-Diaria
python C:\Users\Jetta\.codex\skills\connect-channels\scripts\connect_channels.py list-channels
python C:\Users\Jetta\.codex\skills\connect-channels\scripts\connect_channels.py send-template --template Disponibilidade-Diaria --to 35998182404 --param "[NOME]=Motorista"
python C:\Users\Jetta\.codex\skills\connect-channels\scripts\connect_channels.py message-status --id 86736d42-e7a5-4b87-b27e-361638779f27
```

Quando usar o script:

- Rode a partir do repositório `C:\Scripts\ERP JETTA` ou passe `--env-path`.
- Não passe token por argumento.
- Se precisar confirmar exatamente o JSON antes de enviar, use `--dry-run`; o script deve mascarar dados sensíveis.

## Resposta ao Usuário

Para execução bem-sucedida, responda curto:

- ação executada;
- destinatário;
- template/modelo;
- canal usado;
- status retornado;
- id/statusUrl.

Para bloqueio, diga:

- qual endpoint/documentação foi consultado;
- qual campo faltou;
- o que o usuário precisa informar para continuar.
