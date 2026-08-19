---
name: designer
description: Revisa qualidade visual de paginas, fluxos e componentes web com foco em layout, espacamento, tipografia, contraste, hierarquia, consistencia e responsividade. Nao e auditoria de UX ou regra de negocio.
---

# Designer

## Skill Path Rules

- Resolve every relative path in this skill from `C:\Users\Jetta\.codex\skills\designer\`.
- Se o usuario fornecer screenshot, video, URL, pagina local, componente ou arquivo especifico, use isso como evidencia principal.
- Se nao houver alvo claro, peca o alvo exato antes de revisar.
- Se houver ambiente executavel, browser ou Playwright disponivel, use screenshot apenas quando a evidencia visual real for necessaria para decidir a qualidade da entrega ou quando o usuario pedir validacao visual.
- Aceite review sem screenshot quando a avaliacao por codigo/teste for suficiente para o risco da mudanca; nesse caso declare `static evidence only`.
- Se so existir codigo estatico, declare isso como `evidencia estatica` e nao finja comportamento de runtime.
- Revise aparencia, consistencia visual, estados de interface e responsividade. Nao misture com regra de negocio, performance profunda ou fluxo funcional, a menos que isso afete diretamente o visual.

## Goal

Determinar se a interface parece profissional, consistente e polida ou se ainda transmite aspecto improvisado. O foco e detectar problemas visuais reais e apontar as correcoes com maior impacto perceptivel.

Sempre terminar com:
- impressao geral da interface
- achados priorizados por severidade
- o que esta visualmente bom e deve ser preservado
- top 3 correcoes com maior impacto

## When To Use

Use esta skill quando o pedido soar como:
- revisar design
- revisar visual
- checar layout
- ver se esta polido
- isso esta bonito?
- faz um design review
- auditar interface
- algo esta estranho na tela
- make it look better

## Scope

Esta skill cobre:
- paginas completas
- dashboards
- telas administrativas
- componentes isolados
- formularios
- modais
- tabelas
- landing pages
- estados desktop, tablet e mobile
- estados light e dark quando existirem

Esta skill nao cobre sozinha:
- auditoria de UX de fluxo completo
- review de regra de negocio
- performance tecnica sem sintoma visual
- code review geral de arquitetura

## Core Principle

A pergunta central e:

`uma pessoa exigente com design olharia essa interface e acharia que ela foi bem acabada?`

Se a resposta for nao, a revisao precisa explicar exatamente onde a percepcao de baixa qualidade aparece.

## Evidence Modes

Declare um destes modos no inicio:

- `runtime evidence`: quando houver execucao real, screenshot, video, browser, ambiente local ou observacao concreta.
- `static evidence only`: quando houver apenas leitura de codigo, HTML, CSS, TSX, estilos e estrutura.
- `runtime + static evidence`: quando houver os dois.

## Runtime Capture Policy

Quando runtime for necessario:

- capturar screenshot antes de fechar a analise visual
- preferir Playwright direto para evidenciar o estado real
- testar no minimo os viewports `375`, `768` e `1280`
- registrar em quais viewports o problema aparece
- se houver dark mode relevante, capturar ao menos o modo em que a falha aparece

Quando runtime nao for usado:

- declarar `static evidence only`
- dizer por que o screenshot nao foi necessario ou nao foi gerado
- reduzir a confianca dos achados visuais dependentes de render real

## Playwright Default Flow

Quando houver URL local, ambiente web rodando ou pagina navegavel, siga este fluxo padrao:

1. abrir a pagina alvo
2. capturar screenshot em `375x812`
3. capturar screenshot em `768x1024`
4. capturar screenshot em `1280x900`
5. inspecionar estados visiveis e variacoes relevantes
6. registrar quebra por viewport quando existir

Se a tela depender de interacao para revelar o problema, abrir tambem:

- menu mobile
- modal ou drawer
- tabela com scroll
- estado de erro, vazio ou loading quando praticavel

## Automatic Detection Checks

Durante runtime review, verificar automaticamente:

- `overflow horizontal`
- `elementos fora do viewport`
- `grid quebrado`
- `cards ou tabelas espremidos alem do limite legivel`
- `botoes ou CTAs cortados`
- `texto vazando ou truncando sem tratamento`
- `modais/drawers maiores que a viewport`
- `headers, sidebars ou footers cobrindo conteudo`

Se qualquer um ocorrer, trate como finding confirmado quando a evidencia visual existir.

## Review Axes

Avalie sempre os eixos abaixo.

### 1. Layout and Spacing

Olhe para:
- consistencia de gaps e paddings
- alinhamento horizontal e vertical
- respiro entre blocos
- disciplina de grid e colunas
- proporcao entre sidebar, conteudo e areas auxiliares
- ritmo vertical coerente
- espacos acidentais ou apertos visuais

Sinais comuns de problema:
- cards com gaps diferentes entre si
- headings, textos e blocos iniciando em colunas diferentes
- botoes colados em inputs
- secoes com padding aleatorio
- layout que funciona em desktop e quebra em tablet

### 2. Typography

Olhe para:
- hierarquia clara entre titulo, subtitulo, label e corpo
- line-height adequado
- comprimento de linha legivel
- escala de tamanhos consistente
- pesos tipograficos com intencao
- truncamento e overflow de texto

Sinais comuns de problema:
- tudo parece ter o mesmo peso visual
- texto longo ocupa largura demais
- tamanhos parecem escolhidos no improviso
- labels, valores e status nao se diferenciam

### 3. Colour and Contrast

Olhe para:
- contraste suficiente para leitura
- consistencia semantica das cores
- uso controlado de cor de destaque
- estados de erro, aviso, sucesso e selecao
- comportamento em dark mode e light mode

Sinais comuns de problema:
- cinza claro demais em fundo claro
- mesma cor com significados diferentes
- excesso de cores competindo
- bordas invisiveis ou texto apagado em dark mode

### 4. Visual Hierarchy

Olhe para:
- CTA principal evidente
- agrupamento visual de informacoes relacionadas
- destaque do que importa primeiro
- distribuicao de peso visual
- uso intencional de espaco negativo

Sinais comuns de problema:
- varias acoes com o mesmo peso
- nada chama a atencao no teste de "squint"
- detalhes disputam com a informacao principal
- tela densa sem agrupamento

### 5. Component Consistency

Olhe para:
- estilos de botoes
- inputs
- cards
- sombras
- bordas
- border-radius
- icones
- badges
- tabelas
- modais

Sinais comuns de problema:
- cada area usa um botao diferente
- campos com alturas diferentes
- mistura de familias de icones
- sombras e raios sem padrao

### 6. Interaction States

Olhe para:
- hover
- focus
- active
- selected
- disabled
- loading
- empty
- error

Sinais comuns de problema:
- elemento clicavel sem feedback
- foco invisivel
- item ativo com a mesma cara do inativo
- loading que causa layout shift
- disabled que ainda parece clicavel

### 7. Responsive Quality

Olhe para:
- navegacao mobile
- tablet em `768px`
- touch targets
- tabelas em largura estreita
- imagens e midia responsivas
- modais e drawers em viewport menor
- densidade de informacao em telas medias

Sinais comuns de problema:
- menu desktop espremido no mobile
- tabela maior que a tela sem estrategia
- alvos pequenos demais para toque
- layout aceitavel no desktop e ruim no tablet
- overflow horizontal em `375px`
- componente saindo da viewport em `768px`
- grid colapsando ou quebrando alinhamento em `1280px`

## Severity

- `ALTO`: parece quebrado, amador ou compromete a leitura/acao principal.
- `MEDIO`: nao quebra a tela, mas deixa a interface com cara de inacabada ou inconsistente.
- `BAIXO`: refinamento visual de menor impacto.

## Review Heuristics

Pergunte sempre:
- a acao principal fica obvia em 3 segundos?
- existe uma escala clara de espacamento e tipografia?
- a tela aguenta texto maior, dados maiores e estados vazios?
- dark mode e light mode continuam legiveis?
- os componentes parecem pertencer ao mesmo sistema?
- tablet foi tratado de verdade ou ignorado?
- a interface passa confianca visual?

## Output

Use esta estrutura:

1. `Alvo revisado`
2. `Modo de evidencia`
3. `Capturas e viewports testados`
4. `Impressao geral`
5. `Achados`
6. `O que esta bom`
7. `Top 3 correcoes`
8. `Lacunas de evidencia`

## Finding Format

`[SEVERITY] [confirmado|provavel] [arquivo, tela ou componente] Titulo curto` -> Evidencia -> Impacto visual -> Correcao recomendada

## Output Rules

- Priorize achados relevantes, nao micro-nitpicks.
- Findings primeiro, resumo depois.
- Diferencie `confirmado` de `provavel`.
- Cite viewport quando isso mudar o problema (`375px`, `768px`, `1280px`).
- Se houver screenshot ou browser, use isso como ancora da evidencia.
- Quando houver runtime, liste explicitamente os viewports testados e quais screenshots foram gerados.
- Se estiver tudo razoavelmente bom, diga explicitamente o que sustenta essa avaliacao.
- Se faltarem modos ou telas importantes, declare a lacuna.

## Ready Prompt

Quando usar esta skill, siga este enquadramento:

`Faça um design review de [alvo] com foco em layout, espacamento, tipografia, contraste, hierarquia visual, consistencia de componentes, estados interativos e responsividade. Se houver runtime, use Playwright, teste 375, 768 e 1280, gere screenshots e detecte overflow horizontal, elementos fora da viewport e grid quebrado. Separe achados confirmados de provaveis, priorize impacto perceptivel e termine com o que esta bom e as 3 correcoes mais importantes.`
