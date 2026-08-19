# ERP Jetta Project Context

## Produto

Jetta Move e um sistema web interno para gestao operacional de frota. O objetivo e substituir gradualmente processos em Google Sheets e Apps Script por uma base oficial em API, banco e interface operacional.

## Stack

- Monorepo npm workspaces.
- Frontend: Next.js + TypeScript em `apps/web`.
- Backend: NestJS em `apps/api`.
- Banco: PostgreSQL.
- ORM: Prisma.
- Deploy: VPS com Caddy, PM2 e scripts PowerShell.

## Dominios atuais

- Cliente principal observado: `3-coracoes`.
- Unidade recorrente: `guarulhos`.
- Programacao:
  - Disponibilidade de frota/motoristas.
  - Programacao diaria.
  - Reentregas/devolucao.
  - Cargas, status de importacao e hidratacao.
  - Roteirizacao e mapa.
- SAC:
  - Acompanhamento de frota.
  - Carros em rota.
  - Ocorrencias.
  - Confirmacao/acompanhamento de tracking.
- Cadastros e dashboards:
  - Motoristas.
  - Veiculos/frota.
  - Regras operacionais.
- Integracoes:
  - Greenmile para rotas, paradas, status, coordenadas e enriquecimento.
  - Processos legados de planilhas ainda podem existir durante migracao.

## Sinais de valor

Ideias boas para este projeto normalmente melhoram uma destas coisas:

- Visibilidade operacional em tempo real.
- Confiabilidade do dado oficial.
- Menos retrabalho de SAC/programacao.
- Menos dependencia de planilha.
- Deteccao antecipada de excecoes.
- Rastreamento de responsabilidade e historico.
- Decisao mais rapida sobre motorista, veiculo, carga, rota e ocorrencia.
- Integracao Greenmile com fallback claro quando a rota nao for localizada.

## Telas e arquivos uteis

- Navegacao 3 Coracoes: `apps/web/src/data/tres-coracoes-nav.config.ts`.
- Disponibilidade: `apps/web/src/app/clientes/3-coracoes/[unit]/programacao/disponibilidade/page.tsx`.
- Programacao diaria: `apps/web/src/app/clientes/3-coracoes/[unit]/programacao/programacao`.
- SAC/carros em rota: `apps/web/src/app/clientes/3-coracoes/[unit]/sac/carros-em-rota`.
- SAC/ocorrencias: `apps/web/src/app/clientes/3-coracoes/[unit]/sac/ocorrencias`.
- Greenmile fast route: `apps/web/src/lib/greenmile-fast-route.ts`.
- Roteirizacao: `apps/web/src/lib/programacao-routing.ts`.
- Cargas/programacao API web: `apps/web/src/app/api/programacao/cargas/route.ts`.
- Dominio backend de cargas: `apps/api/src/modules/daily-loads`.
- Schema: `apps/api/prisma/schema.prisma`.

## Ideias que tendem a valer

- Torre de excecoes para SAC: atrasos, rota sem Greenmile, parada longa, ocorrencia aberta, divergencia de status.
- Timeline por veiculo/carga: importacao, enriquecimento Greenmile, saida, paradas, ocorrencias, confirmacoes e fechamento.
- Fila operacional priorizada: "o que precisa de acao agora" em vez de apenas listagem.
- Alertas de divergencia entre programacao, disponibilidade e status em rota.
- Auditoria simples de alteracoes criticas.
- Indicadores de qualidade de dados: rotas pendentes, coordenadas incertas, motoristas sem telefone, veiculos sem perfil/capacidade.
- Atalhos de acao no fluxo: abrir ocorrencia, confirmar acompanhamento, remarcar status, acionar responsavel.

## Ideias que normalmente nao valem agora

- Dashboard executivo sofisticado antes de consolidar excecoes operacionais.
- IA generativa para decisao automatica sem historico confiavel.
- Regras complexas no frontend que deveriam morar no backend.
- Nova area de cadastro manual sem reduzir tarefa existente.
- Integracao externa profunda sem retry, cache, observabilidade e fallback operacional.
