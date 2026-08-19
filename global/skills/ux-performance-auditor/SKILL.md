---
name: ux-performance-auditor
description: Audita paginas, fluxos, componentes ou pedidos livres com foco em experiencia percebida pelo usuario, travamentos, fluidez, responsividade, gargalos e nota final de 0 a 10.
---

# UX Performance Auditor

## Skill Path Rules

- Resolve every relative path in this skill from `C:\Users\Jetta\.codex\skills\ux-performance-auditor\`.
- Se o usuario citar uma pagina, fluxo, componente, screenshot, video, URL local ou arquivo especifico, use esse material como evidencia principal.
- Se faltar alvo claro para a auditoria, pare e peca o alvo exato em vez de inventar escopo.
- Nao chute comportamento de runtime quando voce so tiver codigo estatico. Declare isso como `evidencia estatica`.

## Goal

Analisar qualquer tela, pagina, fluxo, funcionalidade ou pedido livre sob a otica de:
- velocidade percebida
- travamentos e engasgos
- responsividade de interacao
- custo cognitivo para o usuario
- gargalos tecnicos que afetam a experiencia
- estabilidade visivel e consistencia de uso

Sempre terminar com:
- diagnostico objetivo
- principais gargalos
- impacto para o usuario
- prioridade de correcao
- nota final de `0` a `10`

## When To Use

Use esta skill quando o pedido soar como:
- analisar pagina
- revisar travamentos
- checar lentidao
- ver gargalos de UX
- medir fluidez
- entender por que a tela esta pesada
- dar uma nota para experiencia
- auditar performance percebida pelo usuario

Tambem serve quando o usuario disser apenas:
- `analisa isso`
- `ve se esta bom`
- `essa tela trava`
- `essa pagina esta lenta`

## Scope

Esta skill cobre:
- paginas completas
- dashboards
- tabelas pesadas
- formularios
- modais
- fluxos multi-step
- listas com filtros
- paginas mobile ou desktop
- componentes isolados com problema perceptivel
- pedidos mais abertos sobre experiencia e desempenho

Esta skill nao cobre sozinha:
- tuning profundo de banco sem relacao com UX percebida
- benchmarking cientifico de infra sem superficie de usuario
- review puramente estetico sem impacto de uso

## Core Principle

O foco nao e performance abstrata. O foco e:

`o usuario sente atraso, travamento, confusao ou friccao?`

Se sim, trate isso como problema mesmo quando o codigo pareca tecnicamente aceitavel.

## Evidence Modes

Declare um destes modos no inicio da auditoria:

- `runtime evidence`: quando houver execucao real, screenshot, video, teste manual, log de runtime, DevTools, Lighthouse ou observacao concreta.
- `static evidence only`: quando houver apenas leitura de codigo, HTML, CSS, JS, TS, configuracao ou estrutura de componentes.
- `runtime + static evidence`: quando houver os dois.

## Review Axes

Avalie sempre os eixos abaixo.

### 1. Performance Percebida

Olhe para:
- tempo para primeira resposta visivel
- tela vazia, loading longo ou loading sem feedback
- excesso de skeleton sem progresso real
- atraso entre clique e reacao
- payloads grandes
- queries/fetches redundantes
- renderizacao excessiva

### 2. Fluidez e Travamentos

Olhe para:
- congelamento ao digitar
- scroll engasgando
- tabela travando ao filtrar
- modal abrindo com atraso
- input com debounce ruim ou sem debounce
- recalculo pesado no client
- efeitos que disparam em cascata
- loops, mapas, filtros ou sorts caros em toda renderizacao

### 3. Responsividade de Interacao

Olhe para:
- clique sem feedback imediato
- botao que parece nao responder
- estados `loading`, `disabled`, `success` e `error` ausentes ou ruins
- acao que bloqueia a tela inteira sem necessidade
- transicao que mascara lentidao em vez de orientar o usuario

### 4. Clareza e Custo Cognitivo

Olhe para:
- usuario precisa pensar demais para completar a tarefa
- excesso de informacao ao mesmo tempo
- hierarquia fraca
- fluxo com etapas desnecessarias
- filtros ou opcoes que confundem
- feedback de erro ruim ou sem proximo passo

### 5. Estabilidade Perceptivel

Olhe para:
- layout shift
- conteudo pulando
- dados aparecendo e sumindo sem contexto
- componentes que remontam sem necessidade
- perda de foco ao atualizar
- selecao sumindo
- estado reiniciando apos interacao

## Passo a Passo da Auditoria

1. Identifique o alvo exato.
2. Descubra os arquivos principais que definem estrutura, dados, fetch, renderizacao e estilos.
3. Procure evidencias de gargalo real ou altamente provavel.
4. Separe problemas por impacto no usuario, nao por tecnologia.
5. Classifique cada problema como `confirmado` ou `provavel`.
6. Diga o que mais pesa na experiencia.
7. Calcule a nota final de `0` a `10`.

## Heuristics

Pergunte sempre:
- o usuario recebe resposta visual rapida apos interagir?
- existe alguma parte que parece travada ou pesada?
- a tela piora com listas grandes, filtros, busca ou muito conteudo?
- existe trabalho demais no client para algo simples?
- o fluxo ajuda o usuario a terminar rapido ou cria atrito?
- o problema aparece no caminho principal ou so em caso de borda?
- a lentidao e objetiva ou e sensacao causada por falta de feedback?

## Common Technical Smells

Sinais que devem ser tratados como risco relevante:
- fetch duplicado
- polling desnecessario
- N+1 no backend refletindo em atraso da tela
- filtros, sort ou agregacoes pesadas no browser
- listas sem paginacao ou virtualizacao quando necessario
- `useEffect` disparando cascatas
- estado demais no componente raiz
- rerender amplo por props instaveis ou arquitetura mal dividida
- componentes pesados montados antes da hora
- imagens grandes, scripts grandes, tabelas grandes, logs demais
- loading global bloqueando acao local

## Severity

- `CRITICO`: a tela trava, bloqueia uso, perde dados, falha no fluxo principal ou fica impraticavel em uso normal.
- `ALTO`: lentidao perceptivel forte, atraso frequente, filtros/tabelas/formularios ruins, experiencia compromete conversao ou operacao.
- `MEDIO`: friccao clara, peso desnecessario, feedback ruim, gargalo relevante mas contornavel.
- `BAIXO`: refinamentos, microatrasos, pequenos ajustes de clareza ou fluidez.

## Scoring

A nota final deve ser um numero com uma casa decimal, de `0.0` a `10.0`.

Base de interpretacao:
- `9.0 a 10.0`: experiencia muito boa, sem gargalos relevantes.
- `7.5 a 8.9`: boa, com ajustes importantes mas nao bloqueantes.
- `6.0 a 7.4`: aceitavel, mas o usuario sente friccao clara.
- `4.0 a 5.9`: ruim, gargalos perceptiveis frequentes.
- `0.0 a 3.9`: experiencia critica ou quase inutilizavel.

Calcule usando estes pesos:
- `30%` performance percebida
- `25%` fluidez e travamentos
- `20%` responsividade de interacao
- `15%` clareza e custo cognitivo
- `10%` estabilidade perceptivel

Se faltar evidencia de runtime:
- reduza a confianca da nota
- explique que a nota e preliminar
- nunca finja precisao maior do que a evidencia permite

## Output

Use esta estrutura:

1. `Alvo auditado`
2. `Modo de evidencia`
3. `Veredito`
4. `Nota final`
5. `Principais achados`
6. `Impacto para o usuario`
7. `Acoes prioritarias`
8. `Riscos residuais ou lacunas`

## Finding Format

`[SEVERITY] [confirmado|provavel] [arquivo ou area] Titulo curto` -> Evidencia -> Impacto no usuario -> Acao recomendada

## Verdict

Use um destes:
- `APROVADO`
- `APROVADO COM AJUSTES`
- `REPROVADO`

## Output Rules

- Foque primeiro no que piora a vida do usuario.
- Nao transforme a analise em aula teorica.
- Nao encha a resposta de micro-otimizacao sem impacto real.
- Se houver poucos problemas, diga isso com clareza.
- Se nao houver evidencia suficiente, diga exatamente o que faltou.
- Sempre explique por que a nota nao e maior.
- Se a tela estiver boa, diga o que sustenta a nota.

## Ready Prompt

Quando usar esta skill, siga este enquadramento:

`Audite [alvo] com foco em experiencia do usuario, gargalos perceptiveis, travamentos, fluidez, responsividade e clareza. Separe achados confirmados de provaveis, priorize impacto real no usuario e finalize com uma nota de 0 a 10 com justificativa curta.`
