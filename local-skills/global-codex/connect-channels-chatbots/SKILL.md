---
name: connect-channels-chatbots
description: "Create or edit Connect Channels Builder chatbots over HTTP using recovered editor contracts: menus, conditions, actions, CRM, webhooks and AI nodes."
---

# Connect Channels

O Codex é a LLM que transforma o pedido em um payload nativo. Use o script para enviar esse payload; não é necessário instalar outra LLM nem redesenhar a plataforma.

## Estado e fontes

Leia [contracts.md](references/contracts.md) antes de montar ou alterar um fluxo. Ele identifica o catálogo real e as diferenças entre HELENA_SIMPLE e HELENA_ADVANCED. Preserve campos existentes fora da alteração solicitada.

A engenharia reversa está em `C:/Users/caila/Documents/Codex/connect-channels-automation`. Consulte os bundles/excertos apontados quando uma opção exigir mais detalhe. Não deduza contratos por rótulos ou apenas por enum. Biblioteca pública recuperada em 13/10/2026; alterações do fornecedor podem invalidar os contratos.

## Conexão

Reutilize a sessão DPAPI em `~/.codex/connect-channels-session.dpapi`. O cliente a lê em memória e renova pelo endpoint real de refresh, preservando tenantId. `CONNECT_ACCESS_TOKEN` pode fornecer uma sessão existente em vez desse arquivo; `CONNECT_API_BASE_URL` seleciona uma das bases recuperadas, padrão `https://api.wts.chat`. Não trate o token público de integração como prova de autorização para endpoints internos de criação.

A skill executa por HTTP e não usa browser, inclusive para autenticar. Chrome foi usado somente na investigação original da biblioteca. Se a sessão HTTP ainda não estiver disponível, use o fluxo abaixo; continue o planejamento local enquanto aguarda autenticação.

Antes de solicitar código, tente a sessão protegida existente numa leitura da API. O cliente renova tokens próximos do vencimento; se a API rejeitar a sessão com HTTP 401, tenta refresh uma vez. Peça OTP ao usuário somente quando não houver sessão ou o refresh for rejeitado por autenticação. Erros de rede, HTTP 403 e HTTP 5xx não justificam enviar outro código: diagnostique o erro e preserve a sessão. O código de e-mail é de uso temporário; o que se reaproveita é accessToken/refreshToken da sessão salva.

1. Solicite OTP pelo contrato recuperado: `node scripts/auth.mjs request <email> <challenge-novo.json>`.
2. Procure a mensagem enviada por `no-reply@app.connectchannels.com.br` ao usuário, após requestedAt. Inclua spam: Gmail exclui spam na busca padrão; use `in:anywhere` ou uma busca explícita `in:spam` quando necessário. Confira remetente, destinatário e horário antes de usar o código.
3. Peça ao usuário o código do challenge atual quando necessário. Se o conector Gmail devolver `one-time authentication code withheld`, mantenha esse passo manual; não busque formatos alternativos para contorná-la. Esta interação manual foi aceita pelo usuário em 13/10/2026. Nas próximas execuções, priorize sempre reutilização/refresh da sessão, sem solicitar OTP preventivamente.
4. Forneça o OTP ao stdin de `node scripts/auth.mjs authenticate <challenge.json>`. O helper envia o campo real `password`, armazena tokens com DPAPI do usuário Windows e exibe só resultado sanitizado. Mantenha códigos/tokens fora de relatórios e saídas.

O e-mail serve apenas à autenticação solicitada; a skill não envia mensagens pelo Gmail. Não use browser como fallback. Se o OTP foi consumido/expirou, confirme a rejeição e inicie um novo challenge uma única vez; evite loop de pedidos de e-mail.

## Criar pelo pedido do usuário

1. Resolva atendimento ou automação, canal, equipe padrão e modo do editor. Consulte IDs reais; peça apenas decisões de negócio ausentes. Não selecione o primeiro departamento/canal como regra automática.
2. Defina mensagens, perguntas, alternativas, saídas, fallback e ações. Consulte a seção **Compatibilidade HTTP comprovada no fluxo TI** da referência: parâmetros QUESTION de mensagens não podem ser copiados para campos de card; use SET_METADATA → SESSION_METADATA. O helper rejeita os casos observados antes do envio. Para nós IA, consulte agentes/equipes existentes; criar um agente LLM tem contrato próprio e não é o mesmo que adicionar um nó IA.
3. Escreva um arquivo JSON `{kind, create, version}` conforme a referência. `create` e `version` mantêm os formatos nativos, inclusive opções adicionais recuperadas da biblioteca. Para edição, leia o chatbot antes de produzir a versão.
4. Valide sem chamadas externas:
   `node scripts/connect.mjs plan <spec.json>`
   Esse check cobre estrutura, referências e alguns invariantes; não substitui os validadores do fornecedor ou a revisão semântica dos caminhos.
5. Execute `node scripts/connect.mjs create <spec.json> <journal.json>` com caminho de journal novo. Para salvar um rascunho existente: `save <id> <version.json> <journal.json>`.
6. Leia o snapshot gerado e compare cada obrigação do pedido com os nós/grupos, opções, mensagens, destinos, configurações e IDs persistidos. Confira a ordem por grupo e registre divergências de encadeamento; a compilação READY não comprova a execução da conversa. A gravação termina em `saved-content-review-required`, não em aceite automático.
7. Publique somente quando o pedido autorizar ativação e a revisão do fluxo estiver concluída: `publish <id> <versionId>`. Consulte o status até READY/FAILED com limite de tempo e confirme a versão implantada. Vincular canais/triggers operacionais e disparar mensagens exigem escopo do pedido correspondente; a criação de rascunho não faz isso automaticamente.

## Retomada e limites

Em timeout/erro de escrita, consulte o journal e reconcilie a conta antes de repetir. A ausência de resposta não prova ausência de criação. Se já existe `chatbotId`, retome esse rascunho; evite criar outro. URLs assinadas recebem JSON sem Authorization e não seguem redirects.

Para HTTP 500, retenha o vendorCode/requestId sanitizados mostrados pelo helper. Isole a diferença entre contratos em um rascunho sem canal, corrija com prova e restaure o fluxo completo; não deixe uma versão de diagnóstico como resultado final. Registre contratos comprovados na referência e cubra a regressão nos testes. O endpoint chamado `validate` compara versões e não aprova os caminhos do fluxo.

O helper rejeita edição direta de chatbot vinculado a canal ou arquivado. A associação inicial de uma automação NOT_PUBLISHED, com inUse=false, identidade chatbotId conferida e somente seu próprio canal é aceita para concluir o rascunho. READY, uso ativo ou vínculos adicionais continuam bloqueados. Prepare uma cópia/rascunho com o contrato de duplicação da referência para mudanças em operação.

`list` obtém uma página; para descoberta completa siga a paginação retornada pela API. `read <id>` consulta metadados e conteúdo. Todos os recursos são locais ao usuário; o ERP não é parte desta skill.

## Prova de conclusão

Informe separadamente: geração/validação local, autenticação, persistência/readback, publicação e comportamento integrado. Testes locais de protocolo estão em `scripts/connect.test.mjs` e `scripts/auth.test.mjs`; não chamam o fornecedor. DPAPI é exercitado no Windows real.

Em 13/10/2026 foram comprovados login HTTP, sessão protegida lida por outro processo e criação/gravação/readback de um rascunho HELENA_ADVANCED sem browser. Prova: `C:/Users/caila/Documents/Codex/connect-channels-automation/live-validation-result.json`. O rascunho ficou NOT_PUBLISHED, sem canal vinculado. Essa prova não certifica publicação, todos os tipos de nós ou renovação real, que só deve ocorrer quando necessária.
