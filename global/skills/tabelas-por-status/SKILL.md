---
name: tabelas-por-status
description: Replicar telas operacionais com tabelas separadas por blocos de status, busca local/remota, filtros, blocos recolhíveis, finalizados/concluídos fechados embaixo, blocos vazios recolhidos, header clicável, ícone SVG laranja, rolagem por bloco e padrão visual HTML/CSS animado. Use quando Codex precisar transformar uma lista única em blocos como "Atrasadas", "Abertas", "Em análise", "Finalizadas", "Contestadas", "Pendentes" e "Concluídos"; padronizar dashboards operacionais por status; ou copiar a estrutura do SAC de acompanhamento de frota para outras telas.
---

# Tabelas Por Status

## Objetivo

Criar ou adaptar telas operacionais que exibem uma lista de registros em blocos separados por status, com uma tabela por bloco, busca robusta, filtros locais, blocos recolhíveis, finalizados/concluídos embaixo e visual consistente.

Use esta skill para copiar o padrão do SAC de acompanhamento de frota para outras telas sem inventar contrato, sem refatorar fora de escopo e sem misturar regra de negócio com decoração visual.

## Fluxo Obrigatório

1. Identificar a lista base da tela: origem dos dados, tipo do item, campo de status, rota/API, filtros existentes, paginação e permissões.
2. Mapear os status reais antes de codar: labels visíveis, enums, status legados, cancelados, finalizados, concluídos e estados sem dados.
3. Definir blocos operacionais com ordem fixa, colocando atenção/pendência primeiro e terminal/concluído por último.
4. Criar um normalizador de texto para status e busca, removendo acentos somente para comparação.
5. Montar `displayRows`, depois `filteredRows`, depois `statusBlocks`. Nunca agrupar antes de filtrar.
6. Renderizar todos os blocos configurados, inclusive os vazios, para preservar a hierarquia visual.
7. Bloco com linhas deve iniciar aberto, exceto blocos terminais marcados como `collapsedByDefault`.
8. Bloco vazio deve iniciar recolhido, mesmo se não for terminal.
9. Quando houver busca ativa, blocos recolhidos com resultado devem expandir automaticamente.
10. Fazer o header inteiro do bloco expandir/recolher, mantendo botão/ícone real para acessibilidade.
11. Usar ícone SVG laranja sem fundo/forma atrás no botão de expandir/recolher, com `title`/tooltip.
12. Colocar rolagem horizontal no corpo de cada bloco para a tabela não cortar.
13. Validar com teste no nível da tela/API que cubra agrupamento, busca, blocos vazios, header clicável e finalizados/concluídos.

## Leitura De Referências

Carregar apenas o necessário:

- Para implementar a lógica React/TypeScript, ler `references/implementation.md`.
- Para copiar HTML/CSS, cores, ícones e animações, ler `references/visual-pattern.md`.

## Regras De Status

Classificar por intenção operacional, não por string exata isolada.

Ordem recomendada para telas operacionais:

1. Status de maior atenção operacional.
2. Status em aberto.
3. Status em análise/andamento.
4. Status contestado/intermediário, quando existir.
5. Status terminal: finalizado, concluído, cancelado, aprovado/rejeitado definitivo.

Exemplo SAC Ocorrências:

1. `Atrasadas`
2. `Abertas`
3. `Em análise`
4. `Finalizadas` recolhido por padrão

Exemplo SAC Custo Extra:

1. `Contestadas`
2. `Pendentes`
3. `Concluídos` recolhido por padrão

Heurística padrão:

```ts
function normalizeStatusLabel(value: unknown) {
  return String(value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim()
    .toLowerCase();
}

function resolveStatusBlock(row: { statusLabel?: string | null; rawStatus?: string | null }) {
  const status = normalizeStatusLabel(`${row.statusLabel ?? ""} ${row.rawStatus ?? ""}`);

  if (/cancelad|canceled|cancelled/.test(status)) return "Cancelados";
  if (/finaliz|completed|finished|concluid|aprovad|rejeitad/.test(status)) return "Finalizado";
  if (/atras|crit|vencid|sla/.test(status)) return "Crítico";
  if (/contest/.test(status)) return "Contestados";
  if (/analise|analis|andamento/.test(status)) return "Em análise";
  if (/abert|pendente/.test(status)) return "Abertos";
  if (/cliente|atend/.test(status)) return "Em cliente";
  if (/rota|transito|in_progress/.test(status)) return "Em rota";
  return "Crítico";
}
```

Adaptar nomes e heurísticas aos status reais da tela. Nunca inventar status que a API não retorna; se a tela precisa de um bloco novo, derivar de dados reais e explicar a regra.

## Estrutura Esperada

A tela deve seguir esta pipeline:

```ts
const displayRows = mergeLoadedAndSupplementalRows(rows, remoteSearchRows);
const filteredRows = applyLocalSearchAndFilters(displayRows, filters);
const statusBlocks = buildStatusBlocks(filteredRows, statusBlockConfig);
```

Regra importante: `buildStatusBlocks` deve retornar todos os blocos configurados, inclusive vazios. Não aplicar `.filter((block) => block.rows.length > 0)` depois do agrupamento.

Expansão padrão:

```ts
function isStatusBlockExpanded(block: StatusBlock) {
  if (search.trim() && block.rows.length > 0) return true;

  return (
    blockExpansionOverrides[block.id] ??
    (!block.collapsedByDefault && block.rows.length > 0)
  );
}
```

## Busca

Implementar busca local assim:

- normalizar acentos e caixa;
- permitir múltiplos termos separados por `;`;
- buscar por campos humanos importantes;
- comparar também versão compactada sem pontuação para placas, notas, pedidos, planos, rotas e códigos.

Se a tela usa lote único com limite alto, ainda vale enviar `search` para o backend quando o usuário pressiona Enter:

- frontend envia `search`;
- backend filtra antes do `LIMIT/OFFSET`;
- frontend aplica filtro local secundário nos dados retornados;
- busca ativa expande blocos recolhidos que tenham resultado.

## Blocos Recolhíveis E Finalizados

Padrão recomendado:

- blocos ativos com linhas: abertos por padrão;
- blocos vazios: visíveis e recolhidos por padrão;
- blocos terminais (`Finalizadas`, `Concluídos`, `Cancelados` quando fizer sentido): embaixo e recolhidos por padrão;
- busca ativa: se houver resultado em bloco recolhido, expandir automaticamente para não esconder o match;
- clique no header inteiro: alterna expandir/recolher;
- botão do header: mantém `aria-expanded`, `aria-controls`, `aria-label` e `title`;
- ícone do botão: SVG laranja, sem fundo/forma atrás.

Quando a tela ainda carregar finalizados sob demanda, preservar a ação existente, mas o resultado final deve entrar no bloco terminal embaixo e recolhido por padrão quando não houver busca ativa.

## Visual

Usar visual operacional, denso e escaneável:

- header de bloco com título e meta;
- header inteiro clicável para expandir/recolher;
- botão de expandir/recolher com SVG laranja sem fundo e tooltip;
- bloco vazio visível e recolhido;
- corpo do bloco com rolagem horizontal própria para a tabela não cortar;
- tabela clara, cabeçalho forte, hover discreto;
- status badge com cor por bloco;
- ações em menu contextual ou botões compactos;
- animação leve de entrada para blocos e linhas;
- sem hero, sem cards decorativos, sem gradientes chamativos.

Para CSS completo e HTML/React detalhado, usar `references/visual-pattern.md`.

## Validação Mínima

Criar ou atualizar testes para:

- status diferentes caírem nos blocos corretos;
- blocos aparecerem na ordem configurada mesmo quando algum bloco estiver vazio;
- blocos vazios iniciarem recolhidos;
- finalizados/concluídos ficarem embaixo e recolhidos por padrão;
- busca com resultado em bloco recolhido expandir automaticamente;
- clique no header do bloco expandir/recolher;
- botão de expandir/recolher ter SVG, `aria-label`, `aria-expanded`, `aria-controls` e `title`;
- corpo do bloco ter rolagem horizontal própria;
- busca local encontrar por acento, placa/código sem pontuação e termos separados por `;`;
- busca remota encaminhar `search` antes da paginação/limite;
- tabela renderizar uma seção por bloco com título/meta corretos.

Se não for possível testar em runtime, informar exatamente o que ficou sem validação.
