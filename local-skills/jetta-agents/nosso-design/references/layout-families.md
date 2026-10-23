# Famílias de layout

## Operacional 3 Corações

Rotas sob `/clientes/3-coracoes/[unit]` compartilham navegação do cliente/unidade, topbar Jetta, conteúdo claro e alta densidade. Dentro dessa família:

- Cadastros: KPIs/resumo, filtros, toolbar, tabela e ação de criação.
- Programação: ferramentas operacionais compactas, tabelas extensas, estados e modais especializados.
- SAC: organização por acompanhamento/status, prioridade de leitura e ações contextuais.
- Dashboards: kit `@/components/dashboard`, não o CSS ad hoc das telas operacionais.

Use Guarulhos como referência visual principal solicitada, mas preserve particularidades funcionais de outras unidades.

## Administração

Use `AdminShell`, sidebar escura, superfícies `--admin-*` e componentes administrativos existentes. Não transportar composição de dashboard ou SAC para a administração sem precedente.

## Captação

Listagem e detalhe de parceiros possuem família própria. Preserve seus cards, documentos, estados e ações; reutilize elementos operacionais compartilhados somente quando já integrados nessa área.

## Chamados

A central de chamados possui stylesheet e experiência próprios. Não converter essa área para o visual de cadastro ou dashboard como efeito colateral.

## CSC e Operações

`/csc` e `/operacoes` usam shells autenticados próprios. Preserve a composição e os componentes já empregados em cada área; não assuma que o shell administrativo ou o dashboard é intercambiável.

## Cooperflora

As telas Cooperflora reutilizam partes operacionais do 3 Corações, inclusive cadastros e SAC, mas também possuem estados vazios próprios. Reutilize o wrapper e o componente compartilhado existente; não duplique a implementação apenas para trocar o cliente.

## Frota externa, roteirização e comparativo

`/frota/3-coracoes`, `/roterizacao` e `/guarulhos/comparativo` são experiências independentes ou legadas. Elas servem de referência apenas para mudanças dentro da própria família.

## Páginas públicas e especiais

Login, disponibilidade pública, formulário por token, painel de TV, workshop e páginas temporárias têm contratos próprios. Não são referência para telas internas comuns e não devem contaminar o padrão operacional.

## Regra para tela nova

Escolha uma única família antes de montar a página. Reutilize o layout dessa família, depois seus componentes e, por último, pequenos estilos locais já existentes. Se nenhuma família atender, apresente a lacuna ao usuário antes de criar uma linguagem visual nova.

Consulte [routes.md](routes.md) para encontrar exemplos reais e capturas de cada família.
