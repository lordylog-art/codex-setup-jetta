---
name: jetta-local-runtime
description: "Start, validate or diagnose the local ERP Jetta only when its API, Web, PostgreSQL or authentication must run. Excludes other localhost tools."
---

# Runtime local do ERP Jetta

## Quando executar

Execute o fluxo somente para iniciar/parar o ERP local por pedido do usuário ou quando uma implementação, validação ou diagnóstico depender concretamente do ERP em execução. Antes de qualquer comando de runtime, identifique qual comportamento da API/Web, banco ou autenticação do ERP precisa ser exercitado.

Estar neste repositório, mencionar localhost ou editar código não basta. Documentação, planejamento, skills, Git, análises estáticas, testes que dispensam o ERP e ferramentas auxiliares como Jetta Control ou scripts de deploy seguem seu próprio fluxo. Use esta skill nesses trabalhos apenas se houver uma etapa concreta que dependa do ERP local; execute-a nessa etapa, não como preparação automática.

Para validação visual, confirme que o arquivo alterado é renderizado por uma rota do próprio ERP. Uma UI de Jetta Control, outro programa ou HTML avulso deve ser aberta no seu próprio ambiente; uma exigência genérica de screenshot, browser ou teste visual não autoriza iniciar o ERP. Confira o alvo antes do primeiro comando de status ou bootstrap.

Opere somente a instância do worktree atual. `tools/start-erp.ps1` é a fonte de verdade; para bootstrap, baseline ou recriação, leia [docs/local-runtime.md](../../../docs/local-runtime.md).

## Ambiente principal

Use sempre `C:\Projetos\Jeta Move\.env` como origem do ambiente em toda operação oficial do runtime, inclusive `status`, `start`, autenticação e `stop`. Antes de cada comando, defina `JETTA_RUNTIME_ENV` somente no processo que invoca o launcher:

```powershell
rtk proxy powershell -NoProfile -ExecutionPolicy Bypass -Command '$env:JETTA_RUNTIME_ENV = "C:\Projetos\Jeta Move\.env"; & npm.cmd run status'
```

Troque `status` pela ação solicitada e preserve o mesmo caminho durante todo o ciclo. Se o arquivo ou as chaves necessárias não existirem, pare e reporte apenas os nomes ausentes. Nunca mostre valores nem copie segredos para `runtime.env`; não permita fallback silencioso para outra configuração.

## Guardrails

- Leia `AGENTS.md`; prefixe todo shell com `rtk` e use `rtk proxy` apenas sem suporte nativo.
- Preserve a fronteira do launcher, que deriva IP, portas, database, JWT, lease e sessão próprios. Use os scripts npm, não inicie workspaces diretamente.
- Relate apenas URLs sanitizadas, saúde e caminhos. Não exponha env, connection strings, tokens, cookies, bodies ou conteúdo do state.
- Bloqueie destino externo, ownership duvidoso ou efeito externo habilitado. Produção, VPS, deploy e Git remoto estão fora do escopo.

## Fluxo

1. Consulte `rtk npm run status`. Se faltar configuração compartilhada, rode `rtk npm run local:configure` somente em checkout com `.env` autorizado. Se o baseline faltar ou divergir, rode `rtk npm run local:baseline:create`. Nenhum comando deve imprimir valores.
2. Rode `rtk npm start -- -WithCodexBrowser`. Aceite apenas instância saudável e URL fixa de autorização efêmera. Abra-a no Browser interno: a API a consome uma vez, grava cookie host-only e redireciona à Web. Não transporte token por URL ou chat.
3. Valide `/api/auth/me` pelo Browser sem copiar cookie ou payload. Se necessário, use `rtk npm run auth:local:playwright`; aceite somente o caminho do state e o perfil resumido. O gerador reutiliza state válido ou corrige uma sessão expirada uma vez.
4. Termine com `rtk npm run stop` para preservar dados e confirme `parada` com `rtk npm run status`.

## Recuperação

- Configuração ausente: `rtk npm run local:configure` no checkout-fonte; o bootstrap recusa overwrite.
- Baseline ausente/incompatível: `rtk npm run local:baseline:create`; nunca use database compartilhado.
- Prisma incompatível: aceite a única regeneração indicada pelo launcher e execute `rtk npm start` uma vez depois.
- Autorização expirada: repita `rtk npm start -- -WithCodexBrowser` e abra só a nova URL.
- Estado descartável corrompido: com a instância parada, `rtk npm run local:instance:recreate` remove apenas database/state do worktree e restaura o baseline.
- Stop recusado: preserve a lease e reporte a mensagem sanitizada; ownership duvidoso não autoriza matar por porta ou PID.
