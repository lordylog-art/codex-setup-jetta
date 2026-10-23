# Veículos, placas e ativos operacionais

## Fonte canônica

- Mapeamento e aliases: `apps/web/src/app/clientes/3-coracoes/[unit]/programacao/disponibilidade/vehicle-visuals.ts`.
- Renderização: `apps/web/src/app/clientes/3-coracoes/[unit]/programacao/vehicle-render.tsx`.
- Componente obrigatório: `VehicleAvailabilityCell`.
- Placa brasileira: `VehiclePlateBadge`; a fonte `Fe` e os ativos de placa são exclusivos dessa representação.

## Perfis e imagens existentes

| Perfil | Ativo |
| --- | --- |
| Fiorino/utilitário | `/images/vehicles/fiorino.png` |
| 3/4 veículo leve | `/images/vehicles/34.png` |
| Van/HR | `/images/vehicles/van.png` |
| VUC/Iveco | `/images/vehicles/vuc-iveco.png` |
| Toco | `/images/vehicles/toco.png` |
| Truck/Truck alongado | `/images/vehicles/truck-truck-alongado.png` |
| Cavalo simples/trucado | `/images/vehicles/cavalo-cavalo-trucado.png` |

Aliases devem passar por `resolveProjectVehicleProfile` e `resolveVehicleVisual`. Não duplicar mapa, fazer `includes` local, inventar imagem, usar emoji ou escolher veículo “parecido” diretamente pelo nome.

## Regras de uso

- Preserve `alt`, dimensões, escala e fallback do componente.
- Não reimplemente placa em HTML/CSS fora de `VehiclePlateBadge`.
- Não exponha placas reais em documentação ou screenshots da skill.
- Para dashboard, use `DashboardVehicleProfileIcon` quando a linguagem do dashboard pedir marcador SVG, conforme o kit existente.
- Consulte [source-assets.md](source-assets.md) para outros logos e imagens já disponíveis.
