# Referência visual: Operação de Guarulhos

Use esta referência como baseline obrigatório para features administrativas da operação 3 Corações. Ela documenta o padrão implementado na rota `/clientes/3-coracoes/guarulhos/programacao/programacao`; não substitui a inspeção da tela existente mais próxima do novo escopo.

## Fontes de verdade

- Shell, topbar e sidebar: `apps/web/src/components/admin-shell.tsx`, `apps/web/src/components/erp-topbar.tsx` e `apps/web/src/app/globals.css` (`.erp-*`).
- Página operacional: `apps/web/src/app/clientes/3-coracoes/[unit]/programacao/programacao/screen.tsx`.
- Composição por blocos de status: `apps/web/src/app/clientes/3-coracoes/[unit]/programacao/reentregas/page.tsx` e a variante `tableVariant="reentregas"` de `ProgramacaoDiariaScreen`.
- Estilos da página, KPIs, toolbar, tabela, dark mode e responsividade: `apps/web/src/app/globals.css` (`.tail-page-*`, `.availability-overview`, `.programacao-*`, `.admin-table-*`).

## Mapa obrigatório de elementos

| Elemento | Referência de Guarulhos | Regra de reaproveitamento |
|---|---|---|
| Shell | `AdminShell`, `erp-shell`, `erp-content`, `erp-content-scale` | Não criar outra topbar, sidebar ou page shell para uma tela interna. |
| Topbar | `ErpTopbar`, `erp-topbar` | Manter barra sticky, menu, logotipo, busca central, chip contextual, notificações, suporte e menu do usuário; respeitar os modos claro/escuro e o layout móvel. |
| Cabeçalho | `tail-page-shell`, `tail-page-head-live`, `eyebrow`, `h1` | Usar hierarquia curta: contexto/eyebrow, título forte e ação contextual única quando necessária. Manter o ritmo de 28px entre blocos. |
| Composição de nova tela | Reentregas (blocos por status) ou Programação (tabela geral) | Antes de especificar uma nova tela, perguntar ao usuário qual dos dois padrões ela deve seguir e registrar a resposta. Não criar outro arranjo sem pedido ou aprovação explícita do usuário. |
| Painel de contexto | `settings-card availability-overview programacao-overview` | Usar painel operacional escuro, borda e raio amplos, agrupando o contexto e os indicadores; não converter em card decorativo ou dashboard de marketing. |
| KPIs | `drivers-summary-card`, `programacao-kpis-grid`, `programacao-operational-kpis` | Cards clicáveis filtram a visão. Manter ícone discreto, label, número dominante e meta curta; preservar estado selecionado, hover e atenção. |
| Semântica dos KPIs | `is-all`, `is-empty`, `is-active`, `is-inactive`, `is-on-leave`, `is-neutral` | Azul para total, cinza para vazio/neutro, verde/teal para pronto, vermelho para risco e laranja para programado. Usar borda esquerda e faixa superior, não orbs ou gradientes decorativos. |
| Toolbar | `programacao-table-toolbar programacao-operational-table-toolbar` | Para grade operacional, usar fundo azul `#155bd5 → #123f91`, linha inferior laranja `#f57c20`, título branco e marcador laranja. Ações ficam agrupadas à direita. |
| Busca e filtros | `programacao-table-search`, `settings-input`, `availability-filter-select`, `programacao-table-toolbar__filter` | Campos têm altura e raio consistentes, texto escuro sobre fundo branco na toolbar e estado ativo laranja suave. Não inventar controles visualmente incompatíveis. |
| Botões | `admin-btn-secondary`, botões da toolbar e de linha | Diferenciar ações por semântica: processamento verde `#138a4d`, comunicação verde `#16a34a`, atalho/link azul `#1d6fb8`. Estados hover, focus e disabled devem permanecer perceptíveis. |
| Tabela | `admin-table-wrap admin-table-wrap--fast programacao-desktop-table programacao-operational-table`, `admin-table` | Preservar tabela densa, toolbar fixada lateralmente durante scroll horizontal e cabeçalho azul escuro com linha laranja, texto branco e colunas compactas. Não trocar por tabela genérica. |
| Linhas e ações | `programacao-table-cell`, `programacao-row-action-button`, `programacao-route-button` | Dado principal usa texto maior; metadado é menor; ações de linha são compactas, previsíveis e com alvos clicáveis claros. |
| Modais | `admin-overlay`, `programacao-feedback-dialog`, `programacao-autoassign-dialog`, `programacao-manual-modal`, `sac-export-modal__close` | Para modal operacional, usar overlay com blur, diálogo com dimensão adequada e overflow interno, header azul full-bleed com linha laranja, corpo `#f7faff`, cards brancos e ações semânticas. Não usar modal genérico acolchoado ou card de marketing. |
| Responsividade | `isMobileViewport`, `programacao-mobile-list`, breakpoints `760px` e `640px` | Em telas estreitas, a programação não operacional vira cards. Toolbars passam a uma coluna, campos e ações ocupam largura total e a tabela que permanecer deve ter scroll horizontal explícito. |
| Movimento e tema | `is-entry-animated`, `prefers-reduced-motion`, `html[data-theme="dark"]` | Animação é curta e progressiva, nunca bloqueia leitura; desativar para redução de movimento. Implementar claro e escuro com contraste equivalente. |

## Critérios visuais de aceite

1. A leitura segue esta ordem: título e contexto → KPIs/alertas → filtros e ações → dados da tabela.
2. Toda tela nova tem a decisão de composição registrada: blocos por status de Reentregas ou tabela geral de Programação. Outro padrão possui pedido ou aprovação explícita do usuário.
3. A tela parece parte do mesmo shell de Guarulhos antes mesmo de o usuário ler o conteúdo.
4. Nenhuma ação principal fica visualmente igual a uma ação secundária ou destrutiva.
5. KPI, filtro, botão e linha interativos apresentam estado selected/hover/focus/disabled quando aplicável.
6. Em `1280px`, `768px` e `375px`, não há controle oculto, overflow acidental, texto sem tratamento ou tabela espremida; scroll horizontal é aceitável apenas quando explicitamente fornecido pelo wrapper operacional.
7. Todo modal operacional tem `role="dialog"`, `aria-modal`, nome acessível, fechamento visível e foco/hover perceptíveis. O modal preserva overlay, header full-bleed, corpo, ações, estados disabled/erro/loading, dark mode e largura móvel; não herda passivamente o limite genérico de `560px` quando o conteúdo operacional exige mais espaço.
8. Não adicionar gradientes radiais, blobs, cards de marketing, novos raios arbitrários, sombras pesadas ou ícones de outra família.

## Uso pelo SpecKit

- `$speckit-specify`, `$speckit-plan` e `$speckit-implement` DEVEM ler este arquivo para features administrativas 3 Corações e registrar os itens aplicáveis.
- A tela de Guarulhos é a referência-base; a tela existente do mesmo módulo é a referência de proximidade e prevalece se houver diferença funcional legítima.
- Em tela nova, a escolha entre blocos por status e tabela geral é uma decisão obrigatória do usuário, não uma suposição do agente. Outro padrão requer instrução ou aprovação explícita registrada.
- Toda exceção precisa declarar o elemento divergente, a razão funcional e a aprovação explícita.
