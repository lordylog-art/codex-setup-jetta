---
name: criar-issues-com-instrucoes
description: Criar ou atualizar issues locais em Markdown com instru??es claras para Codex implementar. Use quando o usu?rio pedir para criar issue, insue, tarefa, feature, melhoria ou bug com escopo t?cnico; organizar demandas em arquivo `.md` dentro de `.requirements/issues`; transformar pedido solto em descri??o execut?vel; ou configurar uma issue com crit?rios de aceite, impactos em SQL, tabelas, functions, APIs, endpoints, telas e fluxos existentes.
---

# Criar Issues com Instru??es

## Overview

Use esta skill para transformar demandas do usu?rio em issues locais em Markdown, prontas para execu??o por Codex. O objetivo ? evitar issue vaga: perguntar at? o escopo ficar claro, escrever instru??es t?cnicas em portugu?s do Brasil, confirmar o resumo com o usu?rio e s? ent?o criar ou atualizar o arquivo `.md`.

N?o use conectores externos ou APIs de issue tracker. Trate os arquivos `.md` como a fonte de verdade.

## Armazenamento Local

Por padr?o, criar issues em:

```text
.requirements/issues/
```

Use este padr?o de arquivo quando o usu?rio n?o indicar outro:

```text
.requirements/issues/ISSUE-YYYYMMDD-HHMM-slug-curto.md
```

Para subissues, usar uma pasta da issue m?e:

```text
.requirements/issues/ISSUE-YYYYMMDD-HHMM-slug-curto/
  01-slug-da-subissue.md
  02-slug-da-subissue.md
```

Se j? existir um arquivo ou pasta equivalente, atualizar o existente em vez de duplicar. Preservar qualquer conte?do manual do usu?rio e alterar somente os campos necess?rios.

## Fluxo Obrigat?rio

1. Identificar onde o arquivo `.md` deve ficar.
2. Entender exatamente o que ser? implementado.
3. Investigar ou pedir nomes reais quando houver entidade t?cnica existente.
4. Montar descri??o no padr?o Codex.
5. Mostrar resumo final e perguntar se est? certo.
6. Criar ou atualizar o `.md` apenas ap?s confirma??o clara do usu?rio.

N?o pule a confirma??o final quando a issue ainda n?o foi criada ou quando a altera??o muda escopo, comportamento, banco, API ou tela.

## Perguntas

Pergunte em lotes curtos, preferindo 1 a 3 perguntas por vez. Continue perguntando at? ficar sem d?vida pr?tica sobre o que criar.

Antes de perguntar "o que voc? quer fazer" quando o usu?rio pedir para criar issue/insue/tarefa sem dizer qual ideia ou melhoria deseja implementar:

- Procure primeiro por arquivos de ideias no reposit?rio ou contexto dispon?vel, priorizando `ideias.md`, `IDEIAS.md`, `Ideias.md` e varia??es pr?ximas de nome.
- Leia apenas o necess?rio para extrair os t?tulos ou resumos das ideias.
- Responda com uma lista numerada curta das ideias encontradas e pergunte qual delas o usu?rio quer transformar em issue.
- Se houver muitas ideias, agrupe ou mostre as mais recentes/relevantes e ofere?a continuar a lista.
- Se nenhum arquivo de ideias existir ou ele n?o tiver itens claros, explique isso brevemente e s? ent?o fa?a as perguntas normais de escopo.

Pergunte obrigatoriamente quando n?o estiver claro:

- Onde criar: pasta, pacote local, issue m?e, grupo l?gico, label ou prioridade.
- Tipo da demanda: feature, melhoria, bug, investiga??o, d?bito t?cnico ou tarefa operacional.
- O que exatamente precisa ser implementado, alterado ou corrigido.
- Qual tela, fluxo, endpoint, tabela, function, job, integra??o ou regra de neg?cio ser? impactada.
- Quais valores, estados, op??es, permiss?es, filtros, colunas ou mensagens devem existir.
- O que fica fora do escopo.
- Como o usu?rio saber? que ficou pronto.

Se o usu?rio disser algo como "cria igual o outro", "dentro do 047" ou "naquela tela", busque contexto nos arquivos `.md` locais e no reposit?rio quando poss?vel. Se ainda houver ambiguidade, pergunte.

## Regra de Clareza

N?o invente:

- Pasta, pacote local, issue m?e, label ou prioridade.
- Nome de tabela, coluna, rota, endpoint, service, function, job ou integra??o.
- Payload, status, regra de valida??o, permiss?o ou comportamento de API.

Quando a demanda envolver SQL, tabela, coluna, migration, function, endpoint ou API existente:

- Mencione explicitamente esses elementos na issue, usando nomes reais quando conhecidos.
- Se estiver trabalhando dentro de um reposit?rio dispon?vel, pesquise rapidamente nomes existentes antes de escrever a issue.
- Se n?o for poss?vel verificar, escreva como hip?tese marcada: "Verificar tabela/modelo existente respons?vel por..." e pe?a confirma??o se isso muda o escopo.
- Diferencie dado persistido real de coluna visual/calculada no frontend.

## Padr?o da Issue

Escreva descri??es em portugu?s do Brasil, objetivas e execut?veis por Codex. Use esta estrutura quando couber:

```markdown
---
id: ISSUE-YYYYMMDD-HHMM
tipo: feature | melhoria | bug | investiga??o | tarefa
status: Aberta
prioridade: Alta | M?dia | Baixa
parent: ""
labels: []
---

# T?tulo

## Objetivo

[O que precisa existir ou ser corrigido, em uma frase clara.]

## Contexto

[Por que isso ? necess?rio e onde aparece no produto.]

## Escopo

- [Mudan?a concreta 1.]
- [Mudan?a concreta 2.]

## Impactos T?cnicos

- Telas:
- APIs/endpoints:
- Banco/SQL/tabelas/colunas:
- Functions/services/jobs:
- Integra??es:

## Regras e Valida??es

- [Valores permitidos, estados, permiss?es, filtros, defaults e caminhos negativos.]

## Crit?rios de Aceite

- [Condi??o verific?vel 1.]
- [Condi??o verific?vel 2.]

## Fora do Escopo

- [O que n?o deve ser implementado agora.]

## Observa??es para Implementa??o

- Reutilizar padr?es existentes.
- N?o refatorar fora do escopo.
- Validar comportamento no n?vel mais pr?ximo do uso real.
```

Remova se??es vazias. Para bugs, inclua tamb?m "Comportamento atual", "Comportamento esperado" e "Cen?rio de reprodu??o" quando houver informa??o suficiente.

## Resumo Antes de Criar

Antes de criar ou atualizar o arquivo `.md`, mostre um resumo curto com:

- Caminho proposto do arquivo.
- T?tulo proposto.
- Tipo, prioridade e labels.
- Issue m?e ou pacote local, quando existir.
- Escopo principal.
- Itens t?cnicos que ser?o mencionados.
- Crit?rios de aceite.
- Pontos ainda assumidos.

Depois pergunte: "Est? certo assim para eu criar/atualizar esse `.md`?"

S? prossiga quando o usu?rio confirmar de forma inequ?voca. Se o usu?rio corrigir algo, atualize o resumo e confirme novamente quando a mudan?a for relevante.

## Uso dos Arquivos Locais

Leia antes de escrever:

- Busque arquivos `.md` existentes quando o destino vier por apelido, n?mero, t?tulo ou contexto.
- Confira se j? existe issue parecida em `.requirements/issues` para evitar duplicata.
- Ao criar filhos, preserve v?nculo com a issue m?e via `parent` e pela pasta da issue m?e.
- Ao atualizar issue existente, altere apenas os campos pedidos ou necess?rios.
- Nunca chame issue tracker externo nem dependa de status remoto.

Ap?s criar ou atualizar, responda com o caminho do arquivo, resumo do que foi configurado e qualquer limita??o n?o validada.
