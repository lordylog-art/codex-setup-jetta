---
name: linear-subissue-architect
description: Quebrar uma issue m?e local em Markdown em subissues menores, seguras, test?veis e implement?veis uma por vez; criar tarefas filhas como arquivos `.md` em `.requirements/issues`; organizar bug, projeto ou an?lise grande em etapas; separar investiga??o de implementa??o; definir crit?rios de aceite; ou planejar trabalho envolvendo deploy, produ??o, banco de dados, integra??es externas, autentica??o, sincroniza??o, Google Sheets, GreenMile, SAC, programa??o di?ria, ocorr?ncias, permiss?es, dados sens?veis ou fluxo operacional cr?tico.
---

# Subissue Architect Local

## Objetivo

Criar subissues filhas de uma issue m?e local em Markdown de forma controlada, t?cnica e segura, transformando um problema grande em unidades pequenas de investiga??o, implementa??o, valida??o e hardening.

N?o use conectores externos ou APIs de issue tracker. Trate os arquivos `.md` em `.requirements/issues` como se fossem o quadro de issues.

Evitar:

1. Criar subissues demais sem evid?ncia.
2. Misturar investiga??o com implementa??o.
3. Permitir que uma subissue altere escopo demais e gere regress?o.

Use esta skill antes de implementar qualquer mudan?a relevante que precise nascer de uma issue m?e.

## Armazenamento Local

A issue m?e deve existir ou ser criada como `.md` em:

```text
.requirements/issues/
```

Criar subissues dentro de uma pasta com o mesmo ID/slug da issue m?e:

```text
.requirements/issues/ISSUE-YYYYMMDD-HHMM-slug/
  01-investigar-causa.md
  02-criar-teste-regressao.md
  03-corrigir-fluxo.md
```

Cada subissue deve ter frontmatter pr?prio:

```yaml
---
id: ISSUE-YYYYMMDD-HHMM-01
tipo: investiga??o | implementa??o | teste | valida??o | seguran?a | rollback
status: Aberta
prioridade: Alta | M?dia | Baixa
parent: ISSUE-YYYYMMDD-HHMM
ordem: 1
depends_on: []
---
```

## Regras de Topo

Nunca criar subissues diretamente a partir de brainstorming. Primeiro transformar a ideia em issue m?e clara.

Antes de propor ou criar subissues, classificar cada item como:

1. Evidenciado pelo c?digo, log ou arquivo.
2. Hip?tese prov?vel.
3. Risco futuro ou melhoria.

Criar subissues apenas para os grupos 1 e 2. O grupo 3 deve ir para "backlog futuro" e n?o virar subissue agora.

N?o limitar artificialmente a quantidade de subissues. Criar a quantidade suficiente para implementar tudo com seguran?a, desde que cada subissue tenha objetivo ?nico, evid?ncia ou hip?tese prov?vel, crit?rios de aceite claros e reduza risco real.

Toda subissue precisa responder claramente:

- O que ser? feito?
- Por que isso existe?
- Como saberemos que terminou?
- Qual teste/smoke test valida?
- O que n?o pode ser alterado?
- Qual risco de regress?o?

## Fluxo Obrigat?rio

### Fase 1 - Entender a issue m?e

Antes de criar subissues, ler a issue m?e local e extrair problema real, impacto operacional, comportamento atual, comportamento esperado, ?reas afetadas, arquivos prov?veis, riscos t?cnicos, riscos operacionais, depend?ncias externas e a??es perigosas que n?o devem ser feitas sem autoriza??o.

Se faltar contexto, n?o inventar. Marcar como "n?o validado".

### Fase 2 - Classificar possibilidades

Criar uma tabela com estas colunas:

| Item | Tipo | Evid?ncia | Risco | Prioridade | Deve virar subissue? |
|---|---|---|---|---|---|

Tipos permitidos: Causa prov?vel, Valida??o obrigat?ria, Implementa??o principal, Teste obrigat?rio, Seguran?a / segredo, Rollback / recupera??o, Observabilidade / logs, Melhoria futura e Fora de escopo.

Regras:

- "Causa prov?vel" pode virar subissue.
- "Valida??o obrigat?ria" quase sempre vira subissue de investiga??o.
- "Implementa??o principal" pode virar subissue se houver evid?ncia suficiente.
- "Melhoria futura" n?o vira subissue agora, a menos que o usu?rio pe?a.
- "Fora de escopo" nunca vira subissue.

### Fase 3 - Criar subissues pequenas

Cada subissue deve ter exatamente um objetivo principal.

N?o misturar investiga??o + implementa??o, backend + frontend salvo se forem insepar?veis, altera??o de regra + altera??o visual, refatora??o + bugfix, deploy + migration, ou melhoria opcional + corre??o cr?tica.

Formato obrigat?rio de cada subissue:

```md
# T?tulo

## Objetivo
Explique em 1 ou 2 frases o que ser? feito.

## Contexto
Explique por que isso existe e como se conecta ? issue m?e.

## Escopo permitido
- Item permitido 1
- Item permitido 2

## Fora de escopo
- O que n?o deve ser alterado
- O que n?o deve ser implementado agora

## Arquivos/?reas prov?veis
- caminho/arquivo prov?vel
- m?dulo prov?vel

## Crit?rios de aceite
- Crit?rio verific?vel que mostra como saberemos que terminou
- Resultado esperado no fluxo real
- Condi??o objetiva de conclus?o

## Testes obrigat?rios
- Teste unit?rio/integrado/manual/smoke esperado
- Caso de regress?o que deve ser coberto

## Riscos e cuidados
- Risco de regress?o principal
- Cuidados para n?o quebrar fluxo existente

## Depend?ncias
- Depende de ISSUE-...-01, se existir
- Bloqueia ISSUE-...-03, se existir

## Pol?tica de execu??o
- N?o fazer push sem revis?o, se aplic?vel
- N?o executar em produ??o, se aplic?vel
- N?o alterar segredos, se aplic?vel
```

## Ordem Recomendada

Ordenar subissues assim:

1. Investiga??o sem altera??o de c?digo.
2. Teste de regress?o que reproduz o problema.
3. Corre??o m?nima.
4. Valida??o/smoke test.
5. Observabilidade/logs.
6. Rollback/recupera??o.
7. Hardening futuro.

Para deploy ou produ??o, ordenar por mapeamento do fluxo atual, identifica??o de risco, prote??o contra falha, mudan?a m?nima, health check, rollback, valida??o em ambiente seguro e melhorias opcionais.

## Pol?tica para A??es Sens?veis

Nunca criar subissue que mande executar automaticamente deploy em produ??o, migration destrutiva, altera??o de `.env`, remo??o de dados, altera??o de credenciais, troca de proxy/dom?nio, altera??o em servi?o ativo, push direto para branch principal, restart de produ??o ou rollback autom?tico sem plano.

Nesses casos, a subissue deve dizer:

```md
A??o sens?vel. Criar diff/plano primeiro e aguardar autoriza??o expl?cita antes de executar.
```

## Preview Antes de Criar

Antes de criar os arquivos `.md`, mostrar um preview:

```md
Vou criar as seguintes subissues filhas de ISSUE-YYYYMMDD-HHMM:

| Ordem | T?tulo | Tipo | Prioridade | Por que existe | Depende de |
|---|---|---|---|---|---|
| 1 | Investigar ... | Investiga??o | Alta | Evita implementa??o no escuro | - |
| 2 | Criar teste de regress?o ... | Teste | Alta | Garante que o bug seja reproduzido | 1 |
| 3 | Corrigir ... | Implementa??o | Alta | Aplica corre??o m?nima | 1, 2 |

N?o vou criar agora:

- Item X: melhoria futura, sem evid?ncia suficiente.
- Item Y: overengineering para o problema atual.
```

S? criar os `.md` depois de confirma??o do usu?rio quando houver risco operacional, cria??o em massa ou escopo ainda sens?vel.

## Prompt Padr?o

Usar este prompt quando o usu?rio pedir subissues:

```md
Voc? ? um arquiteto de subissues locais em Markdown.

Analise a issue m?e abaixo e crie subissues pequenas, seguras e implement?veis uma por vez.

Regras obrigat?rias:
- Primeiro separe evid?ncias, hip?teses prov?veis, possibilidades sem evid?ncia e melhorias futuras.
- N?o crie subissue para melhoria futura sem necessidade real.
- Separe investiga??o de implementa??o.
- Cada subissue deve ter um ?nico objetivo.
- Cada subissue deve conter escopo permitido, fora de escopo, crit?rios de aceite, testes obrigat?rios, riscos e depend?ncias.
- Para a??es sens?veis, n?o permita execu??o autom?tica sem autoriza??o expl?cita.
- Ordene as subissues por depend?ncia.
- Mostre primeiro um preview antes de criar os arquivos `.md`.

Issue m?e:
[COLE A ISSUE AQUI]
```

## Checklist Final

Confirmar:

- [ ] Existe pelo menos uma subissue de investiga??o quando h? incerteza.
- [ ] Nenhuma subissue mistura investiga??o com implementa??o.
- [ ] Nenhuma subissue depende de chute sem marcar como investiga??o.
- [ ] Toda subissue tem crit?rio de aceite verific?vel.
- [ ] Toda subissue tem "fora de escopo".
- [ ] Toda subissue cr?tica tem teste ou smoke test.
- [ ] A ordem respeita depend?ncias.
- [ ] Melhorias futuras foram separadas do escopo imediato.
- [ ] A??es sens?veis exigem autoriza??o expl?cita.
- [ ] O usu?rio consegue implementar uma subissue por vez sem perder o contexto.

## Sa?da Esperada

A resposta final deve conter diagn?stico resumido da issue m?e, tabela de classifica??o, lista ordenada de subissues propostas, caminhos dos `.md` criados ou atualizados, itens n?o criados agora e o motivo, e pergunta objetiva pedindo confirma??o quando aplic?vel.

Nunca responder apenas com uma lista solta de t?tulos.
