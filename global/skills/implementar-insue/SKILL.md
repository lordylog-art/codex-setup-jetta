---
name: implementar-insue
description: Implementar uma issue local em Markdown ou pacote local de subissues em etapas, executando obrigatoriamente uma subissue por vez em sequ?ncia at? concluir o escopo autorizado. Use quando o usu?rio pedir para implementar um insue/issue em `.md`, executar feature, melhoria ou bug j? descrito em `.requirements/issues`, quebrar trabalho grande em partes menores, atualizar status local durante execu??o, executar subissues locais em `.requirements`, fazer item a item sem pedir aprova??o entre etapas quando o pacote j? estiver autorizado, ou pausar apenas em bloqueio, reprova??o, risco operacional ou ambiguidade real.
---

# Implementar Insue

## Overview

Use esta skill para implementar uma issue local em Markdown ou um pacote local de subissues sem misturar tudo de uma vez. O fluxo obrigat?rio ? receber uma issue pai ou um escopo local aprovado, quebrar em subissues execut?veis quando necess?rio, implementar uma subissue por vez, validar cada etapa e continuar em sequ?ncia at? concluir o escopo autorizado.

N?o use conectores externos ou APIs de issue tracker. O estado da execu??o deve ser registrado nos arquivos `.md`.

O padr?o da skill ? **execu??o sequencial cont?nua**: depois que o usu?rio autoriza implementar o pacote, n?o pare para pedir `aprovado`/`continue` entre subissues. Fa?a item a item, com checkpoint interno, valida??o e commit/registro conforme as regras do projeto. S? pare antes do fim se houver bloqueio real, risco operacional, decis?o de produto aberta, necessidade de a??o sens?vel ou reprova??o expl?cita do usu?rio.

## Entrada Obrigat?ria

A entrada deve conter uma issue local identific?vel, como caminho para `.md`, ID `ISSUE-YYYYMMDD-HHMM`, pasta em `.requirements/issues`, ou um pacote local de subissues aprovado.

Se o usu?rio n?o fornecer uma issue e n?o houver pacote local claro/aprovado, pare e pe?a o arquivo de escopo antes de planejar, criar subissues ou alterar c?digo.

Antes de implementar:

1. Ler a issue pai local ou o arquivo local de escopo em `.requirements`.
2. Ler t?tulo, descri??o, status, labels, prioridade, parent e filhos existentes.
3. Confirmar que a issue/pacote est? claro o suficiente para decompor ou executar.
4. Se houver ambiguidade de produto, perguntar ao usu?rio antes de criar subissues ou alterar c?digo.
5. Se houver filhos existentes, reaproveitar quando fizerem sentido em vez de duplicar.

## Status Local

Use o campo `status` no frontmatter do `.md`. Quando dispon?vel, siga este fluxo:

- Antes de trabalhar em uma subissue: `Analisando` ou `Em progresso`.
- Durante valida??o local: `Testando`.
- Ao terminar a subissue e antes de pedir aceite humano: `Verifica??o do Usu?rio`.
- Se o usu?rio aprovar: `Aprovado`.
- Se o usu?rio reprovar: manter ou retornar para `Analisando` ou `Em progresso` e corrigir.

Nunca marque como `Aprovado` sem aprova??o expl?cita do usu?rio.

Registrar tamb?m uma se??o no fim do arquivo quando houver avan?o:

```md
## Registro de Execu??o

- YYYY-MM-DD HH:mm BRT: status alterado para `Em progresso`; valida??o planejada: ...
- YYYY-MM-DD HH:mm BRT: implementa??o conclu?da; valida??es executadas: ...
```

## Decomposi??o em Subissues

Crie subissues locais dentro da pasta da issue pai para separar implementa??o em partes pequenas e verific?veis. Cada subissue deve ter objetivo ?nico, crit?rios de aceite pr?prios, v?nculo com a issue pai e escopo pequeno o bastante para valida??o isolada.

Ordem recomendada:

1. Contratos, dados, migrations ou endpoints m?nimos.
2. Backend/services.
3. Frontend/UI.
4. Integra??es externas.
5. Ajustes visuais, testes finais e regress?es.

N?o implemente a issue pai como uma massa ?nica. Execute somente a subissue atual, finalize a valida??o dessa etapa e ent?o avance para a pr?xima subissue autorizada.

## Modo de Execu??o Sequencial Cont?nua

Quando o usu?rio disser algo como `pode implementar`, `pode fazer todas`, `executa em sequ?ncia`, `sem eu aprovar uma por uma`, `pode seguir item a item` ou equivalente:

- Trate isso como autoriza??o para executar todas as subissues do pacote atual em sequ?ncia.
- N?o pergunte `aprova esta subissue?` entre etapas.
- N?o pergunte `posso ir para a pr?xima?` entre etapas.
- Mantenha uma fila ordenada de subissues e trabalhe sempre na primeira pendente.
- Antes de cada subissue, anuncie brevemente o progresso no formato `Subissue 3/5: [t?tulo]`.
- Ao terminar cada subissue, registre o resultado no `.md`, rode as valida??es relevantes e siga para a pr?xima.
- Se o projeto exigir commits, prefira commits pequenos por subissue ou por bloco coerente, desde que o diff permane?a revis?vel.
- Continue at? concluir todas as subissues, sem impor limite artificial de tempo de entrega.

Parar e pedir autoriza??o somente quando a pr?xima etapa exigir deploy, push, migration, altera??o de `.env`, segredo, credencial, banco, VPS ou produ??o; surgir ambiguidade de produto; alterar contrato backend/API fora do escopo; uma valida??o invalidar a premissa; houver conflito relevante no working tree; ou o usu?rio interromper, reprovar ou mudar a prioridade.

Se o usu?rio pedir explicitamente aprova??o etapa a etapa, use o modo pausado.

## Uso Opcional de Subagents

Use subagents somente quando a subissue atual tiver risco, m?ltiplas ?reas ou exigir revis?o especializada.

Subagents podem investigar padr?es, revisar impacto t?cnico, revisar seguran?a, revisar layout, propor valida??es, comparar com padr?es existentes e analisar riscos de regress?o.

N?o use subagents para mudan?as pequenas de texto, ajustes simples de CSS, corre??es ?bvias em um ?nico arquivo, tarefas de escopo totalmente claro, substituir aprova??o expl?cita, criar burocracia ou trabalhar em m?ltiplas subissues ao mesmo tempo.

Subagents n?o podem aprovar subissues, alterar status para `Aprovado`, criar novas subissues sem autoriza??o do agente principal, ampliar escopo, executar deploy, fazer push, rodar migrations destrutivas, alterar credenciais, modificar `.env`, avan?ar para a pr?xima subissue ou ignorar aprova??o humana.

## Ciclo de Execu??o

Para cada subissue, execute este ciclo:

1. Selecionar somente uma subissue.
2. Atualizar o status local para `Analisando` ou `Em progresso`.
3. Confirmar escopo da subissue e arquivos prov?veis.
4. Avaliar se a subissue precisa de subagent.
5. Se precisar, usar subagent apenas para investiga??o/revis?o especializada.
6. Implementar de forma cir?rgica.
7. Rodar valida??es relevantes.
8. Quando aplic?vel, acionar subagent revisor antes de concluir.
9. Atualizar o `.md` com status compat?vel com o momento e registro de execu??o.
10. Em modo sequencial cont?nuo, seguir diretamente para a pr?xima subissue autorizada.
11. Em modo pausado, resumir o que foi feito e perguntar: `Voc? aprova esta subissue?`
12. Em modo pausado, s? mover para `Aprovado` e continuar ap?s confirma??o.

Se o usu?rio disser `n?o` sem detalhar, pergunte o motivo antes de alterar qualquer coisa. Depois que o usu?rio explicar, reproduza ou entenda a reprova??o, corrija apenas o problema relatado, rode valida??es novamente, pe?a nova revis?o quando necess?rio e s? marque `Aprovado` ap?s novo `sim`.

## Regras de Implementa??o

- Respeitar a issue pai e a subissue atual como limite de escopo.
- N?o corrigir problemas fora da subissue sem autoriza??o.
- N?o criar abstra??es, endpoints, tabelas ou helpers sem verificar padr?es existentes.
- Para SQL, tabela, migration, endpoint, function ou integra??o, investigar nomes reais antes de alterar.
- Preferir TDD ou teste de regress?o quando a mudan?a for comportamental.
- Ao mexer com `.env`, SQL, dumps, credenciais, integra??es ou dados sens?veis, acionar revis?o de seguran?a aplic?vel antes de finalizar.
- Nunca fazer deploy, push, migration destrutiva ou altera??o de credencial sem autoriza??o expl?cita.
- No projeto ERP Jetta, respeitar branch `main` e regras locais de commit quando a tarefa exigir altera??o no reposit?rio.
- N?o usar subagents como desculpa para ampliar o escopo.
- N?o permitir que subagents executem trabalho fora da subissue atual.
- N?o aceitar sugest?o de subagent automaticamente; o agente principal deve validar se faz sentido.

## Subissue Bem Escrita

Cada subissue criada deve usar descri??o objetiva:

```markdown
---
id: ISSUE-YYYYMMDD-HHMM-01
tipo: implementa??o
status: Aberta
prioridade: Alta
parent: ISSUE-YYYYMMDD-HHMM
ordem: 1
depends_on: []
---

# T?tulo

## Objetivo

[Mudan?a ?nica e verific?vel.]

## Escopo

- [Item concreto.]
- [Item concreto.]

## Crit?rios de Aceite

- [Condi??o verific?vel.]
- [Condi??o verific?vel.]

## Valida??o Esperada

- [Teste, smoke test ou verifica??o manual.]

## Fora do Escopo

- [O que n?o deve ser feito nesta etapa.]
```

## Comunica??o com o Usu?rio

Ao iniciar, informe a issue pai recebida e caminho do `.md`, subissues criadas ou reaproveitadas, primeira subissue, uso de subagent, modo de execu??o, total da fila e marcador `Subissue 1/5`.

Ao concluir uma subissue, informe o que mudou, arquivos alterados, valida??es executadas, o que n?o foi validado, uso de subagents, status registrado no `.md`, n?mero conclu?do e pr?xima etapa.

Ao aprovar, informe que a subissue foi marcada como `Aprovado` no `.md` e pergunte se pode continuar para a pr?xima.

Ao concluir todas as subissues em modo sequencial cont?nuo, entregue resumo final com lista de subissues conclu?das, arquivos alterados, valida??es executadas, o que n?o foi validado, riscos/observa??es e commits criados quando aplic?vel.

## Regra Principal

A skill deve manter execu??o controlada, incremental e verific?vel, com obriga??o de fazer item a item at? concluir o escopo autorizado.

Subagents s?o apoio de investiga??o e revis?o, n?o substituem o agente principal, n?o substituem valida??o local e nunca autorizam a??es sens?veis. A aprova??o expl?cita do usu?rio ? obrigat?ria para iniciar o pacote ou para a??es sens?veis, mas n?o precisa ser repetida entre subissues quando o usu?rio autorizou execu??o sequencial cont?nua.
