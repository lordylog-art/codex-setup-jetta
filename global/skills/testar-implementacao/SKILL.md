---
name: testar-implementacao
description: Testar implementações na prática exclusivamente pelos endpoints autenticados do ERP Jetta. Use quando o usuário pedir para testar uma implementação, testar endpoint, validar fluxo completo, validar na prática pelo endpoint, ou confirmar se uma mudança está funcionando usando o usuário/token de teste do .env, iniciando a API ou o site local quando necessário e desfazendo os dados criados.
---

# Testar Implementação

## Objetivo

Validar uma implementação por fluxo real de endpoints, autenticando com o usuário/token de teste do `.env`, executando as chamadas detalhadamente como um usuário faria pela aplicação, observando evidências concretas e desfazendo tudo que o teste criou ou alterou.

Esta skill não usa navegador, Selenium, Playwright, Puppeteer, Browser plugin, automação visual, clique em UI, console do browser ou fallback por tela. A validação deve acontecer somente por HTTP/API contra endpoints reais do ERP Jetta.

## Regras de Segurança

- Nunca gravar, imprimir ou repetir valores reais de senha, token, cookie, JWT ou segredo.
- Usar apenas os nomes das variáveis: `TEST_LOGIN_EMAIL`, `TEST_LOGIN_PASSWORD`, `TEST_AUTH_TOKEN`, `NEXT_PUBLIC_API_URL`, `APP_URL`, `API_PORT`.
- Usar token/cookie somente a partir do `.env` ou da resposta real de autenticação; nunca inventar token, usuário, payload ou contrato.
- Não testar em produção, VPS ou serviço externo real sem autorização explícita do usuário.
- Não executar operação destrutiva, migration, truncate, delete massivo, deploy, restart crítico ou alteração de `.env`.
- Se não houver forma segura de desfazer os dados criados ou alterados, parar antes da escrita e reportar o bloqueio.
- Se o fluxo envolver e-mail, WhatsApp, pagamento, Greenmile ou integração externa real, reduzir o impacto para sandbox/noop/test account ou pedir autorização explícita.

## Escolha do Ambiente

Antes de qualquer chamada HTTP, perguntar explicitamente se o teste deve rodar no `local` ou na `produção`, exceto quando o usuário já tiver informado isso de forma clara no pedido.

Pergunta padrão:

`Você quer que eu rode esse teste no local ou na produção?`

- Se a resposta for `local`, usar somente endpoints locais e variáveis locais.
- Se a resposta for `produção`, confirmar que o usuário autorizou produção e seguir as regras de segurança para ambiente real.
- Se a resposta for ambígua, parar e pedir confirmação antes de autenticar, ler dados, executar sync ou disparar qualquer endpoint com efeito.
- Em ambiente `local`, verificar primeiro se a API e o site necessários ao fluxo já estão acessíveis.
- Se a API ou o site local necessário estiver desligado, existe autorização permanente desta skill para iniciá-lo sem pedir nova confirmação, usando somente o comando oficial já existente no projeto.
- Iniciar apenas o serviço local que estiver inativo. Não reiniciar, parar, substituir nem duplicar processo que já esteja ativo.
- Aguardar a prontidão do serviço iniciado e repetir a verificação de acesso. Se o processo não subir ou não ficar saudável, parar e reportar o comando usado e o erro observado, sem criar comando alternativo ou fallback silencioso.
- Essa autorização não vale para produção, VPS, banco, proxy ou serviço externo e não autoriza alterar `.env`, instalar dependências ou liberar portas encerrando processos.

## Proibições

- Não abrir navegador.
- Não usar Selenium, Playwright, Puppeteer, Browser plugin ou automação visual.
- Não substituir o teste por acesso direto à UI, inspeção manual de tela ou chamada simulada.
- Não usar fallback silencioso: se um endpoint, payload, token, cookie, leitura, cleanup ou contrato falhar, parar, registrar a falha e reportar.
- Não trocar endpoint, método, payload, autenticação, filtro, ordenação ou validação para "fazer passar" sem evidência no código e autorização do usuário quando mudar regra de negócio.
- Não aceitar somente status 2xx como prova.

## Fluxo Obrigatório

1. Identificar o endpoint, o fluxo completo informado pelo usuário e o ambiente (`local` ou `produção`).
2. Se o ambiente não estiver explícito, perguntar se deve rodar no `local` ou na `produção` e parar até receber resposta.
3. Descobrir contratos reais no código antes de chamar: método, rota, payload, resposta esperada, autenticação, efeitos colaterais e endpoint de leitura/remoção quando existir.
4. Definir a base URL conforme o ambiente autorizado:
   - Preferir `NEXT_PUBLIC_API_URL` quando apontar para proxy local utilizável.
   - Usar `APP_URL` ou `http://127.0.0.1:<API_PORT>/api` quando for mais direto para a API.
   - Em produção, usar somente a URL real autorizada pelo usuário, sem inferir ambiente por conta própria.
   - Em ambiente `local`, testar a disponibilidade da API e do site exigidos pelo fluxo antes da autenticação.
   - Se algum deles estiver desligado, localizar o script oficial nos arquivos do projeto (`package.json`, scripts ou documentação local), iniciar somente esse serviço e aguardar sua prontidão antes de continuar.
   - Não inventar comando de inicialização, não matar processo para liberar porta e não iniciar o mesmo serviço duas vezes.
5. Autenticar obrigatoriamente por endpoint:
   - Se `TEST_AUTH_TOKEN` existir e o contrato do endpoint aceitar `Authorization: Bearer`, usar esse token.
   - Caso contrário, fazer `POST /api/auth/login` com `TEST_LOGIN_EMAIL` e `TEST_LOGIN_PASSWORD`.
   - Preservar o cookie/token retornado para todas as próximas chamadas.
   - Não criar token manual, não reaproveitar token antigo de log e não pular autenticação.
   - Se o login travar, não responder ou falhar por conexão no ambiente `local`, verificar novamente a disponibilidade da API. Se ela estiver desligada, iniciá-la conforme a autorização local desta skill e repetir o login uma única vez após a prontidão; se a API estiver ativa ou a nova tentativa falhar, parar e reportar.
6. Validar a sessão via `GET /api/auth/me`; se falhar, parar e reportar que deu ruim.
7. Registrar o estado inicial mínimo necessário para cleanup: IDs existentes, contagens, valores originais ou ausência do registro.
8. Executar o fluxo completo pelo endpoint real, na mesma sequência operacional que um usuário faria:
   - chamar endpoints de listagem/busca necessários para obter IDs e opções reais;
   - chamar endpoint de criação/alteração principal com payload real validado no código;
   - consultar o efeito por endpoint de leitura independente;
   - validar caminho negativo quando for parte essencial da mudança;
   - registrar cada chamada relevante com método, rota, status e resumo seguro.
9. Guardar evidências objetivas: endpoint, método, status, payload resumido, resposta resumida, ID criado, leitura pós-ação, log relevante ou efeito observado.
10. Desfazer somente o que o teste criou ou alterou:
   - preferir endpoint oficial de delete/reversão;
   - se usar SQL, limitar por IDs/valores rastreados e validar antes/depois;
   - restaurar valores originais quando a ação for update;
   - confirmar que o dado temporário não ficou visível no fluxo.
11. Rodar uma verificação final por endpoint para provar que o cleanup funcionou.

## Critério de Sucesso

Considerar funcionando somente quando todos forem verdadeiros:

- autenticação por `TEST_AUTH_TOKEN` ou `POST /api/auth/login` funcionou;
- `GET /api/auth/me` confirmou a sessão do usuário de teste;
- o fluxo foi executado exclusivamente por endpoints reais;
- o endpoint executou o fluxo completo esperado;
- o efeito real foi observado por leitura independente via endpoint;
- todos os dados temporários foram removidos ou revertidos;
- não houve fallback, navegador, Selenium ou automação visual;
- não houve segredo exposto em comando, log ou resposta final.

## Quando Deu Ruim

Se qualquer etapa falhar, responder explicitamente que deu ruim e incluir:

- etapa que falhou;
- endpoint/método envolvido;
- status e erro resumidos, sem segredo;
- evidência observada;
- se algo foi criado/alterado antes da falha;
- se o cleanup foi concluído, parcial ou bloqueado;
- confirmação de que nenhum fallback foi usado;
- próximo menor passo recomendado.

## Saída Final

Responder curto e operacional:

- `Resultado`: funcionou ou deu ruim.
- `Fluxo testado`: endpoint(s), método(s) e ambiente.
- `Ambiente`: `local` ou `produção`, conforme autorizado pelo usuário.
- `Serviços locais`: informar se API/site já estavam ativos ou quais foram iniciados e se ficaram prontos.
- `Autenticação`: token/cookie usado sem expor valor, e confirmação de `GET /api/auth/me`.
- `Evidência`: status, resposta resumida e efeito observado.
- `Cleanup`: o que foi removido/revertido e como foi confirmado.
- `Sem fallback`: confirmar que não houve navegador, Selenium, automação visual ou rota alternativa.
- `Limitações`: o que não foi validado ou exigiria autorização.
