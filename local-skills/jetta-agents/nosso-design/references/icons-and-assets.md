# Ícones, logos e ativos visuais

## Ordem de escolha

1. Reutilize o mesmo ícone ou componente da ação equivalente na própria família.
2. Para Bootstrap Icons, use o carregador local em `apps/web/src/lib/bootstrap-icons.ts` e os arquivos já hospedados em `apps/web/public/vendor/bootstrap-icons`.
3. Para SVGs customizados, consulte `apps/web/public/SVG Customizado/README.md` e confirme um uso existente no código.
4. Preserve SVG inline apenas quando ele já pertence ao componente canônico, como `AdminShell`, `ErpTopbar` ou a navegação 3 Corações. Não copie um SVG para criar outra variante.

Não adicionar emoji como ícone, biblioteca externa, ativo remoto ou desenho gerado por IA quando existir equivalente local. `@untitledui/icons` estar instalado não autoriza seu uso: primeiro deve haver precedente aprovado no ERP.

## Logos e marcas

- Logos Jetta: comece pelos arquivos `apps/web/public/jetta-logo*.svg`.
- Marcas de clientes: use `apps/web/public/images/clients`.
- Fundos de autenticação: use apenas precedentes em `apps/web/public/images/backgrounds`.
- Painel de frota/TV: preserve o manifesto e as variantes documentadas em `apps/web/public/assets/painel-frota/README.md`.

Não redesenhar, recolorir, recortar ou substituir marca existente sem pedido explícito.

## Veículos e placas

As regras específicas estão em [vehicle-assets.md](vehicle-assets.md). Não referencie diretamente uma imagem de veículo se `vehicle-render.tsx` já resolve o tipo, alias, placa e fallback.

## Validação

Depois da implementação, compare tamanho, alinhamento, cor, estado hover/foco/desabilitado e densidade com a página análoga em [routes.md](routes.md). Se o ativo não existir, informe a lacuna antes de criar uma nova linguagem visual.
