# Padrão Visual: Tabelas Operacionais Por Status

## Índice

- Direção visual
- Tokens de cor
- HTML recomendado
- CSS completo
- Animações
- Estados
- Responsividade
- Acessibilidade

## Direção Visual

Usar aparência operacional:

- informação densa, sem parecer poluída;
- blocos em ordem fixa de prioridade operacional;
- blocos vazios visíveis, recolhidos e sem tabela renderizada;
- blocos finais/concluídos embaixo, recolhidos por padrão;
- header de bloco forte, compacto e clicável;
- botão de recolher/expandir apenas com SVG laranja, sem fundo ou forma atrás;
- tooltip no header e no botão dizendo a ação;
- rolagem horizontal dentro do corpo de cada bloco para a tabela não cortar;
- badge sempre textual para não depender só de cor;
- animação discreta para entrada e atualização.

Evitar:

- cards dentro de cards;
- botões grandes de texto para expandir/recolher;
- ícone com círculo/fundo atrás;
- esconder bloco vazio e quebrar a hierarquia;
- tabela larga sem barra de rolagem;
- hero visual, gradientes grandes, sombras pesadas.

## Tokens De Cor

```css
:root {
  --status-bg: #f6f8fb;
  --status-surface: #ffffff;
  --status-surface-soft: #f9fbfd;
  --status-border: #d8e0ea;
  --status-border-strong: #b9c6d6;
  --status-text: #172033;
  --status-muted: #64748b;
  --status-heading: #0f2747;

  --status-blue: #1d4ed8;
  --status-blue-soft: #dbeafe;
  --status-blue-border: #93c5fd;

  --status-green: #047857;
  --status-green-soft: #d1fae5;
  --status-green-border: #6ee7b7;

  --status-orange: #f97316;
  --status-orange-hover: #ea580c;
  --status-orange-soft: #fff7ed;
  --status-orange-border: #fdba74;

  --status-red: #b91c1c;
  --status-red-soft: #fee2e2;
  --status-red-border: #fca5a5;

  --status-gray: #475569;
  --status-gray-soft: #e2e8f0;
  --status-gray-border: #cbd5e1;

  --status-focus: #2563eb;
  --status-row-hover: #f1f5f9;
  --status-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
}
```

## HTML Recomendado

```html
<section class="status-block-shell" aria-label="Tabelas operacionais por status">
  <section class="status-block status-block--critical is-collapsed">
    <header class="status-block__header" title="Mostrar bloco Atrasadas">
      <div class="status-block__copy">
        <span class="status-block__eyebrow">0 registros</span>
        <h2 id="status-block-delayed-title" class="status-block__title">Atrasadas</h2>
      </div>

      <button
        class="status-block__toggle"
        type="button"
        aria-expanded="false"
        aria-controls="status-block-delayed"
        aria-label="Mostrar bloco Atrasadas"
        title="Mostrar bloco Atrasadas"
      >
        <svg
          class="status-block__toggle-icon"
          viewBox="0 0 16 16"
          fill="currentColor"
          aria-hidden="true"
          focusable="false"
        >
          <path
            fill-rule="evenodd"
            d="M1 8a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13A.5.5 0 0 1 1 8M7.646.146a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 1.707V5.5a.5.5 0 0 1-1 0V1.707L6.354 2.854a.5.5 0 1 1-.708-.708zM8 10a.5.5 0 0 1 .5.5v3.793l1.146-1.147a.5.5 0 0 1 .708.708l-2 2a.5.5 0 0 1-.708 0l-2-2a.5.5 0 0 1 .708-.708L7.5 14.293V10.5A.5.5 0 0 1 8 10"
          />
        </svg>
        <span class="sr-only">Expandir</span>
      </button>
    </header>
  </section>

  <section class="status-block status-block--neutral is-expanded">
    <header class="status-block__header" title="Ocultar bloco Abertas">
      <div class="status-block__copy">
        <span class="status-block__eyebrow">16 registros</span>
        <h2 class="status-block__title">Abertas</h2>
      </div>
      <button class="status-block__toggle" type="button" aria-expanded="true" aria-label="Ocultar bloco Abertas">
        <svg class="status-block__toggle-icon" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
          <path d="M1 8a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13A.5.5 0 0 1 1 8" />
        </svg>
        <span class="sr-only">Recolher</span>
      </button>
    </header>

    <div class="status-block__body" id="status-block-open">
      <div class="status-block__table-wrap">
        <table class="status-table">
          <thead>
            <tr>
              <th>Plano/Rota</th>
              <th>Transporte</th>
              <th>Cliente atual</th>
              <th>Status</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>6103120989</strong></td>
              <td><strong>Fabia Oliveira</strong><small>LNT-3752</small></td>
              <td>Vera L M Vasconcelos Monteiro</td>
              <td><span class="status-badge status-badge--neutral">Aberta</span></td>
              <td><button class="status-table__icon-btn" type="button">Ver</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</section>
```

## CSS Completo

```css
.status-block-shell {
  display: grid;
  gap: 12px;
  width: 100%;
  min-width: 0;
  max-width: 100%;
  padding: 12px;
  overflow-x: visible;
  overflow-y: visible;
  color: var(--status-text);
}

.status-block {
  min-width: min(1770px, 100%);
  overflow: hidden;
  border: 1px solid rgba(21, 91, 213, 0.12);
  border-left: 4px solid rgba(71, 85, 105, 0.44);
  border-radius: 8px;
  background: var(--status-surface);
  box-shadow:
    0 12px 24px rgba(16, 40, 73, 0.07),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  animation: status-block-enter 220ms ease-out both;
}

.status-block--info {
  border-left-color: rgba(37, 99, 235, 0.62);
}

.status-block--critical {
  border-left-color: rgba(185, 28, 28, 0.62);
}

.status-block--success {
  border-left-color: rgba(15, 118, 110, 0.62);
}

.status-block--cancelled {
  border-left-color: rgba(100, 116, 139, 0.62);
}

.status-block__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 14px;
  border-bottom: 1px solid rgba(21, 91, 213, 0.12);
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  cursor: pointer;
  transition: background 160ms ease;
}

.status-block__header:hover {
  background: linear-gradient(180deg, #ffffff 0%, var(--status-orange-soft) 100%);
}

.status-block.is-collapsed .status-block__header {
  border-bottom: 0;
}

.status-block__copy {
  min-width: 0;
  display: grid;
  gap: 2px;
}

.status-block__eyebrow {
  color: var(--status-muted);
  font-size: 0.68rem;
  font-weight: 850;
  letter-spacing: 0.08em;
  line-height: 1.1;
  text-transform: uppercase;
}

.status-block__title {
  margin: 0;
  color: #102849;
  font-size: 1rem;
  font-weight: 900;
  line-height: 1.15;
}

.status-block__toggle {
  width: 34px;
  height: 34px;
  min-height: 34px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: 0;
  border-radius: 0;
  background: transparent;
  color: var(--status-orange);
  cursor: pointer;
  transition:
    color 160ms ease,
    transform 160ms ease;
}

.status-block__toggle:hover,
.status-block__toggle:focus-visible {
  color: var(--status-orange-hover);
  transform: translateY(-1px);
}

.status-block__toggle:focus-visible {
  outline: 2px solid rgba(249, 115, 22, 0.45);
  outline-offset: 3px;
}

.status-block__toggle-icon {
  width: 18px;
  height: 18px;
  display: block;
  flex: 0 0 auto;
}

.status-block__body {
  animation: status-block-body-in 180ms ease-out both;
  overflow-x: auto;
  overflow-y: visible;
  scrollbar-width: thin;
  -webkit-overflow-scrolling: touch;
}

.status-block__empty {
  margin: 0;
  padding: 14px;
  color: var(--status-muted);
  font-size: 0.84rem;
  font-weight: 700;
}

.status-block__table-wrap {
  margin: 0;
  width: max-content;
  min-width: 100%;
  max-width: none;
  overflow: visible;
}

.status-table {
  width: 100%;
  min-width: 1406px;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 13px;
}

.status-table thead th {
  padding: 11px 14px;
  border-bottom: 2px solid rgba(245, 124, 32, 0.54);
  background: linear-gradient(180deg, #175bd0 0%, #10419b 100%);
  color: #ffffff;
  font-size: 12px;
  font-weight: 900;
  text-align: left;
  white-space: nowrap;
}

.status-table tbody td {
  padding: 13px 14px;
  border-bottom: 1px solid var(--status-border);
  vertical-align: middle;
  background: #ffffff;
}

.status-table tbody tr:last-child td {
  border-bottom: 0;
}

.status-table tbody tr:hover td {
  background: var(--status-row-hover);
}

.status-table strong {
  display: block;
  color: var(--status-text);
  font-size: 13px;
  font-weight: 800;
  line-height: 1.25;
}

.status-table small {
  display: block;
  margin-top: 3px;
  color: var(--status-muted);
  font-size: 12px;
  font-weight: 600;
  line-height: 1.25;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  padding: 4px 9px;
  border: 1px solid var(--status-gray-border);
  border-radius: 999px;
  background: var(--status-gray-soft);
  color: var(--status-gray);
  font-size: 11px;
  font-weight: 900;
  line-height: 1;
  text-transform: uppercase;
  white-space: nowrap;
}

.status-badge--neutral {
  border-color: var(--status-gray-border);
  background: var(--status-gray-soft);
  color: var(--status-gray);
}

.status-badge--info {
  border-color: var(--status-blue-border);
  background: var(--status-blue-soft);
  color: var(--status-blue);
}

.status-badge--critical {
  border-color: var(--status-red-border);
  background: var(--status-red-soft);
  color: var(--status-red);
}

.status-badge--success {
  border-color: var(--status-green-border);
  background: var(--status-green-soft);
  color: var(--status-green);
}

.status-table__icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 32px;
  padding: 0 12px;
  border: 1px solid var(--status-border-strong);
  border-radius: 6px;
  background: #ffffff;
  color: var(--status-heading);
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
}

.status-table__icon-btn:hover {
  border-color: var(--status-blue-border);
  background: var(--status-blue-soft);
  color: var(--status-blue);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

## Animações

```css
@keyframes status-block-enter {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes status-block-body-in {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .status-block,
  .status-block__body {
    animation: none;
  }

  .status-block__header,
  .status-block__toggle {
    transition: none;
  }
}
```

## Estados

Bloco vazio recolhido:

```html
<section class="status-block status-block--critical is-collapsed">
  <header class="status-block__header" title="Mostrar bloco Atrasadas">
    <div class="status-block__copy">
      <span class="status-block__eyebrow">0 registros</span>
      <h2 class="status-block__title">Atrasadas</h2>
    </div>
    <button class="status-block__toggle" type="button" aria-expanded="false">
      <svg class="status-block__toggle-icon" viewBox="0 0 16 16" fill="currentColor"></svg>
      <span class="sr-only">Expandir</span>
    </button>
  </header>
</section>
```

Bloco vazio expandido manualmente:

```html
<div class="status-block__body" role="status">
  <p class="status-block__empty">Sem registros neste bloco.</p>
</div>
```

Sem resultado global:

```html
<div class="status-block-empty" role="status">
  Nenhum registro encontrado para o recorte atual.
</div>
```

Erro:

```html
<div class="status-block-empty" role="alert">
  Não foi possível carregar os dados atualizados.
</div>
```

## Responsividade

```css
@media (max-width: 760px) {
  .status-block-shell {
    gap: 10px;
    padding: 10px;
  }

  .status-block__header {
    align-items: center;
    min-height: unset;
    padding: 12px;
  }

  .status-block__title {
    font-size: 0.95rem;
  }

  .status-block__eyebrow {
    font-size: 0.62rem;
  }

  .status-table {
    min-width: 980px;
  }

  .status-table thead th,
  .status-table tbody td {
    padding: 10px 11px;
  }
}
```

## Acessibilidade

- Usar `aria-label` na região geral das tabelas.
- Usar `role="status"` para mensagens neutras e `role="alert"` para erro.
- O header pode receber clique por mouse, mas o controle acessível deve continuar sendo um `button`.
- O botão deve ter `aria-expanded`, `aria-controls`, `aria-label` e `title`.
- O texto visual pode ser só o SVG; manter texto em `.sr-only`.
- O `title` no header e no botão deve dizer a ação: `Mostrar bloco X` ou `Ocultar bloco X`.
- O clique no botão deve parar propagação para não alternar o bloco duas vezes.
- Manter texto no badge além da cor.
- Respeitar `prefers-reduced-motion`.
