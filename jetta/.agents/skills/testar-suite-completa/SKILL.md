---
name: testar-suite-completa
description: Rodar e auditar todos os testes do ERP Jetta sem excecao e sem mascarar falhas. Use quando o usuario pedir para rodar todos os testes, validar a suite completa, conferir regressoes, investigar testes quebrados, garantir que nada antigo quebrou, ou quando houver falha de teste que precise ser classificada como legado antigo ou regressao recente antes de alterar codigo ou testes.
---

# Testar Suite Completa

## Principio

Rodar a suite completa real do repositorio e mostrar as falhas sem esconder, resumir demais ou alterar testes para passar. Teste quebrado e evidencia: antes de mexer em teste ou producao para "corrigir", perguntar ao usuario se a falha representa comportamento antigo aceito, feature antiga quebrada agora, ou requisito novo esperado.

## Pergunta Obrigatoria Antes de Corrigir Falhas

Quando qualquer teste falhar, parar antes de alterar codigo ou teste e perguntar ao usuario:

`Essa falha e de comportamento antigo que ja existia/era aceito, ou e algo que quebrou agora e precisa ser corrigido como regressao?`

Se houver varias falhas, agrupar por area e perguntar por grupo. Nao pedir decisao teste por teste quando a causa for claramente a mesma.

## Regras Antimaquiagem

- Nao apagar, pular ou desabilitar teste com `.skip`, `xit`, `describe.skip`, filtro de arquivo, alteracao de script ou exclusao de cenario para obter suite verde.
- Nao afrouxar assercao, remover `expect`, aceitar `null`/vazio, trocar dado realista por mock mais fraco, reduzir cobertura ou alterar snapshot sem entender o comportamento protegido.
- Nao mudar teste para refletir o comportamento atual antes de verificar se a feature esta correta.
- Nao transformar falha real em aviso, fallback, retorno vazio, timeout menor, retry oculto ou tratamento generico.
- Nao declarar que "passou" quando algum comando falhou, foi interrompido, nao rodou, ficou pendente ou dependeu de ambiente ausente.

## Descoberta da Suite

Antes de executar, ler os `package.json` relevantes e listar os comandos de teste disponiveis. Neste projeto, a ordem padrao esperada e:

1. `npm run test --workspace @erp-jetta/api`
2. `npm run test --workspace @erp-jetta/web`
3. `npm run test:e2e --workspace @erp-jetta/web`
4. `npm run test:e2e --workspace @erp-jetta/api`, se existir no `apps/api/package.json`

Tambem verificar scripts raiz como `npm run test` e `npm run test:e2e`. Se houver divergencia entre esta lista e os `package.json`, seguir os `package.json` atuais e explicar a diferenca.

## Execucao

- Rodar todos os comandos de teste encontrados, sem excecao, salvo se o usuario autorizar explicitamente pular algum grupo.
- Rodar cada grupo separadamente quando isso ajudar a preservar logs e identificar a area quebrada.
- Capturar comando, exit code, resumo, arquivos de teste falhos e primeiras mensagens uteis de erro.
- Se um comando depender de setup ausente, navegador, banco, variavel de ambiente ou servico local, registrar exatamente o bloqueio e continuar com os demais comandos independentes.
- Nao usar flags de atualizacao automatica, como update de snapshot, sem autorizacao explicita.

## Analise de Falhas

Para cada falha ou grupo de falhas, classificar apenas o que for evidencia direta:

- Area afetada.
- Teste ou arquivo falho.
- Comando que falhou.
- Sintoma observado.
- Hipotese inicial, marcada como hipotese.
- Se parece contrato antigo, regressao recente, ambiente ou requisito ambiguo.

Depois, perguntar ao usuario a classificacao obrigatoria antes de qualquer correcao que mude codigo de producao ou teste.

## Quando o Usuario Responder

- Se o usuario disser que e regressao recente, corrigir o codigo de producao preservando o teste sempre que possivel.
- Se o usuario disser que o comportamento antigo estava errado e a regra mudou, atualizar teste e producao com explicacao explicita da mudanca de regra.
- Se o usuario disser que e legado aceito, nao "corrigir" no embalo. Registrar como falha conhecida/legado e perguntar se deve criar ajuste separado.
- Se o usuario nao souber, investigar a feature antes de editar teste: ler codigo, historico local disponivel, documentacao e fluxos relacionados.

## Entrega

Responder com:

- Comandos executados e resultado de cada um.
- Total de grupos verdes, falhos, bloqueados e nao executados.
- Falhas agrupadas por area, com mensagem objetiva.
- O que foi perguntado ao usuario e qual decisao foi tomada.
- Qualquer teste nao rodado e o motivo.
- Confirmacao explicita de que nenhum teste foi mascarado, pulado ou alterado para passar, salvo quando o usuario autorizou uma mudanca de regra.
