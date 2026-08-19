---
name: criar-webhook
description: Criar webhooks no ERP Jetta ponta a ponta, incluindo contrato de entrada/saida, rota backend na porta dedicada de webhooks, sem token por padrao, testes TDD, registro na tela admin /admin/webhooks, validacao de build/lint focada e observacoes de seguranca. Use quando o usuario pedir novo webhook, rota de webhook, endpoint para Connect Channels/chatbot/automacao, ou quando pedir para fazer o webhook aparecer na tela administrativa de webhooks.
---

# Criar Webhook

## Regra Central

Criar webhook no ERP Jetta sempre como contrato publico completo: backend, testes, documentacao local de requisitos e card na tela `https://www.ciadm.com.br/admin/webhooks`. Nao considerar pronto se existir apenas a rota da API.

Por padrao, nunca criar webhook com token, header secreto, query secreta ou autenticacao. Webhook novo deve ser publico e compatível com provedores que chamam apenas URL, salvo se o usuario pedir explicitamente protecao por token/autenticacao ou se houver risco real de escrita sensivel que precise ser discutido antes.

## Fluxo

1. **Investigar antes de mexer**
   - Ler o padrao atual em `apps/api/src/modules/availability/availability-webhook.controller.ts`.
   - Ler o service correspondente antes de criar regra nova.
   - Ler a tela admin em `apps/web/src/app/admin/webhooks/webhook-links.ts`.
   - Se precisar de mapa rapido dos arquivos, leia `references/erp-jetta-webhook-map.md`.

2. **Fechar contrato**
   - Definir metodo, path, payload aceito, campos obrigatorios, resposta de sucesso e erro.
   - Confirmar se o webhook apenas consulta, altera estado ou chama integracao externa.
   - Nao exigir token por padrao. Se, por excecao confirmada pelo usuario, o webhook precisar de token, ele deve ir por `X-Webhook-Token` ou `Authorization: Bearer`; nunca por query string.
   - Se o recurso nao existir e o usuario quiser falha, retornar erro HTTP apropriado, normalmente `404`.

3. **Criar requisitos TDD**
   - Usar a skill `tdd` quando disponivel.
   - Criar `.requirements/<datetime>_<feature_name>/REQUIREMENTS.md`.
   - Registrar que o card da tela admin faz parte do aceite.

4. **Escrever testes primeiro**
   - Controller: chamada sem token, payload esperado, query de teste manual se existir, erro sem campo obrigatorio.
   - Se token tiver sido explicitamente solicitado por excecao, cobrir token valido/invalido e garantir que token em query string nao e aceito.
   - Service: regra real de negocio, caminho negativo e ausencia de efeito colateral quando for webhook de consulta.
   - Web/admin: garantir que o novo webhook aparece em `WEBHOOKS` e que `buildWebhookUrl` monta URL sem `token=`.

5. **Implementar backend**
   - Reaproveitar controller/service existentes quando o escopo for de disponibilidade.
   - Nao reaproveitar helpers de token em webhooks novos, salvo excecao explicitamente pedida pelo usuario.
   - Reaproveitar helpers de rate limit e extracao de telefone quando existirem.
   - Evitar enviar mensagem, alterar banco ou chamar Sheets se o contrato for somente verificacao.
   - Retornar apenas dados solicitados e nao imprimir segredo em log.

6. **Registrar na tela admin**
   - Adicionar entrada em `apps/web/src/app/admin/webhooks/webhook-links.ts`.
   - Usar label e descricao claros para operador.
   - Nao definir `headerName` para webhooks novos por padrao.
   - Se houver excecao confirmada com token, usar `headerName: "X-Webhook-Token"`.
   - Atualizar `apps/web/src/app/admin/webhooks/webhook-links.spec.ts`.
   - Se a tela renderizar detalhes especificos do payload no futuro, adicionar tambem o texto/teste visual correspondente.

7. **Validar**
   - Rodar testes focados da API e web.
   - Rodar ESLint focado nos arquivos alterados quando o lint global estiver ruidoso.
   - Rodar build do pacote impactado quando o contrato publico ou TypeScript mudar.
   - Se mexer em segredo, env, deploy, SQL ou dados reais, acionar `hacker-safado` antes de finalizar.

8. **Fechar**
   - Revisar `git diff --stat` e `git diff --name-only`.
   - Nao versionar `.env`, dumps SQL, backups, logs ou tokens.
   - No projeto ERP Jetta, commitar localmente em `main` ao terminar, sem push automatico.

## Checklist De Aceite

- Endpoint existe sob `/api/webhooks/...`.
- Webhook novo funciona sem token por padrao.
- Se token foi explicitamente solicitado, autenticacao por header existe e token em query nao e aceito.
- Erros de entrada e recurso nao encontrado retornam status nao-200 quando aplicavel.
- Nao ha efeito colateral indevido.
- Testes focados passam.
- Card aparece em `/admin/webhooks`.
- URL copiada nao contem token.
- Final informa o path exato do webhook e o status de validacao.
