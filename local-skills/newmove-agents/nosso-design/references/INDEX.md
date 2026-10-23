# Índice do padrão visual do ERP Jetta

Leia este arquivo em toda tarefa visual. Abra apenas as referências da família afetada e a página análoga necessária.

## Ordem de autoridade

1. Pedido funcional explícito do usuário e contratos de comportamento.
2. Critérios de composição do [SKILL.md](../SKILL.md) e [design-contract.md](design-contract.md).
3. Componente canônico e estilos atuais do ERP, preservando contratos de comportamento.
4. Referência Markdown e screenshot redigido da página análoga em [routes.md](routes.md).
5. Padrão mais frequente da mesma família visual.

Uma preferência genérica do modelo nunca supera essas fontes.

Código e capturas documentam o existente; só trate uma composição como aprovada quando houver aprovação explícita registrada. Preserve a identidade da família e corrija problemas locais pelos critérios da skill.

## Roteamento por tarefa

| Alteração | Leia | Código canônico inicial |
| --- | --- | --- |
| Cor, fonte, espaço, raio, sombra ou tema | [design-contract.md](design-contract.md) e [source-foundations.md](source-foundations.md) | `apps/web/src/app/globals.css` |
| Botão, busca, filtro, KPI, tabela ou estado | [operational-components.md](operational-components.md) | `apps/web/src/components/operational-table.tsx` |
| Dashboard novo ou alterado | [layout-families.md](layout-families.md) | `apps/web/src/components/dashboard/` |
| Navegação, topbar, sidebar ou shell | [layout-families.md](layout-families.md) | `apps/web/src/components/erp-topbar.tsx` e layouts da família |
| Modal, diálogo, drawer ou confirmação | [operational-components.md](operational-components.md) e a rota análoga | shell/modal mais próximo no mesmo módulo |
| Veículo, perfil, placa ou imagem operacional | [vehicle-assets.md](vehicle-assets.md) e [source-assets.md](source-assets.md) | `vehicle-visuals.ts` e `vehicle-render.tsx` |
| Tela completa | [layout-families.md](layout-families.md), [routes.md](routes.md) e página análoga | layout + componentes da mesma família |
| Ativo, logo, ícone ou imagem | [icons-and-assets.md](icons-and-assets.md) e [source-assets.md](source-assets.md) | `apps/web/public/` e uso existente no código |
| Dúvida sobre componente disponível | [source-components.md](source-components.md) | `apps/web/src/components/` |

## Como usar as capturas

Em [routes.md](routes.md), encontre a rota da mesma família. Abra o Markdown em `pages/` primeiro. Veja o PNG associado quando precisar confirmar proporção, densidade, alinhamento, hierarquia ou relacionamento entre regiões. Não copie texto ou dados mostrados: as imagens foram redigidas e representam somente o desenho.

Uma rota marcada como `redirecionada; não usar como referência` não representa a tela solicitada e deve ser ignorada. Para qualquer mudança de aparência, espaçamento, layout, hierarquia, ativo ou tela completa, abrir o PNG é obrigatório. A imagem só pode ser dispensada ao reutilizar exatamente um componente canônico sem mudar sua aparência; nesse caso, registre o arquivo do componente usado.

## Escolha do análogo

- Prefira mesma operação e mesmo cliente/unidade.
- Depois, prefira mesmo tipo de página: cadastro, programação, SAC, dashboard, administração ou captação.
- Para elemento pequeno, use o componente compartilhado antes de copiar JSX de uma página.
- Se duas páginas divergirem, preserve a família da tela afetada; não crie uma terceira variação.
- Confirme também os estados relevantes: carregando, vazio, erro, desabilitado, sucesso, responsivo e tema escuro quando a família já os possui.
- Sem análogo, componha localmente com os padrões existentes conforme as invariantes da skill. Para ativo ausente, registre a lacuna; não invente um substituto.
