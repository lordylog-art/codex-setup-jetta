# Contrato visual do ERP Jetta

## Identidade

O ERP combina superfície operacional clara, navegação azul-marinho, acento laranja Jetta e alta densidade de informação. A aparência deve transmitir operação, leitura rápida e precisão; não estética promocional de landing page.

## Fontes

- Texto principal: `var(--font-main)`, atualmente Aptos, Segoe UI e Trebuchet MS como fallbacks.
- Títulos/display: `var(--font-display)`, atualmente Aptos Display, Bahnschrift e Segoe UI Variable Display.
- `Fe` existe exclusivamente para a representação visual de placas brasileiras. Não use em texto comum.
- Preserve pesos e tamanhos do componente análogo. Não introduza fonte web ou família nova.

## Cores e temas

- Use variáveis CSS do projeto. As bases incluem `--page-bg`, `--panel-shell`, `--ink`, `--muted`, `--border`, `--button-bg`, `--admin-*` e, no dashboard, `--dashboard-*`.
- O laranja é acento/ação; azul-marinho organiza navegação e cabeçalhos operacionais. Não transforme ambos em gradientes decorativos sem precedente na família.
- Estados de sucesso, alerta, erro e informação devem reutilizar tones/classes existentes.
- Quando a família possui tema escuro, o novo elemento deve herdar as substituições de `html[data-theme="dark"]`; não fixe cores que quebrem o tema.

## Forma, densidade e espaço

- Os tokens globais de raio são deliberadamente contidos: `--radius-xl: 4px`, `--radius-lg: 2px`, `--radius-md: 2px`, `--radius-sm: 0px`.
- Partes legadas ou especializadas possuem raios maiores. Isso não autoriza aplicar cartões arredondados genericamente; copie apenas o componente/família correspondente.
- Telas operacionais priorizam densidade, tabelas legíveis, filtros compactos e ações claras.
- Use a cadência de espaçamento do componente análogo. Não escolha valores isolados só porque “parecem bons”.

## Hierarquia

- Preserve topbar/sidebar/layout da área.
- Uma página deve ter um título primário claro, ações agrupadas e conteúdo organizado pelo mesmo shell de suas vizinhas.
- Listagens operacionais normalmente seguem resumo/KPIs, filtros, toolbar e tabela ou blocos por status.
- Estados loading, vazio, erro e sucesso pertencem à mesma composição; não os trate como páginas visualmente independentes.

## Anti-AI-slop

São proibidos sem referência existente e autorização: gradiente roxo/azul decorativo, glassmorphism, brilho neon, cards excessivamente arredondados, sombras dramáticas, ícones emoji, ilustrações geradas, textos promocionais genéricos, espaçamento “hero” em telas operacionais e variações arbitrárias entre seções.

## Fonte de verdade

[source-foundations.md](source-foundations.md) é um inventário gerado. Confirme sempre o token no código antes de alterar. Uma captura mostra o resultado atual, mas não autoriza copiar valores computados para CSS novo quando já existe token ou classe.
