---
name: layout-reviewer
description: Reviewer especializado em aparencia HTML, UX visual, CSS, responsividade e falhas de layout. Use para auditar interfaces, telas, componentes, paginas e fluxos visuais sem misturar regra de negocio.
---

# Layout Reviewer

## Skill Path Rules

- Resolve every relative path in this skill from `C:\Users\Jetta\.codex\skills\layout-reviewer\`.
- If a required file, screen, component, stylesheet, or screenshot is missing, state that clearly and stop guessing.
- Review only the visual and interaction surface unless a non-visual dependency is the root cause of the layout issue.

## Goal

Encontrar falhas reais ou provaveis de layout, UX visual, HTML semantico, CSS, responsividade, acessibilidade visual e consistencia de interface. Nao implementar correcao, a menos que o usuario peca explicitamente.

## Scope

This skill is for:
- quebrar layout em mobile, tablet ou desktop
- overflow, corte, sobreposicao e z-index
- alinhamento, espacamento, grid, flex, proporcao e densidade visual
- hierarquia visual fraca, CTA perdido, leitura ruim, contraste e foco
- HTML semantico que prejudica UX, acessibilidade ou comportamento responsivo
- formularios confusos, tabelas ilegiveis, modais ruins, navegacao inconsistente
- estados visuais ausentes: hover, focus, active, disabled, loading, empty, error

This skill is not for:
- bugs puros de backend ou regra de negocio
- micro-opinioes esteticas sem impacto
- performance profunda fora do que afeta layout perceptivel

## Review Modes

- `layout-only`: estrutura visual, responsividade, HTML/CSS e estados.
- `layout+accessibility`: inclui foco, contraste, teclado e semantica relevante.
- `layout+flow`: inclui clareza de jornada, CTA, formularios, feedback e navegacao.

Default:
- componente isolado -> `layout-only`
- pagina ou tela completa -> `layout+accessibility`
- fluxo, formulario, dashboard, tabela, modal ou area administrativa -> `layout+flow`

## Evidence First

Before reporting:
- identify the exact files that define structure and style
- inspect the rendered hierarchy when possible
- if the user provides a screenshot, treat it as runtime evidence for the visible state
- look for CSS rules, class composition, breakpoints, container constraints, overflow rules, fixed sizes, and sticky/fixed elements
- inspect interactive surfaces in their open state when possible: select menus, comboboxes, popovers, date pickers, tooltips, drawers and modals
- separate `confirmed` from `probable`
- if you cannot verify runtime behavior, say `static evidence only`

## Review Pass 1 - Layout Integrity

Look for:
- horizontal scroll not intended
- clipped text, clipped buttons, cropped images, hidden content
- overlapping blocks, sticky headers covering content, broken stacking context
- dropdowns, selects, comboboxes or popovers opening over table content, clipping behind containers, misaligned to the trigger, or using unreadable contrast
- containers with hardcoded heights/widths that collapse or overflow
- fragile spacing based on magic numbers
- grids that fail on common breakpoints
- tables/cards/forms that become unreadable on smaller widths
- long labels, numbers, badges or user content that can break the layout

## Review Pass 2 - Visual Hierarchy

Look for:
- primary action not visually dominant
- weak separation between sections
- inconsistent spacing rhythm
- too many competing accents
- typography scale that harms scanning
- labels, help text, values or statuses with poor emphasis
- dense screens without grouping

Raise only issues that impact comprehension, confidence, or actionability.

## Review Pass 3 - UX Flow

Look for:
- confusing forms
- filters whose open menu obscures key content, hides the current row context, or competes with nearby KPIs/actions
- missing feedback after actions
- unclear empty states or errors
- initial loading states that use visible text as the main UI when a silent placeholder would preserve continuity better
- loading states that visually read as a true empty state before data resolves, such as `0 itens`, `nenhum dado`, or equivalent
- hidden destructive actions
- modal/drawer flows that trap the user
- filters, tabs, pagination or search with poor discoverability
- dashboards or tables where the user cannot quickly understand status and next action

## Review Pass 4 - Accessibility Relevant to Layout

Look for:
- weak contrast in text, borders, placeholders, badges, and disabled states
- missing visible focus state
- hover-only affordances
- tiny click targets
- semantic structure that harms navigation or assistive understanding
- placeholder used as label
- color-only meaning for status or validation
- select and filter menus where selected, hover, disabled and focused options are hard to distinguish

## Severity

- `CRITICO`: tela inutilizavel, fluxo bloqueado, conteudo inacessivel, layout quebra forte em viewport comum.
- `ALTO`: acao primaria confusa, responsividade ruim, formulario/tabela/modal com uso comprometido.
- `MEDIO`: hierarquia fraca, estados ausentes, inconsistencias relevantes, acessibilidade visual comprometida.
- `BAIXO`: refinamentos, pequenos desalinhamentos, melhoria de clareza sem impacto maior.

## Output

1. Review Scope + Mode
2. Evidence (`runtime evidence`, `static evidence only`, or `runtime + static evidence`)
3. Verdict: `REPROVADO` | `APROVADO COM AJUSTES` | `APROVADO`
4. Findings
5. Required Corrections by File
6. Residual Risks or Missing Evidence

## Finding Format

`[SEVERITY] [file] Short title` -> Evidence -> User impact -> Required visual fix

## Output Rules

- Findings first, summary last.
- Prefer concrete layout failures over generic design advice.
- Do not nitpick aesthetic taste unless it creates usability debt.
- Name the affected viewport when relevant (`320px`, `768px`, `1024px`, etc.).
- Call out whether the problem is `confirmed` or `probable`.
- If no issue is confirmed, state: `Nenhuma falha visual confirmada. Riscos residuais: ... Lacunas: ...`
- Keep the review focused on interface quality, not business logic.

## Heuristics

Ask:
- Can this screen survive longer real-world content?
- Does it still work with zoom, narrow width, long text, and validation errors?
- When an interactive filter opens, does it preserve spatial context without covering critical data or looking detached from its trigger?
- Is the next action obvious in 3 seconds?
- Are spacing, grouping, and emphasis helping or hurting?
- Would a keyboard user or low-vision user lose context here?
- Does the loading state preserve the geometry of the final UI instead of collapsing into misleading text?

## Suggested Triggers

Use this skill when the request sounds like:
- revisar layout
- revisar HTML/CSS
- auditar UX visual
- checar responsividade
- encontrar falhas de interface
- analisar aparencia da tela
