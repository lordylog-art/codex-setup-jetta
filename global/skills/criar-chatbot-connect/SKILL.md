---
name: criar-chatbot-connect
description: Criar, alterar, clonar e validar chatbots da Connect Channels automaticamente por JSON usando a sessao Chrome logada, o contrato interno GET/PUT/POST de version/url, menus, perguntas, etiquetas, transferencias, condicionais, blocos lineares e validacao visual no builder. Use quando o usuario pedir para criar um chatbot Connect do zero, montar fluxo com etapas, ligar blocos, direcionar para outro chatbot, etiquetar contatos, replicar/alterar um fluxo existente ou automatizar construcao de chatbots na Connect Channels.
---

# Criar Chatbot Connect

## Objetivo

Criar ou alterar chatbots da Connect Channels por JSON, usando a mesma sessao Chrome/CDP logada. O fluxo padrao e: entender o pedido, descobrir contratos reais quando necessario, gerar payload, salvar como rascunho via `version/url` e validar por API. Reabrir o builder para validacao visual somente quando o usuario pedir, quando houver contrato incerto ou quando a API indicar inconsistencia.

## Regras de Seguranca

- Nunca expor token, cookies, localStorage, senha, 2FA ou headers sensiveis.
- Nunca clicar em `Publicar` sem autorizacao explicita.
- Nunca clicar em `Testar chatbot` sem autorizacao explicita.
- Nunca executar webhook real ou disparo externo durante montagem de rascunho.
- Salvar primeiro como rascunho e reportar `versionId`, status e validacoes.
- Se o usuario pedir algo cujo contrato nao foi confirmado, descobrir pela UI ou dizer a incerteza. Nao inventar endpoint, campo ou payload.

## Dependencias Recomendadas

Use tambem, quando aplicavel:

- `$entrar-connect`: abrir/reutilizar Chrome controlavel em `http://127.0.0.1:9222`.
- `$connect-channels`: regras gerais de seguranca/API Connect.
- `$investigar-detalhes`: investigar telas, botoes, modais e contratos antes de automatizar.

## Fluxo Padrao

1. Confirmar objetivo do chatbot em linguagem natural:
   - nome do chatbot;
   - objetivo do atendimento;
   - menus e opcoes;
   - mensagens por etapa;
   - etiquetas finais;
   - transferencia para humano ou outro chatbot;
   - condicionais, aguardas e encerramentos.
2. Reutilizar primeiro a sessao Chrome/CDP ja aberta, sem abrir, clicar ou navegar:
   - rodar `node C:\Users\Jetta\.codex\skills\criar-chatbot-connect\scripts\connect_chatbot_tools.js --session-check`;
   - se `authenticated: true`, seguir por endpoints internos com `--read`/`--save`;
   - se o CDP nao responder ou nao houver aba do Connect logada, so entao usar `$entrar-connect` para abrir/reutilizar o Chrome controlavel e pedir login manual quando necessario.
   - Para auth, seguir o "Caminho Facil Para Auth/Sessao" em `references/contrato-builder.md`: API interna usa token da sessao Chrome/CDP; API publica WTS usa `CONNECT_CHANNELS_API_TOKEN` do `.env`.
3. Ler o chatbot alvo ou um molde real por:
   - `GET /chat/v1/chatbot/{chatbotId}/nodes?includeDetails=All`
4. Converter o payload aceito pelo backend para payload de rascunho:
   - `startGroupClientGeneratedId`
   - `nodes`
   - `edges`
   - `groups`
   - `notes`
   - `config`
   - `triggers`
5. Gerar ou transformar o JSON com IDs clientGeneratedId estaveis.
6. Auditar antes de salvar:
   - menu options tem edges;
   - condition cases tem edges;
   - grupos lineares tem `EXIT` quando necessario;
   - grupos terminais ou com saidas proprias nao recebem `EXIT` artificial;
   - `ACTION.WEBHOOK` so existe se autorizado e validado;
   - `TEMPLATE` so existe se usuario pediu modelo e contrato foi validado;
   - etiquetas usam IDs reais de `/core/v1/tag`;
   - todos os grupos importantes sao alcancaveis.
7. Salvar rascunho:
   - `GET /chat/v1/chatbot/{chatbotId}/version/url`
   - `PUT` do JSON na URL S3 assinada
   - `POST /chat/v1/chatbot/{chatbotId}/version/url` com `{key,url}`
8. Validar por API:
   - repetir `GET /chat/v1/chatbot/{chatbotId}/nodes?includeDetails=All`;
   - auditar grupos, nos, ligacoes, menus, condicionais, webhooks/templates e `EXIT` invalido.
9. Reabrir builder somente se necessario:
   - `https://app.connectchannels.com.br/builder/chatbots/{chatbotId}/edit`
10. Validar visualmente quando aplicavel:
   - nome e status `Rascunho`;
   - blocos aparecem;
   - textos e acentos aparecem;
   - contador vermelho de problemas;
   - handles vermelhos;
   - menu, condicional e etiquetas renderizam.

## Regras De Ligacao

Use estas regras para evitar o erro visual que apareceu no builder:

- `MENU`: ligar cada `menu.options[].clientGeneratedId` ao grupo alvo. Nao forcar `group-EXIT` para o menu.
- `CONDITION`: ligar cada `conditions[].clientGeneratedId` ao grupo alvo. Nao forcar `group-EXIT` no grupo da condicional.
- `COMPLETE_SESSION`: tratar como terminal. Nao forcar `group-EXIT`.
- `TRANSFER_CHATBOT`: tratar como terminal/saida propria. Nao forcar `group-EXIT`.
- Grupos lineares com mensagem, aguarda, etiqueta ou agregacao podem usar `groupClientGeneratedId + "-EXIT"` para o proximo grupo.
- Se o builder mostrar contador de ligacoes invalidas, procurar handles com classe `border-red-500` e comparar com o tipo do no.

## Condicionais Sem Inchar Fluxo

Quando uma condicional tiver varias respostas/variacoes levando para o mesmo destino, nao criar varios blocos nem varios fluxos separados. Criar varios casos dentro do mesmo no `CONDITION`, cada um com seu `conditions[].clientGeneratedId`, e apontar todos para o mesmo `target.clientGroupId`.

Exemplo: para `Sim`, `sim`, `S`, `positivo`, `simm`, criar varios grupos de condicao no mesmo modal/mesmo node e ligar todos ao grupo "Confirmado". Para `Nao`, `Não`, `n`, `negativo`, ligar todos ao grupo "Desistencia".

Regras praticas:

- Um unico node `CONDITION` pode ter muitos casos.
- Cada caso pode apontar para o mesmo destino de outro caso.
- Cada caso precisa de sua propria edge pelo `clientGeneratedId` do caso.
- Usar "Adicionar grupo de condicao" para variacoes alternativas que levam ao mesmo resultado.
- Usar "Adicionar condicao" dentro do mesmo caso apenas quando a regra deve combinar criterios, normalmente em modo `AND`; nao usar isso como substituto de alternativas se o builder exigir todas as condicoes ao mesmo tempo.
- So criar novos grupos/blocos quando o destino ou a acao seguinte forem realmente diferentes.
- Depois de salvar, reabrir o modal da condicional e conferir se os casos ficaram agrupados corretamente antes de publicar.

## Blocos Ja Usados Com Sucesso

- `CONTENT`: enviar mensagem.
- `MENU`: enviar menu com opcoes navegando para grupos.
- `CONDITION`: saidas por casos, mantendo contrato aceito pelo Connect.
- `ACTION.SET_CONTACT_TAG`: adicionar/remover etiquetas do contato.
- `ACTION.AGGREGATE_MESSAGES`: aguardar mensagens do contato.
- `ACTION.DELAY`: esperar segundos.
- `ACTION.TRANSFER_CHATBOT`: direcionar para outro chatbot.
- `ACTION.COMPLETE_SESSION`: concluir atendimento.
- `ACTION.GOTO_RETURN_POINT`: retorno/reorientacao quando herdado de contrato real.

## Caminho Facil Para Template/Modelo

Quando o usuario informar um modelo por `internalName` ou apelido tecnico, como `3b8c3_gestor`, nao usar esse valor direto em `template.templateId`. O builder espera o UUID real do template; usar `internalName` direto pode salvar no S3, mas o `POST /version/url` falha com 500.

Fluxo seguro:

1. Consultar primeiro pela API publica da Connect Channels, usando a skill `$connect-channels` e o token do `.env`, sem imprimir segredo:

```powershell
python C:\Users\Jetta\.codex\skills\connect-channels\scripts\connect_channels.py --env-path "C:\Scripts\ERP JETTA\.env" list-templates --name gestor --page-size 20
```

2. Se o usuario passou `internalName`, buscar pelo nome humano provavel ou listar modelos relacionados e conferir `internalName`.
   - Exemplo confirmado: `internalName = 3b8c3_gestor` resolve para `id = ad1ea2c0-441b-479a-8171-60b994d86d96`, `name = Gestor`.
3. Usar o UUID real em:
   - `node.template.templateId`
   - `node.template.template.id`
   - cada `CONDITION.conditions[].conditions[].templateId`
4. Copiar os dados reais retornados do template (`name`, `text`, `params`, `interactives`, `fileType`, `status`) para `node.template.template` quando montar JSON manualmente.
5. Se houver parametro obrigatorio, preencher em `template.params.items`.
   - Exemplo do Gestor: `[UNIT]` pode ser `STATIC_VALUE` com `replacementName: "UNIT"` e `staticValue: "padaria"`.

Observacoes:

- O endpoint interno do builder `/chat/v1/template` pode retornar vazio mesmo quando a API publica encontra o modelo. Nao concluir que o template nao existe antes de consultar a API publica.
- Para templates com botoes, condicoes por resposta devem usar `field: "TEMPLATE"`, `operator: "EQUAL"`, `values` igual ao texto do botao ou variacao aceita, e `templateId` com UUID real.
- Se o template tiver botoes reais, priorizar os textos reais dos botoes nas condicoes. Variacoes livres podem ser adicionadas, mas podem depender de como a Connect normaliza respostas de template.

## Utilitarios

Leia `references/contrato-builder.md` quando precisar lembrar o contrato, as armadilhas de edges ou os IDs reais descobertos.

Use `scripts/connect_chatbot_tools.js` como base para:

- obter token da sessao CDP sem imprimir;
- confirmar auth sem abrir navegador com `--session-check`;
- chamar API interna autenticada;
- salvar payload de rascunho via S3 assinado;
- auditar menu, condicional, webhook/template e `EXIT` invalido.

## Resposta Final Esperada

Ao terminar, responder:

- chatbot alterado/criado;
- `versionId` salvo;
- status (`NOT_PUBLISHED` esperado);
- contagem de grupos, nos e ligacoes;
- validacoes executadas;
- o que nao foi publicado/testado;
- riscos ou contratos ainda incertos.
