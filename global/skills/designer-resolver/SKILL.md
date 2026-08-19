---
name: designer-resolver
description: Corrige de forma profissional os problemas encontrados pelo designer em interfaces web, com foco em layout, responsividade, hierarquia visual, consistencia de componentes, estados interativos e validacao visual por screenshots.
---

# Designer Resolver

## Skill Path Rules

- Resolve every relative path in this skill from `C:\Users\Jetta\.codex\skills\designer-resolver\`.
- Reuse the visual audit from `../designer/` when available instead of rediscovering the same problems do zero.
- Enforce `../_shared/tdd-decente.md` whenever the fix changes behavior, interaction, state transitions, rendering branches, or layout logic.
- If runtime, local URL, screenshots, or a reproducible page exist, use them as mandatory evidence before and after the fix.
- If the target screen cannot be opened or reproduced, state the blocker explicitly and avoid speculative visual fixes.

## Goal

Resolver com acabamento profissional os problemas que o `designer` identifica, sem virar remendo visual. O foco e corrigir a causa raiz de:

- layout quebrado
- spacing inconsistente
- tipografia fraca
- contraste ruim
- hierarquia visual confusa
- componentes desalinhados
- responsividade ruim
- estados interativos mal resolvidos
- overflow, clipping e elementos fora da viewport

Sempre fechar com:
- problema resolvido por superficie
- validacao visual antes/depois
- riscos remanescentes

## When To Use

Use esta skill quando o pedido soar como:
- corrigir os problemas do designer
- deixar a tela profissional
- arrumar a interface
- polir a UI
- resolver o design review
- consertar responsividade
- eliminar overflow e quebra visual
- aplicar os ajustes visuais encontrados

## Scope

Esta skill cobre:
- paginas
- dashboards
- tabelas
- formularios
- modais e drawers
- componentes isolados
- landing pages
- estados desktop, tablet e mobile
- light mode e dark mode quando relevantes

Esta skill nao cobre sozinha:
- rebranding completo
- redesign de produto sem alvo claro
- mudanca de regra de negocio sem demanda visual
- performance backend profunda sem efeito visual perceptivel

## Inputs Esperados

Aceite qualquer combinacao de:

- achados do `designer`
- screenshots
- URL local ou deployed
- arquivo/componente especifico
- pedido livre para "deixar bonito" ou "corrigir a tela"

Se houver findings existentes, transforme-os em pacote de correcao por superficie:

- `layout`
- `hierarquia`
- `componentes`
- `responsividade`
- `estados`
- `contraste`

## Core Principle

Nao basta "melhorar". A skill precisa produzir uma tela que pareca intencional, consistente e confiavel.

Regra pratica:

`se a correcao nao melhora a percepcao visual no screenshot real, ela ainda nao esta pronta`

## Mandatory Runtime Workflow

Quando houver runtime acessivel, siga obrigatoriamente:

1. abrir a pagina alvo
2. capturar baseline em `375x812`
3. capturar baseline em `768x1024`
4. capturar baseline em `1280x900`
5. identificar quebra visivel e mapear por viewport
6. corrigir a causa raiz no codigo
7. recapturar screenshots nos mesmos viewports
8. comparar antes/depois

Se houver interacao relevante, testar tambem:

- menu mobile
- modal/drawer aberto
- tabela com scroll
- estado de erro
- estado vazio
- loading state, quando praticavel

## Automatic Fix Checklist

Durante a correcao, procurar e resolver quando aplicavel:

- `overflow horizontal`
- `elementos fora da viewport`
- `grid quebrado`
- `cards desalinhados`
- `CTA principal sem destaque`
- `botoes e inputs com alturas inconsistentes`
- `texto vazando ou truncando mal`
- `tabela sem estrategia mobile`
- `modal maior que a viewport`
- `drawer cortando conteudo`
- `header/sidebar cobrindo a pagina`
- `foco invisivel`
- `hover/active/disabled sem feedback claro`
- `contraste insuficiente`
- `spacing sem escala coerente`
- `mistura de radius, sombras ou bordas sem padrao`

## Fix Strategy

Corrija nesta ordem:

1. `quebra estrutural`
   - overflow
   - clipping
   - viewport break
   - grid/flex colapsado
2. `legibilidade`
   - contraste
   - hierarquia
   - tipografia
   - line length
3. `consistencia`
   - buttons
   - inputs
   - cards
   - spacing rhythm
   - radius/shadows/icons
4. `polish interativo`
   - hover
   - focus
   - selected
   - disabled
   - loading/empty/error

## Implementation Rules

- Prefira corrigir a causa raiz no layout, container, breakpoint, token, variant ou componente base.
- Evite remendos por elemento quando o problema e sistemico.
- Nao crie novos estilos isolados se o sistema atual puder ser consolidado.
- Prefira tokens, variantes e classes reutilizaveis a overrides espalhados.
- Preserve o padrao visual existente quando ele for bom; melhore o inconsistente.
- Se a tela ja tiver design system, siga o sistema. Se nao tiver, imponha um minimo de consistencia.
- Nao use numeros magicos sem justificativa clara.
- Nao resolva responsividade escondendo conteudo sem avaliar impacto.

## TDD and Protection Rules

Siga `../_shared/tdd-decente.md` quando a correcao mexer em comportamento.

Exija teste quando houver:

- troca de branch/layout
- estado de modal, drawer ou menu
- render condicional
- loading/empty/error state
- tabs, accordions, sidebars, tables responsivas
- qualquer fix que dependa de interacao para permanecer correto

Minimo esperado:

- 1 teste de regressao para o bug visual/comportamental real quando praticavel
- 1 validacao do caminho corrigido no nivel mais proximo do uso real

Se o problema for puramente CSS estatico e sem comportamento:

- o screenshot antes/depois pode ser a evidencia principal
- ainda assim rode a validacao automatizada mais proxima que proteja a superficie alterada

## Validation Rules

Sempre validar:

- screenshots depois da correcao
- mesmos viewports do baseline
- ausencia de overflow horizontal
- ausencia de elementos cortados fora da viewport
- integridade de grid, cards, tabelas e modais
- CTA e hierarquia visual coerentes

Quando houver mudanca de comportamento, validar tambem:

- teste automatizado focado
- regressao adjacente minima
- runner padrao do projeto quando aplicavel

## Severity and Exit Bar

- `CRITICO`: tela ainda quebra, fica inutilizavel ou esconde acao/conteudo principal
- `ALTO`: problema visual relevante ainda compromete leitura, acao ou confianca
- `MEDIO`: refinamentos ainda faltam, mas a tela ja esta funcional e coerente
- `BAIXO`: pequenos ajustes de polish

A skill so deve se considerar concluida quando:

- os problemas principais do `designer` estiverem resolvidos ou claramente reduzidos
- os screenshots depois da correcao sustentarem a melhoria
- qualquer risco restante estiver documentado

## Output

Use esta estrutura:

1. `Alvo corrigido`
2. `Problemas tratados`
3. `Arquivos alterados`
4. `Validacao visual`
5. `Validacao automatizada`
6. `Resultado final`
7. `Riscos remanescentes`

## Fix Report Format

`[surface] Problema` -> Causa raiz -> Correcao aplicada -> Evidencia de validacao

## Output Rules

- Seja direto.
- Foque no que foi resolvido de verdade.
- Cite viewports testados.
- Se um problema persistir, diga exatamente onde e por que.
- Nao declare polish completo sem screenshot comparativo ou evidencia equivalente.
- Se a correcao depender de tradeoff visual, registre o tradeoff.

## Ready Prompt

Quando usar esta skill, siga este enquadramento:

`Use a skill designer-resolver para corrigir os problemas visuais de [alvo]. Reproduza com runtime se possivel, capture screenshots em 375, 768 e 1280, elimine overflow horizontal, elementos fora da viewport, grid quebrado e inconsistencias de hierarquia/componentes, depois valide o antes/depois e proteja com testes quando a correcao alterar comportamento.`
