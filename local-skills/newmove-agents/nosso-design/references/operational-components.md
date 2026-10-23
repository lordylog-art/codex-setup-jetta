# Componentes operacionais canônicos

## Listagens e tabelas

Comece por `apps/web/src/components/operational-table.tsx`:

- `OperationalKpiGrid`: resumo clicável ou informativo com tones existentes.
- `OperationalFilterPanel`: região de filtros com divisão primária/secundária.
- `OperationalTableToolbar`: título, busca, filtro, contador e ações.
- `OperationalTableFrame`: moldura, overflow horizontal e entrada da tabela.
- `OperationalStatusBlockTable`: separação de tabelas por status.
- `OperationalActionFeedback` e `OperationalEmptyState`: loading, vazio, erro e sucesso.

Não replique essas estruturas com novas classes locais. Estenda o componente apenas quando a necessidade for compartilhável e compatível.

Antes de escolher a composição, consulte também `apps/web/src/components/operational-templates/catalog.ts`. O catálogo registra os templates `app-shell`, `kpi-grid`, `filter-panel`, `fixed-table`, `status-block-table`, `form-editor`, `operational-modal`, `action-feedback` e `visual-asset`. Use `apps/web/src/components/global-pagination.tsx` para paginação em vez de criar controles locais.

## Botões e ações

- Reutilize a classe/componente da mesma intenção na família: ação primária, secundária, perigo, ícone ou ação de toolbar.
- Ação primária é escassa e deve ser semanticamente principal.
- Preserve `type`, `aria-label`, estado desabilitado, loading e foco visível.
- Ícone deve vir do conjunto já utilizado pela área; não use emoji como substituto.
- Em tabelas, ações não devem transformar a linha inteira em um alvo ambíguo nem interferir com elementos interativos filhos.

## Formulários

- Reutilize labels, inputs, selects, mensagens de validação e grupos da tela de cadastro mais próxima.
- Não esconda label estrutural em favor de placeholder.
- Preserve obrigatório, desabilitado, erro, ajuda, loading e confirmação existentes.

## Modais e diálogos

- Procure primeiro um shell no mesmo módulo. Exemplos existentes incluem modais de SAC e `PalletModalShell` em gestão de paletes.
- Preserve os contratos de overlay, fechamento, foco, `Escape`, clique externo quando suportado e bloqueio durante operação. Reutilize o shell e as classes da família; ajuste largura e organização interna pelos critérios de composição da skill.
- Em confirmações, priorize a decisão e sua consequência. Mostre mudanças como comparação entre estado anterior e proposto; agrupe a identificação do registro sem fragmentar cada campo em um cartão.
- Organize ações pela relação entre elas e pelo espaço disponível. No desktop, evite uma pilha estreita à direita que deixe vazio lateral sem função; empilhe quando legibilidade ou viewport exigirem. Preserve as escolhas funcionais existentes.

## Dashboards

Use exclusivamente `apps/web/src/components/dashboard/`: `DashboardShell`, `DashboardSection`, filtros, KPI, gráficos, tabela e estados. O escopo `.jetta-dashboard` e o prefixo `jetta:` são obrigatórios. Não importar Tailwind completo nem adicionar Preflight/reset global.

## Evidência

Para confirmar aparência e combinações reais, localize a família em [routes.md](routes.md). Para descobrir outros componentes compartilhados, consulte [source-components.md](source-components.md), mas não carregue o catálogo inteiro sem necessidade.
