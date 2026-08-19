---
name: table-operacional
description: Aplicar o padrão visual de tabela operacional do ERP Jetta em telas internas, com toolbar azul, destaque laranja, KPIs coloridos, botões de ação legíveis, cabeçalho de tabela forte e exemplo HTML/React reutilizável. Use quando o usuário pedir para melhorar, padronizar, dar vida, dar charme, reaproveitar ou criar uma table/tabela operacional, toolbar de tabela, cabeçalho de tabela, filtros, KPIs ou ações em telas como disponibilidade, programação, SAC, cadastros e dashboards internos.
---

# Table Operacional

Use esta skill para transformar uma tabela interna do ERP em ferramenta operacional: densa, escaneável, bonita e objetiva. O padrão nasceu da tela de disponibilidade e combina com fluxos de frota, SAC, programação, roteirização e painéis administrativos.

## Princípios

- Mudança cirúrgica: prefira CSS/markup local da tabela, sem refatorar fluxo.
- Preserve filtros, sort, paginação, callbacks, APIs, payloads e estado.
- Visual operacional, não landing page.
- Toolbar azul full-width com linha laranja estrutural.
- Cabeçalho da tabela azul mais compacto, com texto branco e destaque laranja.
- KPIs com cor por contexto/status, usando faixa/borda/fundo suave, sem brushes/radiais decorativos.
- Botões devem ter cores fortes e distintas por ação, sem parecerem opacos sobre o azul.
- Campos e filtros devem continuar claros, altos e fáceis de clicar.
- Modo escuro precisa manter contraste e não pode depender só de sombra.

## Workflow

1. Localize a tabela, a toolbar e os KPIs existentes.
2. Verifique se já existem classes de padrão local como `programacao-table-toolbar`, `admin-table`, `drivers-summary-card`, `settings-input`, `availability-filter-select` ou equivalentes.
3. Reaproveite a estrutura existente. Só crie classes novas quando o escopo da tela precisar isolar o visual.
4. Aplique o padrão em camadas:
   - KPIs/contexto acima da tabela;
   - toolbar da tabela;
   - controles/filtros;
   - botões de ação;
   - `thead`/`th`;
   - dark mode.
5. Atualize teste focado quando houver teste fonte/CSS ou interação da tela.
6. Rode teste focado da tela e teste compartilhado de tabela quando existir.
7. Se o app estiver acessível, valide visualmente no navegador.

## Receita Visual

### Toolbar

- Fundo: `linear-gradient(135deg, #155bd5 0%, #123f91 100%)`.
- Linha inferior: `box-shadow: inset 0 -3px 0 #f57c20`.
- Título branco com peso alto.
- Opcional: marcador vertical laranja antes do título.
- Campos/filtros brancos com texto `#102849`.

### Cabeçalho Da Tabela

- `thead`: `linear-gradient(180deg, #175bd0 0%, #10419b 100%)`.
- Linha inferior laranja: `box-shadow: inset 0 -3px 0 #f57c20`.
- `th`: branco, pequeno, forte, com `text-shadow` sutil.
- Não aumente demais a altura do cabeçalho; a tabela continua sendo uma ferramenta de leitura rápida.

### KPIs

- Use uma cor por significado:
  - total/base: azul;
  - vazio/sem status: cinza;
  - disponível/sucesso: verde/teal;
  - indisponível/bloqueio: vermelho;
  - programado/alocado: laranja;
  - inativo/neutro: cinza frio.
- Use `border-left`, faixa superior `::before` e fundo linear suave.
- Evite `radial-gradient`, bolhas, blobs e brushes decorativos.

### Botões

- Ação de preenchimento/processamento: verde operacional `#138a4d`.
- Envio WhatsApp/chatbot: verde WhatsApp `#16a34a`.
- Link/cópia/atalho: azul vivo `#1d6fb8`.
- Botões sobre toolbar azul devem ter texto branco, sombra pequena e estado hover mais escuro.

## Exemplo HTML

Use como referência visual quando precisar explicar a estrutura sem entrar em React.

```html
<section class="table-operacional-page">
  <div class="drivers-summary table-operacional-kpis" aria-label="Resumo operacional">
    <button type="button" class="drivers-summary-card is-all is-selected">
      <span class="drivers-summary-label">Motoristas</span>
      <strong>40</strong>
      <span class="drivers-summary-meta">Base operacional visível</span>
    </button>

    <button type="button" class="drivers-summary-card is-active">
      <span class="drivers-summary-label">Disponíveis</span>
      <strong>12</strong>
      <span class="drivers-summary-meta">Prontos para operação</span>
    </button>

    <button type="button" class="drivers-summary-card is-inactive">
      <span class="drivers-summary-label">Indisponíveis</span>
      <strong>2</strong>
      <span class="drivers-summary-meta">Bloqueados no dia</span>
    </button>
  </div>

  <section class="admin-table-wrap table-operacional-wrap" aria-label="Tabela operacional">
    <div class="programacao-table-toolbar table-operacional-toolbar">
      <strong class="programacao-table-toolbar__title">Motoristas disponíveis</strong>

      <div class="programacao-table-toolbar__actions table-operacional-toolbar__actions">
        <label class="programacao-table-search table-operacional-search">
          <span class="programacao-table-search__icon" aria-hidden="true"></span>
          <input type="search" placeholder="Digite e pressione Enter" />
        </label>

        <input type="date" class="settings-input table-operacional-date" />

        <select class="settings-input table-operacional-filter">
          <option>Todos</option>
          <option>Disponíveis</option>
          <option>Indisponíveis</option>
        </select>

        <button type="button" class="admin-btn-secondary table-operacional-action table-operacional-action--fill">
          Preencher
        </button>
        <button type="button" class="admin-btn-secondary table-operacional-action table-operacional-action--send">
          Enviar
        </button>
        <button type="button" class="admin-btn-secondary table-operacional-action table-operacional-action--link">
          Link
        </button>
      </div>
    </div>

    <table class="admin-table table-operacional-table">
      <thead>
        <tr>
          <th>Motorista</th>
          <th>Placa</th>
          <th>Veículo</th>
          <th>Telefone</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>ADEMIR ALVES DE OLIVEIRA</td>
          <td>CJZ-8D85</td>
          <td>Cavalo simples</td>
          <td>(35) 99818-2404</td>
          <td>Disponível</td>
        </tr>
      </tbody>
    </table>
  </section>
</section>
```

## Exemplo React

Adapte nomes, callbacks, colunas e filtros ao arquivo real. O exemplo mostra a estrutura esperada, não um componente obrigatório.

```tsx
<section className="table-operacional-page">
  <div className="drivers-summary table-operacional-kpis" aria-label="Resumo operacional">
    <button type="button" className="drivers-summary-card is-all is-selected">
      <span className="drivers-summary-label">Motoristas</span>
      <strong>40</strong>
      <span className="drivers-summary-meta">Base operacional visível</span>
    </button>

    <button type="button" className="drivers-summary-card is-empty">
      <span className="drivers-summary-label">Vazios</span>
      <strong>2</strong>
      <span className="drivers-summary-meta">Sem status definido</span>
    </button>

    <button type="button" className="drivers-summary-card is-active">
      <span className="drivers-summary-label">Disponíveis</span>
      <strong>12</strong>
      <span className="drivers-summary-meta">Prontos para operação</span>
    </button>

    <button type="button" className="drivers-summary-card is-inactive">
      <span className="drivers-summary-label">Indisponíveis</span>
      <strong>2</strong>
      <span className="drivers-summary-meta">Bloqueados no dia</span>
    </button>

    <button type="button" className="drivers-summary-card is-on-leave">
      <span className="drivers-summary-label">Programados</span>
      <strong>24</strong>
      <span className="drivers-summary-meta">Já alocados</span>
    </button>
  </div>

  <section className="admin-table-wrap table-operacional-wrap" aria-label="Tabela operacional">
    <div className="programacao-table-toolbar table-operacional-toolbar">
      <strong className="programacao-table-toolbar__title">Motoristas disponíveis</strong>

      <div className="programacao-table-toolbar__actions table-operacional-toolbar__actions">
        <label className="programacao-table-search table-operacional-search">
          <span className="programacao-table-search__icon" aria-hidden="true" />
          <input
            type="search"
            placeholder="Digite e pressione Enter"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </label>

        <input
          type="date"
          className="settings-input table-operacional-date"
          value={date}
          onChange={(event) => setDate(event.target.value)}
        />

        <select
          className="settings-input table-operacional-filter"
          value={statusFilter}
          onChange={(event) => setStatusFilter(event.target.value)}
        >
          <option value="ALL">Todos</option>
          <option value="AVAILABLE">Disponíveis</option>
          <option value="UNAVAILABLE">Indisponíveis</option>
        </select>

        <button type="button" className="admin-btn-secondary table-operacional-action table-operacional-action--fill">
          Preencher
        </button>

        <button type="button" className="admin-btn-secondary table-operacional-action table-operacional-action--send">
          Enviar
        </button>

        <button type="button" className="admin-btn-secondary table-operacional-action table-operacional-action--link">
          Link
        </button>
      </div>
    </div>

    <table className="admin-table table-operacional-table">
      <thead>
        <tr>
          <th>Motorista</th>
          <th>Placa</th>
          <th>Veículo</th>
          <th>Telefone</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.id}>
            <td>{row.driverName}</td>
            <td>{row.plate}</td>
            <td>{row.vehicle}</td>
            <td>{row.phone}</td>
            <td>{row.statusLabel}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </section>
</section>
```

## CSS Base

Copie só o que fizer sentido para a tela. Se o projeto já tiver classes equivalentes, adapte os seletores em vez de duplicar.

```css
.table-operacional-kpis {
  grid-template-columns: repeat(6, minmax(128px, 1fr));
}

.table-operacional-kpis .drivers-summary-card {
  position: relative;
  border-left-width: 3px;
  box-shadow:
    0 14px 30px rgba(16, 40, 73, 0.07),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.table-operacional-kpis .drivers-summary-card::before {
  content: "";
  position: absolute;
  inset: 0 0 auto 0;
  height: 4px;
  background: currentColor;
  opacity: 0.82;
}

.table-operacional-kpis .drivers-summary-card.is-all {
  border-color: rgba(21, 91, 213, 0.5);
  background: linear-gradient(135deg, #ffffff 0%, #eef5ff 100%);
}

.table-operacional-kpis .drivers-summary-card.is-empty {
  border-color: rgba(71, 85, 105, 0.38);
  background: linear-gradient(135deg, #ffffff 0%, #f3f6fa 100%);
}

.table-operacional-kpis .drivers-summary-card.is-active {
  border-color: rgba(15, 118, 110, 0.48);
  background: linear-gradient(135deg, #ffffff 0%, #ecfdf7 100%);
}

.table-operacional-kpis .drivers-summary-card.is-inactive {
  border-color: rgba(185, 28, 28, 0.42);
  background: linear-gradient(135deg, #ffffff 0%, #fff1f2 100%);
}

.table-operacional-kpis .drivers-summary-card.is-on-leave {
  border-color: rgba(180, 83, 9, 0.46);
  background: linear-gradient(135deg, #ffffff 0%, #fff7ed 100%);
}

.table-operacional-toolbar {
  display: grid;
  grid-template-columns: minmax(170px, 0.55fr) auto;
  align-items: center;
  gap: 16px;
  min-width: 1180px;
  padding: 18px 20px 17px;
  background: linear-gradient(135deg, #155bd5 0%, #123f91 100%);
  box-shadow: inset 0 -3px 0 #f57c20;
}

.table-operacional-toolbar .programacao-table-toolbar__title {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #ffffff;
  font-weight: 900;
}

.table-operacional-toolbar .programacao-table-toolbar__title::before {
  content: "";
  width: 4px;
  height: 24px;
  border-radius: 999px;
  background: #f57c20;
  box-shadow: 0 0 0 4px rgba(245, 124, 32, 0.18);
}

.table-operacional-search,
.table-operacional-date,
.table-operacional-filter {
  min-height: 44px;
  border-color: rgba(255, 255, 255, 0.28);
  border-radius: 10px;
  background: #ffffff;
  color: #102849;
  box-shadow: 0 10px 20px rgba(16, 40, 73, 0.12);
}

.table-operacional-action {
  min-height: 44px;
  padding: 0 12px;
  border-color: transparent;
  color: #ffffff;
  box-shadow:
    0 12px 22px rgba(16, 40, 73, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.18);
}

.table-operacional-action--fill {
  background: #138a4d;
}

.table-operacional-action--send {
  background: #16a34a;
}

.table-operacional-action--link {
  background: #1d6fb8;
}

.table-operacional-table thead {
  background: linear-gradient(180deg, #175bd0 0%, #10419b 100%);
  box-shadow: inset 0 -3px 0 #f57c20;
}

.table-operacional-table th {
  color: #ffffff;
  border-bottom-color: rgba(245, 124, 32, 0.54);
  text-shadow: 0 1px 0 rgba(16, 40, 73, 0.22);
}
```

## Checklist De Entrega

- O usuário consegue escanear KPIs, filtros, ações e linhas sem esforço.
- Nenhum texto visível novo está sem acento em português do Brasil.
- A toolbar não oculta ou quebra controles em telas menores; use `overflow-x: auto` quando necessário.
- O visual não depende de radiais/brushes/orbs decorativos.
- As ações principais têm cores distinguíveis.
- Teste focado passou; se não houver teste, informe a lacuna.
