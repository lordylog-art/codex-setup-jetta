---
name: 3coracoes
description: Use quando qualquer tarefa envolver o cliente 3 Coracoes/3-coracoes no ERP Jetta. Obriga identificar se o escopo e Guarulhos, Sumare, Vespasiano, todas as unidades ou global/compartilhado antes de alterar codigo, SQL, planilhas, env, syncs, cadastros, disponibilidade, programacao diaria, acompanhamento de frota, ocorrencias, custo extra ou deploy.
---

# 3coracoes

## Regra Central

Antes de agir em qualquer demanda do cliente 3 Coracoes, determine explicitamente o escopo de unidade:

- `guarulhos`
- `sumare`
- `vespasiano`
- `todas`
- `global/compartilhado`

Se o usuario nao deixar isso claro e a mudanca puder afetar dados, tela, integracao, env, SQL, deploy ou comportamento por unidade, pergunte antes de implementar.

## Quando Perguntar

Pergunte a unidade quando o pedido envolver:

- motoristas, placas, CPF, CNH, disponibilidade ou cadastro;
- programacao diaria, acompanhamento de frota, reentrega, ocorrencias ou custo extra;
- Google Sheets, Gmail, Greenmile, syncs, jobs, envs ou credenciais;
- SQL, backfill, migracao, seed, relatorio ou consulta operacional;
- colunas, filtros, permissoes, textos ou layout que possam variar por unidade;
- deploy ou validacao em VPS relacionada ao cliente.

Pergunta padrao:

`Essa mudanca e para Guarulhos, Sumare, Vespasiano, todas as unidades ou algo global/compartilhado?`

## Como Classificar

- `guarulhos`, `sumare`, `vespasiano`: altere e teste somente o caminho daquela unidade, preservando as outras.
- `todas`: aplique comportamento comum, mas valide que dados/configuracoes separados continuam separados.
- `global/compartilhado`: use apenas para infraestrutura, componentes comuns, regras realmente compartilhadas ou dados que o usuario confirmou como compartilhados.

## Cuidados Obrigatorios

- Nao assumir que dados de Guarulhos servem para Sumare ou Vespasiano.
- Nao assumir que planilhas, envs, e-mails, colunas ou syncs sao iguais, mesmo quando o formato atual parece parecido.
- Nao transformar uma mudanca de uma unidade em mudanca global sem confirmar.
- Para motoristas, uma pessoa pode atender mais de uma unidade, mas consulta/cadastro deve respeitar a unidade do fluxo atual.
- Para SQL em producao, conte antes, faca backup quando houver update e reporte apenas agregados, sem expor dados sensiveis.

## Antes de Finalizar

Inclua na resposta:

- unidade/escopo usado;
- arquivos ou dados alterados;
- validacao feita para a unidade;
- se Guarulhos foi protegido contra regressao quando a mudanca afetar codigo compartilhado.
