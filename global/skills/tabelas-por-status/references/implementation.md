# Implementação De Tabelas Por Blocos De Status

## Índice

- Modelo mental
- Tipos base
- Configuração dos blocos
- Agrupamento sem remover vazios
- Busca local/remota
- Expansão e recolhimento
- Componente React
- HTML estático equivalente
- Testes recomendados

## Modelo Mental

A tela deve tratar a tabela em camadas:

1. `rows`: dados vindos da API.
2. `supplementalRows`: resultados de busca remota ou registros carregados sob demanda.
3. `displayRows`: união deduplicada.
4. `filteredRows`: busca local, filtros, período, perfil, status.
5. `blocks`: agrupamento por status operacional, preservando todos os blocos configurados.
6. `render`: uma seção por bloco; se o bloco estiver vazio, renderizar header recolhido e não renderizar tabela.

Isso permite reaproveitar a estrutura em qualquer tela operacional sem cortar tabela, esconder status vazio ou perder hierarquia.

## Tipos Base

```ts
export type StatusBlockTone =
  | "neutral"
  | "info"
  | "critical"
  | "success"
  | "cancelled";

export type StatusBlock<T> = {
  id: string;
  title: string;
  meta: string;
  tone: StatusBlockTone;
  rows: T[];
  collapsedByDefault?: boolean;
};

export type StatusBlockConfig<T> = {
  id: string;
  title: string;
  tone: StatusBlockTone;
  collapsedByDefault?: boolean;
  match: (row: T) => boolean;
  meta: (rows: T[]) => string;
};
```

## Configuração Dos Blocos

Adaptar campos ao domínio real da tela.

```ts
type OperationalRow = {
  id: string;
  statusLabel?: string | null;
  rawStatus?: string | null;
  planNumber?: string | null;
  driverName?: string | null;
  plate?: string | null;
  customerName?: string | null;
  invoiceNumber?: string | null;
  routeKey?: string | null;
  updatedAt?: string | null;
};

function normalizeText(value: unknown) {
  return String(value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim()
    .toLowerCase();
}

function rowStatusText(row: OperationalRow) {
  return normalizeText(`${row.statusLabel ?? ""} ${row.rawStatus ?? ""}`);
}

function isFinalized(row: OperationalRow) {
  return /finaliz|concluid|completed|finished/.test(rowStatusText(row));
}

function isCancelled(row: OperationalRow) {
  return /cancelad|canceled|cancelled/.test(rowStatusText(row));
}
```

Exemplo no padrão SAC Ocorrências:

```ts
export const occurrenceStatusBlocks: StatusBlockConfig<OperationalRow>[] = [
  {
    id: "delayed",
    title: "Atrasadas",
    tone: "critical",
    match: (row) => /atras/.test(rowStatusText(row)),
    meta: (rows) => `${rows.length} prazo(s) estourado(s)`,
  },
  {
    id: "open",
    title: "Abertas",
    tone: "neutral",
    match: (row) => /abert/.test(rowStatusText(row)),
    meta: (rows) => `${rows.length} aguardando tratativa`,
  },
  {
    id: "analysis",
    title: "Em análise",
    tone: "info",
    match: (row) => /analise|analis/.test(rowStatusText(row)),
    meta: (rows) => `${rows.length} em atendimento manual`,
  },
  {
    id: "finalized",
    title: "Finalizadas",
    tone: "success",
    collapsedByDefault: true,
    match: isFinalized,
    meta: (rows) => `${rows.length} tratativa(s) concluída(s)`,
  },
];
```

Exemplo no padrão SAC Custo Extra:

```ts
export const extraCostStatusBlocks: StatusBlockConfig<OperationalRow>[] = [
  {
    id: "contested",
    title: "Contestadas",
    tone: "info",
    match: (row) => /contestad/.test(rowStatusText(row)),
    meta: (rows) => `${rows.length} em contestação`,
  },
  {
    id: "pending",
    title: "Pendentes",
    tone: "neutral",
    match: (row) => /pendente|aprovacao/.test(rowStatusText(row)),
    meta: (rows) => `${rows.length} aguardando aprovação`,
  },
  {
    id: "concluded",
    title: "Concluídos",
    tone: "success",
    collapsedByDefault: true,
    match: (row) =>
      /aprovad|rejeitad|contestacao aceita|contestacao rejeitada/.test(
        rowStatusText(row),
      ),
    meta: (rows) => `${rows.length} encerrado(s)`,
  },
];
```

## Agrupamento Sem Remover Vazios

Não filtre blocos vazios depois de montar. A hierarquia precisa aparecer mesmo quando um bloco está com `0`.

```ts
export function buildStatusBlocks<T>(
  rows: T[],
  configs: StatusBlockConfig<T>[],
): StatusBlock<T>[] {
  const buckets = new Map<string, T[]>();

  for (const row of rows) {
    const config = configs.find((candidate) => candidate.match(row));
    if (!config) continue;

    const current = buckets.get(config.id) ?? [];
    current.push(row);
    buckets.set(config.id, current);
  }

  return configs.map((config) => {
    const blockRows = buckets.get(config.id) ?? [];
    return {
      id: config.id,
      title: config.title,
      tone: config.tone,
      collapsedByDefault: config.collapsedByDefault,
      meta: config.meta(blockRows),
      rows: blockRows,
    };
  });
}
```

## Busca Local/Remota

```ts
function compactSearchText(value: string) {
  return normalizeText(value).replace(/[^a-z0-9]/g, "");
}

function searchTerms(rawQuery: string) {
  return rawQuery
    .split(";")
    .map((term) => normalizeText(term))
    .filter(Boolean);
}

function buildSearchHaystack(row: OperationalRow) {
  return normalizeText([
    row.planNumber,
    row.routeKey,
    row.driverName,
    row.plate,
    row.customerName,
    row.invoiceNumber,
    row.statusLabel,
    row.rawStatus,
  ].filter(Boolean).join(" "));
}

export function matchesOperationalSearch(row: OperationalRow, rawQuery: string) {
  const terms = searchTerms(rawQuery);
  if (!terms.length) return true;

  const haystack = buildSearchHaystack(row);
  const compactHaystack = compactSearchText(haystack);

  return terms.every((term) => {
    if (haystack.includes(term)) return true;
    const compactTerm = compactSearchText(term);
    return Boolean(compactTerm && compactHaystack.includes(compactTerm));
  });
}
```

Quando houver busca remota, enviar o termo no Enter e filtrar no backend antes do limite:

```ts
async function fetchOperationalRows(input: {
  unit: string;
  limit: number;
  offset: number;
  search?: string;
  category?: string;
}) {
  const params = new URLSearchParams({
    unit: input.unit,
    limit: String(input.limit),
    offset: String(input.offset),
  });

  if (input.category) params.set("category", input.category);
  if (input.search?.trim()) params.set("search", input.search.trim());

  const response = await fetch(`/api/operacional/acompanhamento?${params}`, {
    credentials: "include",
  });

  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(payload?.message || "Não foi possível carregar os dados.");
  }

  return payload as OperationalRow[];
}
```

## Expansão E Recolhimento

Regras:

- bloco com linhas inicia aberto;
- bloco vazio inicia recolhido;
- bloco terminal inicia recolhido por `collapsedByDefault`;
- busca ativa expande bloco com resultado;
- clique no header inteiro alterna o bloco;
- clique no botão interno deve chamar `stopPropagation()` para não alternar duas vezes.

```tsx
function useStatusBlockExpansion(search: string) {
  const [overrides, setOverrides] = useState<Record<string, boolean>>({});

  function isExpanded(block: StatusBlock<unknown>) {
    if (search.trim() && block.rows.length > 0) return true;

    return (
      overrides[block.id] ??
      (!block.collapsedByDefault && block.rows.length > 0)
    );
  }

  function toggle(block: StatusBlock<unknown>) {
    setOverrides((current) => ({
      ...current,
      [block.id]: !isExpanded(block),
    }));
  }

  return { isExpanded, toggle };
}

function StatusBlockToggleIcon({ expanded }: { expanded: boolean }) {
  return (
    <svg
      viewBox="0 0 16 16"
      fill="currentColor"
      aria-hidden="true"
      focusable="false"
      className="status-block__toggle-icon"
    >
      <path
        fillRule="evenodd"
        d={
          expanded
            ? "M1 8a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13A.5.5 0 0 1 1 8m7-8a.5.5 0 0 1 .5.5v3.793l1.146-1.147a.5.5 0 0 1 .708.708l-2 2a.5.5 0 0 1-.708 0l-2-2a.5.5 0 1 1 .708-.708L7.5 4.293V.5A.5.5 0 0 1 8 0m-.5 11.707-1.146 1.147a.5.5 0 0 1-.708-.708l2-2a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 11.707V15.5a.5.5 0 0 1-1 0z"
            : "M1 8a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13A.5.5 0 0 1 1 8M7.646.146a.5.5 0 0 1 .708 0l2 2a.5.5 0 0 1-.708.708L8.5 1.707V5.5a.5.5 0 0 1-1 0V1.707L6.354 2.854a.5.5 0 1 1-.708-.708zM8 10a.5.5 0 0 1 .5.5v3.793l1.146-1.147a.5.5 0 0 1 .708.708l-2 2a.5.5 0 0 1-.708 0l-2-2a.5.5 0 0 1 .708-.708L7.5 14.293V10.5A.5.5 0 0 1 8 10"
        }
      />
    </svg>
  );
}
```

## Componente React

```tsx
type StatusBlockTablesProps = {
  rows: OperationalRow[];
  search: string;
  onOpenDetails: (row: OperationalRow) => void;
};

export function StatusBlockTables(props: StatusBlockTablesProps) {
  const filteredRows = useMemo(
    () => props.rows.filter((row) => matchesOperationalSearch(row, props.search)),
    [props.rows, props.search],
  );

  const blocks = useMemo(
    () => buildStatusBlocks(filteredRows, occurrenceStatusBlocks),
    [filteredRows],
  );

  const expansion = useStatusBlockExpansion(props.search);

  return (
    <section className="status-block-shell" aria-label="Tabelas operacionais por status">
      {blocks.map((block) => {
        const expanded = expansion.isExpanded(block);
        const actionLabel = `${expanded ? "Ocultar" : "Mostrar"} bloco ${block.title}`;
        const contentId = `status-block-${block.id}`;

        return (
          <section key={block.id} className={`status-block status-block--${block.tone} ${expanded ? "is-expanded" : "is-collapsed"}`}>
            <header
              className="status-block__header"
              title={actionLabel}
              onClick={() => expansion.toggle(block)}
            >
              <div>
                <span className="status-block__eyebrow">{block.meta}</span>
                <h2 className="status-block__title">{block.title}</h2>
              </div>

              <button
                type="button"
                className="status-block__toggle"
                aria-expanded={expanded}
                aria-controls={contentId}
                aria-label={actionLabel}
                title={actionLabel}
                onClick={(event) => {
                  event.stopPropagation();
                  expansion.toggle(block);
                }}
              >
                <StatusBlockToggleIcon expanded={expanded} />
                <span className="sr-only">{expanded ? "Recolher" : "Expandir"}</span>
              </button>
            </header>

            {expanded ? (
              <div id={contentId} className="status-block__body">
                {block.rows.length ? (
                  <div className="status-block__table-wrap">
                    <table className="status-table">
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
                        {block.rows.map((row) => (
                          <tr key={row.id}>
                            <td>{row.planNumber || row.routeKey || "-"}</td>
                            <td>{row.driverName || "-"}</td>
                            <td>{row.customerName || "-"}</td>
                            <td>{row.statusLabel || "-"}</td>
                            <td>
                              <button type="button" onClick={() => props.onOpenDetails(row)}>
                                Ver
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p className="status-block__empty">Sem registros neste bloco.</p>
                )}
              </div>
            ) : null}
          </section>
        );
      })}
    </section>
  );
}
```

## HTML Estático Equivalente

```html
<section class="status-block-shell" aria-label="Tabelas operacionais por status">
  <section class="status-block status-block--critical is-collapsed">
    <header class="status-block__header" title="Mostrar bloco Atrasadas">
      <div>
        <span class="status-block__eyebrow">0 registros</span>
        <h2 class="status-block__title">Atrasadas</h2>
      </div>
      <button
        class="status-block__toggle"
        type="button"
        aria-expanded="false"
        aria-controls="status-block-delayed"
        aria-label="Mostrar bloco Atrasadas"
        title="Mostrar bloco Atrasadas"
      >
        <svg class="status-block__toggle-icon" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
          <path d="M1 8a.5.5 0 0 1 .5-.5h13a.5.5 0 0 1 0 1h-13A.5.5 0 0 1 1 8" />
        </svg>
        <span class="sr-only">Expandir</span>
      </button>
    </header>
  </section>
</section>
```

## Testes Recomendados

```ts
describe("status block tables", () => {
  it("preserva blocos vazios na ordem configurada", () => {
    const blocks = buildStatusBlocks(
      [{ id: "1", statusLabel: "Aberta" }],
      occurrenceStatusBlocks,
    );

    expect(blocks.map((block) => block.title)).toEqual([
      "Atrasadas",
      "Abertas",
      "Em análise",
      "Finalizadas",
    ]);
    expect(blocks[0].rows).toEqual([]);
  });

  it("bloco vazio inicia recolhido e header alterna expansão", async () => {
    render(<StatusBlockTables rows={[{ id: "1", statusLabel: "Aberta" }]} search="" onOpenDetails={vi.fn()} />);

    expect(screen.getByRole("button", { name: /Mostrar bloco Atrasadas/i })).toHaveAttribute("aria-expanded", "false");

    fireEvent.click(screen.getByRole("heading", { name: "Atrasadas" }).closest(".status-block__header")!);

    expect(screen.getByRole("button", { name: /Ocultar bloco Atrasadas/i })).toHaveAttribute("aria-expanded", "true");
  });

  it("busca por texto sem acento e código sem pontuação", () => {
    const row = {
      id: "1",
      planNumber: "6103068034",
      plate: "ABC-1234",
      customerName: "São João",
    };

    expect(matchesOperationalSearch(row, "sao joao")).toBe(true);
    expect(matchesOperationalSearch(row, "ABC1234")).toBe(true);
  });
});
```
